# https://apidocs.korbit.co.kr/#private-wallet
import logging
from typing import Dict, List, Optional

from .utils import build_bearer_token_header, send_get_request

TRANSFER_TYPES = (
    "deposit",
    "withdrawal",
)


class KorbitWallet:
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
            assert type in TRANSFER_TYPES
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
