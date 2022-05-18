from datetime import datetime
from typing import Dict, List, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exception import KorbitUnauthorized


def requests_retry_session(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
) -> requests.Session:
    session = requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def send_post_request(
    url,
    headers=None,
    data=None,
) -> Union[Dict, List]:
    """
    Raises:
      KorbitUnauthorized
    """
    resp = requests_retry_session().post(
        url,
        headers=headers,
        data=data,
    )

    if resp.status_code == 401:
        raise KorbitUnauthorized(resp.text)

    return resp.json()


def send_get_request(
    url,
    headers=None,
    params=None,
) -> Union[Dict, List]:
    """
    Raises:
      KorbitUnauthorized
    """
    resp = requests_retry_session().get(
        url,
        headers=headers,
        params=params,
    )

    if resp.status_code == 401:
        raise KorbitUnauthorized(resp.text)

    return resp.json()


def build_bearer_token_header(access_token: str) -> Dict[str, str]:
    return {"Authorization": "Bearer " + access_token}


def utc_now_ms() -> int:
    return int(datetime.utcnow().timestamp() * 1_000)
