"""Discord bot implementation with webhook support."""

from __future__ import annotations

import logging
from typing import Optional

import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook

from .config import BotConfig
from .games import GameEngine, GameError, LanguageOracle
from .storage import UserStore

LOGGER = logging.getLogger(__name__)


class DiscordGameBot(commands.Bot):
    """Discord bot for game commands."""

    def __init__(
        self,
        config: BotConfig,
        store: UserStore,
        language_oracle: Optional[LanguageOracle] = None,
    ):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=config.command_prefix,
            intents=intents,
            help_command=None,
        )
        
        self.config = config
        self.store = store
        self.engine = GameEngine(store, language_oracle=language_oracle)
        self._webhook_url = config.discord_webhook_url

    async def setup_hook(self) -> None:
        """Called when the bot is ready."""
        await self.store.load()
        count = await self.store.count()
        LOGGER.info("Loaded %d người chơi", count)
        LOGGER.info("Bot is ready: %s", self.user)

    async def on_ready(self) -> None:
        """Called when bot is connected."""
        LOGGER.info("Bot %s is online!", self.user)
        await self.change_presence(
            activity=discord.Game(name=f"{self.command_prefix}help | Chơi game kiếm tiền!")
        )

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                f"❌ Lệnh không tồn tại. Dùng `{self.command_prefix}help` để xem danh sách lệnh!"
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Thiếu tham số. Dùng `{self.command_prefix}help {ctx.command}` để xem hướng dẫn.")
        else:
            LOGGER.error("Command error: %s", error, exc_info=True)
            await ctx.send("❌ Có lỗi xảy ra, vui lòng thử lại sau!")

    def send_webhook_message(self, content: str, username: str = "Game Bot") -> None:
        """Send message via Discord webhook."""
        if not self._webhook_url:
            LOGGER.warning("Webhook URL not configured, skipping webhook send")
            return
        
        try:
            webhook = DiscordWebhook(url=self._webhook_url, content=content, username=username)
            webhook.execute()
        except Exception as error:
            LOGGER.error("Failed to send webhook: %s", error)


