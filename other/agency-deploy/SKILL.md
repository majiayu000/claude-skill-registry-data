---
name: agency-deploy
description: Configure Docker, Docker Compose, CI/CD pipelines, environment variables, and production deployments for the Social Media Agency. Use when working with Dockerfiles, docker-compose, GitHub Actions, monitoring, or deployment configuration.
---

# Social Media Agency DevOps & Deployment

## Service Architecture

```
┌─────────────┐    ┌──────────────┐
│  Frontend    │    │  Backend     │
│  Next.js     │───▶│  FastAPI     │
│  :3000       │    │  :8001       │
└─────────────┘    └──────────────┘
                         │
                   ┌─────┴─────┐
                   │           │
              ┌────┴───┐  ┌───┴──┐  ┌──────┐  ┌───────────┐
              │Postgres│  │Redis │  │ S3   │  │  Celery   │
              │ :5432  │  │:6379 │  │      │  │  Workers  │
              └────────┘  └──────┘  └──────┘  └───────────┘
                                                  │
                                         ┌────────┴────────┐
                                         │  Publishing     │
                                         │  Analytics Sync │
                                         │  Report Gen     │
                                         └─────────────────┘
```

## Docker Compose (Development)

```yaml
# docker/docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-agency}
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ../db/init.sql:/docker-entrypoint-initdb.d/01-init.sql
      - ../db/seed.sql:/docker-entrypoint-initdb.d/02-seed.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ../backend
      target: production
    ports:
      - "8001:8001"
    env_file: ../.env
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB:-agency}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  celery-worker:
    build:
      context: ../backend
      target: production
    command: celery -A agency.workers.publishing_worker worker --loglevel=info
    env_file: ../.env
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB:-agency}
      REDIS_URL: redis://redis:6379
    depends_on:
      - backend
      - redis

  celery-beat:
    build:
      context: ../backend
      target: production
    command: celery -A agency.workers.publishing_worker beat --loglevel=info
    env_file: ../.env
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB:-agency}
      REDIS_URL: redis://redis:6379
    depends_on:
      - redis

  frontend:
    build:
      context: ../frontend
      target: runner
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8001
    depends_on:
      - backend

volumes:
  postgres_data:
```

## Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir .

FROM base AS production
EXPOSE 8001
CMD ["uvicorn", "agency.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]
```

## Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --prefer-offline

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

Requires `output: "standalone"` in `next.config.ts`.

## Environment Variables

```bash
# .env.example

# -- Database --
POSTGRES_DB=agency
POSTGRES_USER=postgres
POSTGRES_PASSWORD=              # REQUIRED
DATABASE_URL=postgresql+asyncpg://postgres:PASSWORD@localhost:5432/agency

# -- Redis --
REDIS_URL=redis://localhost:6379

# -- Auth --
JWT_SECRET=                     # REQUIRED: openssl rand -hex 32

# -- AI Services --
OPENAI_API_KEY=                 # REQUIRED
ANTHROPIC_API_KEY=              # Optional (fallback)

# -- Stripe --
STRIPE_SECRET_KEY=              # REQUIRED
STRIPE_WEBHOOK_SECRET=          # REQUIRED
NEXT_PUBLIC_STRIPE_KEY=         # Stripe publishable key

# -- Storage --
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=agency-media

# -- AgentMail --
AGENTMAIL_API_KEY=              # REQUIRED for email
AGENTMAIL_DEFAULT_DOMAIN=       # Custom email domain

# -- App --
APP_ENV=dev
DEBUG=true
CORS_ORIGINS=["http://localhost:3000"]

# -- Frontend --
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: agency_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: testpassword
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
        working-directory: backend
      - run: ruff check src/
        working-directory: backend
      - run: mypy src/agency/
        working-directory: backend
      - run: pytest tests/ -v
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:testpassword@localhost:5432/agency_test
          REDIS_URL: redis://localhost:6379
          JWT_SECRET: test-secret-key
          OPENAI_API_KEY: sk-test-fake
          STRIPE_SECRET_KEY: sk_test_fake
          STRIPE_WEBHOOK_SECRET: whsec_test_fake

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm ci
        working-directory: frontend
      - run: npm run lint
        working-directory: frontend
      - run: npm run build
        working-directory: frontend
        env:
          NEXT_PUBLIC_API_URL: http://localhost:8001
          NEXT_PUBLIC_STRIPE_KEY: pk_test_fake
```

## Local Development Quick Start

```bash
# 1. Clone and set up environment
cp .env.example .env
# Edit .env with your API keys

# 2. Start infrastructure
cd docker && docker compose up -d postgres redis

# 3. Start backend
cd backend
pip install -e ".[dev]"
alembic upgrade head
uvicorn agency.main:app --reload --port 8001

# 4. Start frontend (in another terminal)
cd frontend
npm install
npm run dev

# 5. Open http://localhost:3000
```

## .gitignore

```gitignore
__pycache__/
*.pyc
.venv/
node_modules/
.next/
.env
.env.local
.env.production
postgres_data/
*.log
*.egg-info/
.coverage
htmlcov/
playwright-report/
```

## Key Rules

1. **Never use `version:` in Docker Compose** — deprecated
2. **Always use health checks** for dependent services
3. **Always use multi-stage builds** for smaller images
4. **Never commit `.env`** — only `.env.example`
5. **Pin major versions** of base images (postgres:16, python:3.12, node:20)
6. **CI must test against real Postgres** — not SQLite
7. **Frontend `output: "standalone"`** for Docker deployment
8. **`NEXT_PUBLIC_` vars are build-time** — redeploy after changing them
9. **Celery Beat** for scheduled tasks (publishing, analytics sync)
