---
name: docker-backend-patterns
description: Docker containerization patterns for Node.js applications. Use when containerizing backend services.
---

# Docker Backend Patterns Skill

This skill covers Docker containerization best practices for Node.js applications.

## When to Use

Use this skill when:
- Containerizing Node.js applications
- Optimizing Docker image size
- Implementing multi-stage builds
- Deploying to container platforms

## Core Principle

**MINIMAL, SECURE, REPRODUCIBLE** - Small images, non-root users, deterministic builds.

## Multi-Stage Dockerfile

```dockerfile
# Dockerfile
# Stage 1: Dependencies
FROM node:22-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:22-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 3: Production
FROM node:22-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Security: Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nodejs

# Copy production dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy built application
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./

# Copy Prisma schema for migrations
COPY --from=build /app/prisma ./prisma

# Generate Prisma client
RUN npx prisma generate

# Set ownership
RUN chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

## .dockerignore

```
# .dockerignore
node_modules
npm-debug.log
.git
.gitignore
.env
.env.*
!.env.example
dist
coverage
.nyc_output
*.md
!README.md
Dockerfile*
docker-compose*
.dockerignore
.eslintrc*
.prettierrc*
*.test.ts
__tests__
tests
.vscode
.idea
*.log
```

## Development Dockerfile

```dockerfile
# Dockerfile.dev
FROM node:22-alpine

WORKDIR /app

RUN apk add --no-cache libc6-compat

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

## Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/app
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  migration:
    build:
      context: .
      dockerfile: Dockerfile
    command: npx prisma migrate deploy
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/app
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
```

## Development Compose

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/app
      - NODE_ENV=development
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: app
    volumes:
      - postgres_dev:/var/lib/postgresql/data

volumes:
  postgres_dev:
```

## Build Arguments

```dockerfile
# Dockerfile with build args
ARG NODE_VERSION=22
FROM node:${NODE_VERSION}-alpine AS base

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

# ... rest of Dockerfile
```

```bash
# Build with arguments
docker build \
  --build-arg NODE_VERSION=22 \
  --build-arg APP_VERSION=$(git rev-parse --short HEAD) \
  -t myapp:latest .
```

## Layer Caching Optimization

```dockerfile
# Optimize for layer caching
FROM node:22-alpine AS deps
WORKDIR /app

# Copy only package files first (better caching)
COPY package.json package-lock.json ./
RUN npm ci

# Then copy source (invalidates less often)
FROM deps AS build
COPY . .
RUN npm run build
```

## Security Best Practices

```dockerfile
# Security-focused Dockerfile
FROM node:22-alpine AS runner
WORKDIR /app

# Update packages for security patches
RUN apk update && apk upgrade --no-cache

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 --ingroup nodejs nodejs

# Set strict file permissions
COPY --chown=nodejs:nodejs --from=build /app/dist ./dist
COPY --chown=nodejs:nodejs --from=deps /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs package.json ./

# Remove unnecessary tools
RUN apk del --purge apk-tools

# Switch to non-root user
USER nodejs

# Read-only filesystem (where possible)
# Note: Some apps need writable /tmp
```

## Health Check Endpoint

```typescript
// src/routes/health.ts
import { FastifyPluginAsync } from 'fastify';

interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  version: string;
  uptime: number;
  timestamp: string;
  checks: {
    database: HealthCheck;
    redis: HealthCheck;
  };
}

interface HealthCheck {
  status: 'up' | 'down';
  latency?: number;
}

const healthRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.get<{ Reply: HealthStatus }>('/health', async (request, reply) => {
    const checks = {
      database: await checkDatabase(fastify),
      redis: await checkRedis(fastify),
    };

    const isHealthy = Object.values(checks).every((c) => c.status === 'up');

    const response: HealthStatus = {
      status: isHealthy ? 'healthy' : 'unhealthy',
      version: process.env.APP_VERSION ?? 'unknown',
      uptime: process.uptime(),
      timestamp: new Date().toISOString(),
      checks,
    };

    return reply.status(isHealthy ? 200 : 503).send(response);
  });

  // Liveness probe (basic check)
  fastify.get('/health/live', async () => {
    return { status: 'ok' };
  });

  // Readiness probe (full check)
  fastify.get('/health/ready', async (request, reply) => {
    const dbOk = (await checkDatabase(fastify)).status === 'up';
    if (!dbOk) {
      return reply.status(503).send({ status: 'not ready' });
    }
    return { status: 'ready' };
  });
};

async function checkDatabase(fastify: FastifyInstance): Promise<HealthCheck> {
  const start = Date.now();
  try {
    await fastify.db.$queryRaw`SELECT 1`;
    return { status: 'up', latency: Date.now() - start };
  } catch {
    return { status: 'down' };
  }
}

async function checkRedis(fastify: FastifyInstance): Promise<HealthCheck> {
  const start = Date.now();
  try {
    await fastify.redis.ping();
    return { status: 'up', latency: Date.now() - start };
  } catch {
    return { status: 'down' };
  }
}

export default healthRoutes;
```

## Graceful Shutdown

```typescript
// src/index.ts
const signals: NodeJS.Signals[] = ['SIGTERM', 'SIGINT'];

for (const signal of signals) {
  process.on(signal, async () => {
    app.log.info(`Received ${signal}, shutting down gracefully...`);

    // Stop accepting new connections
    await app.close();

    // Close database connections
    await prisma.$disconnect();

    app.log.info('Graceful shutdown complete');
    process.exit(0);
  });
}
```

## Docker Commands

```bash
# Build image
docker build -t myapp:latest .

# Build with no cache
docker build --no-cache -t myapp:latest .

# Run container
docker run -d --name myapp -p 3000:3000 --env-file .env myapp:latest

# View logs
docker logs -f myapp

# Execute command in container
docker exec -it myapp sh

# Check image size
docker images myapp:latest

# Scan for vulnerabilities
docker scout cves myapp:latest

# Push to registry
docker push registry.example.com/myapp:latest
```

## CI/CD Build

```yaml
# .github/workflows/docker.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Best Practices

1. **Multi-stage builds** - Separate build from runtime
2. **Non-root user** - Never run as root
3. **Health checks** - Enable container orchestration
4. **Minimal base image** - Use Alpine when possible
5. **Layer caching** - Order Dockerfile for cache efficiency
6. **Graceful shutdown** - Handle SIGTERM properly

## Notes

- Alpine images are smaller but use musl libc
- Some npm packages need `libc6-compat`
- Use `.dockerignore` to reduce context size
- Tag images with git SHA for traceability