async def start_command(ctx: commands.Context) -> None:
    """Welcome command."""
    bot: DiscordGameBot = ctx.bot
    user_id = ctx.author.id
    
    state = await bot.engine.ensure_ready(user_id)
    
    embed = discord.Embed(
        title="🎮 Chào mừng đến với Game Bot!",
        description=(
            f"Xin chào {ctx.author.mention}!\n\n"
            f"Tôi là bot game với nhiều mini game thú vị.\n"
            f"Dùng `{bot.command_prefix}help` để xem danh sách lệnh.\n\n"
            f"💰 Số dư hiện tại: **{state.coins}** coins\n"
            "Chúc bạn chơi vui vẻ! 🎉"
        ),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


async def help_command(ctx: commands.Context) -> None:
    """Show help message."""
    bot: DiscordGameBot = ctx.bot
    prefix = bot.command_prefix
    
    embed = discord.Embed(
        title="📖 Danh sách lệnh",
        description="Tất cả các lệnh game có sẵn:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="💼 Cơ bản",
        value=(
            f"`{prefix}start` - Bắt đầu chơi\n"
            f"`{prefix}balance` - Xem số dư\n"
            f"`{prefix}help` - Xem lệnh này"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎮 Game kiếm tiền",
        value=(
            f"`{prefix}work` - Làm việc kiếm tiền (20 phút hồi)\n"
            f"`{prefix}daily` - Nhận quà mỗi ngày\n"
            f"`{prefix}dice` - Chơi xúc xắc may rủi\n"
            f"`{prefix}slots` - Quay hũ vui vẻ"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚔️ Game phiêu lưu",
        value=(
            f"`{prefix}fish` - Chiến dịch câu cá\n"
            f"`{prefix}mine` - Khai thác hầm mỏ"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🧠 Game trí tuệ (AI)",
        value=(
            f"`{prefix}wordchain` - Nối từ siêu tốc\n"
            f"`{prefix}vietking` - Thử sức Vua Tiếng Việt"
        ),
        inline=False
    )
    
    await ctx.send(embed=embed)


async def balance_command(ctx: commands.Context) -> None:
    """Show user balance."""
    bot: DiscordGameBot = ctx.bot
    user_id = ctx.author.id
    
    state = await bot.engine.ensure_ready(user_id)
    
    embed = discord.Embed(
        title=f"💼 Ví của {ctx.author.display_name}",
        color=discord.Color.gold()
    )
    embed.add_field(name="💰 Số dư", value=f"**{state.coins}** coins", inline=True)
    embed.add_field(name="🔥 Chuỗi daily", value=f"**{state.streak}** ngày", inline=True)
    
    await ctx.send(embed=embed)


async def work_command(ctx: commands.Context) -> None:
    """Work to earn money."""
    await _play_game(ctx, "work")


async def dice_command(ctx: commands.Context) -> None:
    """Play dice game."""
    await _play_game(ctx, "dice")


async def slots_command(ctx: commands.Context) -> None:
    """Play slots game."""
    await _play_game(ctx, "slots")


async def daily_command(ctx: commands.Context) -> None:
    """Claim daily reward."""
    await _play_game(ctx, "daily")


async def fish_command(ctx: commands.Context) -> None:
    """Go fishing."""
    await _play_game(ctx, "fish")


async def mine_command(ctx: commands.Context) -> None:
    """Go mining."""
    await _play_game(ctx, "mine")


async def wordchain_command(ctx: commands.Context) -> None:
    """Play word chain game."""
    await _play_game(ctx, "word_chain")


async def vietking_command(ctx: commands.Context) -> None:
    """Play Vietnamese king game."""
    await _play_game(ctx, "viet_king")


async def _play_game(ctx: commands.Context, action: str) -> None:
    """Generic game play handler."""
    bot: DiscordGameBot = ctx.bot
    user_id = ctx.author.id
    
    try:
        if action == "work":
            result = await bot.engine.play_work(user_id)
        elif action == "dice":
            result = await bot.engine.play_dice(user_id)
        elif action == "slots":
            result = await bot.engine.play_slots(user_id)
        elif action == "daily":
            result = await bot.engine.play_daily(user_id)
        elif action == "fish":
            result = await bot.engine.play_fishing(user_id)
        elif action == "mine":
            result = await bot.engine.play_mining(user_id)
        elif action == "word_chain":
            result = await bot.engine.play_word_chain(user_id)
        elif action == "viet_king":
            result = await bot.engine.play_vietnamese_king(user_id)
        else:
            raise ValueError(f"Unknown game action: {action}")
    except GameError as error:
        await ctx.send(f"❌ {error}")
        return
    
    # Get updated balance
    state = await bot.engine.ensure_ready(user_id)
    
    embed = discord.Embed(
        description=result.message,
        color=discord.Color.green() if result.coins_delta >= 0 else discord.Color.red()
    )
    embed.set_footer(text=f"Số dư hiện tại: {state.coins} coins")
    
    await ctx.send(embed=embed)


def setup_commands(bot: DiscordGameBot) -> None:
    """Setup all bot commands."""
    bot.command(name="start")(start_command)
    bot.command(name="help")(help_command)
    bot.command(name="balance", aliases=["bal", "money"])(balance_command)
    bot.command(name="work")(work_command)
    bot.command(name="dice")(dice_command)
    bot.command(name="slots")(slots_command)
    bot.command(name="daily")(daily_command)
    bot.command(name="fish")(fish_command)
    bot.command(name="mine")(mine_command)
    bot.command(name="wordchain")(wordchain_command)
    bot.command(name="vietking")(vietking_command)


async def run_bot(
    config: BotConfig,
    language_oracle: Optional[LanguageOracle] = None,
) -> None:
    """Run the Discord bot."""
    store = UserStore(config.data_path)
    bot = DiscordGameBot(config, store, language_oracle)
    setup_commands(bot)
    
    try:
        await bot.start(config.discord_token)
    finally:
        await store.save()
        await bot.close()
