# CRON Project

A small scheduler that fetches data from an API and upserts it into a database on a schedule.

**Tech stack**: Python, SQLAlchemy, schedule

## Prerequisites

- Python 3.10+
- A running PostgreSQL database (or update `DB_URL` for a different supported DB)

## Clone

```bash
git clone <your-github-repo-url>
cd CRON-project
```

## Setup

1. Create and activate a virtual environment

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create your environment file

```bash
cp .env .env.local
```

Then edit `.env.local` and set the values you need. Example:

```
API_URL=https://jsonplaceholder.typicode.com/photos
DB_URL=postgresql://admin:admin@localhost:5432/apidb
```

4. Export environment variables (Linux/macOS)

```bash
set -a
source .env.local
set +a
```

On Windows (PowerShell), you can set variables for the session:

```powershell
$env:API_URL="https://jsonplaceholder.typicode.com/photos"
$env:DB_URL="postgresql://admin:admin@localhost:5432/apidb"
```

## Run

```bash
python main.py
```

The scheduler will start, run once immediately, then continue every minute.

## Notes

- The database tables are created automatically on first run.
