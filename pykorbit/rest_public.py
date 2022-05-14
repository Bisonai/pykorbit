from typing import Any, Dict

from .exception import KorbitUnexpectedResponse
from .utils import send_get_request


class KorbitRestPublic:
    @staticmethod
    def ticker(currency_pair: str) -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#ticker

        Example response:
            {
                "timestamp": 1389678052000,
                "last": "569000"
            }
        """
        url = "https://api.korbit.co.kr/v1/ticker"
        params = [("currency_pair", currency_pair)]
        return send_get_request(url, params=params)

    def detailed_ticker(currency_pair: str) -> Dict[str, Any]:
        """https://apidocs.korbit.co.kr/#detailed-ticker
        Example response:
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
        response = send_get_request(url)
        response_echange = response.get("exchange")

        if response_echange:
            return response_echange
        else:
            raise KorbitUnexpectedResponse(response_echange)
