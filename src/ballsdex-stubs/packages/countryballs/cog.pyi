import logging
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from .countryball import BallSpawnView
from .spawn import BaseSpawnManager

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.countryballs")

class CountryBallsSpawner(commands.Cog):
    bot: "BallsDexBot"
    cache: dict[int, int]
    countryball_cls: type[BallSpawnView]
    spawn_manager: BaseSpawnManager

    async def load_cache(self) -> None: ...
    async def on_message(self, message: discord.Message): ...
    async def on_ballsdex_settings_change(
        self,
        guild: discord.Guild,
        channel: discord.TextChannel | None = None,
        enabled: bool | None = None,
    ): ...
