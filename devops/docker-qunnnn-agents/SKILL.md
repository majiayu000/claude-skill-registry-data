---
tags: [devops, docker, containerization, deployment]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Docker & Containerization

## Context

Apply when containerizing applications or setting up Docker-based development/deployment environments.

## Instructions

1. **Multi-stage builds**: Always use multi-stage Dockerfiles to minimize image size.
2. **Base images**: Use specific version tags (not `latest`).
3. **Layer ordering**: Order Dockerfile instructions from least to most frequently changed for better caching.
4. **Security**:
   - Run as non-root user
   - Don't copy `.env` files into images
   - Use `.dockerignore`
5. **docker-compose**: Use for local development with all service dependencies.
6. **Health checks**: Add health check endpoints and Docker `HEALTHCHECK` directives.

## Examples

### Multi-stage Go Dockerfile

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server ./cmd/api

# Runtime stage
FROM alpine:3.19
RUN adduser -D -g '' appuser
COPY --from=builder /app/server /usr/local/bin/server
USER appuser
EXPOSE 8080
CMD ["server"]
```

### docker-compose.yml

```yaml
services:
  api:
    build: .
    ports:
      - "8080:8080"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
```

## Anti-patterns

- ❌ Using `latest` tags in production
- ❌ Running as root in containers
- ❌ Copying entire project without `.dockerignore`
- ❌ Single-stage builds for compiled languages
