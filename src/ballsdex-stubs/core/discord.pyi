# pyright: reportIncompatibleMethodOverride=false

from typing import TYPE_CHECKING, Self

import discord
from discord.ui import Item
from discord.ui.view import BaseView as DiscordBaseView

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

type Interaction = discord.Interaction["BallsDexBot"]

UNKNOWN_INTERACTION: set[int]
"""
https://discord.com/developers/docs/topics/opcodes-and-status-codes#json-json-error-codes
"""

class BaseView(DiscordBaseView):
    original_message: discord.Message | None
    discord_id: int

    def restrict_author(self, discord_id: int) -> None: ...
    async def on_error(self, interaction: Interaction, error: Exception, item: Item[Self]) -> None: ...
    async def interaction_check(self, interaction: Interaction, /) -> bool: ...
    async def on_timeout(self) -> None: ...

class View(discord.ui.View, BaseView): ...
class LayoutView(discord.ui.LayoutView, BaseView): ...

class Container(discord.ui.Container[LayoutView]):
    async def interaction_check(self, interaction: Interaction, /) -> bool: ...

class Modal(discord.ui.Modal):
    async def on_error(self, interaction: Interaction, error: Exception) -> None: ...
    async def interaction_check(self, interaction: Interaction) -> bool: ...
    async def on_submit(self, interaction: Interaction) -> None: ...
