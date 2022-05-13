import json

from .websocket import KorbitWebsocket


class KorbitWebsocketEcho(KorbitWebsocket):
    @staticmethod
    async def worker(msg: str) -> None:
        msg = json.loads(msg)
        print(msg)
