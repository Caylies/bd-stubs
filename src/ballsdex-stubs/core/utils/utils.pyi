from typing import TYPE_CHECKING

import discord
from bd_models.models import Player

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

async def is_staff(interaction: discord.Interaction["BallsDexBot"], *perms: str) -> bool:
    """
    Checks if an interacting user checks one of the following conditions:

    - The user is a bot owner
    - The user has a role considered root or admin

    Parameters
    ----------
    interaction: Interaction[BallsDexBot]
        The interaction of the user to check.
    perms: *str
        Django permissions to verify. If empty, only staff status will be checked.

    Returns
    -------
    bool
        [`True`][] if the user is a staff, [`False`][] otherwise.
    """
    ...

async def inventory_privacy(
    bot: "BallsDexBot",
    interaction: discord.Interaction["BallsDexBot"],
    player: Player,
    user_obj: discord.User | discord.Member,
):
    """
    Check if the inventory of a user is viewable in the given context. If not, a followup response will be sent with a
    proper message.

    Parameters
    ----------
    bot: BallsDexBot
        Bot object
    interaction: Interaction[BallsDexBot]
        Interaction of the command.
    player: Player
        Ballsdex Player object of the user whose inventory is being inspected.
    user_obj: discord.User | discord.Member
        Discord user object of the user whose inventory is being inspected.

    Returns
    -------
    bool
        [`True`][] if the inventory can be viewed, else [`False`][].
        If this is [`False`][], you should exit the command.
    """
    ...

async def can_mention(players: list[Player]) -> discord.AllowedMentions: ...
