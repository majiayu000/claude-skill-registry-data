---
name: docker-reviewer
description: |
  WHEN: Dockerfile review, multi-stage builds, layer optimization, docker-compose
  WHAT: Image optimization + Layer caching + Security scanning + Compose best practices + Build efficiency
  WHEN NOT: Kubernetes → k8s-reviewer, Terraform → terraform-reviewer
---

# Docker Reviewer Skill

## Purpose
Reviews Dockerfiles and docker-compose configurations for optimization, security, and best practices.

## When to Use
- Dockerfile code review
- Docker image optimization
- docker-compose.yml review
- Container security audit
- Build time optimization

## Project Detection
- `Dockerfile` in project
- `docker-compose.yml` or `docker-compose.yaml`
- `.dockerignore` file
- `Dockerfile.*` variants

## Workflow

### Step 1: Analyze Project
```
**Base Image**: node:20-alpine
**Build Type**: Multi-stage
**Compose**: v3.8
**Registry**: Docker Hub / ECR / GCR
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full Docker review (recommended)
- Dockerfile optimization
- Layer caching strategy
- Security hardening
- docker-compose review
multiSelect: true
```

## Detection Rules

### Image Optimization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Large base image | Use alpine/slim/distroless | HIGH |
| No multi-stage build | Add build stage | MEDIUM |
| Too many layers | Combine RUN commands | MEDIUM |
| Installing dev deps | Separate build/runtime | HIGH |

```dockerfile
# BAD: Large image with dev dependencies
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
CMD ["node", "dist/index.js"]
# Result: ~1GB image

# GOOD: Multi-stage with alpine
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
# Result: ~150MB image
```

### Layer Caching
| Check | Recommendation | Severity |
|-------|----------------|----------|
| COPY . before install | Copy package files first | HIGH |
| No .dockerignore | Add .dockerignore | MEDIUM |
| Changing files early | Order by change frequency | MEDIUM |

```dockerfile
# BAD: Cache invalidation on every code change
FROM node:20-alpine
WORKDIR /app
COPY . .                    # Invalidates cache on ANY change
RUN npm install             # Always reinstalls

# GOOD: Leverage layer caching
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./       # Only invalidates on package change
RUN npm ci                  # Cached if packages unchanged
COPY . .                    # Code changes don't affect npm cache
RUN npm run build
```

```gitignore
# .dockerignore
node_modules
.git
.gitignore
*.md
.env*
dist
coverage
.nyc_output
```

### Security
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Running as root | Add USER directive | CRITICAL |
| Latest tag | Pin specific version | HIGH |
| Secrets in build | Use build secrets | CRITICAL |
| No health check | Add HEALTHCHECK | MEDIUM |

```dockerfile
# BAD: Security issues
FROM node:latest           # Unpinned version
WORKDIR /app
COPY . .
ENV API_KEY=secret123      # Secret in image!
RUN npm install
CMD ["node", "index.js"]   # Running as root

# GOOD: Secure Dockerfile
FROM node:20.10-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20.10-alpine
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -s /bin/sh -D appuser

COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --chown=appuser:appgroup . .

USER appuser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

EXPOSE 3000
CMD ["node", "index.js"]
```

### Build Secrets (Docker BuildKit)
```dockerfile
# syntax=docker/dockerfile:1.4

FROM node:20-alpine
WORKDIR /app

# Mount secret during build (not stored in layer)
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) \
    npm ci

# Build command:
# DOCKER_BUILDKIT=1 docker build --secret id=npm_token,src=.npmrc .
```

### RUN Optimization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Multiple RUN for cleanup | Combine in single RUN | MEDIUM |
| No cleanup after install | Remove cache in same layer | MEDIUM |

```dockerfile
# BAD: Multiple layers, cache not cleaned
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# GOOD: Single layer with cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Docker Compose
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No resource limits | Add deploy.resources | HIGH |
| No health checks | Add healthcheck | MEDIUM |
| Hardcoded config | Use environment variables | MEDIUM |
| No restart policy | Add restart: unless-stopped | MEDIUM |

```yaml
# BAD: Minimal compose
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: password123

# GOOD: Production-ready compose
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:${DB_PASSWORD}@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Response Template
```
## Docker Review Results

**Project**: [name]
**Base Image**: node:20-alpine
**Build**: Multi-stage | **Compose**: v3.8

### Image Optimization
| Status | File | Issue |
|--------|------|-------|
| HIGH | Dockerfile | Using node:latest (~1GB) |

### Layer Caching
| Status | File | Issue |
|--------|------|-------|
| HIGH | Dockerfile:5 | COPY . before npm install |

### Security
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | Dockerfile | Running as root user |

### Compose
| Status | File | Issue |
|--------|------|-------|
| HIGH | docker-compose.yml | No resource limits |

### Recommended Actions
1. [ ] Switch to node:20-alpine base image
2. [ ] Add multi-stage build
3. [ ] Add USER directive for non-root
4. [ ] Add resource limits in compose
```

## Best Practices
1. **Base Image**: Use alpine/slim/distroless
2. **Multi-stage**: Separate build and runtime
3. **Caching**: Order by change frequency
4. **Security**: Non-root, pinned versions, no secrets
5. **Compose**: Health checks, resource limits

## Integration
- `k8s-reviewer`: Kubernetes deployments
- `security-scanner`: Container security
- `ci-cd-reviewer`: Build pipelines
