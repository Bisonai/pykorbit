import json
from typing import Optional

from .websocket_public import KorbitWebsocketPublic


class KorbitWebsocketEcho(KorbitWebsocketPublic):
    def __init__(
        self,
        access_token: Optional[str] = None,
        logging_level: Optional[str] = None,
    ):
        super().__init__(
            access_token=access_token,
            logging_level=logging_level,
        )

    async def worker(self, msg: str) -> None:
        msg = json.loads(msg)
        print(msg)
