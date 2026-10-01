from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def get_queryset(self) -> models.QuerySet[User]: ...

class User(AbstractUser):
    discord_user_id: int | None
    objects: CustomUserManager  # type: ignore

    if TYPE_CHECKING:
        discord_id: int | None
