---
name: Start/Stop App
description: Start, stop, and manage the Orchestra application and its services.
---

# Start/Stop App

Start, stop, and manage the Orchestra application including backend API, frontend UI, and supporting infrastructure services (database, storage, AI services).

## Instructions

### Prerequisites

- Backend: Python 3.12+, uv package manager, dependencies installed (`uv sync`)
- Frontend: Node.js, npm, dependencies installed (`npm install`)
- Docker: For running infrastructure services (Postgres, MinIO, Ollama, etc.)
- Environment files: `.env` for backend, `.env.docker` for Docker services

### Application Architecture

```
Frontend (Vite/React) → Backend (FastAPI) → Services (Postgres, MinIO, Ollama)
Port 5173 (dev)          Port 8000           Ports 5432, 9000, 11434
```

### Workflow

1. **Assess what needs to be started** based on user request
2. **Check if services are already running** to avoid conflicts
3. **Start services in the correct order**:
   - Infrastructure first (database, storage)
   - Backend API second
   - Frontend UI last
4. **Use background processes** for long-running services
5. **Report status and URLs** to the user
6. **Provide stop/restart commands** when needed

## Starting Services

### Backend API (Development)

**Option 1: Using Make (Recommended)**
```bash
cd backend && make dev
```
- Runs: `uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug --env-file .env`
- Auto-reload on code changes
- API docs: http://localhost:8000/docs

**Option 2: Using Script (Interactive)**
```bash
cd backend && bash scripts/dev.sh
```
- Prompts for environment (.env vs .env.production)
- Sets API version from git tags
- Good for connecting to prod database locally

**Background Mode:**
```bash
cd backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug --env-file .env
```
Use `run_in_background: true` with Bash tool

### Frontend UI (Development)

```bash
cd frontend && npm run dev
```
- Vite dev server with HMR (Hot Module Replacement)
- Usually runs on http://localhost:5173
- Auto-reload on code changes

**Background Mode:**
Use `run_in_background: true` with Bash tool

### Infrastructure Services (Docker)

**Start Database (Postgres + PgAdmin)**
```bash
docker compose up postgres pgadmin -d
```
- Postgres: localhost:5432 (user: admin, password: test1234)
- PgAdmin: http://localhost:4040 (admin@example.com / test1234)

**Start File Storage (MinIO)**
```bash
docker compose up minio -d
```
- API: http://localhost:9000
- Console: http://localhost:9001
- Credentials in docker-compose.yml

**Start AI Service (Ollama)**
```bash
docker compose up ollama -d
```
- API: http://localhost:11434
- Requires NVIDIA GPU runtime

**Start Full Stack (Docker)**
```bash
docker compose up orchestra postgres -d
```
- Runs backend in Docker container
- Uses .env.docker configuration

**Start All Services**
```bash
docker compose up -d
```
- Starts all defined services in background

## Stopping Services

### Stop Backend/Frontend (Development)

If running in foreground: `Ctrl+C`

If running in background:
```bash
# Find the process
ps aux | grep uvicorn  # for backend
ps aux | grep vite     # for frontend

# Kill by PID
kill <PID>

# Or kill all
pkill -f uvicorn
pkill -f vite
```

### Stop Docker Services

**Stop specific services:**
```bash
docker compose stop postgres pgadmin
docker compose stop minio
docker compose stop ollama
docker compose stop orchestra
```

**Stop and remove containers:**
```bash
docker compose down
```

**Stop and remove with volumes (CAUTION: destroys data):**
```bash
docker compose down -v
```

## Checking Status

### Check Running Processes
```bash
# Backend
ps aux | grep uvicorn

# Frontend
ps aux | grep vite

# Docker services
docker compose ps
```

### Check Ports
```bash
# See what's listening on ports
lsof -i :8000  # Backend
lsof -i :5173  # Frontend
lsof -i :5432  # Postgres
```

### Check Service Health
```bash
# Backend API
curl http://localhost:8000/health

# Frontend
curl http://localhost:5173

# Postgres
docker compose exec postgres pg_isready
```

## Common Scenarios

### Example 1: Start Full Development Environment

User: "Start the app for development"
Assistant: I'll start the development environment.
1. Starting infrastructure services
   [Executes: `docker compose up postgres pgadmin -d`]
2. Starting backend API
   [Executes: `cd backend && make dev` in background]
3. Starting frontend UI
   [Executes: `cd frontend && npm run dev` in background]

Services running:
- Backend API: http://localhost:8000/docs
- Frontend UI: http://localhost:5173
- Database: localhost:5432
- PgAdmin: http://localhost:4040

### Example 2: Stop Everything

User: "Stop the app"
Assistant: I'll stop all services.
1. Stopping development servers
   [Kills uvicorn and vite processes]
2. Stopping Docker services
   [Executes: `docker compose down`]

All services stopped.

### Example 3: Restart Backend Only

User: "Restart the backend"
Assistant: I'll restart the backend API.
1. Stopping backend
   [Kills uvicorn process]
2. Starting backend
   [Executes: `cd backend && make dev` in background]

Backend restarted at http://localhost:8000/docs

### Example 4: Start with Production Database

User: "Start backend connected to production database"
Assistant: I'll start the backend with production configuration.
[Executes: `cd backend && bash scripts/dev.sh` with "yes" input]

Backend started with production database connection.

### Example 5: Check What's Running

User: "What services are running?"
Assistant: Let me check the status.
[Executes: `docker compose ps` and `ps aux | grep -E "uvicorn|vite"`]

Currently running:
- Backend: Yes (PID: 12345, http://localhost:8000)
- Frontend: Yes (PID: 12346, http://localhost:5173)
- Postgres: Yes (container: postgres)
- PgAdmin: Yes (container: pgadmin)

## Important Notes

### Port Conflicts
If you get "address already in use" errors:
1. Check what's using the port: `lsof -i :<port>`
2. Stop the conflicting process: `kill <PID>`
3. Or use a different port

### Background Processes
When running services in background:
- Always save the task ID for monitoring
- Use `TaskOutput` to check logs
- Provide stop commands to the user

### Environment Variables
- Backend dev: Uses `.env` by default
- Backend Docker: Uses `.env.docker`
- Frontend: Uses Vite's env files (`.env`, `.env.local`)

### Database Migrations
Before starting backend for the first time:
```bash
cd backend
alembic upgrade head
```

### Seeding Data
To seed default users:
```bash
cd backend
make seeds.user
```

## URLs Reference

**Development:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173
- Postgres: localhost:5432
- PgAdmin: http://localhost:4040
- MinIO API: http://localhost:9000
- MinIO Console: http://localhost:9001
- Ollama: http://localhost:11434

**Production:**
- Backend API: https://chat.ruska.ai/docs
- Frontend: https://chat.ruska.ai
- Website: https://ruska.ai
- Docs: https://docs.ruska.ai
