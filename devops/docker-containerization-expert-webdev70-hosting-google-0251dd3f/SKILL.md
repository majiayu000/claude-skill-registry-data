---
name: docker-containerization-expert
description: Expert knowledge of Docker containerization including Dockerfile best practices, docker-compose configuration, Alpine Linux specifics, multi-stage builds, security, health checks, and container optimization. Use when working with Dockerfile, docker-compose.yml, container builds, debugging container issues, or deploying to container platforms.
---

# Docker Containerization Expert

This skill provides comprehensive expert knowledge of Docker containerization for Node.js applications, with emphasis on production-ready configurations, security best practices, and cloud platform deployment.

## Dockerfile Best Practices

### Multi-Stage Builds

**Purpose**: Reduce final image size by separating build dependencies from runtime dependencies.

**Basic Pattern**:
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

**Advanced Pattern with Build Dependencies**:
```dockerfile
# Build stage with dev dependencies
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
USER node
CMD ["node", "dist/server.js"]
```

### Layer Caching Optimization

**Order matters**: Place commands that change least frequently at the top.

```dockerfile
# Good - dependencies cached separately from code
FROM node:18-alpine
WORKDIR /app

# Copy package files first (changes infrequently)
COPY package*.json ./
RUN npm ci --only=production

# Copy application code (changes frequently)
COPY . .

# This ordering means code changes don't invalidate npm install cache
```

**Bad ordering**:
```dockerfile
# Bad - code changes invalidate entire cache
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm ci --only=production
```

### Alpine Linux Specifics

**Why Alpine**: Minimal footprint (~5MB base vs ~100MB+ for full images)

**Base Image Selection**:
```dockerfile
# Recommended for Node.js apps
FROM node:18-alpine

# For specific Alpine version
FROM node:18-alpine3.19

# For LTS versions
FROM node:20-alpine
```

**Package Management in Alpine**:
```dockerfile
# Use apk (not apt-get)
RUN apk add --no-cache \
    python3 \
    make \
    g++
```

**Common Alpine Issues**:

**Missing native dependencies**:
```dockerfile
# If you need native modules (bcrypt, sharp, etc.)
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    libc6-compat
```

**Missing shell utilities**:
```dockerfile
# Alpine uses ash shell, not bash
# For bash compatibility
RUN apk add --no-cache bash

# Or use ash-compatible syntax in scripts
```

**Missing timezone data**:
```dockerfile
# Add timezone support
RUN apk add --no-cache tzdata
ENV TZ=America/New_York
```

### Security Best Practices

#### Non-Root User

**Why**: Limit damage if container is compromised.

**Pattern 1: Use built-in node user**:
```dockerfile
FROM node:18-alpine
WORKDIR /app

# Install dependencies as root
COPY package*.json ./
RUN npm ci --only=production

# Copy application files
COPY . .

# Change ownership to node user
RUN chown -R node:node /app

# Switch to non-root user
USER node

EXPOSE 3000
CMD ["node", "server.js"]
```

**Pattern 2: Create custom user**:
```dockerfile
FROM node:18-alpine

# Create app user and group
RUN addgroup -g 1001 -S appuser && \
    adduser -S -u 1001 -G appuser appuser

WORKDIR /app
COPY --chown=appuser:appuser package*.json ./
RUN npm ci --only=production

COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 3000
CMD ["node", "server.js"]
```

#### Minimal Image Content

**Use .dockerignore**:
```
node_modules
npm-debug.log
.git
.gitignore
.env
.env.*
!.env.example
.vscode
.idea
.DS_Store
Thumbs.db
*.md
!README.md
docs/
tests/
__tests__/
coverage/
.github/
Dockerfile
docker-compose.yml
.dockerignore
```

**Benefits**:
- Faster builds (less context to send)
- Smaller images
- Prevents accidentally copying secrets

#### Read-Only Filesystem

```dockerfile
# Make filesystem read-only (advanced)
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Create temp directory with write permissions
RUN mkdir -p /tmp/app-cache && \
    chown node:node /tmp/app-cache

USER node
EXPOSE 3000

# Run with read-only root filesystem
# (requires docker run --read-only --tmpfs /tmp/app-cache)
CMD ["node", "server.js"]
```

### npm Install Optimization

**Use npm ci instead of npm install**:
```dockerfile
# Good - deterministic, faster, requires package-lock.json
RUN npm ci --only=production

# Bad - slower, may have version drift
RUN npm install --production
```

