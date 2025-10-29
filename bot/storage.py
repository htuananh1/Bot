"""Persistence helpers for player progress and balances."""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from typing import Dict


DEFAULT_USER_STATE = {"coins": 0, "streak": 0, "last_daily": 0}


@dataclass
class UserState:
    """Runtime representation of a player's persistent data."""

    coins: int = 0
    streak: int = 0
    last_daily: int = 0

    @classmethod
    def from_dict(cls, payload: Dict[str, int]) -> "UserState":
        data = {**DEFAULT_USER_STATE, **payload}
        return cls(
            coins=int(data.get("coins", 0)),
            streak=int(data.get("streak", 0)),
            last_daily=int(data.get("last_daily", 0)),
        )

    def to_dict(self) -> Dict[str, int]:
        return {
            "coins": self.coins,
            "streak": self.streak,
            "last_daily": self.last_daily,
        }


class UserStore:
    """Asynchronous JSON-backed storage for user states."""

    def __init__(self, path: str) -> None:
        self._path = path
        self._lock = asyncio.Lock()
        self._users: Dict[str, UserState] = {}

    async def load(self) -> None:
        async with self._lock:
            if not os.path.exists(self._path):
                os.makedirs(os.path.dirname(self._path), exist_ok=True)
                self._users = {}
                return

            loop = asyncio.get_running_loop()
            raw = await loop.run_in_executor(None, self._read_file)
            payload = json.loads(raw) if raw else {}
            self._users = {
                str(user_id): UserState.from_dict(data)
                for user_id, data in payload.items()
            }

    async def save(self) -> None:
        async with self._lock:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._write_file)

    def _read_file(self) -> str:
        with open(self._path, "r", encoding="utf-8") as handle:
            return handle.read()

    def _write_file(self) -> None:
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as handle:
            json.dump({uid: state.to_dict() for uid, state in self._users.items()}, handle, indent=2)

    def _get_unlocked(self, user_id: int) -> UserState:
        key = str(user_id)
        if key not in self._users:
            self._users[key] = UserState()
        return self._users[key]

    async def get(self, user_id: int) -> UserState:
        async with self._lock:
            return self._get_unlocked(user_id)

    async def update(self, user_id: int, **fields: int) -> UserState:
        async with self._lock:
            state = self._get_unlocked(user_id)
            for name, value in fields.items():
                if hasattr(state, name):
                    setattr(state, name, value)
            return state

    async def increment(self, user_id: int, field: str, amount: int) -> UserState:
        async with self._lock:
            state = self._get_unlocked(user_id)
            current = getattr(state, field)
            setattr(state, field, current + amount)
            return state

    async def count(self) -> int:
        async with self._lock:
            return len(self._users)


__all__ = ["UserStore", "UserState"]
