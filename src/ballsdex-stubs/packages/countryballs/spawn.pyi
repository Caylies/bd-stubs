import asyncio
from abc import abstractmethod
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Literal, NamedTuple

import discord

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot
    from discord.ext.commands import Context

class CachedMessage(NamedTuple):
    content: str
    author_id: int

class BaseSpawnManager:
    """
    A class instancied on cog load that will include the logic determining when a countryball
    should be spawned. You can implement your own version and configure it in config.yml.

    Be careful with optimization and memory footprint, this will be called very often and should
    not slow down the bot or cause memory leaks.
    """

    bot: "BallsDexBot"

    @abstractmethod
    async def handle_message(self, message: discord.Message) -> bool | tuple[Literal[True], str]:
        """
        Handle a message event and determine if a countryball should be spawned next.

        Parameters
        ----------
        message: discord.Message
            The message that triggered the event

        Returns
        -------
        bool | tuple[Literal[True], str]
            `True` if a countryball should be spawned, else `False`.

            If a countryball should spawn, do not forget to cleanup induced context to avoid
            infinite spawns.

            You can also return a tuple (True, msg) to indicate which spawn algorithm has been
            used, which is then reported to prometheus. This is useful for comparing the results
            of your algorithms using A/B testing.
        """
        ...

    @abstractmethod
    async def admin_explain(self, ctx: "Context[BallsDexBot]", guild: discord.Guild):
        """
        Invoked by "/admin cooldown", this function should provide insights of the cooldown
        system for admins.

        Parameters
        ----------
        ctx: ~discord.ext.commands.Context[BallsDexBot]
            The context of the invoking hybrid command
        guild: discord.Guild
            The guild that is targeted for the insights
        """
        ...

@dataclass
class SpawnCooldown:
    """
    Represents the default spawn internal system per guild. Contains the counters that will
    determine if a countryball should be spawned next or not.

    Attributes
    ----------
    time: datetime
        Time when the object was initialized. Block spawning when it's been less than ten minutes
    scaled_message_count: float
        A number starting at 0, incrementing with the messages until reaching `threshold`. At this
        point, a ball will be spawned next.
    threshold: int
        The number `scaled_message_count` has to reach for spawn.
        Determined randomly with `SPAWN_CHANCE_RANGE`
    lock: asyncio.Lock
        Used to ratelimit messages and ignore fast spam
    message_cache: ~collections.deque[CachedMessage]
        A list of recent messages used to reduce the spawn chance when too few different chatters
        are present. Limited to the 100 most recent messages in the guild.
    """

    time: datetime
    scaled_message_count: float = ...
    threshold: int = ...
    lock: asyncio.Lock = field(init=False)
    message_cache: deque[CachedMessage] = ...

    def reset(self, time: datetime): ...
    async def increase(self, message: discord.Message) -> bool: ...

class SpawnManager(BaseSpawnManager):
    cooldowns: dict[int, SpawnCooldown]

    async def handle_message(self, message: discord.Message) -> bool: ...
    async def admin_explain(self, ctx: "Context[BallsDexBot]", guild: discord.Guild): ...
