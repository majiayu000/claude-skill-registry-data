---
name: docker-setup
description: "Generates Dockerfile, docker-compose.yml, and .dockerignore for the project. Auto-detects the stack and creates optimized multi-stage builds with caching, health checks, and dev/prod configurations."
argument-hint: "[optional: 'dev', 'prod', or 'both']"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Docker Setup Generator

## Detect Stack
!`ls package.json requirements.txt pyproject.toml go.mod Cargo.toml *.csproj Gemfile composer.json mix.exs 2>/dev/null`
!`ls Dockerfile docker-compose* .dockerignore 2>/dev/null`
!`cat package.json 2>/dev/null | grep -E '"(main|scripts)"' -A 5 | head -10`

---

## Generation Process

### Step 1: Analyze Requirements
From project files, determine:
- Base image (node:20-alpine, python:3.12-slim, golang:1.22, rust:1.75, etc.)
- Build steps (install deps, compile, bundle)
- Runtime dependencies (only what's needed to run, not to build)
- Port(s) the application listens on
- Required services (database, cache, message queue)
- Environment variables needed

### Step 2: Generate Dockerfile

**Multi-stage build pattern:**
```dockerfile
# Stage 1: Dependencies
FROM base AS deps
COPY lock-file .
RUN install-command

# Stage 2: Build
FROM deps AS build
COPY source .
RUN build-command

# Stage 3: Production
FROM base-slim AS production
COPY --from=build /app/dist ./dist
CMD ["start-command"]
```

**Best practices to include:**
- Use specific image tags, not `latest`
- Use `.dockerignore` to minimize context
- Copy lock files before source (layer caching)
- Run as non-root user
- Set HEALTHCHECK
- Use multi-stage builds to minimize final image size
- Set appropriate EXPOSE port
- Use ENTRYPOINT + CMD pattern

### Step 3: Generate docker-compose.yml
```yaml
services:
  app:
    build: .
    ports: ["3000:3000"]
    environment: ...
    depends_on: ...
    volumes: ...  # for dev: mount source code
    healthcheck: ...

  # Add required services
  db:  # if database detected
  redis:  # if cache detected
```

**Include:**
- Development overrides (volume mounts, hot reload)
- Named volumes for persistent data
- Network configuration
- Health checks for all services
- Environment variable references (not hardcoded values)

### Step 4: Generate .dockerignore
```
node_modules/
.git/
dist/
build/
*.log
.env
.env.*
```

### Step 5: Document
Add comments explaining:
- Why each stage exists
- How to build: `docker build -t app .`
- How to run: `docker compose up`
- How to access: `http://localhost:PORT`
- How to run tests in Docker

## Rules
- Never hardcode secrets in Dockerfile or docker-compose
- Always use non-root user in production images
- Always include health checks
- Minimize image size (alpine/slim base, multi-stage)
- Include .dockerignore to speed up builds
