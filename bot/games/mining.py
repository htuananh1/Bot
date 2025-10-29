"""Mining game module."""

from __future__ import annotations

import random

from ..storage import UserStore


class MiningGame:
    """Handle mining game logic."""

    def __init__(self, store: UserStore):
        self.store = store

    async def play(self, user_id: int) -> tuple[str, int]:
        """
        Go mining.
        
        Returns:
            tuple[str, int]: (message, coins_earned)
        """
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

        # Jackpot chance
        if random.random() < 0.1:
            jackpot = True
            relic = random.randint(1500, 2500)
            total += relic
            lines.append(f"🏺 Kho báu cổ đại trị giá {relic}💰!")

        # Fatigue cost
        fatigue = random.randint(120, 240)
        total -= fatigue
        lines.append(f"😮‍💨 Chi phí năng lượng: -{fatigue}💰")

        # Update user coins
        state = await self.store.get(user_id)
        state.coins = max(0, state.coins + total)
        await self.store.save()

        summary = "\n".join(lines)
        highlight = "Bạn đào trúng siêu phẩm!" if jackpot else "Một ngày khai thác hăng say!"
        
        message = (
            "⚒️ Mùa khai thác vĩ đại!\n"
            f"Bạn khoan {excavations} hầm và kết thúc với {total}💰.\n"
            f"{highlight}\n"
            f"Chi tiết:\n{summary}"
        )
        
        return message, total
