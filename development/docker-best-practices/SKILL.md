---
name: docker-best-practices
description: Create optimized Dockerfiles with multi-stage builds, security hardening, layer caching, and health checks. Includes docker-compose patterns for development and production environments.
---

# Docker Best Practices Skill

## When to Use

Use this skill when:
- Creating new Dockerfiles
- Optimizing existing container images
- Setting up docker-compose environments
- Implementing health checks
- Securing container deployments
- Reducing image sizes
- Configuring multi-stage builds

## Dockerfile Patterns

### 1. Multi-Stage Build (Python)

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy wheels from builder
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Layer Caching Optimization

```dockerfile
# ✅ Good: Dependencies first (cached if unchanged)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ Bad: Entire context first (cache invalidated on any change)
COPY . .
RUN pip install -r requirements.txt
```

### 3. Security Hardening

```dockerfile
# ✅ Security checklist:
# 1. Non-root user
USER appuser

# 2. Read-only filesystem
# docker run --read-only ...

# 3. No new privileges
# docker run --security-opt=no-new-privileges ...

# 4. Drop capabilities
# docker run --cap-drop=ALL ...

# 5. Minimal base image
FROM python:3.12-alpine  # or distroless

# 6. No secrets in image
# Use environment variables or secrets mount
```

### 4. Health Checks

```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# TCP health check (no curl)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD nc -z localhost 8000 || exit 1

# Script health check
HEALTHCHECK CMD ["/app/healthcheck.sh"]
```

## Docker Compose Patterns

### Development Environment

```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app:cached
      - /app/__pycache__  # Exclude pycache
    ports:
      - "8000:8000"
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql://...
    depends_on:
      db:
        condition: service_healthy
    
  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=secret
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Production Environment

```yaml
version: "3.9"

services:
  app:
    image: myapp:${VERSION:-latest}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        max_attempts: 3
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - app-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Image Size Optimization

```
✅ Size reduction techniques:
1. Use slim/alpine base images
2. Multi-stage builds
3. Combine RUN commands
4. Clean up apt cache: && rm -rf /var/lib/apt/lists/*
5. Use .dockerignore
6. Remove build dependencies after install
7. Use --no-cache-dir for pip
```

## Output Format

```markdown
## Docker Analysis Report

### Image Analysis
- Base image: python:3.12-slim
- Final size: 125MB
- Layers: 12
- Security: ✅ Non-root user

### Optimization Suggestions
1. [Current] → [Optimized] - [Size saved]

### Security Findings
- ✅ Non-root user configured
- ⚠️ Health check missing
- ❌ Running as root

### docker-compose Review
- ✅ Health checks defined
- ✅ Resource limits set
- ⚠️ No restart policy
```

## Example Usage

```
@docker Create optimized Dockerfile for FastAPI app
@docker Review docker-compose.yml for production readiness
@docker Reduce image size of the current Dockerfile
@docker Add health checks to all services
```
