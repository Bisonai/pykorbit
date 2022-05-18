import logging
from typing import Dict, Union

from .utils import send_post_request


class KorbitAuthenticationApi:
    @staticmethod
    def issue_access_token(
        client_id: str,
        client_secret: str,
    ) -> Dict[str, Union[str, int]]:
        """https://apidocs.korbit.co.kr/#direct-authentication

        Response:
          {
            "token_type":"Bearer",
            "access_token":"1t1LgTslDrGznxPxhYz7RldsNVIbnEK",
            "expires_in":3600,
            "scope": "VIEW,TRADE",
            "refresh_token":"vn5xoOf4PzckgnqjQSL9Sb3KxWJvYtm"
          }
        """
        logging.debug("Issue access token")

        url = "https://api.korbit.co.kr/v1/oauth2/access_token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }

        return send_post_request(
            url,
            data=data,
        )

    def renew_access_token(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> Dict[str, Union[str, int]]:
        """https://apidocs.korbit.co.kr/#refreshing-access-token

        Response:
          {
            "token_type":"Bearer",
            "access_token":"IuqEWTK09eCLThRCZZSALA0oXC8EI7s",
            "expires_in":3600,
            "scope": "VIEW,TRADE",
            "refresh_token":"vn5xoOf4Pzckgn4jQSL9Sb3KxWJvYtm"
          }
        """
        logging.debug("Renew access token")

        url = "https://api.korbit.co.kr/v1/oauth2/access_token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        return send_post_request(
            url,
            data=data,
        )
