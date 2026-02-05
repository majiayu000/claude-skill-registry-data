---
name: Container Best Practices
description: Expert guidance on dockerfile optimization, multi-stage builds, layer caching strategies, and base image selection. Activates when working with "dockerfile", "docker-compose", "multi-stage", "container optimization", "image layers", or "build cache".
version: 1.0.0
---

# Container Best Practices Skill

## Overview

Apply industry-standard best practices for building optimized, maintainable, and efficient Docker containers. Master multi-stage builds, layer caching, base image selection, and build optimization strategies to create production-ready container images.

## Core Principles

### Write Efficient Dockerfiles

**Order Instructions for Maximum Cache Efficiency:**

Structure Dockerfile layers from least to most frequently changing:

```dockerfile
# 1. Base image (changes rarely)
FROM node:20-alpine AS base

# 2. System dependencies (changes occasionally)
RUN apk add --no-cache \
    python3 \
    make \
    g++

# 3. Working directory setup
WORKDIR /app

# 4. Package manifest files (changes moderately)
COPY package.json package-lock.json ./

# 5. Dependencies installation (leverages cache when manifest unchanged)
RUN npm ci --only=production

# 6. Application code (changes frequently)
COPY . .

# 7. Build step (only when code changes)
RUN npm run build

# 8. Runtime configuration
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

**Combine RUN Commands to Reduce Layers:**

Minimize image size by chaining related commands:

```dockerfile
# Bad: Creates 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Good: Creates 1 layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

**Use .dockerignore to Exclude Unnecessary Files:**

Create `.dockerignore` to prevent copying build artifacts and sensitive files:

```
# Development files
node_modules/
npm-debug.log*
.git/
.gitignore

# Test files
*.test.js
coverage/
.nyc_output/

# Documentation
README.md
docs/

# IDE files
.vscode/
.idea/

# Environment files
.env
.env.local
*.key
*.pem
```

### Implement Multi-Stage Builds

**Separate Build and Runtime Environments:**

Use multi-stage builds to create minimal production images:

```dockerfile
# Stage 1: Build environment with all dev dependencies
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && \
    npm run test

# Stage 2: Production environment with only runtime dependencies
FROM node:20-alpine AS production
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

# Security: Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

USER nodejs
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

**Create Specialized Build Targets:**

Define multiple targets for different use cases:

```dockerfile
# Development stage with hot reload
FROM node:20-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000 9229
CMD ["npm", "run", "dev"]

# Testing stage with test dependencies
FROM development AS testing
RUN npm run lint && \
    npm run test:unit && \
    npm run test:integration

# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage (minimal)
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

Build specific stages:

```bash
# Development
docker build --target development -t myapp:dev .

# Testing
docker build --target testing -t myapp:test .

# Production
docker build --target production -t myapp:prod .
```

### Optimize Base Image Selection

**Choose Minimal Base Images:**

Select the smallest viable base image for your runtime:

```dockerfile
# Python examples by size
FROM python:3.11-alpine      # ~50MB (best for simple apps)
FROM python:3.11-slim        # ~120MB (good compatibility)
FROM python:3.11             # ~900MB (avoid in production)

# Node.js examples by size
FROM node:20-alpine          # ~110MB (best for production)
FROM node:20-slim            # ~170MB (good compatibility)
FROM node:20                 # ~900MB (avoid in production)

# Distroless images (Google)
FROM gcr.io/distroless/nodejs20-debian12  # Minimal attack surface
FROM gcr.io/distroless/python3-debian12   # No shell, no package manager
```

**Use Distroless for Maximum Security:**

Distroless images contain only your application and runtime dependencies:

```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Production: Distroless image
FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER nonroot:nonroot
EXPOSE 3000
CMD ["dist/main.js"]
```

**Pin Specific Versions:**

Always use specific version tags for reproducibility:

```dockerfile
# Bad: Version changes unexpectedly
FROM node:20

# Good: Specific version pinned
FROM node:20.11.1-alpine3.19

# Better: Use digest for immutability
FROM node:20.11.1-alpine3.19@sha256:abc123...
```

### Leverage Build Cache Effectively

**Structure for Cache Reuse:**

Place frequently changing instructions after stable ones:

```dockerfile
FROM python:3.11-slim

# System packages (rarely change)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client && \
    apt-get clean

# Requirements (change occasionally)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code (changes frequently)
COPY . .

CMD ["python", "app.py"]
```

**Use BuildKit Cache Mounts:**

Enable BuildKit for advanced caching:

```dockerfile
# syntax=docker/dockerfile:1.4

FROM python:3.11-slim

# Cache pip downloads across builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Cache apt packages
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y postgresql-client
```

