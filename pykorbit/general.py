import logging
from typing import List

from .utils import send_get_request


class KorbitGeneral:
    @staticmethod
    def _build_bearer_token_header(access_token: str):
        return {"Authorization": "Bearer " + access_token}

    @staticmethod
    def user_balances(access_token: str):
        logging.debug("User Balances")
        url = "https://api.korbit.co.kr/v1/user/balances"
        headers = KorbitGeneral._build_bearer_token_header(access_token)
        return send_get_request(url, headers=headers)

    @staticmethod
    def transfer_account_info(access_token: str):
        logging.debug("Transfer Account Info")
        url = "https://api.korbit.co.kr/v1/user/accounts"
        headers = KorbitGeneral._build_bearer_token_header(access_token)
        return send_get_request(url, headers=headers)

    @staticmethod
    def trading_volume_and_fees(
        access_token: str,
        pair: List[str] = [],
    ):
        logging.debug("Transfer Account Info")
        url = "https://api.korbit.co.kr/v1/user/volume"
        headers = KorbitGeneral._build_bearer_token_header(access_token)
        params = [("currency_pair", p) for p in pair]
        return send_get_request(url, headers=headers, params=params)
