"""Game logic handlers for the Telegram bot."""

from __future__ import annotations

import asyncio
import logging
import random
import time
from dataclasses import dataclass
from typing import Dict, Optional

from openai import OpenAI

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
        self._cooldowns: Dict[int, float] = {}
        self._locks: Dict[int, asyncio.Lock] = {}
        self.language_oracle = language_oracle

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
        now = time.time()
        last = self._cooldowns.get(user_id, 0)
        remaining = last + COOLDOWN_SECONDS - now
        if remaining > 0:
            minutes = int(remaining // 60) + 1
            raise GameError(f"Bạn vừa làm việc xong, thử lại sau {minutes} phút nữa nhé!")

        payout = random.randint(25, 65)
        self._cooldowns[user_id] = now
        await self.apply_reward(user_id, payout)
        return GameResult(message=f"Bạn làm việc chăm chỉ và nhận được {payout}💰!", coins_delta=payout)

    async def play_dice(self, user_id: int) -> GameResult:
        roll = random.randint(1, 6)
        if roll >= 5:
            payout = random.randint(50, 120)
            await self.apply_reward(user_id, payout)
            return GameResult(
                message=f"🎲 Bạn đổ được {roll} và kiếm được {payout}💰!",
                coins_delta=payout,
            )

        penalty = random.randint(10, 40)
        await self.apply_reward(user_id, -penalty)
        return GameResult(
            message=f"🎲 Xui quá! Bạn đổ {roll} và mất {penalty}💰...",
            coins_delta=-penalty,
        )

    async def play_slots(self, user_id: int) -> GameResult:
        icons = ["🍒", "🍋", "⭐", "💎", "7️⃣"]
        spin = [random.choice(icons) for _ in range(3)]
        message = "|".join(spin)

        if len(set(spin)) == 1:
            payout = 300 if spin[0] == "7️⃣" else 180
        elif len(set(spin)) == 2:
            payout = random.randint(60, 120)
        else:
            payout = -random.randint(15, 45)

        await self.apply_reward(user_id, payout)
        if payout >= 0:
            return GameResult(message=f"🎰 {message}\nBạn thắng {payout}💰!", coins_delta=payout)
        return GameResult(message=f"🎰 {message}\nBạn mất {-payout}💰...", coins_delta=payout)

    async def play_daily(self, user_id: int) -> GameResult:
        now = int(time.time())
        async with self._lock_for(user_id):
            state = await self.store.get(user_id)
            if now - state.last_daily < DAILY_RESET:
                hours = (DAILY_RESET - (now - state.last_daily)) // 3600 + 1
                raise GameError(f"Bạn đã nhận quà hôm nay rồi! Thử lại sau {hours} giờ.")

            state.last_daily = now
            state.streak = state.streak + 1 if state.streak else 1
            base = 120
            bonus = min(100, state.streak * 15)
            payout = base + bonus
            state.coins += payout
            await self.store.save()

        return GameResult(
            message=(
                "🎁 Nhận quà hàng ngày!\n"
                f"Chuỗi hiện tại: {state.streak} ngày\n"
                f"Bạn nhận được {payout}💰 (bao gồm {bonus}💰 thưởng chuỗi)."
            ),
            coins_delta=payout,
        )

    async def play_fishing(self, user_id: int) -> GameResult:
        schools = [
            ("🐟 Cá cơm", 8, 16, 40),
            ("🐠 Cá hồng", 22, 45, 30),
            ("🦑 Mực khổng lồ", 90, 160, 15),
            ("🐬 Cá heo lạc", 200, 400, 8),
            ("🐉 Rồng nước huyền thoại", 800, 1200, 2),
        ]
        haul = []
        total = 0
        casts = random.randint(2, 5)
        weights = [school[3] for school in schools]
        for _ in range(casts):
            name, low, high, _ = random.choices(schools, weights=weights)[0]
            reward = random.randint(low, high)
            total += reward
            haul.append(f"{name} (+{reward}💰)")

        bonus = 0
        if total >= 600 and random.random() < 0.35:
            bonus = random.randint(120, 300)
            haul.append(f"⚡ Cơn sóng vàng mang thêm {bonus}💰")
            total += bonus

        await self.apply_reward(user_id, total)
        details = "\n".join(haul)
        return GameResult(
            message=(
                "🎣 Phiên câu cá hoành tráng!\n"
                f"Bạn quăng lưới {casts} lần và thu về {total}💰.\n"
                f"Chi tiết:\n{details}"
            ),
            coins_delta=total,
        )

    async def play_mining(self, user_id: int) -> GameResult:
        veins = [
            ("⛏️ Quặng sắt", 40, 90, 45),
            ("💎 Quặng kim cương", 180, 320, 25),
            ("🌌 Tinh thể sao", 350, 520, 18),
            ("🪐 Mảnh thiên thạch quý", 600, 900, 9),
            ("⚙️ Cỗ máy cổ đại", 1100, 1600, 3),
        ]
        excavations = random.randint(3, 6)
        total = 0
        lines = []
        jackpot = False
        weights = [item[3] for item in veins]
        for _ in range(excavations):
            name, low, high, _ = random.choices(veins, weights=weights)[0]
            reward = random.randint(low, high)
            total += reward
            lines.append(f"{name}: +{reward}💰")

        if random.random() < 0.1:
            jackpot = True
            relic = random.randint(1500, 2500)
            total += relic
            lines.append(f"🏺 Kho báu cổ đại trị giá {relic}💰!")

        fatigue = random.randint(120, 240)
        total -= fatigue
        lines.append(f"😮‍💨 Chi phí năng lượng: -{fatigue}💰")

        await self.apply_reward(user_id, total)
        summary = "\n".join(lines)
        highlight = "Bạn đào trúng siêu phẩm!" if jackpot else "Một ngày khai thác hăng say!"
        return GameResult(
            message=(
                "⚒️ Mùa khai thác vĩ đại!\n"
                f"Bạn khoan {excavations} hầm và kết thúc với {total}💰.\n"
                f"{highlight}\n"
                f"Chi tiết:\n{summary}"
            ),
            coins_delta=total,
        )

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
