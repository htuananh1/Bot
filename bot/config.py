"""Runtime configuration utilities for the Telegram bot."""

from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """Raised when mandatory configuration is missing."""


@dataclass(frozen=True)
class BotConfig:
    """Container for runtime configuration values."""

    token: str
    data_path: str = "bot/data/users.json"


def load_config() -> BotConfig:
    """Load configuration from environment variables."""

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ConfigError(
            "Missing TELEGRAM_TOKEN environment variable. "
            "Set it to your bot token before running the bot."
        )

    data_path = os.getenv("DATA_PATH", "bot/data/users.json")
    return BotConfig(token=token, data_path=data_path)
