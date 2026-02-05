---
name: dokploy-compose-structure
description: "Generate Docker Compose files following Dokploy conventions with proper networking, volumes, and service patterns. Use when creating new Dokploy templates or converting existing compose files."
version: 1.0.0
author: Home Lab Infrastructure Team
---

# Dokploy Compose Structure

## When to Use This Skill

- When creating a new Dokploy template from scratch
- When converting an existing docker-compose to Dokploy format
- When adding new services to existing Dokploy templates
- When user asks to "create a dokploy template for [application]"
- When user asks about "dokploy compose patterns"

## When NOT to Use This Skill

- For Kubernetes manifests (use kubernetes patterns instead)
- For standalone Docker deployments without Dokploy
- For modifying existing working templates without understanding context (use dokploy-template-validation first)

## Prerequisites

- Application name and version to deploy
- Required services (database, cache, etc.)
- Port mappings needed for external access
- Storage requirements (persistent volumes)

---

## Core Patterns

### Pattern 1: Network Structure (MANDATORY)

Every Dokploy template MUST have exactly two networks:

```yaml
networks:
  ${app-name}-net:
    driver: bridge
  dokploy-network:
    external: true
```

**Rules:**
- `${app-name}-net`: Internal app communication (bridge driver)
- `dokploy-network`: External network for Traefik routing (ALWAYS external: true)
- Web-facing services connect to BOTH networks
- Internal-only services (databases) connect ONLY to app-net

### Pattern 2: Service Definition Template

```yaml
services:
  ${service-name}:
    image: ${image}:${version}  # ALWAYS pin version, NEVER use :latest
    restart: always             # ALWAYS set restart policy
    depends_on:
      ${dependency}:
        condition: service_healthy  # Use health-based dependencies
    volumes:
      - ${volume-name}:/path/in/container
    environment:
      REQUIRED_VAR: ${REQUIRED_VAR:?Set description here}
      OPTIONAL_VAR: ${OPTIONAL_VAR:-default_value}
    networks:
      - ${app-name}-net
      - dokploy-network  # ONLY for web-facing services
    labels:
      - "traefik.enable=true"
      # ... additional traefik labels
    healthcheck:
      test: ["CMD", "command"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

### Pattern 3: Volume Definition

```yaml
volumes:
  ${service-name}-data:
    driver: local
```

**Rules:**
- ALWAYS use named volumes (never bind mounts)
- Naming convention: `${service-name}-${type}` (e.g., `mongodb-data`, `postgres-data`)
- Use `driver: local` for standard storage

### Pattern 4: Image Version Pinning

```yaml
# CORRECT - Pinned versions
image: postgres:16-alpine
image: mongo:7
image: redis:7-alpine
image: wardpearce/paaster:3.1.7

# WRONG - Never use these
image: postgres:latest
image: mongo
image: myapp  # implies :latest
```

---

## Complete Examples

### Example 1: Simple Web Application (1 service)

**Context**: Single container app like AnonUpload

```yaml
services:
  anonupload:
    image: supernero/anonupload:latest-1.0.3
    restart: always
    volumes:
      - anonupload-data:/var/www/html/files
    environment:
      UPLOAD_MAX_SIZE: ${UPLOAD_MAX_SIZE:-1024}
      DELETE_FILES_OLDER_THAN: ${DELETE_FILES_OLDER_THAN:-30}
    networks:
      - anonupload-net
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.anonupload.rule=Host(`${ANONUPLOAD_DOMAIN}`)"
      - "traefik.http.routers.anonupload.entrypoints=websecure"
      - "traefik.http.routers.anonupload.tls.certresolver=letsencrypt"
      - "traefik.http.services.anonupload.loadbalancer.server.port=80"
      - "traefik.docker.network=dokploy-network"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

volumes:
  anonupload-data:
    driver: local

networks:
  anonupload-net:
    driver: bridge
  dokploy-network:
    external: true
```

### Example 2: Web App with Database (2 services)

**Context**: Paaster with MongoDB (from actual template)

```yaml
services:
  paaster:
    image: wardpearce/paaster:3.1.7
    restart: always
    depends_on:
      mongodb:
        condition: service_healthy
    environment:
      PAASTER_DOMAIN: ${PAASTER_DOMAIN:?Set your domain}
      COOKIE_SECRET: ${COOKIE_SECRET:?Set a secure random cookie secret}
      MONGO_DB: ${MONGO_DB:-paasterv3}
      MONGO_URL: mongodb://mongodb:27017/${MONGO_DB:-paasterv3}
      # S3 storage (Cloudflare R2)
      S3_ENDPOINT: ${S3_ENDPOINT:?Set Cloudflare R2 endpoint}
      S3_REGION: ${S3_REGION:-auto}
      S3_ACCESS_KEY_ID: ${S3_ACCESS_KEY_ID:?Set R2 access key ID}
      S3_SECRET_ACCESS_KEY: ${S3_SECRET_ACCESS_KEY:?Set R2 secret access key}
      S3_BUCKET: ${S3_BUCKET:?Set R2 bucket name}
      S3_FORCE_PATH_STYLE: "false"
    networks:
      - paaster-net
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.paaster.rule=Host(`${PAASTER_DOMAIN}`)"
      - "traefik.http.routers.paaster.entrypoints=websecure"
      - "traefik.http.routers.paaster.tls.certresolver=letsencrypt"
      - "traefik.http.services.paaster.loadbalancer.server.port=3000"
      - "traefik.docker.network=dokploy-network"
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  mongodb:
    image: mongo:7
    restart: always
    volumes:
      - mongodb-data:/data/db
    environment:
      MONGO_INITDB_DATABASE: ${MONGO_DB:-paasterv3}
    networks:
      - paaster-net
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

