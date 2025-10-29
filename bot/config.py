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
    webhook_enabled: bool = False
    webhook_url: str = ""
    webhook_port: int = 8443
    webhook_path: str = "/webhook"


def load_config() -> BotConfig:
    """Load configuration from environment variables."""

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ConfigError(
            "Missing TELEGRAM_TOKEN environment variable. "
            "Set it to your bot token before running the bot."
        )

    data_path = os.getenv("DATA_PATH", "bot/data/users.json")
    webhook_enabled = os.getenv("WEBHOOK_ENABLED", "false").lower() in ("true", "1", "yes")
    webhook_url = os.getenv("WEBHOOK_URL", "")
    webhook_port = int(os.getenv("WEBHOOK_PORT", "8443"))
    webhook_path = os.getenv("WEBHOOK_PATH", "/webhook")
    
    if webhook_enabled and not webhook_url:
        raise ConfigError(
            "WEBHOOK_ENABLED is true but WEBHOOK_URL is not set. "
            "Please provide the full webhook URL (e.g., https://yourdomain.com)."
        )
    
    return BotConfig(
        token=token,
        data_path=data_path,
        webhook_enabled=webhook_enabled,
        webhook_url=webhook_url,
        webhook_port=webhook_port,
        webhook_path=webhook_path,
    )
