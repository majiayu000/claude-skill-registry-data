---
name: container-workflow
description: Guidelines for containerized projects using Docker, Dockerfile, docker-compose, container, and containerization. Covers multi-stage builds, security, signal handling, entrypoint scripts, and deployment workflows.
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Container-Based Projects

**Auto-activate when:** Working with `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`, `.dockerignore`, Kubernetes manifests (`*.yaml`, `*.yml` in k8s directories), container registries, or when user mentions Docker, containers, orchestration, or deployment workflows.

Guidelines for containerized applications using Docker, Docker Compose, and orchestration tools.

## Out of Scope
- Infrastructure orchestration - see `ansible-workflow`
- Kubernetes patterns - separate skill

## CRITICAL: Docker Compose V2 Syntax

**MUST NOT use `version:` field** (deprecated) **or `docker-compose` with hyphen:**

```yaml
# MUST NOT
version: '3.8'
services:
  app:
    image: myapp

# MUST
services:
  app:
    image: myapp
```

```bash
docker compose up    # MUST
docker-compose up    # MUST NOT
```

## CRITICAL: DNS Configuration

```yaml
# MUST use .internal for container DNS
services:
  app:
    environment:
      - DNS_DOMAIN=.internal

# MUST NOT use .local (conflicts with mDNS/Bonjour)
```

## Dockerfile Core Requirements

### Base Images
- Use **Alpine Linux** for minimal attack surface and smaller images
  - Example: `python:3.12-alpine`, `node:20-alpine`
- **MUST specify version tags** for reproducible builds (MUST NOT use `latest`)
- **SHOULD use image digest pinning (SHA256)** for production deployments
- Use official images from trusted registries
- Consider distroless images for production
- If Alpine packages unavailable, use Debian Slim-based containers

```dockerfile
# RECOMMENDED: Pin by digest for production
FROM python:3.12-alpine@sha256:abc123...

# Acceptable: Pin by tag for development
FROM python:3.12-alpine
```

### Multi-stage Builds
- **Separate stages** for different purposes:
  - `base` - Common dependencies and user setup
  - `development` - Development tools and dependencies
  - `production` - Minimal runtime with only production dependencies
- **Copy only necessary artifacts** to final stage
- Reduces final image size and attack surface
- Order commands from least to most frequently changing

### Security Checklist
- MUST create and use non-root users
- MUST set USER directive before EXPOSE and CMD
- MUST NOT include secrets in layers
- MUST use `.dockerignore` to exclude sensitive files
- SHOULD scan images for vulnerabilities regularly
- SHOULD keep base images updated
- MUST run as non-root user (USER directive)
- MUST NOT hardcode secrets or commit credentials
- MUST validate all input, even from trusted sources
- MUST include health checks for orchestration
- MUST use Docker secrets for sensitive data in production (NOT environment variables)
- MUST set `no-new-privileges:true` security option

```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
```

## Project Structure Recognition

**Key files:** `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.devcontainer/`, `Makefile`, `k8s/`

## Workflow Patterns

**Before starting:** Check README, Makefile, docker-compose.yml, .env files

**Command hierarchy:** Makefile - Project scripts - Docker commands

## Layer Optimization

### Reduce Layer Count
- **Group RUN commands** to reduce layers
- Use `&&` to chain related commands
- Clean up in the same layer as installation

### Example: Bad vs. Good
```dockerfile
# MUST NOT: Multiple layers
RUN apk update
RUN apk add curl
RUN apk add git
RUN rm -rf /var/cache/apk/*

# MUST: Single optimized layer
RUN apk update && \
    apk add --no-cache \
        curl \
        git && \
    rm -rf /var/cache/apk/*
```

### Alpine APK Best Practices
- Use `apk add --no-cache` to avoid caching package index
- Maintain **alphabetical order** in package lists for maintainability
- Remove cache in the same RUN command if not using `--no-cache`

```dockerfile
RUN apk add --no-cache \
        bash \
        curl \
        git \
        openssh \
        vim
```

### Cache Optimization
- **Order commands from least to most frequently changing**
- Copy dependency files separately before copying source code
- Use BuildKit cache mounts for package managers

```dockerfile
# MUST: Dependency layer cached separately
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Source code changes won't invalidate dependency cache
COPY app/ ./app/
```

### Package Management Best Practices

#### Python UV (Modern Package Manager)
```dockerfile
# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies with cache mount
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache -r requirements.txt
```

#### Traditional Python Pip
```dockerfile
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt
```

## Non-Root User Setup

```dockerfile
# Create non-root user
ARG PUID=1000
ARG PGID=1000
ARG USER=appuser

RUN addgroup -g ${PGID} ${USER} && \
    adduser -D -u ${PUID} -G ${USER} -s /bin/sh ${USER}

# Switch to non-root user before EXPOSE and CMD
USER ${USER}
```

