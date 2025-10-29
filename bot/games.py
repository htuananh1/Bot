"""Game engine and orchestration for all games."""

from __future__ import annotations

import asyncio
import logging
import random
import time
from dataclasses import dataclass
from typing import Dict, Optional

from openai import OpenAI

from .games import DailyGame, DiceGame, FishingGame, MiningGame, SlotsGame, WorkGame
from .storage import UserState, UserStore


COOLDOWN_SECONDS = 20 * 60  # 20 minutes between work commands
DAILY_RESET = 20 * 60 * 60  # 20 hours


LOGGER = logging.getLogger(__name__)


@dataclass
class GameResult:
    message: str
    coins_delta: int = 0


class GameError(RuntimeError):
    pass


class LanguageOracle:
    """Thin wrapper around the OpenAI client for language-heavy games."""

    def __init__(self, client: OpenAI) -> None:
        self._client = client

    async def _generate(self, system_prompt: str, user_prompt: str, *, max_tokens: int = 400) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self._call,
            system_prompt,
            user_prompt,
            max_tokens,
        )

    def _call(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        response = self._client.chat.completions.create(
            model="openai/gpt-20-oss",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()

    async def word_chain(self, start_word: str) -> str:
        system_prompt = (
            "Bạn là MC dẫn dắt trò chơi nối từ tiếng Việt. "
            "Hãy luôn trả lời bằng tiếng Việt, gọn gàng, nhiệt huyết."
        )
        user_prompt = (
            "Tạo một lượt chơi nối từ bắt đầu bằng từ "
            f"'{start_word}'. Liệt kê ít nhất 6 lượt nối tiếp nhau, "
            "mỗi lượt dạng 'A → B' trên một dòng. "
            "Giải thích ngắn (tối đa 10 từ) nếu cần ngay sau từ bằng ngoặc đơn."
        )
        return await self._generate(system_prompt, user_prompt)

    async def vietnamese_king(self) -> str:
        system_prompt = (
            "Bạn là giám khảo chương trình Vua Tiếng Việt. "
            "Tạo thử thách sáng tạo, thân thiện cho người chơi luyện tiếng Việt."
        )
        user_prompt = (
            "Viết một thử thách gồm ba phần: \n"
            "1. Khởi động bằng một câu đố mẹo ngắn.\n"
            "2. Thử thách từ vựng với 3 từ khó, yêu cầu người chơi giải nghĩa.\n"
            "3. Bài tập đặt câu với một thành ngữ hoặc tục ngữ.\n"
            "Hãy định dạng rõ ràng bằng danh sách đánh số."
        )
        return await self._generate(system_prompt, user_prompt, max_tokens=500)


class GameEngine:
    """Coordinate game commands and persistence operations."""

    def __init__(self, store: UserStore, language_oracle: Optional[LanguageOracle] = None) -> None:
        self.store = store
        self._locks: Dict[int, asyncio.Lock] = {}
        self.language_oracle = language_oracle
        
        # Initialize game modules
        self.work_game = WorkGame(store)
        self.dice_game = DiceGame(store)
        self.slots_game = SlotsGame(store)
        self.daily_game = DailyGame(store)
        self.fishing_game = FishingGame(store)
        self.mining_game = MiningGame(store)

    def _lock_for(self, user_id: int) -> asyncio.Lock:
        if user_id not in self._locks:
            self._locks[user_id] = asyncio.Lock()
        return self._locks[user_id]

    async def ensure_ready(self, user_id: int) -> UserState:
        async with self._lock_for(user_id):
            return await self.store.get(user_id)

    async def apply_reward(self, user_id: int, coins: int) -> UserState:
        async with self._lock_for(user_id):
            state = await self.store.get(user_id)
            state.coins = max(0, state.coins + coins)
            await self.store.save()
            return state

    async def play_work(self, user_id: int) -> GameResult:
        try:
            message, coins_delta = await self.work_game.play(user_id)
            return GameResult(message=message, coins_delta=coins_delta)
        except ValueError as error:
            raise GameError(str(error)) from error

    async def play_dice(self, user_id: int) -> GameResult:
        message, coins_delta = await self.dice_game.play(user_id)
        return GameResult(message=message, coins_delta=coins_delta)

    async def play_slots(self, user_id: int) -> GameResult:
        message, coins_delta = await self.slots_game.play(user_id)
        return GameResult(message=message, coins_delta=coins_delta)

    async def play_daily(self, user_id: int) -> GameResult:
        try:
            message, coins_delta = await self.daily_game.play(user_id)
            return GameResult(message=message, coins_delta=coins_delta)
        except ValueError as error:
            raise GameError(str(error)) from error

    async def play_fishing(self, user_id: int) -> GameResult:
        message, coins_delta = await self.fishing_game.play(user_id)
        return GameResult(message=message, coins_delta=coins_delta)

    async def play_mining(self, user_id: int) -> GameResult:
        message, coins_delta = await self.mining_game.play(user_id)
        return GameResult(message=message, coins_delta=coins_delta)

    async def play_word_chain(self, user_id: int) -> GameResult:
        if not self.language_oracle:
            raise GameError(
                "Tính năng nối từ cần cấu hình AI_GATEWAY_API_KEY để gọi mô hình ngôn ngữ."
            )

        start_word = random.choice(
            ["ánh sáng", "nông dân", "hải đăng", "thiên nhiên", "cộng đồng", "khởi nghiệp"]
        )
        try:
            sequence = await self.language_oracle.word_chain(start_word)
        except Exception as error:  # pragma: no cover - defensive logging
            LOGGER.exception("Word chain generation failed: %s", error)
            raise GameError("Không thể tạo lượt chơi nối từ lúc này, thử lại sau nhé!") from error

        reward = random.randint(90, 180)
        await self.apply_reward(user_id, reward)
        return GameResult(
            message=(
                "🔗 Trò chơi nối từ!\n"
                f"Từ khởi động: {start_word}\n"
                f"{sequence}\n\n"
                f"Bạn nhận được {reward}💰 cho sự nhanh trí!"
            ),
            coins_delta=reward,
        )

    async def play_vietnamese_king(self, user_id: int) -> GameResult:
        if not self.language_oracle:
            raise GameError(
                "Vua Tiếng Việt cần cấu hình AI_GATEWAY_API_KEY để kích hoạt thử thách ngôn ngữ."
            )

        try:
            challenge = await self.language_oracle.vietnamese_king()
        except Exception as error:  # pragma: no cover - defensive logging
            LOGGER.exception("Vietnamese king generation failed: %s", error)
            raise GameError("Không thể tạo thử thách Vua Tiếng Việt, bạn thử lại giúp mình nhé!") from error

        reward = random.randint(110, 220)
        await self.apply_reward(user_id, reward)
        return GameResult(
            message=(
                "👑 Thử thách Vua Tiếng Việt!\n"
                f"{challenge}\n\n"
                f"Hoàn thành và bạn được thưởng {reward}💰. Cố lên nào!"
            ),
            coins_delta=reward,
        )


__all__ = ["GameEngine", "GameResult", "GameError", "LanguageOracle"]
