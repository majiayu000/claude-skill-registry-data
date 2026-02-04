---
name: docker-init
description: Initialize Docker environment with Dockerfile, compose config, and .dockerignore
---

# Docker Environment Initialization Skill

## Overview

This skill creates a complete Docker environment for a project, including:
- Dockerfile optimized for the application type
- docker-compose.yaml with all required services
- .dockerignore for efficient builds
- .env.example for environment configuration

## Activation

Use this skill when:
- Setting up Docker for a new project
- Migrating an existing project to Docker
- Adding Docker support to a codebase

## Process

### 1. Detect Project Type

Analyze the project to determine:
- Primary language (Node.js, Python, PHP, Go, etc.)
- Framework (Laravel, Express, Django, etc.)
- Required services (database, cache, queue)
- Existing configuration files

### 2. Consult Documentation

Read relevant documentation:
- `02-dockerfile.md` for Dockerfile patterns
- `03-compose-fundamentals.md` for compose structure
- `05-databases.md` if database needed
- `10-architecture.md` for folder structure

### 3. Generate Files

#### Dockerfile

```dockerfile
# Multi-stage build pattern
FROM base AS builder
# Build steps

FROM base AS production
# Production setup
```

Key elements:
- Use appropriate base image
- Multi-stage build for smaller images
- Non-root user for security
- Health check
- Proper COPY order for caching

#### docker-compose.yaml

```yaml
services:
  app:
    build: .
    # Configuration

  db:
    image: postgres:16
    # Configuration

volumes:
  # Named volumes

networks:
  # Network configuration
```

Key elements:
- No version field (modern compose)
- Health checks
- Dependencies with conditions
- Named volumes
- Proper networking

#### .dockerignore

```
node_modules/
.git/
.env
*.log
```

#### .env.example

```bash
# Application
NODE_ENV=development
PORT=3000

# Database
DB_HOST=db
DB_USER=appuser
DB_PASSWORD=
```

### 4. Provide Instructions

Include:
- How to start services
- Available commands
- Environment setup
- Development workflow

## Templates by Project Type

### Node.js

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
USER node
EXPOSE 3000
CMD ["node", "src/index.js"]
```

### Python

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER nobody
EXPOSE 8000
CMD ["python", "app.py"]
```

### PHP/Laravel

```dockerfile
FROM php:8.3-fpm-alpine
WORKDIR /var/www/html
RUN apk add --no-cache postgresql-dev && \
    docker-php-ext-install pdo pdo_pgsql
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer
COPY . .
RUN composer install --no-dev --optimize-autoloader
EXPOSE 9000
CMD ["php-fpm"]
```

### Go

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o main .

FROM alpine:latest
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

## Output

Generated files:
- `Dockerfile`
- `docker-compose.yaml` (or `compose.yaml`)
- `.dockerignore`
- `.env.example`
- `docker/` folder for additional configs (if needed)
