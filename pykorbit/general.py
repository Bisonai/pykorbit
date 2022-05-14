# https://apidocs.korbit.co.kr/#private-general
import logging
from typing import Any, Dict, List

from .utils import build_bearer_token_header, send_get_request


class KorbitGeneral:
    @staticmethod
    def user_balances(access_token: str) -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#user-balances

        Response
          {
            "krw" : {
                "available" : "123000",
                "trade_in_use" : "13000",
                "withdrawal_in_use" : "0"
            },
            "btc" : {
                "available" : "1.50200000",
                "trade_in_use" : "0.42000000",
                "withdrawal_in_use" : "0.50280000",
                "avg_price": "7115500",
                "avg_price_updated_at": 1528944850000
            },
            ...
          }
        """
        logging.debug("User Balances")

        url = "https://api.korbit.co.kr/v1/user/balances"
        headers = build_bearer_token_header(access_token)

        return send_get_request(
            url,
            headers=headers,
        )

    @staticmethod
    def transfer_account_info(access_token: str) -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#transfer-account-info

        Response:
          {
            "deposit": {
              "btc": {
                "address" :"3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"
              },
              "etc": {
                "address" :"0x123f681646d4a755815f9cb19e1acc8565a0c2aa"
              },
              ...
            },
            "withdrawal": {
              ...
            }
          }
        """
        logging.debug("Transfer Account Info")

        url = "https://api.korbit.co.kr/v1/user/accounts"
        headers = build_bearer_token_header(access_token)

        return send_get_request(
            url,
            headers=headers,
        )

    @staticmethod
    def trading_volume_and_fees(
        access_token: str,
        pair: List[str] = [],
    ) -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#trading-volume-and-fees

        Response:
          {
            "eth_krw": {
              "volume" : "0",
              "maker_fee" : "0.00100000",
              "taker_fee" : "0.00200000"
            },
            ...
            "etc_krw": {
              "volume" : "6570000",
              "maker_fee" : "0.00100000",
              "taker_fee" : "0.00200000"
            },
            "total_volume" : "24140000",
            "timestamp" : 1386418990000
          }
        """
        logging.debug("Transfer Account Info")

        url = "https://api.korbit.co.kr/v1/user/volume"
        headers = build_bearer_token_header(access_token)
        params = [("currency_pair", p) for p in pair]

        return send_get_request(
            url,
            headers=headers,
            params=params,
        )
