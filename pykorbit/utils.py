import sys
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


def send_post_request(url, headers=None, data=None):
    try:
        resp = requests_retry_session().post(
            url,
            headers=headers,
            data=data,
        )
        return resp.json()
    except Exception as x:
        # FIXME
        frame_stack = sys._getframe(2).f_code.co_name
        print(f"send post request failed {x.__class__.__name__}")
        print(f"caller: {frame_stack}")

        return None


def send_get_request(url, headers=None, params=None):
    try:
        resp = requests_retry_session().get(
            url,
            headers=headers,
            params=params,
        )
        return resp.json()
    except Exception as x:
        # FIXME
        frame_stack = sys._getframe(2).f_code.co_name
        print(f"send get request failed {x.__class__.__name__}")
        print(f"caller: {frame_stack}")

        return None


def utc_now_ms() -> int:
    return int(datetime.utcnow().timestamp() * 1_000)
