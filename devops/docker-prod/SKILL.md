---
name: docker-prod
description: Docker prod — image optimization, multi-stage builds, best practices.
---

# Docker for Production

## Core Principles

- **Minimal images**: only what the app needs to run — no dev tools, no build artifacts
- **Multi-stage builds**: separate build and runtime stages
- **Non-root user**: never run processes as root
- **Read-only filesystem** where possible
- **Explicit versions**: never use `latest` tags in production
- **Health checks**: always define them so orchestrators know when a container is ready

---

## Multi-Stage Dockerfile

```dockerfile
# ─── Stage 1: Build ───────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# ─── Stage 2: Runtime ─────────────────────────────────────────
FROM node:20-alpine AS runtime

# Security: non-root user
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

WORKDIR /app

# Copy only what's needed
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/package.json .

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

## PHP (Laravel/FrankenPHP) Example

```dockerfile
FROM dunglas/frankenphp:1-php8.3-alpine AS base

RUN install-php-extensions \
    pdo_pgsql \
    redis \
    opcache \
    intl

# ─── Build stage ──────────────────────────────────────────────
FROM base AS builder

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --prefer-dist --optimize-autoloader

COPY . .
RUN composer run-script post-autoload-dump

# ─── Runtime stage ────────────────────────────────────────────
FROM base AS runtime

RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup www-data-custom

WORKDIR /app

COPY --from=builder --chown=www-data-custom:appgroup /app .

USER www-data-custom

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget -qO- http://localhost:8080/up || exit 1

CMD ["frankenphp", "run", "--config", "/etc/caddy/Caddyfile"]
```

## Production docker-compose.yml

```yaml
services:
  app:
    image: registry.example.com/myapp:${IMAGE_TAG:-latest}
    container_name: myapp
    restart: always
    environment:
      - APP_ENV=production
    env_file:
      - .env.production
    ports:
      - "127.0.0.1:8000:8000"   # bind to loopback — nginx/caddy handles external
    read_only: true              # filesystem is read-only
    tmpfs:
      - /tmp                     # writable temp
      - /run
    depends_on:
      db:
        condition: service_healthy
    networks:
      - internal
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 512M

  db:
    image: postgres:16-alpine
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    networks:
      - internal

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  db_data:

networks:
  internal:
    driver: bridge
    internal: true   # no external access
```

## Image Size Optimization

- Use Alpine or Distroless base images
- Combine `RUN` commands to reduce layers: `RUN apt-get update && apt-get install -y pkg && rm -rf /var/lib/apt/lists/*`
- Use `.dockerignore` to exclude: `.git`, `node_modules`, `*.log`, `tests/`, `docs/`
- Multi-stage builds to exclude build tools from final image

## Security Checklist

- [ ] Non-root user
- [ ] No secrets in `ENV` or image layers — use Docker secrets or env file (not committed)
- [ ] Image pinned to specific digest or version tag
- [ ] Healthcheck defined
- [ ] Ports bound to `127.0.0.1` if behind reverse proxy
- [ ] Resource limits set
- [ ] `.dockerignore` excludes sensitive files
- [ ] Image scanned (Trivy, Snyk, Docker Scout) before push

## Logging

Configure structured JSON logging and send to stdout/stderr — let the orchestrator handle log routing:
```
LOG_FORMAT=json
LOG_LEVEL=info
```
Never write logs to files inside the container.
