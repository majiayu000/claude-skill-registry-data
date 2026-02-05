---
name: docker-infra
description: Docker and Docker Compose configuration and troubleshooting. Use for containers, services, volumes, networking, health checks, and deployment patterns.
---

# Docker & Infrastructure Skill

**Activation:** Docker, Docker Compose, containers, services, deployment

## Development Environment

### Services Overview

| Service | Port | Image | Purpose |
|---------|------|-------|---------|
| backend | 8000 | python:3.14-slim | FastAPI with uvicorn --reload |
| frontend | 4321 | node:22-alpine | Astro dev server |
| worker | - | python:3.14-slim | TaskIQ workers |
| db | 5432 | postgres:17-alpine | PostgreSQL database |
| redis | 6379 | redis:7-alpine | Job queue + cache |

### Quick Commands

```bash
# Start all services
docker compose up

# Start specific service
docker compose up backend

# Rebuild after dependency changes
docker compose build backend
docker compose up backend

# View logs
docker compose logs -f backend worker

# Shell into container
docker compose exec backend bash
docker compose exec frontend sh

# Stop all
docker compose down

# Stop and remove volumes (reset DB)
docker compose down -v
```

## Dockerfile Patterns

### Backend (Python)

```dockerfile
# backend/Dockerfile.dev
FROM python:3.14-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy source (volumes override in dev)
COPY . .

# Run with hot-reload
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Frontend (Node.js)

```dockerfile
# frontend/Dockerfile.dev
FROM node:22-alpine

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy dependency files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source (volumes override in dev)
COPY . .

# Run dev server
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
```

### Production (Multi-stage)

```dockerfile
# backend/Dockerfile
FROM python:3.14-slim AS builder

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.14-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose Patterns

### Development Compose

```yaml
# docker-compose.yml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - backend-cache:/app/.venv
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/shootout
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "4321:4321"
    volumes:
      - ./frontend:/app
      - frontend-node-modules:/app/node_modules
    environment:
      - PUBLIC_API_URL=http://localhost:8000

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    command: uv run taskiq worker app.tasks:broker
    volumes:
      - ./backend:/app
      - ./pipeline:/pipeline:ro
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/shootout
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: shootout
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
  backend-cache:
  frontend-node-modules:
```

### Environment Variables

```bash
# .env.example
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/shootout
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=shootout

# Redis
REDIS_URL=redis://redis:6379

# Tone 3000 OAuth
TONE3000_CLIENT_ID=your_client_id
TONE3000_CLIENT_SECRET=your_client_secret
TONE3000_REDIRECT_URI=http://localhost:8000/auth/callback

# Frontend
PUBLIC_API_URL=http://localhost:8000
```

## Networking

### Service Discovery

Services communicate using service names as hostnames:
- Backend → DB: `postgresql://postgres:5432`
- Backend → Redis: `redis://redis:6379`
- Frontend → Backend: `http://backend:8000` (internal)
- Browser → Backend: `http://localhost:8000` (external)

### Port Mapping

```yaml
ports:
  - "host:container"
  - "8000:8000"  # Accessible from host at localhost:8000
```

### Expose vs Ports

```yaml
# Expose: Internal only (other containers)
expose:
  - "5432"

# Ports: External (host machine)
ports:
  - "5432:5432"
```

## Volume Patterns

### Named Volumes (Persistent)

```yaml
volumes:
  postgres-data:  # Database files
  redis-data:     # Redis persistence
```

### Bind Mounts (Development)

```yaml
volumes:
  - ./backend:/app           # Source code (hot-reload)
  - ./pipeline:/pipeline:ro  # Read-only access
```

### Anonymous Volumes (Cache)

```yaml
volumes:
  - /app/node_modules  # Preserve installed dependencies
  - /app/.venv         # Preserve Python venv
```

## Health Checks

```yaml
db:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 5s
    timeout: 5s
    retries: 5
    start_period: 10s

backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs backend

# Check container status
docker compose ps

# Rebuild from scratch
docker compose build --no-cache backend
```

### Hot-reload Not Working

```bash
# Verify volume mount
docker compose exec backend ls -la /app

# Check file permissions
docker compose exec backend stat /app/app/main.py

# Restart service
docker compose restart backend
```

### Database Connection Issues

```bash
# Check if DB is healthy
docker compose ps db

# Check DB logs
docker compose logs db

# Verify network
docker compose exec backend ping db

# Test connection
docker compose exec backend python -c "
import asyncpg
import asyncio
asyncio.run(asyncpg.connect('postgresql://postgres:postgres@db:5432/shootout'))
"
```

### Reset Everything

```bash
# Stop all containers
docker compose down

# Remove all volumes
docker compose down -v

# Remove all images
docker compose down --rmi all

# Fresh start
docker compose build --no-cache
docker compose up
```

## Production Patterns

### Multi-stage Builds

See Dockerfile examples above for smaller production images.

### Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
```

### Logging

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```
