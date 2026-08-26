# News Set

News Set is a full-stack news application with a FastAPI backend and a Vue 3 mobile-style frontend.

## Project Structure

```text
news-set/
  main.py                 # FastAPI app entry
  routers/                # API routes
  service/                # Business logic
  models/                 # SQLAlchemy ORM models
  schemas/                # Pydantic request/response schemas
  database/               # PostgreSQL schema and example seed data
  config/                 # Runtime settings, database, and Redis config
  frontend/               # Vue 3 + Vite frontend app
  docker-compose.yml      # Local PostgreSQL and Redis services
  start-dev.ps1           # Windows one-command dev startup
```

## Requirements

- Python 3.10+
- Node.js 18+ or 20+
- Docker Desktop
- Windows PowerShell for `start-dev.ps1`

Docker is used only for local PostgreSQL and Redis. The backend and frontend still run directly on your machine for development.

## One-Command Startup

From the project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-dev.ps1
```

The script will:

- create `.env` from `.env.example` when missing
- create `frontend/.env` from `frontend/.env.example` when missing
- start PostgreSQL and Redis with Docker Compose
- create the Python virtual environment when missing
- install backend dependencies
- install frontend dependencies
- apply `database/schema.sql`
- load `database/seed.example.sql`
- start the backend at `http://127.0.0.1:8000`
- start the frontend at `http://127.0.0.1:5173`

API docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Manual Startup

Use these steps if you do not want to use the PowerShell startup script.

### 1. Start PostgreSQL and Redis

```bash
docker compose up -d postgres redis
```

### 2. Create Environment Files

Backend:

```bash
cp .env.example .env
```

Frontend:

```bash
cp frontend/.env.example frontend/.env
```

The default `.env.example` values match `docker-compose.yml`.

### 3. Install Backend Dependencies

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
Get-Content -Raw database/schema.sql | docker compose exec -T postgres psql -U postgres -d news_set
Get-Content -Raw database/seed.example.sql | docker compose exec -T postgres psql -U postgres -d news_set
```

### 5. Start the Backend

```bash
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### 6. Install and Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

## Frontend

The frontend is in `frontend/`.

Important files:

- `frontend/package.json`
- `frontend/src/main.js`
- `frontend/src/router/index.js`
- `frontend/src/config/api.js`

Available commands:

```bash
cd frontend
npm run dev
npm run build
npm run preview
```

The frontend defaults to:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Backend

Main API groups:

- `/api/news/*`
- `/api/user/*`
- `/api/favorite/*`
- `/api/history/*`
- `/api/ai/chat`

The backend uses:

- FastAPI
- SQLAlchemy async
- PostgreSQL
- Redis
- passlib/bcrypt

## Environment Variables

### Backend

| Name | Required | Description |
| --- | --- | --- |
| `APP_DEBUG` | No | Set to `true` to include detailed error payloads. Defaults to `false`. |
| `CORS_ORIGINS` | No | Comma-separated allowed frontend origins. Defaults to local Vite origins. |
| `CORS_ALLOW_CREDENTIALS` | No | Set to `true` only when credentialed browser requests are required. Defaults to `false`. |
| `ASYNC_DATABASE_URL` | Yes | SQLAlchemy async PostgreSQL URL, for example `postgresql+asyncpg://postgres:change-me@localhost:5432/news_set`. |
| `DATABASE_SCHEMA` | No | PostgreSQL schema search path. Defaults to `public`. |
| `SQLALCHEMY_ECHO` | No | Set to `true` to print SQL statements. Defaults to `false`. |
| `REDIS_URL` | No | Full Redis URL. Takes priority over host/port settings when set. |
| `REDIS_HOST` | No | Redis host. Defaults to `localhost`. |
| `REDIS_PORT` | No | Redis port. Defaults to `6379`. |
| `REDIS_DB` | No | Redis database number. Defaults to `0`. |
| `REDIS_PASSWORD` | No | Redis password when required. |
| `REDIS_SOCKET_TIMEOUT` | No | Redis socket timeout in seconds. Defaults to `5`. |
| `AI_API_ENDPOINT` | No | Optional OpenAI-compatible chat completions endpoint for `/api/ai/chat`. |
| `AI_API_KEY` | No | Optional AI provider API key. Keep this on the backend only. |
| `AI_MODEL` | No | Optional chat model name. Defaults to `qwen3-max-preview`. |
| `AI_REQUEST_TIMEOUT` | No | Optional AI provider timeout in seconds. Defaults to `60`. |

### Frontend

| Name | Required | Description |
| --- | --- | --- |
| `VITE_API_BASE_URL` | No | Backend API base URL. Defaults to `http://127.0.0.1:8000`. |
| `VITE_AI_MODEL` | No | Model name sent to the backend AI chat endpoint. |

## Production Build

Build the frontend:

```bash
cd frontend
npm run build
```

Build output is written to:

```text
frontend/dist/
```

`frontend/dist/` and `frontend/node_modules/` are intentionally ignored by Git.

## Notes

- Do not commit `.env` files.
- The example seed file is safe to run more than once.
- For larger deployments, add a migration tool such as Alembic.
