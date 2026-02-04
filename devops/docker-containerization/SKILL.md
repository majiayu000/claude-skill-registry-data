---
name: docker-containerization
description: Docker development and container orchestration expertise. Use when creating Dockerfiles, docker-compose configurations, debugging container issues, optimizing images, or setting up isolated development environments. Integrates with CI/CD workflows and security scanning.
model_tier: opus
parallel_hints:
  can_parallel_with: [security-audit, code-review]
  must_serialize_with: [database-migration]
  preferred_batch_size: 2
context_hints:
  max_file_context: 40
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "production|prod"
    reason: "Production container changes require human approval"
  - pattern: "secrets|credentials"
    reason: "Secret management requires security review"
  - keyword: ["registry", "push", "deploy"]
    reason: "Container deployment requires human oversight"
---

# Docker Containerization Skill

Production-grade Docker patterns for multi-stage builds, orchestration, development environments, and container security. Tailored to the Residency Scheduler's existing Docker infrastructure.

## When This Skill Activates

- Creating or modifying Dockerfiles
- Setting up docker-compose configurations
- Debugging container build failures or runtime issues
- Optimizing Docker image size or build performance
- Configuring health checks and service dependencies
- Implementing container security hardening
- Setting up isolated development environments (devcontainers)
- Troubleshooting networking between containers
- CI/CD pipeline Docker integration
- Multi-architecture image builds

## Project Docker Architecture

### File Locations

```
/backend/Dockerfile              → Production backend (multi-stage)
/backend/Dockerfile.local        → Development backend (hot reload)
/frontend/Dockerfile             → Production frontend (multi-stage)
/frontend/Dockerfile.local       → Development frontend
/nginx/Dockerfile                → Nginx reverse proxy
.docker/backend.Dockerfile       → Hardened production backend
.docker/frontend.Dockerfile      → Hardened production frontend
.docker/docker-compose.prod.yml  → Production with secrets
.dockerignore                    → Build exclusions
```

### Compose Files

| File | Purpose | Command |
|------|---------|---------|
| `docker-compose.yml` | Base configuration | `docker compose up` |
| `docker-compose.dev.yml` | Development overrides | `docker compose -f docker-compose.yml -f docker-compose.dev.yml up` |
| `docker-compose.prod.yml` | Production overrides | `docker compose -f docker-compose.yml -f docker-compose.prod.yml up` |
| `.docker/docker-compose.prod.yml` | Hardened production | Uses Docker secrets |
| `monitoring/docker-compose.monitoring.yml` | Prometheus/Grafana | Observability stack |
| `load-tests/docker-compose.k6.yml` | Load testing | k6 test runner |

## Multi-Stage Dockerfile Patterns

### Backend (Python/FastAPI)

```dockerfile
# syntax=docker/dockerfile:1.4

# =============================================================================
# STAGE 1: Builder - Install dependencies
# =============================================================================
FROM python:3.12-slim AS builder

# Build dependencies for compiled packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies in virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 2: Runtime - Minimal production image
# =============================================================================
FROM python:3.12-slim AS runtime

# Runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Security: Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup alembic/ ./alembic/
COPY --chown=appuser:appgroup alembic.ini .

# Security: Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Next.js)

```dockerfile
# syntax=docker/dockerfile:1.4

# =============================================================================
# STAGE 1: Dependencies
# =============================================================================
FROM node:22-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --only=production

# =============================================================================
# STAGE 2: Builder
# =============================================================================
FROM node:22-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build arguments for environment
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

# =============================================================================
# STAGE 3: Production
# =============================================================================
FROM node:22-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Security: Non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["node", "server.js"]
```

## Docker Compose Patterns

### Development Configuration

```yaml
# docker-compose.yml (base)
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: scheduler
      POSTGRES_PASSWORD: ${DB_PASSWORD:-localdev}
      POSTGRES_DB: residency_scheduler
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U scheduler"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql+asyncpg://scheduler:${DB_PASSWORD:-localdev}@db:5432/residency_scheduler
      REDIS_URL: redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000
    depends_on:
      - backend

