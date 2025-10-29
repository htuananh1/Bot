"""Work game module."""

from __future__ import annotations

import random
import time
from typing import Dict

from ..storage import UserStore

COOLDOWN_SECONDS = 20 * 60  # 20 minutes


class WorkGame:
    """Handle work game logic."""

    def __init__(self, store: UserStore):
        self.store = store
        self._cooldowns: Dict[int, float] = {}

    async def play(self, user_id: int) -> tuple[str, int]:
        """
        Play work game.
        
        Returns:
            tuple[str, int]: (message, coins_earned)
        """
        now = time.time()
        last = self._cooldowns.get(user_id, 0)
        remaining = last + COOLDOWN_SECONDS - now
        
        if remaining > 0:
            minutes = int(remaining // 60) + 1
            raise ValueError(f"Bạn vừa làm việc xong, thử lại sau {minutes} phút nữa nhé!")

        payout = random.randint(25, 65)
        self._cooldowns[user_id] = now
        
        # Update user coins
        state = await self.store.get(user_id)
        state.coins += payout
        await self.store.save()
        
        message = f"Bạn làm việc chăm chỉ và nhận được {payout}💰!"
        return message, payout
