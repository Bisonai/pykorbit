# https://apidocs.korbit.co.kr/#private-wallet
import logging
from typing import List, Optional

from .utils import build_bearer_token_header, send_get_request

TRANSFER_TYPES = (
    "deposit",
    "withdrawal",
)


class KorbitWallet:
    @staticmethod
    def view_transfers(
        access_token: str,
        currency: Optional[str] = None,
        type: Optional[str] = None,
        offset: int = 0,
        limit: int = 40,
    ) -> List:
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
