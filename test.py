import os
import time
from pprint import pprint

from dotenv import load_dotenv

from pykorbit.authentication import KorbitAuthentication

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

r2 = korbit.renew_access_token(
    client_id=client_id,
    client_secret=client_secret,
    refresh_token=r.get("refresh_token"),
)

pprint(r2, indent=4)
