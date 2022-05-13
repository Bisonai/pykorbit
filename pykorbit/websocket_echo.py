import json
from typing import Optional

from .websocket import KorbitWebsocket


class KorbitWebsocketEcho(KorbitWebsocket):
    def __init__(
        self,
        access_token: str,
        logging_level: Optional[str] = None,
    ):
        super().__init__(
            access_token=access_token,
            logging_level=logging_level,
        )

    @staticmethod
    async def worker(msg: str) -> None:
        msg = json.loads(msg)
        print(msg)
