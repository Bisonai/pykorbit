from typing import Dict

from .exception import KorbitUnexpectedResponse
from .utils import send_get_request


class KorbitRestPublic:
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
