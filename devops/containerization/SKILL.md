---
name: containerization
description: Build and deploy Docker containers for Node.js applications. Use when containerizing applications, optimizing Docker builds, or configuring container security.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Containerization Skill

Build secure, optimized Docker containers for Node.js applications.

## Core Principles

| Principle | Description |
|-----------|-------------|
| Minimal Images | Use slim base images, multi-stage builds |
| Non-root User | Never run as root in production |
| Layer Caching | Order Dockerfile for optimal caching |
| Security First | No secrets in images, scan for vulnerabilities |
| Reproducible | Pin versions, use lock files |

## Project Structure

```
project/
├── Dockerfile              # Production image
├── Dockerfile.dev          # Development with hot reload
├── docker-compose.yml      # Multi-container orchestration
├── docker-compose.dev.yml  # Development overrides
├── .dockerignore           # Files to exclude from build
└── .env.example            # Environment variable template
```

## Production Dockerfile

### Node.js Application

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM node:20-slim AS deps
WORKDIR /app

# Install dependencies only (cached unless package files change)
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-slim AS build
WORKDIR /app

# Install all dependencies including devDependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-slim AS production
WORKDIR /app

# Create non-root user
RUN groupadd --gid 1001 nodejs && \
    useradd --uid 1001 --gid nodejs --shell /bin/bash --create-home nodejs

# Copy production dependencies from deps stage
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules

# Copy built application from build stage
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist
COPY --from=build --chown=nodejs:nodejs /app/package.json ./

# Set environment
ENV NODE_ENV=production
ENV PORT=3000

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

# Start application
CMD ["node", "dist/server.js"]
```

### Static Site (Nginx)

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Build
FROM node:20-slim AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine AS production

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built static files
COPY --from=build /app/dist /usr/share/nginx/html

# Create non-root user for nginx
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

USER nginx

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

## Development Dockerfile

```dockerfile
# Dockerfile.dev
FROM node:20-slim

WORKDIR /app

# Install dependencies (will be mounted over in dev)
COPY package.json package-lock.json ./
RUN npm install

# Copy source (will be mounted over in dev)
COPY . .

ENV NODE_ENV=development

EXPOSE 3000

# Use nodemon for hot reload
CMD ["npx", "nodemon", "--watch", "src", "src/server.js"]
```

## Docker Compose

### Production

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    env_file:
      - .env.production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M

  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Development

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      # Mount source for hot reload
      - ./src:/app/src:delegated
      - ./package.json:/app/package.json
      # Exclude node_modules from mount
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    env_file:
      - .env.development

  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=devuser
      - POSTGRES_PASSWORD=devpass
      - POSTGRES_DB=devdb
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data

volumes:
  postgres_dev_data:
```

## .dockerignore

```
# Git
.git
.gitignore

# Node
node_modules
npm-debug.log

# Build output (will be created in container)
dist
build

# Development
.env
.env.local
.env.*.local
*.log

# IDE
.vscode
.idea
*.swp
*.swo

# Documentation
*.md
docs/

# Tests
test/
tests/
__tests__/
*.test.js
*.spec.js
coverage/

# CI/CD
.github/
.gitlab-ci.yml
Jenkinsfile

# Docker (prevent recursive copying)
Dockerfile*
docker-compose*
.dockerignore
```

## Security Best Practices

### Non-root User

```dockerfile
# Create user with specific UID/GID
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/false --no-create-home appuser

# Set ownership
COPY --chown=appuser:appgroup . .

# Switch to non-root
USER appuser
```

### Secret Management

```dockerfile
# DON'T: Embed secrets in image
ENV API_KEY=secret123  # Bad!

# DO: Pass at runtime
# docker run -e API_KEY=secret123 myapp

# DO: Use Docker secrets (Swarm/Compose)
# docker secret create api_key ./api_key.txt

# DO: Use BuildKit secrets for build-time secrets
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci
```

### Vulnerability Scanning

```bash
# Scan image for vulnerabilities
docker scout cves myapp:latest

# Or use Trivy
trivy image myapp:latest

# Scan during CI
docker scout cves --exit-code --only-severity critical,high myapp:latest
```

### Read-only Filesystem

```yaml
# docker-compose.yml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

## Layer Optimization

### Order for Best Caching

```dockerfile
# 1. Base image and system deps (rarely changes)
FROM node:20-slim
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init

# 2. Package files (changes when dependencies change)
COPY package.json package-lock.json ./

# 3. Install dependencies (cached unless package files change)
RUN npm ci --only=production

# 4. Application code (changes frequently)
COPY . .

# 5. Build step (runs when code changes)
RUN npm run build
```

### Multi-stage Build Benefits

| Stage | Purpose | Final Image |
|-------|---------|-------------|
| deps | Install production dependencies | Copied |
| build | Install all deps, compile TypeScript | Build artifacts only |
| production | Runtime only | Final image |

## Health Checks

### HTTP Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"
```

### Application Health Endpoint

```javascript
// src/api/health.js
export function healthHandler(req, res) {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    checks: {
      database: await checkDatabase(),
      redis: await checkRedis()
    }
  };

  const isHealthy = Object.values(health.checks).every(c => c === true);

  res.status(isHealthy ? 200 : 503).json(health);
}
```

## Common Commands

```bash
# Build image
docker build -t myapp:latest .

# Build with BuildKit (recommended)
DOCKER_BUILDKIT=1 docker build -t myapp:latest .

# Build specific stage
docker build --target build -t myapp:build .

# Run container
docker run -p 3000:3000 --env-file .env myapp:latest

# Development with compose
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker compose up -d

# View logs
docker compose logs -f app

# Shell into container
docker compose exec app sh

# Rebuild single service
docker compose up -d --build app

# Prune unused images
docker image prune -a
```

## DigitalOcean Deployment

### App Platform (app.yaml)

```yaml
name: my-app
services:
  - name: web
    dockerfile_path: Dockerfile
    source_dir: /
    github:
      repo: username/repo
      branch: main
    http_port: 3000
    instance_size_slug: basic-xxs
    instance_count: 1
    health_check:
      http_path: /health
```

### Droplet Deployment

```bash
# Build and push to registry
docker build -t registry.digitalocean.com/myregistry/myapp:latest .
docker push registry.digitalocean.com/myregistry/myapp:latest

# On droplet
docker pull registry.digitalocean.com/myregistry/myapp:latest
docker compose up -d
```

## Checklist

When containerizing:

- [ ] Multi-stage build used for smaller images
- [ ] Running as non-root user
- [ ] No secrets in Dockerfile or image
- [ ] .dockerignore excludes unnecessary files
- [ ] Health check configured
- [ ] Layer order optimized for caching
- [ ] Vulnerability scan passes
- [ ] Resource limits set in compose

## Related Skills

- **deployment** - Deploy containers to infrastructure
- **ci-cd** - Build images in CI pipeline
- **security** - Container security practices
- **nodejs-backend** - Node.js application patterns
