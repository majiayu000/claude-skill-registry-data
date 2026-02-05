---
name: zero-to-running
description: Automate local development environment setup for multi-service applications. Use when developers need to quickly set up or configure local dev environments with frontend (React/TypeScript/Tailwind), backend (Node/TypeScript), PostgreSQL, Redis, and Kubernetes orchestration. Handles single-command setup, teardown, configuration management, health checks, and docker-compose/k8s deployment workflows.
---

# Zero-to-Running Developer Environment

Automate the creation of production-grade local development environments that start with a single command. This skill handles multi-service application stacks including frontend, backend, databases, caches, and orchestration.

## Core Workflows

### 1. Initial Setup Script Generation

Generate the main setup script that orchestrates the entire environment:

```bash
# Target: make dev (or ./scripts/dev-up.sh)
# Requirements:
# - Check prerequisites (Docker, kubectl, etc.)
# - Load configuration
# - Start services in dependency order
# - Run health checks
# - Display status and access URLs
```

**Key considerations:**
- Validate all prerequisites before starting
- Provide clear, actionable error messages
- Show progress indicators during setup
- Handle port conflicts gracefully
- Support both docker-compose and Kubernetes

### 2. Configuration File Creation

Generate externalized configuration (`.env.example` or `config/dev.yml`):

```yaml
# Service ports
FRONTEND_PORT=3000
API_PORT=8000
POSTGRES_PORT=5432
REDIS_PORT=6379

# Database credentials (mock/dev only)
DB_NAME=dev_db
DB_USER=dev_user
DB_PASSWORD=dev_password_change_in_production

# Feature flags
ENABLE_HOT_RELOAD=true
ENABLE_DEBUG_MODE=true
LOG_LEVEL=debug
```

**Patterns:**
- Separate dev/prod concerns clearly
- Comment all configuration options
- Use secure defaults
- Document credential management pattern

### 3. Service Orchestration Files

#### Docker Compose (Simpler Option)

Generate `docker-compose.yml` for local development:

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "${REDIS_PORT}:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "${API_PORT}:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgres://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
      REDIS_URL: redis://redis:6379
    volumes:
      - ./backend:/app
      - /app/node_modules

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "${FRONTEND_PORT}:3000"
    depends_on:
      - api
    environment:
      VITE_API_URL: http://localhost:${API_PORT}
    volumes:
      - ./frontend:/app
      - /app/node_modules
```

#### Kubernetes (Production-Like Option)

Generate k8s manifests in `k8s/dev/`:
- `postgres-deployment.yaml` - Database with persistent volume
- `redis-deployment.yaml` - Cache service
- `api-deployment.yaml` - Backend with readiness probes
- `frontend-deployment.yaml` - Frontend with service
- `configmap.yaml` - Configuration
- `secrets.yaml` - Mock secrets with warning comments

**Key patterns:**
- Use ConfigMaps for configuration
- Include health/readiness probes
- Set appropriate resource limits
- Use local storage classes for PVs

### 4. Health Check Implementation

Create health check scripts that verify all services:

```bash
#!/bin/bash
# scripts/health-check.sh

echo "🔍 Checking service health..."

# Check PostgreSQL
if pg_isready -h localhost -p $POSTGRES_PORT -U $DB_USER > /dev/null 2>&1; then
  echo "✅ PostgreSQL is ready"
else
  echo "❌ PostgreSQL is not responding"
  exit 1
fi

# Check Redis
if redis-cli -h localhost -p $REDIS_PORT ping > /dev/null 2>&1; then
  echo "✅ Redis is ready"
else
  echo "❌ Redis is not responding"
  exit 1
fi

# Check API
if curl -f -s http://localhost:$API_PORT/health > /dev/null; then
  echo "✅ API is ready"
else
  echo "❌ API is not responding"
  exit 1
fi

# Check Frontend
if curl -f -s http://localhost:$FRONTEND_PORT > /dev/null; then
  echo "✅ Frontend is ready"
else
  echo "❌ Frontend is not responding"
  exit 1
fi

echo "🎉 All services are healthy!"
```

### 5. Teardown Script

Generate cleanup script (`make dev-down` or `./scripts/dev-down.sh`):

```bash
#!/bin/bash
# Gracefully stop all services and clean up resources

