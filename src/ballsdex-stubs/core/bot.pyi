from datetime import datetime
from typing import Self, Sequence

import discord
from ballsdex.core.metrics import PrometheusServer
from cachetools import TTLCache
from discord import app_commands
from discord.app_commands.translator import TranslationContextTypes, locale_str
from discord.enums import Locale
from discord.ext import commands
from discord.ext.commands.bot import PrefixType
from discord.utils import MISSING

DEFAULT_PACKAGES: tuple[tuple[str, str], ...]

def owner_check(ctx: commands.Context["BallsDexBot"]) -> bool: ...

class Translator(app_commands.Translator):
    async def translate(self, string: locale_str, locale: Locale, context: TranslationContextTypes) -> str | None: ...

class CommandTree[Bot: BallsDexBot](app_commands.CommandTree[Bot]):
    disable_time_check: bool

    async def interaction_check(self, interaction: discord.Interaction[Bot], /) -> bool: ...
    async def load_command_mentions(
        self, app_commands: list[app_commands.AppCommand] | None = None, *, cog: commands.Cog | None = None
    ) -> None: ...
    async def sync(self, *, guild: discord.abc.Snowflake | None = None) -> list[app_commands.AppCommand]: ...

class BallsDexBot(commands.AutoShardedBot):
    """
    BallsDex Discord bot
    """

    tree: CommandTree[Self]  # type: ignore
    skip_tree_sync: bool
    gateway_url: str | None

    dev: bool
    prometheus_server: PrometheusServer | None

    startup_time: datetime | None
    application_emojis: dict[int, discord.Emoji]
    blacklist: set[int]
    blacklist_guild: set[int]
    catch_log: set[int]
    command_log: set[int]
    locked_balls: TTLCache
    impersonations: dict[int, discord.Member]
    owner_ids: set[int]  # type: ignore

    def __init__(
        self,
        command_prefix: PrefixType["BallsDexBot"],
        disable_message_content: bool = False,
        disable_time_check: bool = False,
        skip_tree_sync: bool = False,
        gateway_url: str | None = None,
        dev: bool = False,
        **options,
    ) -> None: ...
    async def start_prometheus_server(self) -> None: ...
    async def invoke(self, ctx: commands.Context[Self], /) -> None: ...  # type: ignore
    def get_emoji(self, id: int) -> discord.Emoji | None: ...
    async def load_cache(self) -> None: ...
    async def gateway_healthy(self) -> bool:
        """Check whether or not the gateway proxy is ready and healthy."""
        ...

    async def setup_hook(self) -> None: ...
    async def add_cog(
        self,
        cog: commands.Cog,
        /,
        *,
        override: bool = False,
        guild: discord.abc.Snowflake | None = MISSING,
        guilds: Sequence[discord.abc.Snowflake] = MISSING,
    ) -> None: ...
    async def on_ready(self) -> None: ...
    async def blacklist_check(self, source: discord.Interaction[Self] | commands.Context[Self]) -> bool: ...
    async def on_command_error(
        self, context: commands.Context, exception: commands.errors.CommandError | app_commands.AppCommandError
    ) -> None: ...
    async def on_application_command_error(
        self, interaction: discord.Interaction[Self], error: app_commands.AppCommandError
    ) -> None: ...
    async def on_error(self, event_method: str, /, *args, **kwargs) -> None: ...
