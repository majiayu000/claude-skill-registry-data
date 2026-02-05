---
name: app-docker-deploy-with-traefik
description: >
  Generate Docker and Traefik deployment configurations for any application
  (Node.js, Python, Go, Rust, Java). Creates Dockerfile, docker-compose.yml,
  docker-compose.for-traefik.yml overlay, and .env.sample with production best
  practices. Use when: dockerize app, containerize, add Docker, deploy with
  Traefik, reverse proxy setup, HTTPS/SSL, Let's Encrypt certificates,
  production deployment, docker-compose setup. Requires: Docker, docker-compose.
---

# Docker + Traefik Deployment Setup

Generate production-ready Docker deployment configurations with Traefik reverse proxy integration, automatic HTTPS via Let's Encrypt.

## Overview

This skill creates a deployment configuration following a proven pattern:

1. **Dockerfile** - Multi-stage build for the application
2. **docker-compose.yml** - Base service definitions
3. **docker-compose.for-traefik.yml** - Traefik routing overlay (composable)
4. **.env.sample** - Environment variable template

## Instructions

### Step 1: Analyze the Project

Before generating configurations, understand the project:

1. **Detect the project type** by examining:
   - `package.json` → Node.js/TypeScript
   - `requirements.txt` / `pyproject.toml` / `Pipfile` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pom.xml` / `build.gradle` → Java

2. **Identify the application port** from:
   - Start scripts in package.json
   - Application configuration files
   - Common defaults (3000 for Node, 8000 for Python, 8080 for Go/Java)

3. **Check for existing Docker files** - Don't overwrite without asking

### Step 2: Generate Dockerfile

Create a multi-stage Dockerfile appropriate for the project type. See [DOCKERFILES.md](DOCKERFILES.md) for templates.

Key principles:

- Use official base images with specific version tags (not `:latest`)
- Multi-stage builds to minimize final image size
- Non-root user for security
- Proper layer caching (dependencies before source code)
- Health checks when appropriate

### Step 3: Generate docker-compose.yml

Base configuration with:

- Service definitions for app and dependencies (db, redis, etc.)
- Volume mounts for persistent data (`./data/<service>:/path`)
- Environment variable references (`${VARIABLE}`)
- Restart policy: `unless-stopped`
- Health checks where appropriate
- Watchtower labels for auto-updates (optional)

```yaml
services:
  app:
    build: .
    restart: unless-stopped
    volumes:
      - ./data/app:/app/data
    environment:
      - NODE_ENV=${NODE_ENV}
      - PORT=${PORT}
    depends_on:
      - db
    labels:
      - 'com.centurylinklabs.watchtower.enable=true'
      - 'com.centurylinklabs.watchtower.scope=${WATCHTOWER_SCOPE}'

  db:
    image: postgres:17-alpine
    restart: unless-stopped
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    healthcheck:
      test: pg_isready -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"
      interval: 10s
      timeout: 2s
      retries: 10
```

### Step 4: Generate docker-compose.for-traefik.yml

Traefik overlay that can be composed with the base file:

```yaml
services:
  app:
    networks:
      - default
      - traefik
    labels:
      - 'traefik.enable=true'
      - 'traefik.docker.network=traefik'
      # Service (internal port)
      - 'traefik.http.services.${SERVICE_NAME}.loadbalancer.server.port=${PORT}'
      # HTTPS Router
      - 'traefik.http.routers.${SERVICE_NAME}.rule=Host(`${DOMAIN}`)'
      - 'traefik.http.routers.${SERVICE_NAME}.entrypoints=websecure'
      - 'traefik.http.routers.${SERVICE_NAME}.tls=true'
      - 'traefik.http.routers.${SERVICE_NAME}.tls.certResolver=webcert'
      - 'traefik.http.routers.${SERVICE_NAME}.service=${SERVICE_NAME}'

  db:
    networks:
      - default

networks:
  traefik:
    external: true
```

### Step 5: Generate .env.sample

Template for required environment variables:

```bash
# Domain and Deployment
DOMAIN=myapp.example.com
PORT=3000

# Database
POSTGRES_DB=myapp
POSTGRES_USER=myapp
POSTGRES_PASSWORD=change-me-in-production

# Application
NODE_ENV=production