volumes:
  mongodb-data:
    driver: local

networks:
  paaster-net:
    driver: bridge
  dokploy-network:
    external: true
```

### Example 3: Complex Multi-Service (5+ services)

**Context**: Paperless-ngx with PostgreSQL, Redis, Gotenberg, Tika

```yaml
services:
  paperless:
    image: ghcr.io/paperless-ngx/paperless-ngx:2.13
    restart: always
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      gotenberg:
        condition: service_started
      tika:
        condition: service_started
    volumes:
      - paperless-data:/usr/src/paperless/data
      - paperless-media:/usr/src/paperless/media
      - paperless-export:/usr/src/paperless/export
      - paperless-consume:/usr/src/paperless/consume
    environment:
      PAPERLESS_REDIS: redis://redis:6379
      PAPERLESS_DBHOST: postgres
      PAPERLESS_DBNAME: ${POSTGRES_DB:-paperless}
      PAPERLESS_DBUSER: ${POSTGRES_USER:-paperless}
      PAPERLESS_DBPASS: ${POSTGRES_PASSWORD:?Set database password}
      PAPERLESS_SECRET_KEY: ${PAPERLESS_SECRET_KEY:?Set secret key}
      PAPERLESS_URL: https://${PAPERLESS_DOMAIN}
      PAPERLESS_TIKA_ENABLED: 1
      PAPERLESS_TIKA_ENDPOINT: http://tika:9998
      PAPERLESS_TIKA_GOTENBERG_ENDPOINT: http://gotenberg:3000
    networks:
      - paperless-net
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.paperless.rule=Host(`${PAPERLESS_DOMAIN}`)"
      - "traefik.http.routers.paperless.entrypoints=websecure"
      - "traefik.http.routers.paperless.tls.certresolver=letsencrypt"
      - "traefik.http.services.paperless.loadbalancer.server.port=8000"
      - "traefik.docker.network=dokploy-network"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  postgres:
    image: postgres:16-alpine
    restart: always
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-paperless}
      POSTGRES_USER: ${POSTGRES_USER:-paperless}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set database password}
    networks:
      - paperless-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-paperless} -d ${POSTGRES_DB:-paperless}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis-data:/data
    networks:
      - paperless-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  gotenberg:
    image: gotenberg/gotenberg:8
    restart: always
    networks:
      - paperless-net
    command:
      - "gotenberg"
      - "--chromium-disable-javascript=true"
      - "--chromium-allow-list=file:///tmp/.*"

  tika:
    image: apache/tika:2.9.1.0
    restart: always
    networks:
      - paperless-net

volumes:
  paperless-data:
    driver: local
  paperless-media:
    driver: local
  paperless-export:
    driver: local
  paperless-consume:
    driver: local
  postgres-data:
    driver: local
  redis-data:
    driver: local

networks:
  paperless-net:
    driver: bridge
  dokploy-network:
    external: true
```

---

## Quality Standards

### Mandatory Requirements
- [ ] All images have pinned versions (no `:latest`)
- [ ] All services have `restart: always`
- [ ] Two networks defined (app-net + dokploy-network)
- [ ] dokploy-network marked as `external: true`
- [ ] All volumes are named (not bind mounts)
- [ ] Web services connect to both networks
- [ ] Database services connect only to app-net
- [ ] All services have health checks
- [ ] Required env vars use `:?` syntax with error message
- [ ] Optional env vars use `:-` syntax with default

### Naming Conventions
- Service names: lowercase, hyphenated (e.g., `my-service`)
- Network names: `${app}-net` (e.g., `paaster-net`)
- Volume names: `${service}-${type}` (e.g., `postgres-data`)
- Environment variables: UPPER_SNAKE_CASE

---

## Common Pitfalls

### Pitfall 1: Using :latest tags
**Issue**: Images break when upstream updates
**Solution**: Always pin to specific version (major.minor at minimum)

### Pitfall 2: Missing dokploy-network
**Issue**: Traefik cannot route to service
**Solution**: Ensure `dokploy-network` is defined as external and web services connect to it

### Pitfall 3: Bind mounts for data
**Issue**: Data lost on redeployment, path issues
**Solution**: Use named volumes with `driver: local`

### Pitfall 4: Missing health checks
**Issue**: Dependencies start before services are ready
**Solution**: Add health checks to all services, use `service_healthy` condition

### Pitfall 5: Database on external network
**Issue**: Database exposed to other containers
**Solution**: Connect databases ONLY to app-net, not dokploy-network

---

## Integration

### Skills-First Approach (v2.0+)

This skill is part of the **skills-first architecture** - loaded progressively by generic agents instead of being embedded in specialized agents.

### Related Skills
- `dokploy-traefik-routing`: Configure Traefik labels
- `dokploy-health-patterns`: Define health checks
- `dokploy-environment-config`: Environment variable patterns
- `dokploy-multi-service`: Complex service dependencies

### Invoked By
- `/dokploy-create` command: Phase 3 (Generation) - Step 1

### Order in Workflow (Progressive Loading)
1. **This skill**: Create base compose structure (loaded first)
2. `dokploy-traefik-routing`: Add routing labels
3. `dokploy-health-patterns`: Add health checks
4. `dokploy-environment-config`: Configure environment
5. `dokploy-template-toml`: Create template.toml

See: `.claude/commands/dokploy-create.md` for full workflow
