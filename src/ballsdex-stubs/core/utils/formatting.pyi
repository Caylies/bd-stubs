from re import Pattern
from typing import TYPE_CHECKING, Iterator, Sequence

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

COMMAND_MENTION_RE: Pattern[str]
"""
matches "</command>", "</command sub>" and "</command group sub>", the deepest nesting Discord allows
"""

def pagify(
    text: str,
    delims: Sequence[str] = ["\n"],
    *,
    priority: bool = False,
    escape_mass_mentions: bool = True,
    shorten_by: int = 8,
    page_length: int = 2000,
    prefix: str = "",
    suffix: str = "",
) -> Iterator[str]:
    """
    Generate multiple pages from the given text.

    Parameters
    ----------
    text: str
        The content to pagify and send.
    delims: Sequence[str]
        Characters where page breaks will occur. If no delimiters are found
        in a page, the page will break after `page_length` characters.
        By default this only contains the newline.

    Other Parameters
    ----------------
    priority: bool
        Set to `True` to choose the page break delimiter based on the
        order of `delims`. Otherwise, the page will always break at the
        last possible delimiter.
    escape_mass_mentions: bool
        If `True`, any mass mentions (here or everyone) will be
        silenced.
    shorten_by: int
        How much to shorten each page by. Defaults to 8.
    page_length: int
        The maximum length of each page. Defaults to 2000.

    Yields
    ------
    str
        Pages of the given text.
    """
    ...

def escape(text: str, *, mass_mentions: bool = False, formatting: bool = False) -> str:
    """
    Get text with all mass mentions or markdown escaped.

    Parameters
    ----------
    text: str
        The text to be escaped.
    mass_mentions: bool
        Set to `True` to escape mass mentions in the text.
    formatting: bool
        Set to `True` to escape any markdown formatting in the text.

    Returns
    -------
    str
        The escaped text.
    """
    ...

def format_command_mentions(text: str, bot: "BallsDexBot") -> str:
    """
    Replace every `</command name>` reference in a text by a clickable slash command mention.

    This allows admin-configured messages to link to slash commands without knowing their IDs.
    Unknown commands, or commands that were never synced, fall back to `` `/command name` ``.

    Parameters
    ----------
    text: str
        The text to scan for command references.
    bot: BallsDexBot
        The bot, used to resolve command IDs assigned on sync.

    Returns
    -------
    str
        The text with its command references resolved.
    """
    ...