volumes:
  postgres_data:

networks:
  default:
    driver: bridge
```

### Development Overrides

```yaml
# docker-compose.dev.yml
services:
  db:
    ports:
      - "5432:5432"  # Expose for local tools

  redis:
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.local
    volumes:
      - ./backend/app:/app/app:delegated  # Hot reload
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    environment:
      LOG_LEVEL: DEBUG

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.local
    volumes:
      - ./frontend/src:/app/src:delegated
      - ./frontend/public:/app/public:delegated
    command: npm run dev
    ports:
      - "3000:3000"
```

### Production Security Hardening

```yaml
# .docker/docker-compose.prod.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 1G
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    secrets:
      - db_password
      - secret_key
    environment:
      DATABASE_PASSWORD_FILE: /run/secrets/db_password
      SECRET_KEY_FILE: /run/secrets/secret_key

  db:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

secrets:
  db_password:
    external: true
  secret_key:
    external: true

networks:
  backend-network:
    internal: true  # No external access
  frontend-network:
    driver: bridge
```

## Health Check Patterns

### Backend Health Endpoint

```python
# app/api/routes/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.api.deps import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Comprehensive health check for Docker."""
    checks = {}

    # Database connectivity
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Redis connectivity (if used)
    try:
        from app.core.redis import redis_client
        await redis_client.ping()
        checks["redis"] = "healthy"
    except Exception:
        checks["redis"] = "unhealthy"

    is_healthy = all(v == "healthy" for v in checks.values())

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "checks": checks
    }
```

### Docker Health Check Configuration

```dockerfile
# Liveness check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

```yaml
# docker-compose.yml equivalent
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  start_period: 5s
  retries: 3
```

## Container Debugging

### Common Issues and Solutions

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Container exits immediately | `docker logs <container>` | Check for missing env vars or failed health check |
| Build fails at COPY | File doesn't exist or in .dockerignore | Verify path and check `.dockerignore` |
| Port already in use | `lsof -i :PORT` | Stop conflicting service or change port |
| Permission denied | File ownership issues | Use `--chown` in COPY or fix user UID |
| Out of memory | Container limits | Increase `deploy.resources.limits.memory` |
| Slow builds | No layer caching | Order Dockerfile commands correctly |

### Debugging Commands

```bash
# View container logs
docker compose logs backend -f --tail=100

# Execute shell in running container
docker compose exec backend /bin/bash

# Inspect container filesystem
docker compose exec backend ls -la /app

# Check container resource usage
docker stats

# View container details
docker inspect <container_id>

# Debug network connectivity
docker compose exec backend curl -v http://db:5432

# Check health status
docker inspect --format='{{json .State.Health}}' <container_id>

# View image layers (find bloat)
docker history <image>:tag --no-trunc

# Prune unused resources
docker system prune -a --volumes
```

### Build Debugging

```bash
# Build with no cache (fresh)
docker compose build --no-cache

# Build with progress output
docker compose build --progress=plain

# Build specific service
docker compose build backend

# Build with build args
docker compose build --build-arg NEXT_PUBLIC_API_URL=http://api.example.com frontend

# Export image for analysis
docker save <image> | tar -xf - -C ./image-layers/
```

## Image Optimization

### Size Reduction Techniques

1. **Multi-stage builds**: Only copy artifacts, not build tools
2. **Alpine base images**: `python:3.12-alpine` vs `python:3.12` (50MB vs 1GB)
3. **Minimize layers**: Combine RUN commands with `&&`
4. **Clean up in same layer**: `apt-get clean && rm -rf /var/lib/apt/lists/*`
5. **Use .dockerignore**: Exclude tests, docs, git history

### Example .dockerignore

```dockerignore
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
.pytest_cache
.coverage
htmlcov/
.mypy_cache

# Virtual environments
venv/
.venv/
env/

# IDE
.vscode/
.idea/

# Tests (for production image)
tests/
**/test_*.py

# Documentation
docs/
*.md
!README.md

# Docker
Dockerfile*
docker-compose*

# Environment
.env
.env.*
```

