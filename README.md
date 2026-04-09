# VRS Analytics ETL Scheduler

A small ETL scheduler that pulls bookings from the Holibob GraphQL API, enriches each booking with property data, and upserts the result into a Postgres database. The job runs on a schedule and reports status to Sentry, with optional email notifications.

**Tech stack**: Python, SQLAlchemy, schedule, requests, Sentry

**What it does**
1. Fetch booking data from Holibob (paginated, 10 records per page).
2. Fetch property details per booking.
3. Transform + upsert into `vrs_analytics` table.
4. Emit cron checkins to Sentry and send a summary email.

## Features

- Scheduled ETL job with configurable interval (`CRON_RUN_TIME`).
- Holibob GraphQL fetch with pagination (10 records per page).
- Property enrichment per booking via property API.
- Upsert into Postgres using SQLAlchemy models.
- Sentry cron monitoring for job health and failures.
- Email notification after each sync (Gmail SMTP).

**Project structure**
- `main.py` CLI entrypoint (accepts `--start` / `--end` dates)
- `vrs_analytics/cron/holibob_cron.py` scheduler + job wiring
- `vrs_analytics/services/holibob_service.py` API fetch + transform
- `vrs_analytics/services/upsert.py` DB upsert logic
- `vrs_analytics/db/postgres/models.py` SQLAlchemy model
- `vrs_analytics/notifier/mailer.py` email notification
- `config/global_config.py` runtime config
- `config/sentry.py` Sentry init

## Prerequisites

- Python 3.10+
- PostgreSQL

## Setup

1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create your env file

```bash
cp .env .env.local
```

Then update `.env.local` with the values you need.

## Environment variables

Required
- `DB_USER` - Postgres user
- `DB_PASSWORD` - Postgres password
- `DB_NAME` - Postgres database name
- `HOLIBOB_BASE_URL` - Holibob API base URL
- `HOLIBOB_API_KEY` - Holibob API key
- `PROPERTY_BASE_URL` - Property API URL
- `MAIL_APP_PASS` - Gmail app password (used in `mailer.py`)

- `CURRENCY` - Default currency, defaults to `USD`
- `SENTRY_DSN` - Sentry DSN

## Database

Tables are created automatically on first run via `Base.metadata.create_all(...)`.

Key columns in `vrs_analytics`:
- Booking info: `transaction_id`, `transaction_date`, `transaction_ts_utc`, `currency`, `revenue`, `sale_amount`
- Property info: `property_id`, `property_name`, `property_type_category`, `location_*`, etc.
- JSON payloads: `partner_response`, `property`
- Timestamps: `created_at`, `updated_at`

## Run

Provide a date range for the API filter:

```bash
python main.py --start 2025-03-01 --end 2026-03-01
```

The cron scheduler will start, run the job immediately, then repeat every `CRON_RUN_TIME` minutes (see `config/global_config.py`).

## Notes

- Pagination is enabled in Holibob fetch (10 records per page).
- Email sending uses Gmail SMTP and requires an app password.
- Sentry cron monitoring is enabled when `SENTRY_DSN` is set.
