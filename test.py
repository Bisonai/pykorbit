import asyncio
import os
import time
from pprint import pprint

from dotenv import load_dotenv

from pykorbit.authentication import KorbitAuthentication
from pykorbit.websocket_echo import KorbitWebsocketEcho

load_dotenv()
client_id = os.environ.get("korbit_client_id")
client_secret = os.environ.get("korbit_client_secret")


korbit = KorbitAuthentication()
r = korbit.issue_access_token(
    client_id=client_id,
    client_secret=client_secret,
)

pprint(r, indent=4)

time.sleep(1)

# r2 = korbit.renew_access_token(
#     client_id=client_id,
#     client_secret=client_secret,
#     refresh_token=r.get("refresh_token"),
# )

# pprint(r2, indent=4)

k_ws = KorbitWebsocketEcho(
    access_token=r.get("access_token"),
)

asyncio.run(
    k_ws.connect_and_subscribe(
        channels=[
            "ticker:btc_krw",
        ],
    )
)
