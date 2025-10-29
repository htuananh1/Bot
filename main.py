"""Main entry point - orchestrates all bot components."""

from __future__ import annotations

import asyncio
import logging
import os
import sys

from openai import OpenAI

# Import bot modules
from bot.config import BotConfig, ConfigError, load_config
from bot.discord_bot import run_bot
from bot.games import LanguageOracle
from bot.webhook_server import WebhookServer

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


def build_language_oracle() -> LanguageOracle | None:
    """Create the language oracle if the gateway API key is configured."""
    api_key = os.getenv("AI_GATEWAY_API_KEY")
    if not api_key:
        LOGGER.info("AI_GATEWAY_API_KEY not set, AI games will be disabled")
        return None

    client = OpenAI(
        api_key=api_key,
        base_url="https://ai-gateway.vercel.sh/v1",
    )
    LOGGER.info("AI Gateway configured for word games")
    return LanguageOracle(client)


async def main_async() -> None:
    """Main async entry point."""
    LOGGER.info("🚀 Starting Discord Game Bot...")
    
    # Load configuration
    try:
        config = load_config()
        LOGGER.info("✅ Configuration loaded successfully")
    except ConfigError as error:
        LOGGER.error("❌ Configuration error: %s", error)
        sys.exit(1)

    # Start webhook server in background
    webhook_server = WebhookServer(port=config.webhook_port, path=config.webhook_path)
    webhook_thread = webhook_server.run_threaded()
    LOGGER.info("✅ Webhook server started on port %d", config.webhook_port)

    # Build language oracle for AI games
    language_oracle = build_language_oracle()
    
    # Run Discord bot
    LOGGER.info("🤖 Starting Discord bot...")
    try:
        await run_bot(config, language_oracle)
    except Exception as error:
        LOGGER.error("❌ Bot crashed: %s", error, exc_info=True)
        sys.exit(1)


def main() -> None:
    """Main synchronous entry point."""
    try:
        # Check Python version
        if sys.version_info < (3, 11):
            LOGGER.warning("Python 3.11+ is recommended, you have %s", sys.version)
        
        # Run async main
        asyncio.run(main_async())
    except KeyboardInterrupt:
        LOGGER.info("👋 Bot stopped by user")
    except Exception as error:
        LOGGER.error("💥 Fatal error: %s", error, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
