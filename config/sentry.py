import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

def init_sentry():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        traces_sample_rate=1.0,
    )

    sentry_sdk.set_user({
        "id": 101,
        "email": "ali@gmail.com"
    })