Build with BuildKit:

```bash
DOCKER_BUILDKIT=1 docker build -t myapp:latest .
```

**Implement Layer Caching in CI/CD:**

Use registry cache for faster CI builds:

```bash
# GitHub Actions with BuildKit cache
docker buildx build \
  --cache-from type=registry,ref=ghcr.io/org/app:cache \
  --cache-to type=registry,ref=ghcr.io/org/app:cache,mode=max \
  --tag ghcr.io/org/app:latest \
  --push .
```

### Optimize Runtime Configuration

**Configure Health Checks:**

Define health checks for container orchestration:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .

# HTTP health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Alternative: Using curl
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000
CMD ["node", "server.js"]
```

**Set Appropriate Working Directory:**

Always use absolute paths for WORKDIR:

```dockerfile
# Bad: Relative path
WORKDIR app

# Good: Absolute path
WORKDIR /app

# Better: Clear organization
WORKDIR /opt/application
```

**Use COPY Instead of ADD:**

Prefer COPY for clarity unless you need ADD's special features:

```dockerfile
# Bad: ADD has implicit behavior (extracts tars, fetches URLs)
ADD archive.tar.gz /app/

# Good: COPY is explicit and predictable
COPY src/ /app/src/
COPY package.json /app/

# OK: ADD when you need tar extraction
ADD rootfs.tar.gz /
```

## Docker Compose Best Practices

### Structure Compose Files for Environments

**Create Environment-Specific Overrides:**

Use base compose file with environment overrides:

```yaml
# docker-compose.yml (base)
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      NODE_ENV: production
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}

volumes:
  postgres_data:
```

```yaml
# docker-compose.override.yml (development)
version: '3.9'

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    environment:
      NODE_ENV: development

  db:
    ports:
      - "5432:5432"
```

```yaml
# docker-compose.prod.yml (production)
version: '3.9'

services:
  app:
    build:
      target: production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

Use with:

```bash
# Development (uses docker-compose.override.yml automatically)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Implement Dependency Management

**Control Startup Order:**

Use depends_on with health checks:

```yaml
version: '3.9'

services:
  app:
    image: myapp:latest
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
```

### Configure Resource Limits

**Set Memory and CPU Constraints:**

Prevent resource exhaustion:

```yaml
version: '3.9'

services:
  app:
    image: myapp:latest
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    mem_limit: 1g
    cpus: 1.0
```

## Build Optimization Strategies

### Implement Build Arguments

**Parameterize Builds:**

Use ARG for build-time configuration:

```dockerfile
ARG NODE_VERSION=20
FROM node:${NODE_VERSION}-alpine

ARG BUILD_DATE
ARG VERSION
ARG REVISION

LABEL org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${REVISION}"

ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

WORKDIR /app
COPY . .
RUN npm ci --only=${NODE_ENV}

CMD ["node", "server.js"]
```

Build with arguments:

```bash
docker build \
  --build-arg NODE_VERSION=20 \
  --build-arg VERSION=1.2.3 \
  --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --build-arg REVISION=$(git rev-parse --short HEAD) \
  -t myapp:1.2.3 .
```

### Use Multi-Platform Builds

**Build for Multiple Architectures:**

Create images for AMD64 and ARM64:

```bash
# Create buildx builder
docker buildx create --name multiarch --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ghcr.io/org/app:latest \
  --push .
```

Platform-specific optimizations:

```dockerfile
FROM --platform=$BUILDPLATFORM node:20-alpine AS builder
ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "Building on $BUILDPLATFORM for $TARGETPLATFORM"

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/main.js"]
```

## Performance Optimization

### Minimize Image Size

**Remove Unnecessary Files:**

Clean up in the same layer:

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3 && \
    # Build your app here
    apt-get purge -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
```

**Analyze Image Layers:**

Use dive to inspect layers:

```bash
# Install dive
brew install dive

# Analyze image
dive myapp:latest
```

### Implement Parallel Builds

**Speed Up Multi-Stage Builds:**

Use multiple FROM statements for parallel builds:

```dockerfile
# These stages build in parallel
FROM node:20 AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20 AS tester
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm test

# Final stage depends on builder and tester
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

## Official References

- **Dockerfile Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **Multi-Stage Builds**: https://docs.docker.com/build/building/multi-stage/
- **BuildKit**: https://docs.docker.com/build/buildkit/
- **Docker Compose Reference**: https://docs.docker.com/compose/compose-file/
- **Build Cache**: https://docs.docker.com/build/cache/

## Related Skills

- **Container Security** - Hardening and vulnerability management
- **Docker Skill** - Container runtime operations
- **DevOps Practices** - CI/CD integration and deployment
