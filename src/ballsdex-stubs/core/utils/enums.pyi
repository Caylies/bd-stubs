import enum

from typing import  Literal

DONATION_POLICY_MAP: dict[
    Literal[1, 2, 3, 4],
    Literal[
        "Accept all donations",
        "Approve donations",
        "Deny all donations",
        "Accept donations from friends only",
    ],
]

PRIVATE_POLICY_MAP: dict[
    Literal[1, 2, 3, 4],
    Literal[
        "Public",
        "Private",
        "Mutual Servers",
        "Friends",
    ],
]

MENTION_POLICY_MAP: dict[
    Literal[1, 2],
    Literal[
        "Allow all mentions",
        "Deny all mentions",
    ],
]

FRIEND_POLICY_MAP: dict[
    Literal[1, 2],
    Literal[
        "Allow all friend requests",
        "Deny all friend requests",
    ],
]

TRADE_COOLDOWN_POLICY_MAP: dict[
    Literal[1, 2],
    Literal[
        "Use 10s acceptance cooldown",
        "Bypass acceptance cooldown",
    ],
]

class SortingChoices(enum.Enum):
    alphabetic: str
    catch_date: str
    rarity: str
    special: str
    health: str
    attack: str
    health_bonus: str
    attack_bonus: str
    stats_bonus: str
    total_stats: str
    catch_time: str
    duplicates: str

class FilteringChoices(enum.Enum):
    only_specials: str
    non_specials: str
    self_caught: str
    traded_only: str
    this_server: str
    favorites: str
    duplicates: str
