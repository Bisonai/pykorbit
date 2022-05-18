import asyncio
import json
import time
from typing import Optional

from pykorbit.websocket_api import KorbitWebsocketApi


def now_milliseconds() -> int:
    return time.time_ns() // 1_000_000


class KorbitWebsocketSpeed(KorbitWebsocketApi):
    def __init__(self, logging_level: Optional[str] = None):
        super().__init__(logging_level=logging_level)

    async def worker(self, msg: str) -> None:
        client_ts = now_milliseconds()
        msg = json.loads(msg)
        server_ts = msg["timestamp"]
        print(client_ts - server_ts)


if __name__ == "__main__":
    ws = KorbitWebsocketSpeed()

    asyncio.run(
        ws.connect_and_subscribe_ticker(
            currency_pairs="btc_krw",
        )
    )
