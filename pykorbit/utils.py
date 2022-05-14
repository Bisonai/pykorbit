from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def requests_retry_session(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
):
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
):
    resp = requests_retry_session().post(
        url,
        headers=headers,
        data=data,
    )
    return resp.json()


def send_get_request(
    url,
    headers=None,
    params=None,
):
    resp = requests_retry_session().get(
        url,
        headers=headers,
        params=params,
    )
    return resp.json()


def build_bearer_token_header(access_token: str):
    return {"Authorization": "Bearer " + access_token}


def utc_now_ms() -> int:
    return int(datetime.utcnow().timestamp() * 1_000)