**Cache npm packages**:
```dockerfile
# Use BuildKit cache mounts (requires Docker BuildKit)
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production
```

**Clean npm cache**:
```dockerfile
RUN npm ci --only=production && \
    npm cache clean --force
```

### EXPOSE and CMD/ENTRYPOINT

**EXPOSE**: Documents port, doesn't publish it
```dockerfile
EXPOSE 3000
# Actual port binding happens at runtime: docker run -p 3000:3000
```

**CMD vs ENTRYPOINT**:

**CMD (recommended for apps)**:
```dockerfile
# Can be overridden at runtime
CMD ["node", "server.js"]

# Docker run: docker run myimage
# Override: docker run myimage node debug.js
```

**ENTRYPOINT (for tools/scripts)**:
```dockerfile
# Always runs, arguments appended
ENTRYPOINT ["node"]
CMD ["server.js"]

# Docker run: docker run myimage
# With args: docker run myimage debug.js
```

**Combined pattern**:
```dockerfile
ENTRYPOINT ["node"]
CMD ["server.js"]
# Default: node server.js
# Override: docker run myimage debug.js → node debug.js
```

### Environment Variables

**Build-time (ARG)**:
```dockerfile
ARG NODE_VERSION=18
FROM node:${NODE_VERSION}-alpine

ARG BUILD_DATE
LABEL build.date=${BUILD_DATE}
```

**Runtime (ENV)**:
```dockerfile
ENV NODE_ENV=production
ENV PORT=3000

# Reference in CMD
CMD ["sh", "-c", "node server.js"]
```

**Best practice - don't set sensitive defaults**:
```dockerfile
# Good - require at runtime
# (set via docker-compose.yml or docker run -e)

# Bad - hardcoded secrets
ENV API_KEY=secret123  # NEVER DO THIS
```

## docker-compose.yml Configuration

### Basic Service Definition

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: my-app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
    restart: unless-stopped
