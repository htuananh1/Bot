"""Standalone entry point that wires optional language AI to the bot."""

from __future__ import annotations

import os

from openai import OpenAI

from bot.bot import main as run_bot
from bot.games import LanguageOracle


def build_language_oracle() -> LanguageOracle | None:
    """Create the language oracle if the gateway API key is configured."""

    api_key = os.getenv("AI_GATEWAY_API_KEY")
    if not api_key:
        return None

    client = OpenAI(
        api_key=api_key,
        base_url="https://ai-gateway.vercel.sh/v1",
    )
    return LanguageOracle(client)


if __name__ == "__main__":
    run_bot(language_oracle=build_language_oracle())