echo "🛑 Stopping development environment..."

# Docker Compose variant
docker-compose down -v  # -v removes volumes

# Kubernetes variant
kubectl delete namespace dev-env --wait=true

echo "✅ Environment cleaned up"
```

### 6. Documentation Generation

Create comprehensive `DEVELOPER_SETUP.md`:

```markdown
# Developer Setup Guide

## Prerequisites
- Docker Desktop 24+ or Docker Engine + Docker Compose
- kubectl (if using Kubernetes)
- Git
- Node.js 20+ (for local development)

## Quick Start
1. Clone repository: `git clone <repo-url>`
2. Copy configuration: `cp .env.example .env`
3. Start environment: `make dev`
4. Access services:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Teardown
```bash
make dev-down
```

## Troubleshooting
- **Port conflicts**: Edit `.env` to change ports
- **Services won't start**: Run `docker-compose logs <service>`
- **Database issues**: Remove volumes with `docker-compose down -v`
```

### 7. Makefile Integration

Generate `Makefile` for developer convenience:

```makefile
.PHONY: dev dev-down dev-reset health logs test

dev:
	@echo "🚀 Starting development environment..."
	@./scripts/dev-up.sh

dev-down:
	@echo "🛑 Stopping development environment..."
	@./scripts/dev-down.sh

dev-reset: dev-down dev
	@echo "🔄 Environment reset complete"

health:
	@./scripts/health-check.sh

logs:
	docker-compose logs -f

test:
	@echo "🧪 Running tests..."
	docker-compose exec api npm test
```

## Common Patterns

### Dependency Ordering
Ensure services start in correct order:
1. Infrastructure (Postgres, Redis)
2. Backend API (after DB is ready)
3. Frontend (after API is ready)

### Secret Management
Pattern for handling secrets:
```bash
# .env.example (committed)
DB_PASSWORD=dev_password_change_in_production

# .env (gitignored)
DB_PASSWORD=actual_dev_password

# Production
DB_PASSWORD_SECRET=arn:aws:secretsmanager:...
```

### Hot Reload Configuration
Enable development-friendly features:
- Volume mounts for live code changes
- Debug ports exposed (Node: 9229, Python: 5678)
- Source maps enabled
- File watchers configured

### Error Handling
Scripts should:
- Exit on first error (`set -e`)
- Provide clear error messages
- Suggest fixes for common problems
- Log errors to file for debugging

## Best Practices

1. **Make it fast**: Use caching, parallel starts where safe
2. **Make it clear**: Show progress, log to console and file
3. **Make it safe**: Never commit real secrets, validate inputs
4. **Make it flexible**: Support configuration overrides
5. **Make it reproducible**: Pin all versions (images, packages)
6. **Make it documented**: Include inline comments and README

## Troubleshooting Guide

### Common Issues

**Port already in use:**
```bash
# Find process using port
lsof -i :3000
# Kill process or change port in .env
```

**Docker daemon not running:**
```bash
# macOS/Windows: Start Docker Desktop
# Linux: sudo systemctl start docker
```

**Database won't connect:**
```bash
# Check if container is running
docker ps | grep postgres
# Check logs
docker logs <container-id>
# Reset database
docker-compose down -v && docker-compose up -d
```

**Out of date images:**
```bash
# Pull latest images
docker-compose pull
# Rebuild with no cache
docker-compose build --no-cache
```

## Performance Optimizations

1. **Parallel service startup**: Start independent services simultaneously
2. **Image layer caching**: Structure Dockerfiles for optimal caching
3. **Volume optimization**: Use named volumes instead of bind mounts for node_modules
4. **Network configuration**: Use custom networks for better isolation
5. **Resource limits**: Set appropriate CPU/memory limits to prevent resource exhaustion

## Skill Integrations

This skill works seamlessly with companion skills:

- **database-seeding**: Automatically seed databases with realistic test data
- **git-hooks**: Set up pre-commit linting and pre-push testing
- **local-ssl**: Enable HTTPS for local development with trusted certificates
- **env-manager**: Switch between dev/test/staging environments easily

When multiple skills are available, reference them in the setup documentation and scripts.
