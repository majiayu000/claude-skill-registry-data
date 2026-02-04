---
name: go-docker
description: Docker containerization for Go applications
sasmp_version: "1.3.0"
bonded_agent: 08-go-devops
bond_type: PRIMARY_BOND
---

# Go Docker Skill

Containerize Go applications with production-ready Docker images.

## Overview

Best practices for Docker images including multi-stage builds, minimal base images, and security hardening.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| base_image | string | no | "distroless" | Base: "distroless", "alpine", "scratch" |
| platforms | list | no | ["linux/amd64"] | Target platforms |

## Core Topics

### Production Dockerfile
```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download && go mod verify

# Build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w -X main.version=${VERSION}" \
    -trimpath -o /app/server ./cmd/api

# Final stage - distroless for security
FROM gcr.io/distroless/static:nonroot

COPY --from=builder /app/server /server
COPY --from=builder /app/configs /configs

USER nonroot:nonroot
EXPOSE 8080 9090

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD ["/server", "health"]

ENTRYPOINT ["/server"]
```

### Alpine Variant (when shell needed)
```dockerfile
FROM golang:1.22-alpine AS builder
RUN apk add --no-cache ca-certificates tzdata
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server ./cmd/api

FROM alpine:3.19
RUN apk --no-cache add ca-certificates tzdata && \
    adduser -D -u 1000 appuser
COPY --from=builder /app/server /server
USER appuser
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        VERSION: ${VERSION:-dev}
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:8080/healthz"]
      interval: 10s
      timeout: 5s
      retries: 3

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Multi-Platform Build
```bash
# Setup buildx
docker buildx create --name multiplatform --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag myapp:latest \
  --push .
```

### Security Scanning
```bash
# Scan with Trivy
trivy image myapp:latest

# Scan with Docker Scout
docker scout cves myapp:latest
```

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Binary not found | Wrong GOOS/GOARCH | Match target platform |
| Permission denied | Root user required | Check file permissions |
| Large image size | No multi-stage | Use distroless/scratch |

### Debug Commands
```bash
docker build --progress=plain .
docker run --rm -it myapp:latest sh
docker history myapp:latest
```

## Usage

```
Skill("go-docker")
```