## 12-Factor App Compliance

| Factor | Implementation |
|--------|---------------|
| Configuration | Environment variables only, MUST NOT hardcode |
| Dependencies | Explicit declarations with lockfiles |
| Stateless | No local state, horizontally scalable |
| Port Binding | Self-contained, exports via port binding |
| Disposability | Fast startup/shutdown, graceful termination |
| Dev/Prod Parity | Keep environments similar |

## Resource Limits

**MUST define resource limits** for production deployments:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
          pids: 100
        reservations:
          cpus: '0.25'
          memory: 128M
```

## Log Rotation

**MUST configure log rotation** to prevent disk exhaustion:

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Complete Multi-Stage Build Template

```dockerfile
# Base stage with common setup
FROM python:3.12-alpine AS base

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Build arguments
ARG PUID=1000
ARG PGID=1000
ARG USER=appuser
ARG WORKDIR=/app

# Create non-root user
RUN addgroup -g ${PGID} ${USER} && \
    adduser -D -u ${PUID} -G ${USER} -s /bin/sh ${USER}

WORKDIR ${WORKDIR}

# Development stage
FROM base AS development

# Install development tools
RUN apk add --no-cache \
        bash \
        curl \
        git \
        vim

# Install development dependencies
COPY requirements.txt requirements-dev.txt ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache -r requirements-dev.txt

# Copy source code
COPY --chown=${USER}:${USER} . .

USER ${USER}

CMD ["python", "run.py"]

# Production stage
FROM base AS production

# Install runtime system dependencies
RUN apk add --no-cache \
        bash \
        curl

# Install production dependencies only
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache -r requirements.txt

# Copy application code
COPY --chown=${USER}:${USER} app/ ./app/
COPY --chown=${USER}:${USER} run.py .

# Switch to non-root user
USER ${USER}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "run.py"]
```

## Health Checks

```dockerfile
# HTTP service
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Database
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD pg_isready -U postgres || exit 1
```

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Docker Compose File Organization

Use `include` directive for modular Compose files:

```
project/
├── docker-compose.yml
├── compose/
│   ├── dev.yml
│   ├── service1.yml
│   └── service2.yml
├── .env
├── .env.development
└── .env.production
```

```yaml
# docker-compose.yml - Main compose file with includes
include:
  - compose/service1.yml
  - compose/service2.yml

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app_network
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
          pids: 100
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_network

volumes:
  db_data:

networks:
  app_network:
    driver: bridge
```

## Docker Secrets

**MUST use Docker secrets over environment variables** for sensitive data:

```yaml
services:
  app:
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true
```

```dockerfile
# Read secret in application
RUN --mount=type=secret,id=db_password \
    cat /run/secrets/db_password > /app/config/db_password
```

## Development Workflow

| Aspect | Development | Production |
|--------|-------------|------------|
| Base Image | Full OS for debugging | Alpine (minimal) |
| Code Mount | Volume mount for hot reload | Copied into image |
| Dependencies | Include dev tools | Runtime only |
| Ports | Exposed for debugging | Necessary only |
| Restart | no (manual control) | unless-stopped |
| Logging | DEBUG | INFO/WARN |

```yaml
# compose/dev.yml
services:
  app:
    build:
      target: development
    volumes:
      - .:/workspace:cached
    command: python run.py --reload
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=debug
```

## DevContainer Configuration

```json
{
  "name": "Project Dev Container",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "dev",
  "workspaceFolder": "/workspace",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-azuretools.vscode-docker"
      ]
    }
  },
  "postCreateCommand": "pip install -e .[dev]",
  "remoteUser": "appuser"
}
```

## Makefile Integration Pattern

```makefile
.PHONY: dev build up down logs
dev:
	@docker compose -f docker-compose.yml -f compose/dev.yml up
build:
	@docker compose build
up:
	@docker compose up -d
down:
	@docker compose down
logs:
	@docker compose logs -f

# Pattern rules
run-%:
	@docker compose -f docker-compose.yml -f compose/$*.yml up
stop-%:
	@docker compose stop $*
```

## Environment Variables

### Build-time Variables (ARG)
- Use ARG for build-time configuration
- Common ARGs: PUID, PGID, USER, WORKDIR, VERSION

```dockerfile
ARG PYTHON_VERSION=3.12
ARG PUID=1000
ARG PGID=1000
ARG USER=appuser
ARG WORKDIR=/app
```

### Runtime Variables (ENV)
- Use ENV for runtime environment variables
- Provide sensible defaults
- Document required vs. optional variables

```dockerfile
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production
```

## .dockerignore Best Practices

Comprehensive `.dockerignore` organized by category to exclude unnecessary files from build context:

```
# Git
.git/
.gitignore
.gitattributes

# Documentation
README.md
docs/
*.md

