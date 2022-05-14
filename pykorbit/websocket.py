# https://apidocs.korbit.co.kr/#public-websocket
import json
import logging
from abc import ABC, abstractstaticmethod
from typing import Any, Dict, List, Optional

import websockets
from websockets.client import WebSocketClientProtocol

from .exception import (KorbitMessageNotAccepted,
                        KorbitWebsocketMessageReceiveFailed)
from .logging import LOGGING_LEVELS
from .utils import utc_now_ms


class KorbitWebsocket(ABC):
    def __init__(
        self,
        access_token: str,
        logging_level: Optional[str] = None,
    ):
        logging.basicConfig(
            level=LOGGING_LEVELS.get(
                logging_level,
                logging.INFO,
            ),
        )

        self.access_token = access_token
        self.ws_uri = "wss://ws.korbit.co.kr/v1/user/push"
        self.ws = None

    @staticmethod
    def _build_event_request(
        access_token: str,
        event: str,
        channels: List[str],
    ) -> Dict[str, Any]:
        return json.dumps(
            {
                "accessToken": access_token,
                "timestamp": utc_now_ms(),
                "event": event,
                "data": {
                    "channels": channels,
                },
            }
        )

    @staticmethod
    async def _test_event_response(
        ws: WebSocketClientProtocol,
        expected_event: str,
    ) -> None:
        """
        Raises:
            KorbitWebsocketMessageReceiveFailed
            KorbitMessageNotAccepted
        """
        try:
            recv_event = json.loads(await ws.recv()).get("event")
        except Exception as e:
            raise KorbitWebsocketMessageReceiveFailed from e

        if recv_event != expected_event:
            raise KorbitMessageNotAccepted(f"{recv_event} != {expected_event}")

        logging.debug(f"Event {expected_event} OK")

    @staticmethod
    async def _send_request(
        ws: WebSocketClientProtocol,
        access_token: str,
        event_request: str,
        channels: List[str],
    ) -> None:
        """
        Raises:
            ConnectionClosed – when the connection is closed.
            TypeError – if message doesn’t have a supported type.
            KorbitWebsocketMessageReceiveFailed
            KorbitMessageNotAccepted
        """
        request_fmt = KorbitWebsocket._build_event_request(
            access_token,
            event_request,
            channels,
        )

        logging.debug(f"Event {event_request}")
        await ws.send(request_fmt)

        await KorbitWebsocket._test_event_response(
            ws,
            expected_event=event_request,
        )

    @staticmethod
    def _build_channels(
        pairs: List[str],
        channel_name: str,
    ) -> List[str]:
        assert len(list(filter(lambda p: ":" in p, pairs))) == 0
        return list(map(lambda p: f"{channel_name}:{p}", pairs))

    async def connect_and_subscribe_ticker(
        self,
        pairs: List[str],
    ) -> None:
        channels = self._build_channels(pairs, "ticker")
        await self.connect_and_subscribe(channels=channels)

    async def connect_and_subscribe_orderbook(
        self,
        pairs: List[str],
    ) -> None:
        channels = self._build_channels(pairs, "orderbook")
        await self.connect_and_subscribe(channels=channels)

    async def connect_and_subscribe_transaction(
        self,
        pairs: List[str],
    ) -> None:
        channels = self._build_channels(pairs, "transaction")
        await self.connect_and_subscribe(channels=channels)

    async def connect_and_subscribe(
        self,
        channels: List[str],
    ) -> None:
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
        """
        async for self.ws in websockets.connect(self.ws_uri):
            try:
                await KorbitWebsocket._test_event_response(
                    self.ws,
                    expected_event="korbit:connected",
                )

                await self.subscribe(channels)

                await self.receive_loop()

            except websockets.ConnectionClosed:
                # Open new websocket connection if current connection
                # was closed.
                continue

    async def subscribe(self, channels: List[str]) -> None:
        await self._send_request(
            self.ws,
            self.access_token,
            "korbit:subscribe",
            channels,
        )

    async def unsubscribe(self, channels: List[str]) -> None:
        await self._send_request(
            self.ws,
            self.access_token,
            "korbit:unsubscribe",
            channels,
        )

    async def receive_loop(self) -> None:
        """Process every incoming message with `worker` method.

        Raises:
            ConnectionClosed – when the connection is closed.
            RuntimeError – if two coroutines call recv() concurrently.
        """
        logging.debug("Starting event loop")
        async for msg in self.ws:
            await self.worker(msg)

    @abstractstaticmethod
    async def worker(msg: str) -> None:
        raise NotImplementedError
