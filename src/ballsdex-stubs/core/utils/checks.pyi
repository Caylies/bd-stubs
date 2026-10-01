"""
Internal checks for commands. To be used as decorators on commands.

Multiple decorators can be chained, in which case all conditions must pass.

These checks can only be used on text and hybrid commands. To use them on application commands, use the [`app_check`][]
wrapper.

See also
--------
    - [`discord.py` general documentation on checks](https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#checks)
    - [List of built-in `discord.py` checks](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#checks)
"""

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from discord.ext.commands._types import Check as CommandsCheck

    from ballsdex.core.bot import BallsDexBot
    from users.models import User

type Context = commands.Context["BallsDexBot"]

registered_perms: set[str]

async def check_perms(): ...

async def get_user_for_check(
    bot: "BallsDexBot", user: discord.abc.User
) -> "bool | User":
    """
    Get a Django user ready and performs common permission checking.

    Paremeters
    ----------
    ctx: commands.Context[BallsDexBot]
        The context of the invoked command

    Returns
    -------
    bool | django.contrib.auth.models.User
        - [`False`][] if the user should not be granted anything (not found or inactive)
        - [`True`][] if the user should immediately be granted permissions (superuser or bot owner)
        - [`User`][django.contrib.auth.models.User] if the user was found but should be inspected further
    """
    ...

def is_staff():
    """
    Checks that the user is registered on Django and has the staff or superuser status.
    """
    ...

def is_superuser():
    """
    Checks that the user is registered on Django and has the superuser status.
    """
    ...

def has_permissions(*perms: str):
    """
    Checks that the user is registered on Django and has the required permissions.
    """
    ...

def has_any_permissions(*perms: str):
    """
    Checks that the user is registered on Django and has any of the required permissions.
    """
    ...

def app_check(func: "CommandsCheck[Context]"):
    """
    Converts a commands check decorator to an app command compatible check decorator.

    Example
    -------
        from ballsdex.core.utils.checks import app_check, is_staff

        @app_commands.command()
        @app_check(is_staff())
        async def command(interaction):
            ...
    """

    async def check(interaction: discord.Interaction["BallsDexBot"]):
        return await func.predicate(
            await commands.Context.from_interaction(interaction)
        )

    return app_commands.check(check)
