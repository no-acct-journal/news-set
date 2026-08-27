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

## 项目简介

**News Set** 是一个前后端分离的新闻浏览应用。后端基于 **FastAPI** 提供新闻、用户、收藏、历史记录和 AI 问答接口；前端基于 **Vue 3 + Vite + Vant** 构建移动端新闻阅读体验。

> 定位：一个适合展示全栈能力的新闻类 App 项目，覆盖用户认证、内容浏览、收藏历史、缓存、数据库和 AI 服务代理。

---

## 功能亮点

- 新闻分类、分页列表、详情阅读
- 新闻阅读量统计
- 用户注册、登录、资料更新、密码修改
- 收藏新闻、取消收藏、清空收藏
- 浏览历史记录、删除历史、清空历史
- Redis 缓存新闻分类、列表、详情和相关新闻
- AI Chat 后端代理，前端不暴露 AI provider key
- Vue 3 移动端 UI，风格对标北美主流新闻浏览 App
- Docker Compose 一键启动 PostgreSQL 和 Redis
- Windows PowerShell 一键开发启动脚本

---

## 技术栈

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

## 架构说明

当前项目的开发环境是：

```text
Frontend Vue  -> runs locally with npm
Backend API   -> runs locally with Python venv
PostgreSQL    -> runs in Docker
Redis         -> runs in Docker
```

Docker 目前只负责本地依赖服务，不负责运行前端和后端代码。

---

## 项目结构

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

## 快速启动

### 环境要求

- Python 3.10+
- Node.js 18+ or 20+
- Docker Desktop
- Windows PowerShell

### 一键启动

在项目根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\start-dev.ps1
```

脚本会自动完成：

- 创建 `.env`
- 创建 `frontend/.env`
- 启动 Docker PostgreSQL 和 Redis
- 创建 Python virtual environment
- 安装后端依赖
- 安装前端依赖
- 初始化数据库表
- 导入示例新闻数据
- 启动后端和前端

启动后访问：

| Service | URL |
| --- | --- |
| Frontend | http://127.0.0.1:5173 |
| API Docs | http://127.0.0.1:8000/docs |

---

## 手动启动

### 1. 启动 PostgreSQL 和 Redis

```powershell
docker compose up -d postgres redis
```

PostgreSQL 对外端口是 `5433`，避免和本机 PostgreSQL 的默认 `5432` 冲突。

### 2. 创建环境文件

```powershell
Copy-Item .env.example .env
Copy-Item frontend/.env.example frontend/.env
```

### 3. 安装后端依赖

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. 初始化数据库

```powershell
Get-Content -Raw database/schema.sql | docker compose exec -T postgres psql -U postgres -d news_set
Get-Content -Raw database/seed.example.sql | docker compose exec -T postgres psql -U postgres -d news_set
```

### 5. 启动后端

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### 6. 启动前端

```powershell
cd frontend
npm install
npm run dev
```

---

## API 模块

| Module | Prefix | Description |
| --- | --- | --- |
| News | `/api/news` | Categories, list, detail, related news |
| User | `/api/user` | Register, login, profile, password |
| Favorite | `/api/favorite` | Add, remove, list, clear favorites |
| History | `/api/history` | Add, list, delete, clear browsing history |
| AI | `/api/ai` | AI chat proxy endpoint |

---

## 环境变量

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

## 前端命令

```powershell
cd frontend
npm run dev
npm run build
npm run preview
```

构建产物位于：

```text
frontend/dist/
```

`frontend/dist/` 和 `frontend/node_modules/` 不会提交到 Git。

---

## Docker 说明

`docker-compose.yml` 会启动：

| Service | Container | Host Port |
| --- | --- | --- |
| PostgreSQL | `news_set_postgres` | `5433` |
| Redis | `news_set_redis` | `6379` |

开发默认数据库账号：

```text
user: postgres
password: change-me
database: news_set
```

这是本地开发默认密码，不是生产密码。生产环境请使用服务器环境变量或 secret 管理真实凭据。

---

## 注意事项

- 不要提交 `.env`。
- `database/seed.example.sql` 可以重复执行。
- 如果 Docker PostgreSQL 密码或数据卷状态混乱，开发环境可运行 `docker compose down -v` 重置数据。
- 当前仓库没有声明开源许可证；如需开源分发，请先添加 `LICENSE`。