# Auto-updates (optional)
WATCHTOWER_SCOPE=myapp
```

### Step 6: Provide Usage Instructions

Include in the output:

1. How to copy and configure .env
2. How to run without Traefik (development)
3. How to run with Traefik (production)
4. Prerequisites (external traefik network)

## Usage Commands

```bash
# Development (without Traefik)
docker compose up -d

# Production (with Traefik)
docker compose -f docker-compose.yml -f docker-compose.for-traefik.yml up -d

# Create external traefik network (first time only)
docker network create traefik
```

## Traefik Label Reference

| Label                                                      | Purpose                                   |
| ---------------------------------------------------------- | ----------------------------------------- |
| `traefik.enable=true`                                      | Enable Traefik routing for this container |
| `traefik.docker.network=traefik`                           | Specify which network Traefik should use  |
| `traefik.http.services.NAME.loadbalancer.server.port=PORT` | Container's internal port                 |
| `traefik.http.routers.NAME.rule=Host(\`domain\`)`          | Domain routing rule                       |
| `traefik.http.routers.NAME.entrypoints=websecure`          | Use HTTPS entrypoint                      |
| `traefik.http.routers.NAME.tls=true`                       | Enable TLS                                |
| `traefik.http.routers.NAME.tls.certResolver=webcert`       | Use Let's Encrypt                         |
| `traefik.http.routers.NAME.service=NAME`                   | Link router to service                    |

## Optional: Basic Auth Middleware

For admin panels or protected routes:

```yaml
labels:
  # Define middleware
  - 'traefik.http.middlewares.myapp-auth.basicauth.users=${USERNAME}:${HASHED_PASSWORD}'
  # Apply to router
  - 'traefik.http.routers.myapp.middlewares=myapp-auth@docker'
```

Generate password hash: `htpasswd -nb username password`

## Optional: Multiple Domains/Subdomains

```yaml
# API subdomain
- 'traefik.http.routers.myapp-api.rule=Host(`api.${DOMAIN}`)'
- 'traefik.http.routers.myapp-api.entrypoints=websecure'
- 'traefik.http.routers.myapp-api.tls=true'
- 'traefik.http.routers.myapp-api.tls.certResolver=webcert'
- 'traefik.http.routers.myapp-api.service=myapp'
```

## Best Practices

1. **Use specific image tags** - Never use `:latest` in production
2. **External database volumes** - Persist data outside containers
3. **Secrets management** - Use Docker secrets for production passwords
4. **Health checks** - Enable for proper orchestration
5. **Resource limits** - Add memory/CPU limits in production
6. **Logging** - Configure appropriate log drivers
7. **Non-root users** - Run containers as non-root when possible

## Helper Scripts

Located in the `scripts/` directory:

### generate-htpasswd.sh

Generate password hashes for Traefik basic auth:

```bash
./scripts/generate-htpasswd.sh admin mypassword
```

### validate-compose.py

Validate docker-compose files for common issues:

```bash
python scripts/validate-compose.py docker-compose.yml docker-compose.for-traefik.yml
```

Requires: `pip install pyyaml`

### check-network.sh

Check if the traefik network exists (and optionally create it):

```bash
./scripts/check-network.sh          # Check only
./scripts/check-network.sh --create # Create if missing
```

## Template Files

Located in the `templates/` directory. Copy and customize:

| Template                         | Description                        |
| -------------------------------- | ---------------------------------- |
| `Dockerfile.node`                | Node.js multi-stage build          |
| `Dockerfile.python`              | Python with uv package manager     |
| `docker-compose.yml`             | Base compose with app + PostgreSQL |
| `docker-compose.for-traefik.yml` | Traefik routing overlay            |
| `.dockerignore`                  | Optimized Docker build context     |
| `.env.sample`                    | Environment variables template     |

Replace placeholders: `{{SERVICE_NAME}}`, `{{PORT}}`, `{{NODE_VERSION}}`, etc.

## Additional Resources

- [DOCKERFILES.md](DOCKERFILES.md) - Complete Dockerfile templates for all languages
- [EXAMPLES.md](EXAMPLES.md) - Real-world deployment examples

## Requirements

- **Docker** >= 20.10
- **Docker Compose** >= 2.0 (V2 syntax)
- **Traefik** >= 2.0 (running with `webcert` certificate resolver)
- External `traefik` network: `docker network create traefik`