# CI/CD
.github/
.gitlab-ci.yml

# Development
.vscode/
.idea/
.devcontainer/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.coverage
htmlcov/
.venv/
venv/
*.egg-info/

# Environment files
.env
.env.*

# Build artifacts
build/
dist/

# Testing
tests/
.spec/

# Logs
*.log

# System
.DS_Store
.windows
Thumbs.db

# Docker files
docker-compose*.yml
Dockerfile*
.dockerignore

# Node (if applicable)
node_modules/

# Misc
*.tmp
.cache/
```

## Network Configuration

```yaml
networks:
  app_network:
    driver: bridge
  db_network:
    driver: bridge
    internal: true  # No external access
```

## Language-Specific Patterns

### Flask Application
```dockerfile
FROM python:3.12-alpine AS production

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ARG USER=appuser
RUN adduser -D -s /bin/sh ${USER}

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache -r requirements.txt

COPY --chown=${USER}:${USER} app/ ./app/
COPY --chown=${USER}:${USER} run.py .

USER ${USER}

EXPOSE 5000

HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "run.py"]
```

### Background Worker
```dockerfile
FROM python:3.12-alpine AS production

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ARG USER=worker
RUN adduser -D -s /bin/sh ${USER}

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache -r requirements.txt

COPY --chown=${USER}:${USER} worker/ ./worker/

USER ${USER}

# No EXPOSE needed for background workers
# No HEALTHCHECK - use orchestrator health checks

CMD ["python", "-m", "worker.main"]
```

## BuildKit Features

### Cache Mounts
```dockerfile
# Cache pip packages
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Cache npm packages
RUN --mount=type=cache,target=/root/.npm \
    npm install
```

### Multi-platform Builds
```dockerfile
# Support ARM and AMD architectures
FROM --platform=$BUILDPLATFORM python:3.12-alpine

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "Building for $TARGETPLATFORM on $BUILDPLATFORM"
```

### Multi-platform Build Guidance
- Use `docker buildx` for building multiple architectures
- Reference build platform variables: `$BUILDPLATFORM`, `$TARGETPLATFORM`
- Leverage BuildKit cache exports for CI/CD: `--cache-to=type=registry` and `--cache-from=type=registry`
- Pin base image versions to exact patches for consistent caching

## Signal Handling and Entrypoint Scripts

### Production Containers
- Use `gosu` with `exec` in production entrypoint scripts to drop privileges and forward signals
- Ensure CMD uses direct command execution (not shell wrapping) for proper signal delivery
- When docker.sock is mounted, fix permissions in entrypoint with: `chown ${USER}:${USER} /var/run/docker.sock >/dev/null 2>&1 || true`

### Development Containers
- Sudo is acceptable for devcontainer usage

### Production Entrypoint Script with Signal Handling
```bash
#!/bin/bash
set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # do not hide errors within pipes
if [ -v DOCKER_ENTRYPOINT_DEBUG ] && [ "$DOCKER_ENTRYPOINT_DEBUG" == 1 ]; then
    set -x
    set -o xtrace
fi

# If running as root, adjust the ${USER} user's UID/GID and drop to that user
if [ "$(id -u)" = "0" ]; then
    groupmod -o -g ${PGID:-1000} ${USER} 2>&1 >/dev/null|| true
    usermod -o -u ${PUID:-1000} ${USER} 2>&1 >/dev/null|| true

    # Ensure docker.sock is owned by the target user when running as root
    chown ${USER}:${USER} /var/run/docker.sock >/dev/null 2>&1 || true

    echo "Running as user ${USER}: $@"
    exec gosu ${USER} "$@"
fi

echo "Running: $@"
exec "$@"
```

## Common Container Patterns

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
          pids: 100

  db:
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:
```

## Git Submodules in Containers

```dockerfile
RUN git clone --recurse-submodules https://github.com/user/repo.git
# Or: RUN git submodule update --init --recursive
```

## Essential Docker Commands

```bash
# Service management
docker compose up / up -d / down / down -v
docker compose restart app
docker compose build / build --no-cache

# Monitoring
docker compose ps / logs -f / logs -f app
docker stats

# Execute commands
docker compose exec app sh
docker compose run --rm app pytest

# Cleanup
docker image prune -a
docker system prune
```

## Quick Reference

**Before running containers:**
- Check README and Makefile
- Review docker-compose.yml dependencies
- Check for .env.example
- Understand dev vs production configs

**Common mistakes:**
- Using `version:` field or `docker-compose` with hyphen
- Running as root user
- Using large base images (not Alpine)
- Committing secrets
- Using `.local` domain
- Skipping health checks
- Using env vars instead of secrets for sensitive data
- Missing resource limits in production
- No log rotation configured

---

**Note:** Container projects vary in complexity. MUST check project-specific documentation before making changes to Docker configurations.
