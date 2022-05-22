# https://apidocs.korbit.co.kr/#public-websocket
import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import websockets
from websockets.client import WebSocketClientProtocol

from .exception import (KorbitMessageNotAccepted,
                        KorbitWebsocketMessageReceiveFailed)
from .logging import _ALLOWED_LOGGING_LEVELS
from .utils import utc_now_ms


class KorbitWebsocketApi(ABC):
    def __init__(self, logging_level: Optional[str] = None):
        logging.basicConfig(
            level=_ALLOWED_LOGGING_LEVELS.get(
                logging_level,
                logging.INFO,
            ),
        )

        self.ws_uri = "wss://ws.korbit.co.kr/v1/user/push"
        self.ws = None

    @staticmethod
    def _build_event_request(
        event: str,
        channels: List[str],
    ) -> Dict[str, Any]:
        return json.dumps(
            {
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
        request_fmt = KorbitWebsocketApi._build_event_request(
            event_request,
            channels,
        )

        logging.debug(f"Event {event_request}")
        await ws.send(request_fmt)

        await KorbitWebsocketApi._test_event_response(
            ws,
            expected_event=event_request,
        )

    @staticmethod
    def _build_channels(
        currency_pairs: List[str],
        channel_name: str,
    ) -> List[str]:
        if not isinstance(currency_pairs, list):
            currency_pairs = [currency_pairs]

        assert len(list(filter(lambda p: ":" in p, currency_pairs))) == 0
        return list(map(lambda p: f"{channel_name}:{p}", currency_pairs))

    async def connect_and_subscribe_ticker(
        self,
        currency_pairs: List[str] = [],
    ) -> None:
        """
        Ticker fields
          timestamp     Unix timestamp in milliseconds of the last filled order.
          last          Price of the last filled order.
          open          First price in 24 hours.
          bid           Best bid price.
          ask           Best ask price.
          low           Lowest price within the last 24 hours.
          high          Highest price within the last 24 hours.
          volume        Transaction volume within the last 24 hours.
          change        The change in the last price from the OPEN price.
          changePercent The rate of change in the last price from the OPEN price.
        """
        if currency_pairs:
            channels = self._build_channels(currency_pairs, "ticker")
        else:
            channels = ["ticker"]
        await self.connect_and_subscribe(channels=channels)

    async def connect_and_subscribe_orderbook(
        self,
        currency_pairs: List[str] = [],
    ) -> None:
        if currency_pairs:
            channels = self._build_channels(currency_pairs, "orderbook")
        else:
            channels = ["orderbook"]
        await self.connect_and_subscribe(channels=channels)

    async def connect_and_subscribe_transaction(
        self,
        currency_pairs: List[str] = [],
    ) -> None:
        if currency_pairs:
            channels = self._build_channels(currency_pairs, "transaction")
        else:
            channels = ["transaction"]
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

        Raises:
          InvalidURI – if uri isn’t a valid WebSocket URI.
          InvalidHandshake – if the opening handshake fails.
          TimeoutError – if the opening handshake times out.
          ConnectionClosed – when the connection is closed.
        """
        while True:
            try:
                self.ws = await websockets.connect(self.ws_uri)
            except asyncio.exceptions.CancelledError:
                logging.error("Reconnecting after asyncio.exceptions.CancelledError")
                continue
            except asyncio.exceptions.TimeoutError:
                logging.error("Reconnecting after asyncio.exceptions.TimeoutError")
                continue

            try:
                await KorbitWebsocketApi._test_event_response(
                    self.ws,
                    expected_event="korbit:connected",
                )

                await self.subscribe(channels)

                await self.receive_loop()

            except websockets.ConnectionClosed:
                # Open new websocket connection if current connection
                # was closed.
                logging.error("Connection closed")
                continue

    async def subscribe(self, channels: List[str]) -> None:
        await self._send_request(
            self.ws,
            "korbit:subscribe",
            channels,
        )

    async def unsubscribe(self, channels: List[str]) -> None:
        await self._send_request(
            self.ws,
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

    @abstractmethod
    async def worker(self, msg: str) -> None:
        raise NotImplementedError