### Layer Caching Optimization

```dockerfile
# BAD: Invalidates cache on any code change
COPY . .
RUN pip install -r requirements.txt

# GOOD: Dependencies cached separately from code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

## DevContainer Configuration

### Basic Setup for Claude Code

```json
// .devcontainer/devcontainer.json
{
  "name": "Residency Scheduler Dev",
  "dockerComposeFile": [
    "../docker-compose.yml",
    "../docker-compose.dev.yml",
    "docker-compose.devcontainer.yml"
  ],
  "service": "backend",
  "workspaceFolder": "/workspace",

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/opt/venv/bin/python"
      }
    }
  },

  "forwardPorts": [8000, 3000, 5432, 6379],

  "postCreateCommand": "pip install -e '.[dev]'",

  "remoteUser": "vscode"
}
```

### DevContainer Docker Compose Override

```yaml
# .devcontainer/docker-compose.devcontainer.yml
services:
  backend:
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
    user: vscode
```

## CI/CD Integration

### GitHub Actions Docker Build

```yaml
# .github/workflows/cd.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/backend
          tags: |
            type=semver,pattern={{version}}
            type=sha,prefix=
            type=ref,event=branch

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Security Scanning

```yaml
# .github/workflows/security.yml (excerpt)
- name: Run Trivy container scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload Trivy results
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

## Quick Commands

```bash
# === Development ===
# Start all services
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Start with rebuild
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

# View logs (follow)
docker compose logs -f backend

# Stop all services
docker compose down

# Stop and remove volumes (DESTRUCTIVE)
docker compose down -v

# === Debugging ===
# Shell into backend
docker compose exec backend bash

# Run tests in container
docker compose exec backend pytest

# Check database connectivity
docker compose exec backend python -c "from app.db.session import engine; print('Connected!')"

# === Production ===
# Build production images
docker compose -f docker-compose.yml -f docker-compose.prod.yml build

# Run database migrations
docker compose exec backend alembic upgrade head

# === Maintenance ===
# View resource usage
docker stats

# Clean up unused resources
docker system prune -af --volumes

# List images with sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## Integration with Other Skills

### With security-audit
When reviewing Docker configurations:
1. Check for non-root users
2. Verify secrets are not in environment variables
3. Ensure health checks exist
4. Review network isolation

### With production-incident-responder
For container-related incidents:
1. Collect container logs: `docker compose logs --since=1h`
2. Check health status: `docker inspect --format='{{json .State.Health}}'`
3. Review resource limits
4. Check for OOM kills in `dmesg`

### With code-review
When reviewing Dockerfile changes:
1. Verify multi-stage builds are used
2. Check layer ordering for cache efficiency
3. Ensure .dockerignore is updated
4. Review security hardening

### With automated-code-fixer
For Dockerfile linting:
```bash
# Install hadolint for Dockerfile linting
docker run --rm -i hadolint/hadolint < Dockerfile
```

## Escalation Rules

**Escalate to human when:**

1. Production docker-compose.yml changes
2. Secrets management configuration
3. Network security policy changes
4. Resource limit adjustments for production
5. Multi-architecture build requirements
6. Kubernetes migration planning
7. Container registry access issues

**Can handle autonomously:**

1. Development Dockerfile creation
2. docker-compose.dev.yml modifications
3. Health check implementation
4. .dockerignore updates
5. Image size optimization
6. Build caching improvements
7. Container debugging and log analysis

## References

- `/backend/Dockerfile` - Production backend pattern
- `/frontend/Dockerfile` - Production frontend pattern
- `/docker-compose.yml` - Base orchestration
- `/.docker/docker-compose.prod.yml` - Security hardening example
- `/.github/workflows/cd.yml` - CI/CD Docker integration
- `/.github/workflows/security.yml` - Container scanning
