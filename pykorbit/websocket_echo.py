import json
from typing import Optional

from .websocket_public import KorbitWebsocketPublic


class KorbitWebsocketEcho(KorbitWebsocketPublic):
    def __init__(self, logging_level: Optional[str] = None):
        super().__init__(logging_level=logging_level)

    async def worker(self, msg: str) -> None:
        msg = json.loads(msg)
        print(msg)
