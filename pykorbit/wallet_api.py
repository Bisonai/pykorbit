# https://apidocs.korbit.co.kr/#private-wallet
# https://apidocs.korbit.co.kr/#private-general
import logging
from typing import Any, Dict, List, Optional

from .utils import build_bearer_token_header, send_get_request

_ALLOWED_TRANSFER_TYPES = (
    "deposit",
    "withdrawal",
)


class KorbitWalletApi:
    """
    TODO
    * Request Crypto Currency Withdrawal
    * Cancel Transfer Request
    * Assign Crypto Currency Address
    """

    @staticmethod
    def view_transfers(
        access_token: str,
        currency: Optional[str] = None,
        type: Optional[str] = None,
        offset: int = 0,
        limit: int = 40,
    ) -> List[Dict]:
        """https://apidocs.korbit.co.kr/#view-transfers

        Response:
          [
            {
              "id": "270",
              "type": "deposit",
              "currency": "btc",
              "amount": "0.81140000",
              "completed_at": 11750020020,
              "updated_at": 11550050080,
              "created_at": 11550020020,
              "status": "filled",
              "details": {
                "transaction_id": "2d84855aa9c...",
                "address": "1F1zAaz5x1HUXrCNLbtMDqcw6o5GNx4xqX"
            },
              ...
          ]
        """
        logging.debug("View Transfers")

        url = "https://api.korbit.co.kr/v1/user/transfers"
        headers = build_bearer_token_header(access_token)
        params = [
            ("offset", offset),
            ("limit", limit),
        ]

        if currency:
            params.append(("currency", currency))

        if type:
            assert type in _ALLOWED_TRANSFER_TYPES
            params.append(("type", type))

        return send_get_request(
            url,
            headers=headers,
            params=params,
        )

    @staticmethod
    def query_status_of_deposit_and_withdrawal(
        access_token: str,
        currency: str,
        request_id: Optional[int] = None,
    ) -> List[Dict]:
        """https://api.korbit.co.kr/v1/user/coins/status

        Response:
          [
            {
              "timestamp": 1392620446000,
              "id": "5180",
              "type": "coin-in",
              "amount": { "currency": "btc", "value": "0.01"},
              "in": "1anjg6B2XbpjHx8LFw8mXHATH54vrxs2F",
              "completedAt": 1392620446100
            }
          ]"""
        logging.debug("Query Status of Deposit and Withdrawal")

        url = "https://api.korbit.co.kr/v1/user/coins/status"
        headers = build_bearer_token_header(access_token)

        params = [("type", type)]

        if request_id:
            params.append(("id", request_id))

        return send_get_request(
            url,
            headers=headers,
            params=params,
        )

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
