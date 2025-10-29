"""Daily reward game module."""

from __future__ import annotations

import time

from ..storage import UserStore

DAILY_RESET = 20 * 60 * 60  # 20 hours


class DailyGame:
    """Handle daily reward logic."""

    def __init__(self, store: UserStore):
        self.store = store

    async def play(self, user_id: int) -> tuple[str, int]:
        """
        Claim daily reward.
        
        Returns:
            tuple[str, int]: (message, coins_earned)
        """
        now = int(time.time())
        state = await self.store.get(user_id)
        
        if now - state.last_daily < DAILY_RESET:
            hours = (DAILY_RESET - (now - state.last_daily)) // 3600 + 1
            raise ValueError(f"Bạn đã nhận quà hôm nay rồi! Thử lại sau {hours} giờ.")

        state.last_daily = now
        state.streak = state.streak + 1 if state.streak else 1
        
        base = 120
        bonus = min(100, state.streak * 15)
        payout = base + bonus
        
        state.coins += payout
        await self.store.save()

        message = (
            "🎁 Nhận quà hàng ngày!\n"
            f"Chuỗi hiện tại: {state.streak} ngày\n"
            f"Bạn nhận được {payout}💰 (bao gồm {bonus}💰 thưởng chuỗi)."
        )
        
        return message, payout
