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

4. Initialize the database schema.

```bash
psql "postgresql://user:password@localhost:5432/news_set" -f database/schema.sql
```

For `psql`, use a regular PostgreSQL URL. The application uses the async SQLAlchemy form, such as `postgresql+asyncpg://...`, in `ASYNC_DATABASE_URL`.

5. Optional: load example data for local development.

```bash
psql "postgresql://user:password@localhost:5432/news_set" -f database/seed.example.sql
```

6. Start the API.

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

The SQL files in `database/` are intended for local development and simple deployments. For larger deployments, add a migration tool such as Alembic.
