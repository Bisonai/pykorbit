import json
from abc import ABC, abstractstaticmethod
from typing import List

import websockets
from websockets.client import WebSocketClientProtocol

from .exception import KorbitConnectionFailed
from .utils import utc_now_ms


class KorbitWebsocket(ABC):
    async def connect_and_receive(
        self,
        access_token: str,
        channels: List[str],
    ):
        """
        Connect to websocket, detect if connection was established,
        start receiving messages and and process them with `worker`
        method.

        Websocket is automatically closed on exiting this method and
        recovered if connection is corrupted.

        Raises
            InvalidURI – if uri isn’t a valid WebSocket URI.
            InvalidHandshake – if the opening handshake fails.
            TimeoutError – if the opening handshake times out.
            ConnectionClosed – when the connection is closed.
            TypeError – if message doesn’t have a supported type.
            KorbitConnectionFailed - if connection to Korbit was not
            successfull
        """
        uri = "wss://ws.korbit.co.kr/v1/user/push"
        async for ws in websockets.connect(
            uri,
            ping_interval=None,  # FIXME
        ):
            try:
                subscribe_fmt = json.dumps(
                    {
                        "accessToken": access_token,
                        "timestamp": utc_now_ms(),
                        "event": "korbit:subscribe",
                        "data": {
                            "channels": channels,
                        },
                    }
                )

                await ws.send(subscribe_fmt)

                await KorbitWebsocket._test_connection(
                    ws,
                    expected_event="korbit:connected",
                )

                await KorbitWebsocket._test_connection(
                    ws,
                    expected_event="korbit:subscribe",
                )

                await self.receive_loop(ws)

            except websockets.ConnectionClosed:
                # Open new websocket connection if current connection
                # was closed.
                continue

    @staticmethod
    async def _test_connection(
        ws: WebSocketClientProtocol,
        expected_event: str,
    ):
        """
        Raises:
            KorbitConnectionFailed
        """
        recv_event = json.loads(await ws.recv()).get("event")
        if recv_event != expected_event:
            raise KorbitConnectionFailed(f"{recv_event} != {expected_event}")

    async def receive_loop(self, ws: WebSocketClientProtocol) -> None:
        """Process every incoming message with `worker` method.

        Raises:
            ConnectionClosed – when the connection is closed.
            RuntimeError – if two coroutines call recv() concurrently.
        """
        async for msg in ws:
            await self.worker(msg)

    @abstractstaticmethod
    async def worker(msg: str) -> None:
        raise NotImplementedError
