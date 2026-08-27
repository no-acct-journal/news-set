<div align="center">

# News Set

**A full-stack news reading app with FastAPI, Vue 3, PostgreSQL, Redis, and AI chat.**

<p>
  <code>News App</code>
  <code>FastAPI</code>
  <code>Vue 3</code>
  <code>PostgreSQL</code>
  <code>Redis</code>
  <code>Docker Compose</code>
</p>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=flat-square&logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?style=flat-square&logo=vite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)

</div>

<p align="center">
  <img src="./docs/banner.svg" alt="News Set banner" width="100%" />
</p>

---

## Overview

**News Set** is a full-stack news browsing application. The backend uses **FastAPI** to provide news, user, favorite, history, and AI chat APIs. The frontend uses **Vue 3 + Vite + Vant** to deliver a mobile-first news reading experience.

> Goal: a portfolio-ready full-stack news app covering authentication, content browsing, favorites, reading history, caching, database integration, and an AI service proxy.

---

## Features

- News categories, paginated feeds, and article detail pages
- Article view count tracking
- User registration, login, profile update, and password update
- Add, remove, list, and clear favorites
- Add, list, delete, and clear browsing history
- Redis caching for categories, feeds, article details, and related news
- AI Chat backend proxy so provider keys stay out of frontend code
- Mobile UI styled after mainstream North American news apps
- Docker Compose setup for PostgreSQL and Redis
- Windows PowerShell one-command development startup

---

## Tech Stack

| Layer | Tech |
| --- | --- |
| Frontend | Vue 3, Vite, Vant, Pinia, Vue Router, Axios |
| Backend | FastAPI, SQLAlchemy async, Pydantic, Uvicorn |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Auth | Token-based auth, passlib, bcrypt |
| AI | OpenAI-compatible chat completions proxy |
| DevOps | Docker Compose, PowerShell startup script |

---

## Architecture

The current development setup is:

```text
Frontend Vue  -> runs locally with npm
Backend API   -> runs locally with Python venv
PostgreSQL    -> runs in Docker
Redis         -> runs in Docker
```

Docker currently provides local dependency services only. The frontend and backend application code run on the host machine during development.

---

## Project Structure

```text
news-set/
  main.py                 # FastAPI app entry
  routers/                # API routes
  service/                # Business logic
  models/                 # SQLAlchemy ORM models
  schemas/                # Pydantic request/response schemas
  database/               # PostgreSQL schema and seed data
  config/                 # Runtime settings, database, Redis config
  cache/                  # Redis cache helpers
  frontend/               # Vue 3 + Vite frontend
  docs/                   # README assets
  docker-compose.yml      # Local PostgreSQL and Redis
  start-dev.ps1           # Windows one-command dev startup
```

---

## Quick Start

### Requirements

- Python 3.10+
- Node.js 18+ or 20+
- Docker Desktop
- Windows PowerShell

### One-Command Startup

Run this from the project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-dev.ps1
```

The script will:

- create `.env`
- create `frontend/.env`
- start Docker PostgreSQL and Redis
- create the Python virtual environment
- install backend dependencies
- install frontend dependencies
- initialize database tables
- load example news data
- start the backend and frontend

After startup:

| Service | URL |
| --- | --- |
| Frontend | http://127.0.0.1:5173 |
| API Docs | http://127.0.0.1:8000/docs |

---

## Manual Startup

### 1. Start PostgreSQL and Redis

```powershell
docker compose up -d postgres redis
```

PostgreSQL is exposed on host port `5433` to avoid conflicts with a local PostgreSQL installation on the default `5432` port.

### 2. Create Environment Files

```powershell
Copy-Item .env.example .env
Copy-Item frontend/.env.example frontend/.env
```

### 3. Install Backend Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Initialize the Database

```powershell
Get-Content -Raw database/schema.sql | docker compose exec -T postgres psql -U postgres -d news_set
Get-Content -Raw database/seed.example.sql | docker compose exec -T postgres psql -U postgres -d news_set
```

### 5. Start the Backend

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### 6. Start the Frontend

```powershell
cd frontend
npm install
npm run dev
```

---

## API Modules

| Module | Prefix | Description |
| --- | --- | --- |
| News | `/api/news` | Categories, list, detail, related news |
| User | `/api/user` | Register, login, profile, password |
| Favorite | `/api/favorite` | Add, remove, list, clear favorites |
| History | `/api/history` | Add, list, delete, clear browsing history |
| AI | `/api/ai` | AI chat proxy endpoint |

---

## Environment Variables

### Backend

| Name | Required | Description |
| --- | --- | --- |
| `ASYNC_DATABASE_URL` | Yes | PostgreSQL async URL. Default dev value: `postgresql+asyncpg://postgres:change-me@localhost:5433/news_set`. |
| `CORS_ORIGINS` | No | Allowed frontend origins. |
| `REDIS_HOST` | No | Redis host. Default: `localhost`. |
| `REDIS_PORT` | No | Redis port. Default: `6379`. |
| `AI_API_ENDPOINT` | No | OpenAI-compatible chat completions endpoint. |
| `AI_API_KEY` | No | AI provider key. Keep it only in backend `.env`. |
| `AI_MODEL` | No | Chat model name. |

### Frontend

| Name | Required | Description |
| --- | --- | --- |
| `VITE_API_BASE_URL` | No | Backend base URL. Default: `http://127.0.0.1:8000`. |
| `VITE_AI_MODEL` | No | Model name sent to `/api/ai/chat`. |

---

## Frontend Commands

```powershell
cd frontend
npm run dev
npm run build
npm run preview
```

Build output is written to:

```text
frontend/dist/
```

`frontend/dist/` and `frontend/node_modules/` are intentionally ignored by Git.

---

## Docker Notes

`docker-compose.yml` starts:

| Service | Container | Host Port |
| --- | --- | --- |
| PostgreSQL | `news_set_postgres` | `5433` |
| Redis | `news_set_redis` | `6379` |

Default development database credentials:

```text
user: postgres
password: change-me
database: news_set
```

This is a local development password, not a production secret. Use server environment variables or secret management for production credentials.

---

## Notes

- Do not commit `.env` files.
- `database/seed.example.sql` is safe to run more than once.
- If the Docker PostgreSQL password or volume state becomes inconsistent, run `docker compose down -v` in development to reset the database volume.
- This repository does not currently declare an open-source license. Add a `LICENSE` file before distributing it as open source.
