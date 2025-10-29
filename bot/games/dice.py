"""Dice game module."""

from __future__ import annotations

import random

from ..storage import UserStore


class DiceGame:
    """Handle dice game logic."""

    def __init__(self, store: UserStore):
        self.store = store

    async def play(self, user_id: int) -> tuple[str, int]:
        """
        Play dice game.
        
        Returns:
            tuple[str, int]: (message, coins_delta)
        """
        roll = random.randint(1, 6)
        
        if roll >= 5:
            payout = random.randint(50, 120)
            state = await self.store.get(user_id)
            state.coins += payout
            await self.store.save()
            
            message = f"🎲 Bạn đổ được {roll} và kiếm được {payout}💰!"
            return message, payout
        else:
            penalty = random.randint(10, 40)
            state = await self.store.get(user_id)
            state.coins = max(0, state.coins - penalty)
            await self.store.save()
            
            message = f"🎲 Xui quá! Bạn đổ {roll} và mất {penalty}💰..."
            return message, -penalty
