import schedule
import time
import sentry_sdk
import socket
from sentry_sdk.crons import monitor

from vrs_analytics.db.postgres.db_operations import get_connection
from vrs_analytics.services.holibob_service import get_fresh_data
from vrs_analytics.services.upsert import sync_data
from config.sentry import init_sentry
from config.global_config import CRON_RUN_TIME 


# Monitor config
monitor_config = {
    "schedule": {"type": "crontab", "value": "*/10 * * * *"},
    "timezone": "UTC",
    "checkin_margin": 5,
    "max_runtime": 10,
    "failure_issue_threshold": 3,
    "recovery_threshold": 2,
}

# Decorated job function
@monitor(monitor_slug='data_sync_cron', monitor_config=monitor_config)
def job():
    sentry_sdk.set_tag("job", "data_sync")
    sentry_sdk.set_tag("type", "cron")

    sentry_sdk.add_breadcrumb(message="Job started", category="cron.step", level="info")
    
    print("Fetching Data From API...")
    data = get_fresh_data()

    sentry_sdk.add_breadcrumb(message="Data fetched", category="cron.step", level="info")
    
    sync_data(data)

    sentry_sdk.add_breadcrumb(message="Sync done", category="cron.step", level="info")


def run():
    
    init_sentry()

    # Global corn context to see the ypdate in the sentry
    sentry_sdk.set_context("cron_info", {
        "job": "data_sync",
        "schedule": "*/10 * * * *",
        "server": socket.gethostname(),
        "owner": "data-team"
    })

    get_connection()

    print("CRON started...")
    schedule.every(CRON_RUN_TIME).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
