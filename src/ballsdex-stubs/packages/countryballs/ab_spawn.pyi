from typing import TYPE_CHECKING, Literal

from ballsdex.packages.countryballs.spawn import BaseSpawnManager

if TYPE_CHECKING:
    import discord
    from discord.ext.commands import Context

    from ballsdex.core.bot import BallsDexBot

class ABSpawner(BaseSpawnManager):
    """
    This is an unused class made available for A/B testing your spawn algorithms.
    https://en.wikipedia.org/wiki/A/B_testing

    Using this, you can mix two different spawn managers with a repartition of your choosing to
    test and see how well it performs. Prometheus can then be used to compare the results.

    Each guild will be assigned to one of your spawn manager defined below, using the configured
    percentage.
    """

    percentage: int
    manager_class_a: type[BaseSpawnManager]
    manager_class_b: type[BaseSpawnManager]

    def get_manager(self, guild: "discord.Guild") -> BaseSpawnManager:
        """
        Return manager A or B for the guild. This will consistently return the same
        manager accross restarts, unless the percentage is changed.
        """
        ...

    async def handle_message(self, message: "discord.Message") -> bool | tuple[Literal[True], str]: ...
    async def admin_explain(self, ctx: "Context[BallsDexBot]", guild: "discord.Guild"): ...
