"""Runtime configuration utilities for the Discord bot."""

from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """Raised when mandatory configuration is missing."""


@dataclass(frozen=True)
class BotConfig:
    """Container for runtime configuration values."""

    discord_token: str
    discord_webhook_url: str = ""
    data_path: str = "bot/data/users.json"
    webhook_port: int = 8080
    webhook_path: str = "/discord-webhook"
    command_prefix: str = "!"


def load_config() -> BotConfig:
    """Load configuration from environment variables."""

    discord_token = os.getenv("DISCORD_TOKEN")
    if not discord_token:
        raise ConfigError(
            "Missing DISCORD_TOKEN environment variable. "
            "Set it to your Discord bot token before running."
        )

    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "")
    data_path = os.getenv("DATA_PATH", "bot/data/users.json")
    webhook_port = int(os.getenv("WEBHOOK_PORT", "8080"))
    webhook_path = os.getenv("WEBHOOK_PATH", "/discord-webhook")
    command_prefix = os.getenv("COMMAND_PREFIX", "!")
    
    return BotConfig(
        discord_token=discord_token,
        discord_webhook_url=discord_webhook_url,
        data_path=data_path,
        webhook_port=webhook_port,
        webhook_path=webhook_path,
        command_prefix=command_prefix,
    )
