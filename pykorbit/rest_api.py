# https://apidocs.korbit.co.kr/#public
import logging
from typing import Any, Dict, List

from .exception import KorbitUnexpectedResponse
from .utils import send_get_request

_ALLOWED_TIMES = (
    "day",
    "hour",
    "minute",
)


class KorbitRestApi:
    @staticmethod
    def ticker(currency_pair: str) -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#ticker

        Response:
          {
            "timestamp": 1389678052000,
            "last": "569000"
          }
        """
        logging.debug("Ticker")

        url = "https://api.korbit.co.kr/v1/ticker"
        params = [("currency_pair", currency_pair)]

        return send_get_request(
            url,
            params=params,
        )

    def detailed_ticker(currency_pair: str) -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#detailed-ticker

        Response:
          {
            "timestamp": 1558590089274,
            "last": "9198500",
            "open": "9500000",
            "bid": "9192500",
            "ask": "9198000",
            "low": "9171500",
            "high": "9599000",
            "volume": "1539.18571988",
            "change": "-301500",
            "changePercent": "-3.17"
          }
        """
        logging.debug("Detailed Ticker")

        url = "https://api.korbit.co.kr/v1/ticker/detailed"
        params = [("currency_pair", currency_pair)]

        return send_get_request(
            url,
            params=params,
        )

    @staticmethod
    def orderbook(currency_pair: str) -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#orderbook

        Response:
          {
            "timestamp" : 1386135077000,
            "bids" : [["1100000", "0.0103918", "1"], ["1000000", "0.01000000", "1"], ... ],
            "asks" : [["569000", "0.50000000", "1"], ["568500", "2.00000000", "1"], ... ]
          }
        """
        logging.debug("Orderbook")

        url = "https://api.korbit.co.kr/v1/orderbook"
        params = [("currency_pair", currency_pair)]

        return send_get_request(
            url,
            params=params,
        )

    @staticmethod
    def list_of_filled_orders(
        currency_pair: str,
        time: str = "hour",
    ) -> List[Dict]:
        """https://apidocs.korbit.co.kr/#list-of-filled-orders

        Response:
          [
            {
              "timestamp": 1389678052000,
              "tid": "22546",
              "price": "569000",
              "amount": "0.01000000",
              "type": "buy"
            },
            {
             "timestamp": 1389678017000,
             "tid": "22545",
             "price": "580000",
             "amount": "0.01000000",
             "type": "sell"
           }
            ...
          ]
        """
        logging.debug("List of Filled Orders")

        assert time in _ALLOWED_TIMES
        url = "https://api.korbit.co.kr/v1/transactions"
        params = [
            ("currency_pair", currency_pair),
            ("time", time),
        ]

        return send_get_request(
            url,
            params=params,
        )

    @staticmethod
    def constants() -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#constants-deprecated
        DEPRECATED

        Raises:
          KorbitUnexpectedResponse
        """
        logging.debug("Constants")

        url = "https://api.korbit.co.kr/v1/constants"
        response = send_get_request(url)
        response_echange = response.get("exchange")

        if response_echange:
            return response_echange
        else:
            raise KorbitUnexpectedResponse(response_echange)

    @staticmethod
    def currency_pairs() -> List[str]:
        return list(KorbitRestApi.constants().keys())
