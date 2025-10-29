"""Slot machine game module."""

from __future__ import annotations

import random

from ..storage import UserStore


class SlotsGame:
    """Handle slots game logic."""

    def __init__(self, store: UserStore):
        self.store = store

    async def play(self, user_id: int) -> tuple[str, int]:
        """
        Play slots game.
        
        Returns:
            tuple[str, int]: (message, coins_delta)
        """
        icons = ["🍒", "🍋", "⭐", "💎", "7️⃣"]
        spin = [random.choice(icons) for _ in range(3)]
        display = " | ".join(spin)

        # Calculate payout
        if len(set(spin)) == 1:  # All same
            payout = 300 if spin[0] == "7️⃣" else 180
        elif len(set(spin)) == 2:  # Two same
            payout = random.randint(60, 120)
        else:  # All different
            payout = -random.randint(15, 45)

        # Update user coins
        state = await self.store.get(user_id)
        state.coins = max(0, state.coins + payout)
        await self.store.save()

        if payout >= 0:
            message = f"🎰 {display}\nBạn thắng {payout}💰!"
        else:
            message = f"🎰 {display}\nBạn mất {-payout}💰..."

        return message, payout
