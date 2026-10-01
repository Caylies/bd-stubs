from typing import TYPE_CHECKING, Self

import discord
from discord.ui import ActionRow, Button, TextInput

from ballsdex.core.discord import LayoutView, Modal
from bd_models.models import Ball, BallInstance, Player, Special

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

class CountryballNamePrompt(Modal):
    name: TextInput

    view: "BallSpawnView"

    def __init__(self, view: "BallSpawnView") -> None: ...
    async def on_error(
        self, interaction: discord.Interaction["BallsDexBot"], error: Exception
    ) -> None: ...
    async def on_submit(
        self, interaction: discord.Interaction["BallsDexBot"]
    ) -> None: ...

class CatchRow(ActionRow["BallSpawnView"]):
    """
    The action row holding the catch button. Components v2 does not allow buttons to be defined
    directly on the view, they must be wrapped in an action row.
    """

    spawn_view: "BallSpawnView"
    catch_button: Button["BallSpawnView"]

    def __init__(self, spawn_view: "BallSpawnView") -> None: ...

class BallSpawnView(LayoutView):
    """
    BallSpawnView is a Discord UI view that represents the spawning and interaction logic for a
    countryball in the BallsDex bot. It handles user interactions, spawning mechanics, and
    countryball catching logic.

    Attributes
    ----------
    bot: BallsDexBot
    model: Ball
        The ball being spawned.
    algo: str | None
        The algorithm used for spawning, used for metrics.
    message: discord.Message
        The Discord message associated with this view once created with `spawn`.
    caught: bool
        Whether the countryball has been caught yet.
    ballinstance: BallInstance | None
        If this is set, this ball instance will be spawned instead of creating a new ball instance.
        All properties are preserved, and if successfully caught, the owner is transferred (with
        a trade entry created). Use the `from_existing` constructor to use this.
    special: Special | None
        Force the spawned countryball to have a special event attached. If None, a random one will
        be picked.
    atk_bonus: int | None
        Force a specific attack bonus if set, otherwise random range defined in config.yml.
    hp_bonus: int | None
        Force a specific health bonus if set, otherwise random range defined in config.yml.
    """

    bot: "BallsDexBot"
    model: Ball
    algo: str | None
    message: discord.Message
    caught: bool
    ballinstance: BallInstance | None
    special: Special | None
    atk_bonus: int | None
    hp_bonus: int | None
    og_id: int

    catch_row: CatchRow

    def __init__(self, bot: "BallsDexBot", model: Ball) -> None: ...
    @property
    def catch_button(self) -> Button["BallSpawnView"]: ...
    @property
    def name(self) -> str: ...
    async def interaction_check(
        self, interaction: discord.Interaction["BallsDexBot"], /
    ) -> bool: ...
    async def on_timeout(self) -> None: ...
    @classmethod
    async def from_existing(
        cls, bot: "BallsDexBot", ball_instance: BallInstance
    ) -> Self:
        """
        Get an instance from an existing `BallInstance`. Instead of creating a new ball instance,
        this will transfer ownership of the existing instance when caught.

        The ball instance must be unlocked from trades, and will be locked until caught or timed
        out.
        """
        ...

    @classmethod
    async def get_random(cls, bot: "BallsDexBot") -> Self:
        """
        Get a new instance with a random countryball. Rarity values are taken into account.
        """
        ...

    @staticmethod
    def get_random_special() -> Special | None: ...
    async def get_tip(self, guild_id: int | None = None) -> str | None:
        """
        Roll for a tip to display below the spawn message.

        Parameters
        ----------
        guild_id: int | None
            The guild where the countryball spawns. If set, its configuration is checked, as server
            admins may opt out of tips.

        Returns
        -------
        str | None
            A formatted tip, or `None` if tips are disabled, no tip is configured, or the roll
            against `tip_chance` failed.
        """
        ...

    async def build(
        self, spawn_message: str, file_name: str, guild_id: int | None = None
    ) -> None:
        """
        Populate the components of this view. This must be called once, right before sending the
        spawn message, since the layout depends on the message and the attached image.

        Parameters
        ----------
        spawn_message: str
            The formatted spawn message, displayed above the countryball.
        file_name: str
            The name of the image uploaded alongside this view.
        guild_id: int | None
            The guild where the countryball spawns, used to determine if a tip may be displayed.
        """
        ...

    async def spawn(self, channel: discord.TextChannel) -> bool:
        """
        Spawn a countryball in a channel.

        Parameters
        ----------
        channel: discord.TextChannel
            The channel where to spawn the countryball. Must have permission to send messages
            and upload files as a bot (not through interactions).

        Returns
        -------
        bool
            `True` if the operation succeeded, otherwise `False`. An error will be displayed
            in the logs if that's the case.
        """
        ...

    def is_name_valid(self, text: str) -> bool:
        """
        Check if the prompted name is valid.

        Parameters
        ----------
        text: str
            The text entered by the user. It will be lowered and stripped of enclosing blank
            characters.

        Returns
        -------
        bool
            Whether the name matches or not.
        """
        ...

    async def catch_ball(
        self,
        user: discord.User | discord.Member,
        *,
        player: Player | None,
        guild: discord.Guild | None,
    ) -> tuple[BallInstance, bool]:
        """
        Mark this countryball as caught and assign a new `BallInstance` (or transfer ownership if
        attribute `ballinstance` was set).

        Parameters
        ----------
        user: discord.User | discord.Member
            The user that will obtain the new countryball.
        player: Player
            If already fetched, add the player model here to avoid an additional query.
        guild: discord.Guild | None
            If caught in a guild, specify here for additional logs. Will be extracted from `user`
            if it's a member object.

        Returns
        -------
        tuple[bool, BallInstance]
            A tuple whose first value indicates if this is the first time this player catches this
            countryball. Second value is the newly created countryball.

            If `ballinstance` was set, this value is returned instead.

        Raises
        ------
        RuntimeError
            The `caught` attribute is already set to `True`. You should always check before calling
            this function that the ball was not caught.
        """
        ...

    def get_catch_message(
        self, ball: BallInstance, new_ball: bool, mention: str
    ) -> str:
        """
        Generate a user-facing message after a ball has been caught.

        Parameters
        ----------
        ball: BallInstance
            The newly created ball instance
        new_ball: bool
            Boolean indicating if this is a new countryball in completion
            (as returned by `catch_ball`)
        """
        ...
