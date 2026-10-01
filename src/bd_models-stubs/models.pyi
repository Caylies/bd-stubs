from datetime import datetime
from io import BytesIO
from typing import TYPE_CHECKING, Any, Self

import discord
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.safestring import SafeText

from ballsdex.core.discord import View

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

def transform_media(path: str) -> str: ...
def image_display(image_link: str) -> SafeText: ...

balls: dict[int, Ball]
regimes: dict[int, Regime]
economies: dict[int, Economy]
specials: dict[int, Special]
groups: dict[int, BallGroup]

class QuerySet[T: models.Model](models.QuerySet[T]):
    def get_or_none(self, *args: Any, **kwargs: Any) -> T | None: ...
    async def aget_or_none(self, *args: Any, **kwargs: Any) -> T | None: ...
    async def aall(self) -> list[T]: ...

class Manager[T: models.Model](models.Manager[T], QuerySet[T]): ...  # type: ignore

class EnabledManager[T: models.Model](Manager[T]):
    def get_queryset(self) -> models.QuerySet[T]: ...

class SpecialEnabledManager(Manager["Special"]):
    def get_queryset(self) -> models.QuerySet[Special]: ...

class BaseBallInstanceManager[T: models.Model](Manager[T]):
    def with_stats(self) -> models.QuerySet[T]: ...

class BallInstanceManager[T: models.Model](BaseBallInstanceManager[T]):
    def get_queryset(self) -> models.QuerySet[T]: ...

class TradeableManager[T: models.Model](BallInstanceManager[T]):
    def get_queryset(self) -> models.QuerySet[T]: ...

class GuildConfig(models.Model):
    guild_id: int
    spawn_channel: int | None
    enabled: bool
    silent: bool
    manual_drop_enabled: bool
    tips_enabled: bool
    admin_command_synced: bool

    objects: Manager[Self]

    def __str__(self) -> str: ...

class Player(models.Model):
    discord_id: int
    money: int
    donation_policy: int
    privacy_policy: int
    mention_policy: int
    friend_policy: int
    trade_cooldown_policy: int
    extra_data: dict[str, Any]

    objects: Manager[Self]

    balls: models.QuerySet["BallInstance"]

    def __str__(self) -> str: ...
    def is_blacklisted(self) -> bool: ...
    async def is_friend(self, other_player: "Player") -> bool: ...
    async def is_blocked(self, other_player: "Player") -> bool: ...
    @property
    def can_be_mentioned(self) -> bool: ...
    async def add_money(self, amount: int) -> int: ...
    async def remove_money(self, amount: int) -> None: ...
    def can_afford(self, amount: int) -> bool: ...

class Economy(models.Model):
    name: str
    icon: ImageFieldFile

    objects: Manager[Self]

    def __str__(self) -> str: ...

class Regime(models.Model):
    name: str
    background: ImageFieldFile

    objects: Manager[Self]

    def __str__(self) -> str: ...

class Special(models.Model):
    name: str
    catch_phrase: str | None
    start_date: datetime | None
    end_date: datetime | None
    rarity: float
    emoji: str | None
    background: ImageFieldFile | None
    tradeable: bool
    hidden: bool
    credits: str | None

    objects: Manager[Self]
    enabled_objects: SpecialEnabledManager

    def __str__(self) -> str: ...

class Ball(models.Model):
    country: str
    health: int
    attack: int
    rarity: float
    emoji_id: int
    wild_card: ImageFieldFile
    collection_card: ImageFieldFile
    credits: str
    capacity_name: str
    capacity_description: str
    capacity_logic: dict[str, Any]
    enabled: bool
    short_name: str | None
    catch_names: str | None
    tradeable: bool
    economy: Economy | None
    economy_id: int | None
    regime: Regime
    regime_id: int
    created_at: datetime | None
    translations: str | None

    objects: Manager[Self]
    enabled_objects: EnabledManager[Self]
    tradeable_objects: TradeableManager[Self]

    @property
    def cached_regime(self) -> Regime: ...
    @property
    def cached_economy(self) -> Economy | None: ...
    def __str__(self) -> str: ...
    def collection_image(self) -> SafeText: ...
    def spawn_image(self) -> SafeText: ...
    def save(self, **kwargs) -> None: ...

class BallGroup(models.Model):
    name: str
    countryballs: models.QuerySet[Ball]

    objects: Manager[Self]

    def __str__(self) -> str: ...
    @property
    def balls(self) -> list[Ball]: ...

class BallInstance(models.Model):
    catch_date: datetime
    health_bonus: int
    attack_bonus: int
    ball: Ball
    ball_id: int
    player: Player
    player_id: int
    trade_player: Player | None
    trade_player_id: int | None
    favorite: bool
    special: Special | None
    special_id: int | None
    server_id: int | None
    tradeable: bool
    extra_data: dict[str, Any]
    locked: datetime | None
    spawned_time: datetime | None
    deleted: bool

    objects: BallInstanceManager[Self]
    tradeable_objects: TradeableManager[Self]
    all_objects: BaseBallInstanceManager[Self]

    def short_description(self, *, is_trade: bool = False) -> str:
        """
        Return a short string representation. Similar to str(x) without arguments.
        """
        ...

    def __str__(self) -> str: ...
    @property
    def is_tradeable(self) -> bool: ...
    @property
    def attack(self) -> int: ...
    @property
    def health(self) -> int: ...
    @property
    def special_card(self) -> ImageFieldFile | None: ...
    @property
    def countryball(self) -> Ball: ...
    @property
    def specialcard(self) -> Special | None: ...
    def admin_description(self) -> SafeText: ...
    def catch_time(self) -> str: ...
    def description(
        self,
        *,
        short: bool = False,
        include_emoji: bool = False,
        bot: "BallsDexBot | None" = None,
        is_trade: bool = False,
    ) -> str: ...
    def draw_card(self) -> BytesIO: ...
    async def prepare_for_message(
        self, interaction: discord.Interaction["BallsDexBot"]
    ) -> tuple[str, discord.File, View]: ...
    async def lock_for_trade(self) -> None: ...
    async def unlock(self) -> None: ...
    async def is_locked(self, refresh: bool = True) -> bool: ...

class BlacklistedID(models.Model):
    discord_id: int
    reason: str | None
    date: datetime | None
    moderator_id: int | None

    objects: Manager[Self]

class BlacklistedGuild(models.Model):
    discord_id: int
    reason: str | None
    date: datetime | None
    moderator_id: int | None

    objects: Manager[Self]

class BlacklistHistory(models.Model):
    discord_id: int
    moderator_id: int
    reason: str | None
    date: datetime
    id_type: str
    action_type: str

    objects: Manager[Self]

class Trade(models.Model):
    date: datetime
    player1: Player
    player1_id: int
    player1_money: int
    player2: Player
    player2_id: int
    player2_money: int
    tradeobject_set: models.QuerySet["TradeObject"]

    objects: Manager[Self]

    def __str__(self) -> str: ...

class TradeObject(models.Model):
    ballinstance: BallInstance
    ballinstance_id: int
    player: Player
    player_id: int
    trade: Trade
    trade_id: int

    objects: Manager[Self]

class Friendship(models.Model):
    since: datetime
    player1: Player
    player1_id: int
    player2: Player
    player2_id: int

    objects: Manager[Self]

class Block(models.Model):
    date: datetime
    player1: Player
    player1_id: int
    player2: Player
    player2_id: int

    objects: Manager[Self]
