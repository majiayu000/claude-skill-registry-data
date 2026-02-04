---
name: dockerfile-builder
description: Generate optimized, production-ready Dockerfiles with multi-stage builds, security best practices, and proper layer caching for various application types. Triggers on "create Dockerfile", "generate Dockerfile for", "docker image for", "containerize my app".
---

# Dockerfile Builder

Generate optimized, secure, production-ready Dockerfiles with multi-stage builds and best practices.

## Output Requirements

**File Output:** `Dockerfile` (no extension)
**Format:** Valid Dockerfile syntax
**Standards:** OCI compliant, BuildKit compatible

## When Invoked

Immediately generate a complete, production-ready Dockerfile. Default to multi-stage builds for compiled languages.

## Dockerfile Best Practices

### Layer Optimization
- Order instructions from least to most frequently changing
- Combine related RUN commands with `&&`
- Use `.dockerignore` to exclude unnecessary files
- Leverage BuildKit cache mounts where appropriate

### Security
- Use specific version tags, never `latest`
- Run as non-root user
- Use minimal base images (alpine, distroless, slim)
- Don't include secrets in image layers
- Scan for vulnerabilities

### Structure
```dockerfile
# Build stage(s)
FROM base AS builder
# ... build steps

# Production stage
FROM minimal-base AS production
# ... copy artifacts and run
```

## Application Templates

### Node.js Application
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production

# Security: run as non-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

WORKDIR /app

# Copy built assets
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./

USER nextjs

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "dist/index.js"]
```

### Python Application
```dockerfile
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim AS production

# Security: create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Go Application
```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Install dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source
COPY . .

# Build binary
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server ./cmd/server

# Production stage - distroless for minimal attack surface
FROM gcr.io/distroless/static-debian12 AS production

COPY --from=builder /app/server /server

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/server"]
```

### React/Frontend Application
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage - nginx
FROM nginx:alpine AS production

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Security headers and non-root
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Java/Spring Boot Application
```dockerfile
# Build stage
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

# Copy gradle files
COPY gradle gradle
COPY gradlew build.gradle.kts settings.gradle.kts ./
RUN chmod +x gradlew

# Download dependencies
RUN ./gradlew dependencies --no-daemon

# Copy source and build
COPY src src
RUN ./gradlew bootJar --no-daemon

# Production stage
FROM eclipse-temurin:21-jre-alpine AS production

# Security
RUN addgroup -S spring && adduser -S spring -G spring

WORKDIR /app

# Copy JAR
COPY --from=builder /app/build/libs/*.jar app.jar

RUN chown -R spring:spring /app

USER spring

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Rust Application
```dockerfile
# Build stage
FROM rust:1.75-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /app

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release && rm -rf src

# Build actual application
COPY src src
RUN touch src/main.rs && cargo build --release

# Production stage
FROM alpine:3.19 AS production

RUN apk add --no-cache ca-certificates

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app/target/release/myapp /usr/local/bin/

USER appuser

EXPOSE 8080

CMD ["myapp"]
```

## Common Patterns

### Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1
```

### Build Arguments
```dockerfile
ARG NODE_VERSION=20
ARG APP_VERSION=1.0.0

FROM node:${NODE_VERSION}-alpine AS builder

LABEL version="${APP_VERSION}"
```

### Cache Mounts (BuildKit)
```dockerfile
# syntax=docker/dockerfile:1.4

RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production
```

### Secrets (BuildKit)
```dockerfile
# syntax=docker/dockerfile:1.4

RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci
```

## .dockerignore Template

Always create alongside Dockerfile:
```
# Dependencies
node_modules
vendor
__pycache__
*.pyc
target

# Build outputs
dist
build
*.egg-info

# Git
.git
.gitignore

# IDE
.idea
.vscode
*.swp

# Docker
Dockerfile*
docker-compose*
.docker

# Environment
.env
.env.*
*.local

# Tests
coverage
.coverage
htmlcov
.pytest_cache
.nyc_output

# Misc
*.log
*.md
LICENSE
README*
```

## Validation Checklist

Before outputting, verify:
- [ ] Uses specific base image tags (not `latest`)
- [ ] Multi-stage build for compiled languages
- [ ] Non-root user for production
- [ ] Dependencies cached properly (COPY package files before source)
- [ ] No secrets in image layers
- [ ] EXPOSE matches application port
- [ ] Appropriate CMD/ENTRYPOINT format

## Example Invocations

**Prompt:** "Create Dockerfile for a Node.js Express API"
**Output:** Complete multi-stage `Dockerfile` with npm caching, non-root user, health check.

**Prompt:** "Dockerfile for Python FastAPI with poetry"
**Output:** Complete `Dockerfile` using poetry for dependencies, gunicorn/uvicorn, security hardened.

**Prompt:** "Generate Dockerfile for Go microservice"
**Output:** Complete `Dockerfile` with static binary build, distroless production image.
