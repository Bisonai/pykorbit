import logging
from typing import Any, Dict, List

from .utils import build_bearer_token_header, send_get_request


class KorbitGeneral:
    @staticmethod
    def user_balances(access_token: str) -> Dict[str, Any]:
        logging.debug("User Balances")

        url = "https://api.korbit.co.kr/v1/user/balances"
        headers = build_bearer_token_header(access_token)

        return send_get_request(
            url,
            headers=headers,
        )

    @staticmethod
    def transfer_account_info(access_token: str) -> Dict[str, Any]:
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
        logging.debug("Transfer Account Info")

        url = "https://api.korbit.co.kr/v1/user/volume"
        headers = build_bearer_token_header(access_token)
        params = [("currency_pair", p) for p in pair]

        return send_get_request(
            url,
            headers=headers,
            params=params,
        )
