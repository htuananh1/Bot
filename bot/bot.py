"""Entry point and Telegram command wiring for the game bot."""

from __future__ import annotations

import logging
from contextlib import suppress

from telegram import Update
from telegram.ext import (
    AIORateLimiter,
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .config import BotConfig, ConfigError, load_config
from .games import GameEngine, GameError, LanguageOracle
from .storage import UserStore


LOGGER = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    engine: GameEngine = context.application.bot_data["engine"]
    user = update.effective_user
    if not user or not update.message:
        return

    state = await engine.ensure_ready(user.id)
    await update.message.reply_text(
        "Xin chào! Tôi là bot cày tiền với nhiều mini game.\n"
        "Dùng /help để xem danh sách lệnh.\n"
        f"Hiện bạn đang có {state.coins}💰. Chúc may mắn!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Danh sách lệnh có sẵn:\n"
        "/balance - Xem số tiền hiện có\n"
        "/work - Làm việc kiếm tiền (20 phút hồi)\n"
        "/dice - Chơi xúc xắc may rủi\n"
        "/slots - Quay hũ vui vẻ\n"
        "/daily - Nhận quà mỗi ngày\n"
        "/fish - Chiến dịch câu cá quy mô lớn\n"
        "/mine - Khai thác hầm mỏ siêu lợi nhuận\n"
        "/wordchain - Gọi MC nối từ siêu tốc\n"
        "/vietking - Thử sức cùng Vua Tiếng Việt\n"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    engine: GameEngine = context.application.bot_data["engine"]
    user = update.effective_user
    if not user or not update.message:
        return

    state = await engine.ensure_ready(user.id)
    await update.message.reply_text(
        f"💼 Ví của bạn hiện có {state.coins}💰.\n"
        f"Chuỗi nhận quà: {state.streak} ngày."
    )


async def _play(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str) -> None:
    engine: GameEngine = context.application.bot_data["engine"]
    user = update.effective_user
    if not user or not update.message:
        return

    try:
        if action == "work":
            result = await engine.play_work(user.id)
        elif action == "dice":
            result = await engine.play_dice(user.id)
        elif action == "slots":
            result = await engine.play_slots(user.id)
        elif action == "daily":
            result = await engine.play_daily(user.id)
        elif action == "fish":
            result = await engine.play_fishing(user.id)
        elif action == "mine":
            result = await engine.play_mining(user.id)
        elif action == "word_chain":
            result = await engine.play_word_chain(user.id)
        elif action == "viet_king":
            result = await engine.play_vietnamese_king(user.id)
        else:
            raise ValueError(f"Unknown game action: {action}")
    except GameError as error:
        await update.message.reply_text(str(error))
        return

    await update.message.reply_text(result.message)


async def work(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _play(update, context, "work")


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _play(update, context, "dice")


async def slots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _play(update, context, "slots")


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _play(update, context, "daily")


async def fish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _play(update, context, "fish")


async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _play(update, context, "mine")


async def word_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _play(update, context, "word_chain")


async def viet_king(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _play(update, context, "viet_king")


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Mình chưa hiểu tin nhắn đó. Dùng /help để xem các lệnh hiện có nhé!"
        )


async def on_startup(application: Application) -> None:
    store: UserStore = application.bot_data["store"]
    await store.load()
    count = await store.count()
    LOGGER.info("Loaded %d người chơi", count)


async def on_shutdown(application: Application) -> None:
    store: UserStore = application.bot_data.get("store")
    if store:
        with suppress(Exception):
            await store.save()


def build_application(
    config: BotConfig, language_oracle: LanguageOracle | None = None
) -> Application:
    store = UserStore(config.data_path)
    engine = GameEngine(store, language_oracle=language_oracle)
    application = (
        ApplicationBuilder()
        .token(config.token)
        .rate_limiter(AIORateLimiter())
        .post_init(on_startup)
        .post_shutdown(on_shutdown)
        .build()
    )

    application.bot_data["config"] = config
    application.bot_data["store"] = store
    application.bot_data["engine"] = engine

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("work", work))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("slots", slots))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("fish", fish))
    application.add_handler(CommandHandler("mine", mine))
    application.add_handler(CommandHandler("wordchain", word_chain))
    application.add_handler(CommandHandler("vietking", viet_king))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    return application


def main(language_oracle: LanguageOracle | None = None) -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    try:
        config = load_config()
    except ConfigError as error:
        LOGGER.error("%s", error)
        raise SystemExit(1) from error

    application = build_application(config, language_oracle=language_oracle)
    LOGGER.info("Starting bot with data path %s", config.data_path)
    application.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
