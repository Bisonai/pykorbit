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
    ) -> List:
        # https://apidocs.korbit.co.kr/#view-transfers
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
        # https://api.korbit.co.kr/v1/user/coins/status
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
