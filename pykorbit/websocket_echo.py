import json

from .websocket import KorbitWebsocket


class KorbitWebsocketEcho(KorbitWebsocket):
    def __init__(self, access_token: str):
        super().__init__(access_token=access_token)

    @staticmethod
    async def worker(msg: str) -> None:
        msg = json.loads(msg)
        print(msg)
