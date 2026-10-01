from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot
    from bd_models.models import Ball

class Settings(models.Model):
    bot_token: str
    prefix: str
    collectible_name: str
    plural_collectible_name: str

    bot_name: str
    balls_slash_name: str
    site_base_url: str

    currency_name: str | None
    currency_plural_name: str | None
    currency_symbol: str | None
    currency_symbol_before: bool
    currency_emoji_id: int | None

    @property
    def currency_plural(self) -> str: ...
    @property
    def currency_enabled(self) -> bool: ...
    def currency_emoji(self, bot: "BallsDexBot") -> str | None: ...
    def currency_display_name(self, bot: "BallsDexBot | None" = None) -> str: ...
    def currency_display_plural(self, bot: "BallsDexBot | None" = None) -> str: ...

    favorited_collectible_emoji: str
    max_favorites: int
    max_attack_bonus: int
    max_health_bonus: int
    show_rarity: bool
    catch_button_label: str

    class TipPosition(models.IntegerChoices):
        ABOVE_BUTTON = 1
        BELOW_BUTTON = 2

    tip_chance: int
    tip_position: int
    tip_container: bool

    spawn_chance_min: int
    spawn_chance_max: int
    spawn_manager: str

    about_description: str
    repository: str
    discord_invite: str
    terms_of_service: str
    privacy_policy: str

    admin_channel_ids: str

    @property
    def inv_privacy_bypass_ids(self) -> list[int]: ...

    webhook_logging: str | None

    team_owners: bool
    coowners: str | None

    @property
    def co_owners(self) -> list[int]: ...

    prometheus_enabled: bool
    prometheus_host: str
    prometheus_port: int

    client_id: int | None
    client_secret: str | None

    sentry_dsn: str | None
    sentry_env: str

    prompts: models.QuerySet["PromptMessage"]
    tips: models.QuerySet["Tip"]

    @property
    def catch_messages(self) -> dict[str, float]: ...
    @property
    def wrong_messages(self) -> dict[str, float]: ...
    @property
    def spawn_messages(self) -> dict[str, float]: ...
    @property
    def slow_messages(self) -> dict[str, float]: ...
    def get_random_message(self, category: "PromptMessage.PromptType") -> str: ...
    def get_formatted_message(
        self,
        category: "PromptMessage.PromptType",
        model: "Ball",
        mention: str,
        bot: "BallsDexBot",
        **kwargs: str,
    ) -> str: ...
    @property
    def tip_messages(self) -> dict[str, float]: ...
    def get_random_tip(self) -> str | None:
        """
        Pick a random tip, weighted by rarity. Returns `None` if no tip is enabled.
        """
        ...

    def get_formatted_tip(self) -> str | None:
        """
        Pick a random tip and substitute its placeholders. Returns `None` if no tip is enabled.

        Slash command references (`</command name>`) are *not* resolved here, since this requires
        the bot to be running. Use `ballsdex.core.utils.formatting.format_command_mentions` for this.
        """
        ...

    @property
    def log_channel(self) -> None: ...
    def clean(self) -> None: ...
    def __str__(self) -> str: ...

class PromptMessage(models.Model):
    class PromptType(models.IntegerChoices):
        CATCH = 1
        WRONG = 2
        SPAWN = 3
        SLOW = 4

    settings: Settings
    message: str
    category: int
    rarity: float

    def __str__(self) -> str: ...

class Tip(models.Model):
    settings: Settings
    message: str
    enabled: bool
    rarity: float

    def __str__(self) -> str: ...

settings: Settings

def load_settings() -> None: ...