```

### Health Checks

**Purpose**: Allow orchestration platforms to detect if container is actually working.

**HTTP health check**:
```yaml
services:
  app:
    build: .
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
```

**Alternative using curl**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**TCP check (if no HTTP endpoint)**:
```yaml
healthcheck:
  test: ["CMD-SHELL", "nc -z localhost 3000 || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
```

**Node.js script health check**:
```yaml
healthcheck:
  test: ["CMD", "node", "healthcheck.js"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Restart Policies

```yaml
services:
  app:
    # Never restart automatically
    restart: "no"

    # Always restart (even after system reboot)
    restart: always

    # Restart on failure only
    restart: on-failure

    # Restart unless explicitly stopped (recommended)
    restart: unless-stopped
```

### Volumes and Bind Mounts

**Named volumes (persist data)**:
```yaml
services:
  app:
    volumes:
      - app-data:/app/data
      - logs:/var/log

volumes:
  app-data:
  logs:
```

**Bind mounts (development)**:
```yaml
services:
  app:
    volumes:
      # Mount current directory into container
      - .:/app
      # Exclude node_modules
      - /app/node_modules
```

**Read-only mounts**:
```yaml
volumes:
  - ./config:/app/config:ro  # Read-only
```

### Environment Variables

**Inline**:
```yaml
services:
  app:
    environment:
      - NODE_ENV=production
      - PORT=3000
      - DEBUG=app:*
```

**From .env file**:
```yaml
services:
  app:
    env_file:
      - .env
      - .env.production
```

**Variable substitution**:
```yaml
services:
  app:
    image: myapp:${TAG:-latest}
    ports:
      - "${HOST_PORT:-3000}:3000"
```

### Networks

**Default network**:
```yaml
# All services can communicate via service names
services:
  app:
    # Can connect to: http://db:5432
  db:
    # Can connect to: http://app:3000
```

**Custom networks**:
```yaml
services:
  app:
    networks:
      - frontend
      - backend

  nginx:
    networks:
      - frontend

  db:
    networks:
      - backend

networks:
  frontend:
  backend:
```

### Dependencies

**depends_on (start order only)**:
```yaml
services:
  app:
    depends_on:
      - db
    # Starts after db, but doesn't wait for db to be ready

  db:
    image: postgres:15-alpine
```

**Wait for service to be ready**:
```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Logging

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Container Security

### Image Scanning

**Scan for vulnerabilities**:
```bash
# Using Docker Scout
docker scout cves myimage:latest

# Using Trivy
trivy image myimage:latest

# Using Snyk
snyk container test myimage:latest
```

**In Dockerfile**:
```dockerfile
# Use specific, patched versions
FROM node:18.19.0-alpine3.19

# Not latest (unpredictable)
FROM node:alpine
```

### Security Best Practices Checklist

- [ ] Use specific image versions, not `latest`
- [ ] Run as non-root user
- [ ] Use Alpine or distroless base images
- [ ] Scan images for vulnerabilities
- [ ] Use multi-stage builds to minimize attack surface
- [ ] Don't include secrets in image
- [ ] Use `.dockerignore` to exclude unnecessary files
- [ ] Set resource limits
- [ ] Implement health checks
- [ ] Use read-only root filesystem where possible
- [ ] Minimize installed packages
- [ ] Keep base images updated

### Runtime Security

**Run with security options**:
```bash
docker run \
  --read-only \
  --tmpfs /tmp \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  myimage
```

**In docker-compose.yml**:
```yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

## Container Registry

### Google Container Registry (GCR) - Legacy

**Push to GCR**:
```bash
docker tag myapp gcr.io/PROJECT_ID/myapp:latest
docker push gcr.io/PROJECT_ID/myapp:latest
```

**Dockerfile reference**:
```dockerfile
FROM gcr.io/PROJECT_ID/base-image:v1.0
```

### Google Artifact Registry (Modern)

**Push to Artifact Registry**:
```bash
# Configure Docker auth
gcloud auth configure-docker us-central1-docker.pkg.dev

# Tag and push
docker tag myapp us-central1-docker.pkg.dev/PROJECT_ID/my-repo/myapp:v1.0
docker push us-central1-docker.pkg.dev/PROJECT_ID/my-repo/myapp:v1.0
```

**Multi-region replication**:
```bash
# Create multi-region repository
gcloud artifacts repositories create my-repo \
  --repository-format=docker \
  --location=us \
  --description="Multi-region Docker repository"
```

### Docker Hub

**Push to Docker Hub**:
```bash
docker login
docker tag myapp username/myapp:v1.0
docker push username/myapp:v1.0
```

### Private Registry

**Authenticate**:
```bash
docker login registry.example.com
```

**Push**:
```bash
docker tag myapp registry.example.com/myapp:v1.0
docker push registry.example.com/myapp:v1.0
```

## Cloud Platform Deployment

### Google Cloud Run

**PORT environment variable**:
```dockerfile
# Cloud Run sets PORT dynamically (usually 8080)
# Application MUST read from process.env.PORT
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Don't hardcode port
EXPOSE 8080
USER node

# Application reads PORT from environment
CMD ["node", "server.js"]
```

**Deployment**:
```bash
# Build and push
docker build -t gcr.io/PROJECT_ID/myapp .
docker push gcr.io/PROJECT_ID/myapp

# Deploy to Cloud Run
gcloud run deploy myapp \
  --image gcr.io/PROJECT_ID/myapp \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

### Google Kubernetes Engine (GKE)

**Deployment manifest**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: gcr.io/PROJECT_ID/myapp:v1.0
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: production
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### AWS Elastic Container Service (ECS)

**Task definition**:
```json
{
  "family": "myapp",
  "containerDefinitions": [
    {
      "name": "myapp",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "NODE_ENV", "value": "production"},
        {"name": "PORT", "value": "3000"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/myapp",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "256",
  "memory": "512"
}
```

## Debugging and Troubleshooting

### Common Issues

#### Container Exits Immediately

**Check logs**:
```bash
docker logs container_name
docker logs --tail 50 container_name
docker logs --follow container_name
```

**Common causes**:
- CMD/ENTRYPOINT incorrect
- Application crashes on startup
- Missing environment variables
- File permissions

#### Port Not Accessible

**Verify port binding**:
```bash
docker ps
# Look for PORT column: 0.0.0.0:3000->3000/tcp

docker port container_name
```

**Test from inside container**:
```bash
docker exec container_name wget -O- http://localhost:3000
```

#### Permission Denied Errors

**Check file ownership**:
```bash
docker exec container_name ls -la /app
```

**Fix in Dockerfile**:
```dockerfile
COPY --chown=node:node . .
# Or
RUN chown -R node:node /app
```

#### Health Check Failing

**Check health status**:
```bash
docker ps
# Look for STATUS column: healthy/unhealthy

docker inspect container_name | grep -A 10 Health
```

**Debug health check**:
```bash
# Run health check command manually
docker exec container_name wget --quiet --tries=1 --spider http://localhost:3000
```

#### Out of Memory

**Check memory usage**:
```bash
docker stats container_name
```

**Increase memory**:
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 1G
```

### Interactive Debugging

**Shell into running container**:
```bash
# Alpine (uses ash shell)
docker exec -it container_name sh

# If bash installed
docker exec -it container_name bash
```

**Run one-off commands**:
```bash
docker exec container_name node -v
docker exec container_name npm list
docker exec container_name cat /app/package.json
```

**Inspect environment variables**:
```bash
docker exec container_name env
docker exec container_name printenv PORT
```

### Build Debugging

**Build with no cache**:
```bash
docker build --no-cache -t myapp .
```

**Build specific stage**:
```bash
docker build --target builder -t myapp-builder .
```

**View build history**:
```bash
docker history myapp
```

**Check image size**:
```bash
docker images myapp
```

## Performance Optimization

### Image Size Reduction

**Before optimization**:
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
# Result: ~1GB
```

**After optimization**:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
USER node
CMD ["node", "server.js"]
# Result: ~150MB
```

### Build Speed Optimization

**Use BuildKit**:
```bash
DOCKER_BUILDKIT=1 docker build -t myapp .
```

**Cache mounts**:
```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production
```

**Parallel builds**:
```bash
docker compose build --parallel
```

### Runtime Performance

**Health check interval tuning**:
```yaml
healthcheck:
  interval: 60s  # Less frequent checks
  timeout: 5s    # Shorter timeout
  retries: 2     # Fewer retries
```

**Resource allocation**:
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'      # More CPU
      memory: 1G       # More memory
```

## Best Practices Summary

### Dockerfile
1. Use Alpine-based images for smaller footprint
2. Implement multi-stage builds
3. Order layers from least to most frequently changing
4. Use `npm ci --only=production` not `npm install`
5. Run as non-root user
6. Use specific version tags, not `latest`
7. Leverage `.dockerignore`
8. Clean up after installs (npm cache, apt cache)

### docker-compose.yml
1. Define health checks for all services
2. Use `restart: unless-stopped` for resilience
3. Set resource limits
4. Use named volumes for persistent data
5. Implement proper networking
6. Never commit secrets (use env files)
7. Configure logging with rotation

### Security
1. Scan images regularly
2. Use minimal base images
3. Don't run as root
4. Keep images updated
5. Use read-only filesystems where possible
6. Implement least privilege
7. Never embed secrets in images

### Cloud Deployment
1. Read PORT from environment (Cloud Run requirement)
2. Implement health checks
3. Use managed container registries
4. Tag images with commit SHA or version
5. Set appropriate resource limits
6. Configure logging for observability

## Common Commands Reference

**Note**: Modern Docker uses `docker compose` (with space) instead of legacy `docker-compose` (with hyphen). Docker Compose V2 is integrated as a Docker CLI plugin.

```bash
# Build
docker build -t myapp .
docker build --no-cache -t myapp .
docker compose build
docker compose build --no-cache

# Run
docker run -p 3000:3000 myapp
docker run -d -p 3000:3000 --name myapp-container myapp
docker compose up
docker compose up -d

# Stop
docker stop container_name
docker compose down

# Logs
docker logs container_name
docker logs -f container_name
docker compose logs
docker compose logs -f app

# Shell access
docker exec -it container_name sh
docker compose exec app sh

# Inspect
docker ps
docker ps -a
docker inspect container_name
docker stats
docker compose ps

# Clean up
docker rm container_name
docker rmi image_name
docker system prune
docker volume prune

# Registry
docker tag myapp gcr.io/PROJECT_ID/myapp:v1.0
docker push gcr.io/PROJECT_ID/myapp:v1.0
docker pull gcr.io/PROJECT_ID/myapp:v1.0
```

## Resources

- Docker Documentation: https://docs.docker.com/
- Docker Compose Specification: https://docs.docker.com/compose/compose-file/
- Alpine Linux Packages: https://pkgs.alpinelinux.org/packages
- Node.js Docker Best Practices: https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md
- Google Cloud Run Documentation: https://cloud.google.com/run/docs
- Docker Security: https://docs.docker.com/engine/security/
