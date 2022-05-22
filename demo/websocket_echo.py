import asyncio
import json
import sys
from typing import Optional

from pykorbit.websocket_api import KorbitWebsocketApi


class KorbitWebsocketEcho(KorbitWebsocketApi):
    def __init__(self, logging_level: Optional[str] = None):
        super().__init__(logging_level=logging_level)

    async def worker(self, msg: str) -> None:
        msg = json.loads(msg)
        json.dump(msg, sys.stdout)


if __name__ == "__main__":
    ws = KorbitWebsocketEcho()

    asyncio.run(
        ws.connect_and_subscribe_ticker(
            currency_pairs="btc_krw",
        )
    )
