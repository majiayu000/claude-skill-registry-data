---
name: docker-wizard
description: Generate optimized Dockerfiles and docker-compose.yml with best practices and multi-stage builds
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash"]
version: 1.0.0
author: GLINCKER Team
license: Apache-2.0
keywords: [docker, containerization, dockerfile, docker-compose, devops]
---

# Docker Wizard

Generate production-ready Dockerfiles and docker-compose.yml files by analyzing your project. Follows best practices, optimizes image size, and includes security hardening.

## What This Skill Does

- Auto-detects project type and dependencies
- Generates multi-stage builds for smaller images
- Applies security best practices (non-root user, minimal base images)
- Creates docker-compose.yml for multi-service setups
- Includes development and production configurations
- Optimizes layer caching for faster builds

## Instructions

### Phase 1: Project Analysis

1. **Detect project type**:
   ```bash
   Use Glob to find:
   - package.json → Node.js
   - requirements.txt/pyproject.toml → Python
   - go.mod → Go
   - Cargo.toml → Rust
   - pom.xml/build.gradle → Java
   ```

2. **Analyze dependencies**:
   ```bash
   Use Read to examine:
   - Runtime dependencies
   - Build dependencies
   - Environment requirements
   - Port requirements
   ```

### Phase 2: Dockerfile Generation

Generate optimized multi-stage Dockerfile:

```dockerfile
# Example for Node.js

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

# Security: Run as non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist

USER nextjs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Best practices applied**:
- Multi-stage builds (reduce image size by 70%)
- Alpine base images (minimal attack surface)
- Non-root user (security)
- Optimized layer caching
- .dockerignore generation

### Phase 3: Docker Compose Generation

Create docker-compose.yml for multi-service setups:

```yaml
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  postgres_data:
```

### Phase 4: Additional Files

1. **.dockerignore**:
   ```
   node_modules
   npm-debug.log
   .git
   .env
   *.md
   .vscode
   .idea
   coverage
   .DS_Store
   ```

2. **docker-compose.dev.yml** (development overrides):
   ```yaml
   version: '3.9'

   services:
     app:
       build:
         target: builder
       volumes:
         - .:/app
         - /app/node_modules
       environment:
         - NODE_ENV=development
       command: npm run dev
   ```

## Language-Specific Optimizations

### Node.js
```dockerfile
# Use npm ci for faster, reproducible builds
RUN npm ci --only=production

# Leverage layer caching
COPY package*.json ./
RUN npm ci
COPY . .
```

### Python
```dockerfile
# Use pip with cache mount
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Use multi-stage for smaller images
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
```

### Go
```dockerfile
# Multi-stage with scratch base
FROM golang:1.21-alpine AS builder
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM scratch
COPY --from=builder /app/app /app
CMD ["/app"]
```

## Security Best Practices

1. **Non-root user**: Always run as non-root
2. **Minimal base**: Use Alpine or distroless
3. **No secrets**: Never COPY .env files
4. **Health checks**: Include HEALTHCHECK directive
5. **Read-only rootfs**: Add security-opt in compose

## Tool Requirements

- **Read**: Examine project files
- **Write**: Create Dockerfiles and compose files
- **Glob**: Find project structure
- **Grep**: Search for patterns
- **Bash**: Test docker build (optional)

## Examples

### Example 1: Full Stack App

**User**: "Generate Docker setup for my MERN app"

**Generated**:
- Multi-stage Dockerfile for React frontend
- Dockerfile for Node.js backend
- docker-compose.yml with MongoDB, Redis
- Nginx reverse proxy config
- .dockerignore for both services

### Example 2: Microservices

**User**: "Create Docker Compose for microservices"

**Generated**:
- Service-specific Dockerfiles
- Shared docker-compose with networking
- Environment-specific overrides
- Health checks and dependencies

## Best Practices

- Use specific versions, not `latest` tags
- Implement health checks for all services
- Use bind mounts in development, volumes in production
- Set resource limits (memory, CPU)
- Enable logging drivers

## Related Skills

- [k8s-generator](../k8s-generator/SKILL.md) - Generate Kubernetes manifests
- [cicd-pipeline-builder](../cicd-pipeline-builder/SKILL.md) - Build CI/CD pipelines

## Changelog

### Version 1.0.0
- Initial release
- Multi-stage build support
- Docker Compose generation
- Security hardening
- Multiple language support

## Author

**GLINCKER Team**
- Repository: [claude-code-marketplace](https://github.com/GLINCKER/claude-code-marketplace)
