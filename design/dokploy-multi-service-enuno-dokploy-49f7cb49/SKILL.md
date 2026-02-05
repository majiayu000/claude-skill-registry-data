---
name: dokploy-multi-service
description: "Multi-service architecture patterns for Dokploy templates including dependency chains, service communication, and complex stack design. Use when building templates with 2+ services."
version: 1.0.0
author: Home Lab Infrastructure Team
---

# Dokploy Multi-Service Architecture

## When to Use This Skill

- When creating templates with 2 or more services
- When designing service dependency chains
- When planning database + app + helper service stacks
- When user asks about "multi-container" or "service dependencies"

## When NOT to Use This Skill

- For single-container applications
- For sidecar patterns (use dedicated sidecar documentation)

## Prerequisites

- Understanding of service dependencies (what calls what)
- Knowledge of startup order requirements
- Understanding of internal vs external service access

---

## Architecture Patterns

### Pattern 1: App + Database (2-tier)

**Structure:**
```
┌─────────────┐     ┌─────────────┐
│     App     │────▶│  Database   │
│  (web UI)   │     │ (internal)  │
└─────────────┘     └─────────────┘
       │
       ▼
  dokploy-network
```

**Characteristics:**
- App connects to both networks (external + internal)
- Database connects only to internal network
- App depends on database with `service_healthy`

**Example (Paaster + MongoDB):**
```yaml
services:
  paaster:
    image: wardpearce/paaster:3.1.7
    depends_on:
      mongodb:
        condition: service_healthy
    networks:
      - paaster-net      # Internal
      - dokploy-network  # External (Traefik)
    # ... traefik labels, health check

  mongodb:
    image: mongo:7
    networks:
      - paaster-net      # Internal ONLY
    # ... health check, no traefik labels

networks:
  paaster-net:
    driver: bridge
  dokploy-network:
    external: true
```

### Pattern 2: App + Database + Cache (3-tier)

**Structure:**
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│     App     │────▶│  Database   │     │    Cache    │
│  (web UI)   │     │ (internal)  │◀────│  (internal) │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                     internal network
```

**Dependency Logic:**
```yaml
services:
  app:
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_healthy
```

**Example (Django + PostgreSQL + Redis):**
```yaml
services:
  app:
    image: myapp:1.0.0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/db
      REDIS_URL: redis://redis:6379
    networks:
      - app-net
      - dokploy-network

  postgres:
    image: postgres:16-alpine
    networks:
      - app-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d db"]

  redis:
    image: redis:7-alpine
    networks:
      - app-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
```

### Pattern 3: App + Helpers (Star Pattern)

**Structure:**
```
                    ┌─────────────┐
                    │   Helper 1  │
                    │ (on-demand) │
                    └──────▲──────┘
                           │
┌─────────────┐     ┌──────┴──────┐     ┌─────────────┐
│  Database   │◀────│     App     │────▶│   Helper 2  │
│ (required)  │     │  (main)     │     │ (on-demand) │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                   dokploy-network
```

**Dependency Logic:**
- Database: `service_healthy` (required at startup)
- Helpers: `service_started` (called on-demand)

**Example (Paperless-ngx):**
```yaml
services:
  paperless:
    image: ghcr.io/paperless-ngx/paperless-ngx:2.13
    depends_on:
      postgres:
        condition: service_healthy   # Required at startup
      redis:
        condition: service_healthy   # Required at startup
      gotenberg:
        condition: service_started   # On-demand helper
      tika:
        condition: service_started   # On-demand helper
    environment:
      PAPERLESS_TIKA_ENABLED: 1
      PAPERLESS_TIKA_ENDPOINT: http://tika:9998
      PAPERLESS_TIKA_GOTENBERG_ENDPOINT: http://gotenberg:3000
    networks:
      - paperless-net
      - dokploy-network

  postgres:
    image: postgres:16-alpine
    networks:
      - paperless-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U paperless -d paperless"]

  redis:
    image: redis:7-alpine
    networks:
      - paperless-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

  gotenberg:
    image: gotenberg/gotenberg:8
    networks:
      - paperless-net
    # No healthcheck - stateless converter

  tika:
    image: apache/tika:2.9.1.0
    networks:
      - paperless-net
    # No healthcheck - stateless parser
```

### Pattern 4: Multiple External Services

**Structure:**
```
┌─────────────┐     ┌─────────────┐
│    App      │────▶│  Database   │
│  (main)     │     │             │
└─────────────┘     └─────────────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│    API      │────▶│  Database   │
│ (secondary) │     │  (shared)   │
└─────────────┘     └─────────────┘
       │
       ▼
dokploy-network (both app and api accessible)
```

**Example (App + API on different subdomains):**
```yaml
services:
  app:
    image: myapp-web:1.0.0
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - app-net
      - dokploy-network
    labels:
      - "traefik.http.routers.app.rule=Host(`${DOMAIN}`)"
      # ...

  api:
    image: myapp-api:1.0.0
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - app-net
      - dokploy-network
    labels:
      - "traefik.http.routers.api.rule=Host(`api.${DOMAIN}`)"
      # ...

  postgres:
    image: postgres:16-alpine
    networks:
      - app-net  # Shared by both app and api
