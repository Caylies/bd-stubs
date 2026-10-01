from typing import TYPE_CHECKING

from aiohttp import web
from prometheus_client import Counter

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

caught_balls: Counter

class PrometheusServer:
    """
    Host an HTTP server for metrics collection by Prometheus.
    """

    bot: "BallsDexBot"
    host: str
    port: int

    app: web.Application
    runner: web.AppRunner
    site: web.TCPSite

    def __init__(
        self, bot: "BallsDexBot", host: str = "localhost", port: int = 15260
    ) -> None: ...
    async def collect_metrics(self) -> None: ...
    async def get(self, request: web.Request) -> web.Response: ...
    async def setup(self) -> None: ...
    async def run(self) -> None: ...
    async def stop(self) -> None: ...
