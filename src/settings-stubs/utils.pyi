from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

def format_currency(amount: int, shortened: bool = True, bot: "BallsDexBot | None" = None) -> str: ...

def parse_currency(text: str) -> int:
    """
    Parse a user-supplied amount back into an integer, raising `ValueError` if it is not one.
    """
    ...