```

---

## Dependency Conditions Reference

| Condition | When to Use | Example |
|-----------|-------------|---------|
| `service_healthy` | Database, cache, required services | PostgreSQL, MongoDB, Redis |
| `service_started` | Helper services, on-demand converters | Gotenberg, Tika, sidecars |
| `service_completed_successfully` | Init containers, migrations | DB migrations, setup scripts |

---

## Complete Examples

### Example 1: 2-Service (Forgejo + PostgreSQL)

```yaml
services:
  forgejo:
    image: codeberg.org/forgejo/forgejo:9
    restart: always
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - forgejo-data:/data
    environment:
      FORGEJO__database__DB_TYPE: postgres
      FORGEJO__database__HOST: postgres:5432
      FORGEJO__database__NAME: ${POSTGRES_DB:-forgejo}
      FORGEJO__database__USER: ${POSTGRES_USER:-forgejo}
      FORGEJO__database__PASSWD: ${POSTGRES_PASSWORD:?Set database password}
    networks:
      - forgejo-net
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.forgejo.rule=Host(`${FORGEJO_DOMAIN}`)"
      - "traefik.http.routers.forgejo.entrypoints=websecure"
      - "traefik.http.routers.forgejo.tls.certresolver=letsencrypt"
      - "traefik.http.services.forgejo.loadbalancer.server.port=3000"
      - "traefik.docker.network=dokploy-network"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  postgres:
    image: postgres:16-alpine
    restart: always
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-forgejo}
      POSTGRES_USER: ${POSTGRES_USER:-forgejo}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set database password}
    networks:
      - forgejo-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-forgejo} -d ${POSTGRES_DB:-forgejo}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

volumes:
  forgejo-data:
    driver: local
  postgres-data:
    driver: local

networks:
  forgejo-net:
    driver: bridge
  dokploy-network:
    external: true
```

### Example 2: 5-Service Complex Stack (Paperless-ngx)

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

## Service Communication Patterns

### Internal Service URLs

| Service | Internal URL Format |
|---------|-------------------|
| PostgreSQL | `postgresql://user:pass@postgres:5432/db` |
| MongoDB | `mongodb://mongodb:27017/dbname` |
| Redis | `redis://redis:6379` |
| MySQL | `mysql://user:pass@mysql:3306/db` |
| HTTP APIs | `http://service-name:port/path` |

### Environment Variable Patterns

```yaml
# Database connections
DATABASE_URL: postgresql://${DB_USER}:${DB_PASS}@postgres:5432/${DB_NAME}
MONGO_URL: mongodb://mongodb:27017/${MONGO_DB}
REDIS_URL: redis://redis:6379

# Internal HTTP services
TIKA_ENDPOINT: http://tika:9998
GOTENBERG_ENDPOINT: http://gotenberg:3000
API_ENDPOINT: http://api:8080
```

---

## Quality Standards

### Mandatory Requirements
- [ ] All service dependencies explicitly declared
- [ ] `service_healthy` for required startup dependencies
- [ ] `service_started` for on-demand helpers
- [ ] Databases on internal network only
- [ ] Web services on both networks
- [ ] Service names match across depends_on and environment URLs

### Dependency Validation
- Each `depends_on` service must exist
- Health checks required for `service_healthy` dependencies
- Connection strings use service names, not IPs

---

## Common Pitfalls

### Pitfall 1: Circular dependencies
**Issue**: Service A depends on B, B depends on A
**Solution**: Redesign architecture, use async communication

### Pitfall 2: Missing health checks for dependencies
**Issue**: `service_healthy` fails without health check
**Solution**: Add health check to dependency service

### Pitfall 3: Wrong service name in URL
**Issue**: Connection refused errors
**Solution**: Use exact docker-compose service name in URLs

### Pitfall 4: Database exposed externally
**Issue**: Security vulnerability
**Solution**: Remove dokploy-network from database services

---

## Integration

### Skills-First Approach (v2.0+)

This skill is part of the **skills-first architecture** - loaded during the Architecture phase to design complex service dependencies before generation begins.

### Related Skills
- `dokploy-compose-structure`: Base structure implementation
- `dokploy-health-patterns`: Health check configuration
- `dokploy-environment-config`: Connection strings and service URLs

### Invoked By
- `/dokploy-create` command: Phase 2 (Architecture) - Loaded when 2+ services detected

### Order in Workflow (Progressive Loading)
1. Phase 1: Discovery (research, no skills)
2. **This skill**: Design service architecture (Phase 2)
3. Phase 3: Generation skills (compose-structure → ... → template-toml)
4. Phase 4: Validation skills

See: `.claude/commands/dokploy-create.md` for full workflow
