"""Fishing game module."""

from __future__ import annotations

import random

from ..storage import UserStore


class FishingGame:
    """Handle fishing game logic."""

    def __init__(self, store: UserStore):
        self.store = store

    async def play(self, user_id: int) -> tuple[str, int]:
        """
        Go fishing.
        
        Returns:
            tuple[str, int]: (message, coins_earned)
        """
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

        # Bonus wave
        bonus = 0
        if total >= 600 and random.random() < 0.35:
            bonus = random.randint(120, 300)
            haul.append(f"⚡ Cơn sóng vàng mang thêm {bonus}💰")
            total += bonus

        # Update user coins
        state = await self.store.get(user_id)
        state.coins += total
        await self.store.save()

        details = "\n".join(haul)
        message = (
            "🎣 Phiên câu cá hoành tráng!\n"
            f"Bạn quăng lưới {casts} lần và thu về {total}💰.\n"
            f"Chi tiết:\n{details}"
        )
        
        return message, total
