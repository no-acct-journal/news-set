# News Set API

FastAPI backend for a news application with users, authentication, favorites, browsing history, PostgreSQL, and Redis caching.

## Requirements

- Python 3.10+
- PostgreSQL
- Redis

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create local environment variables.

```bash
cp .env.example .env
```

Update `.env` with your PostgreSQL and Redis values.

4. Start the API.

```bash
uvicorn main:app --reload
```

The API docs are available at `http://127.0.0.1:8000/docs`.

## Environment Variables

| Name | Required | Description |
| --- | --- | --- |
| `ASYNC_DATABASE_URL` | Yes | SQLAlchemy async PostgreSQL URL, for example `postgresql+asyncpg://user:password@host:5432/database`. |
| `DATABASE_SCHEMA` | No | PostgreSQL schema search path. Defaults to `public`. |
| `SQLALCHEMY_ECHO` | No | Set to `true` to print SQL statements. Defaults to `false`. |
| `REDIS_URL` | No | Full Redis URL. Takes priority over host/port settings when set. |
| `REDIS_HOST` | No | Redis host. Defaults to `localhost`. |
| `REDIS_PORT` | No | Redis port. Defaults to `6379`. |
| `REDIS_DB` | No | Redis database number. Defaults to `0`. |
| `REDIS_PASSWORD` | No | Redis password when required. |
| `REDIS_SOCKET_TIMEOUT` | No | Redis socket timeout in seconds. Defaults to `5`. |

## Notes

This project expects the PostgreSQL tables to already exist. Add migrations or a schema SQL file before using it as a full production-ready template.
