from typing import Any, Dict

from .exception import KorbitUnexpectedResponse
from .utils import send_get_request


class KorbitRestPublic:
    @staticmethod
    def ticker(currency_pair: str) -> Dict[str, Any]:
        # https://apidocs.korbit.co.kr/#ticker
        url = "https://api.korbit.co.kr/v1/ticker"
        params = [("currency_pair", currency_pair)]
        return send_get_request(url, params=params)

    @staticmethod
    def constants() -> Dict:
        """
        Raises
            KorbitUnexpectedResponse
        """
        url = "https://api.korbit.co.kr/v1/constants"
        try:
            return send_get_request(url).get("exchange")
        except Exception as e:
            raise KorbitUnexpectedResponse from e
