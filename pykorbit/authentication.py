import logging
from typing import Dict

from .utils import send_post_request


class KorbitAuthentication:
    @staticmethod
    def issue_access_token(
        client_id: str,
        client_secret: str,
    ) -> Dict[str, str]:
        """
        Issue an access token. Used only for the first connection.

        Raises:
            ValueError
        """
        url = "https://api.korbit.co.kr/v1/oauth2/access_token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }

        logging.debug("Issue access token")
        contents = send_post_request(url, data=data)

        if isinstance(contents, dict):
            if "access_token" in contents.keys():
                return {
                    "access_token": contents.get("access_token"),
                    "refresh_token": contents.get("refresh_token"),
                    "scope": contents.get("scope"),
                    "token_type": contents.get("token_type"),
                }

        raise ValueError(contents)

    def renew_access_token(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> Dict[str, str]:
        """
        Update `access_token` using `refresh_token`.

        Raises:
            ValueError
        """
        url = "https://api.korbit.co.kr/v1/oauth2/access_token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        logging.debug("Renew access token")
        contents = send_post_request(
            url,
            data=data,
        )

        if isinstance(contents, dict):
            if "access_token" in contents.keys():
                return {
                    "access_token": contents.get("access_token"),
                    "refresh_token": contents.get("refresh_token"),
                }

        raise ValueError(contents)
