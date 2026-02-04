---
name: dokploy-health-patterns
description: "Health check patterns for different service types in Dokploy templates. Covers HTTP, PostgreSQL, MongoDB, Redis, MySQL, and custom health checks."
version: 1.0.0
author: Home Lab Infrastructure Team
---

# Dokploy Health Patterns

## When to Use This Skill

- When adding health checks to any Dokploy service
- When configuring service dependencies with `service_healthy`
- When troubleshooting container startup order issues
- When user asks about "health checks" or "service dependencies"

## When NOT to Use This Skill

- For services that don't support health checks (rare, most do)
- For helper services that start instantly (use `service_started` instead)

## Prerequisites

- Understanding of service internals (ports, health endpoints)
- Knowledge of available tools in container (curl, wget, etc.)

---

## Core Pattern

### Standard Health Check Template

Every health check follows this structure:

```yaml
healthcheck:
  test: ["CMD", "command", "args"]
  interval: 30s       # How often to check
  timeout: 10s        # Max time per check
  retries: 3          # Failures before unhealthy
  start_period: 30s   # Grace period for startup
```

**Configuration Guidelines:**

| Parameter | Default | When to Adjust |
|-----------|---------|----------------|
| `interval` | 30s | Increase for resource-constrained systems |
| `timeout` | 10s | Increase for slow-starting services |
| `retries` | 3 | Increase for flaky services |
| `start_period` | 30s | Increase for complex services (databases, Java apps) |

---

## Health Check Patterns by Service Type

### Pattern 1: HTTP Services (curl)

For services with HTTP endpoints (most web apps):

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:${PORT}/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

**Variations:**

```yaml
# With specific health endpoint
test: ["CMD", "curl", "-f", "http://localhost:3000/health"]

# With API endpoint
test: ["CMD", "curl", "-f", "http://localhost:3000/api/healthz"]

# Silent output
test: ["CMD", "curl", "-sf", "http://localhost:8080/ping"]
```

### Pattern 2: HTTP Services (wget - Alpine-based)

For Alpine-based images without curl:

```yaml
healthcheck:
  test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:${PORT}"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

**Example (Paaster):**
```yaml
healthcheck:
  test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

### Pattern 3: PostgreSQL

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

**Variations:**

```yaml
# With specific host
test: ["CMD-SHELL", "pg_isready -U postgres -d mydb -h localhost"]

# With default user
test: ["CMD-SHELL", "pg_isready -U postgres"]

# With environment variable interpolation
test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres}"]
```

### Pattern 4: MongoDB

```yaml
healthcheck:
  test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

**Variations:**

```yaml
# For older MongoDB (pre-6.0, use mongo instead of mongosh)
test: ["CMD", "mongo", "--eval", "db.adminCommand('ping')"]

# With authentication
test: ["CMD", "mongosh", "-u", "admin", "-p", "${MONGO_PASSWORD}", "--eval", "db.adminCommand('ping')"]
```

### Pattern 5: Redis

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s  # Redis starts fast
```

**Variations:**

```yaml
# With password
test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]

# Check specific key exists
test: ["CMD-SHELL", "redis-cli ping | grep PONG"]
```

### Pattern 6: MySQL/MariaDB

```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

**Variations:**

```yaml
# With credentials
test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${MYSQL_ROOT_PASSWORD}"]

# Using mysql client
test: ["CMD-SHELL", "mysql -u root -p${MYSQL_ROOT_PASSWORD} -e 'SELECT 1'"]
```

### Pattern 7: Elasticsearch

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:9200/_cluster/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s  # ES takes longer to start
```

### Pattern 8: RabbitMQ

```yaml
healthcheck:
  test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

### Pattern 9: Custom Shell Commands

For complex checks using shell scripting:

```yaml
healthcheck:
  test: ["CMD-SHELL", "command1 && command2 || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

**Example (ANyONe Relay):**
```yaml
healthcheck:
  test: ["CMD-SHELL", "echo 'GETINFO status/circuit-established' | nc -q 1 localhost 9051 | grep -q '250' || exit 1"]
  interval: 60s
  timeout: 15s
  retries: 3
  start_period: 120s
```

---

## Complete Examples

### Example 1: Web App with MongoDB (Paaster)

```yaml
services:
  paaster:
    image: wardpearce/paaster:3.1.7
    depends_on:
      mongodb:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  mongodb:
    image: mongo:7
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

### Example 2: Complex Stack (Paperless-ngx)

```yaml
services:
  paperless:
    image: ghcr.io/paperless-ngx/paperless-ngx:2.13
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      gotenberg:
        condition: service_started  # Helper, doesn't need healthy
      tika:
        condition: service_started  # Helper, doesn't need healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s  # Longer for complex app

  postgres:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-paperless} -d ${POSTGRES_DB:-paperless}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s  # Redis is fast

  gotenberg:
    image: gotenberg/gotenberg:8
    # No healthcheck needed - stateless helper

  tika:
    image: apache/tika:2.9.1.0
    # No healthcheck needed - stateless helper
```

### Example 3: Git Service with PostgreSQL (Forgejo)

```yaml
services:
  forgejo:
    image: codeberg.org/forgejo/forgejo:9
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  postgres:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${FORGEJO_DB_USER:-forgejo} -d ${FORGEJO_DB_NAME:-forgejo}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

---

## Start Period Recommendations

| Service Type | Recommended start_period |
|-------------|-------------------------|
| Redis | 10s |
| Static file server | 10s |
| Simple web app | 30s |
| Node.js app | 30s |
| PostgreSQL | 30s |
| MongoDB | 30s |
| MySQL | 45s |
| Java/Spring Boot | 60-120s |
| Paperless-ngx | 60s |
| Elasticsearch | 60-120s |
| Custom services | Test and adjust |

---

## Dependency Conditions

### When to use `service_healthy`

```yaml
depends_on:
  database:
    condition: service_healthy
```

Use for:
- Databases (PostgreSQL, MongoDB, Redis, MySQL)
- Services that need initialization time
- Services the app actively connects to on startup

### When to use `service_started`

```yaml
depends_on:
  helper:
    condition: service_started
```

Use for:
- Stateless helper services (Gotenberg, Tika)
- Services called on-demand, not at startup
- Fast-starting auxiliary services

---

## Quality Standards

### Mandatory Requirements
- [ ] All persistent services have health checks
- [ ] Databases use appropriate native health commands
- [ ] Web services use HTTP health checks
- [ ] Dependencies use `service_healthy` condition
- [ ] Start period appropriate for service type

### Testing Health Checks
```bash
# Check health status
docker compose ps

# View health check logs
docker inspect --format='{{json .State.Health}}' container_name
```

---

## Common Pitfalls

### Pitfall 1: Wrong tool for image
**Issue**: curl not available in Alpine images
**Solution**: Use wget for Alpine, curl for Debian/Ubuntu

### Pitfall 2: start_period too short
**Issue**: Service marked unhealthy during startup
**Solution**: Increase start_period for slow-starting services

### Pitfall 3: Checking wrong port
**Issue**: Health check fails, service works
**Solution**: Use internal container port, not mapped port

### Pitfall 4: Missing CMD-SHELL for pipes
**Issue**: Shell commands fail
**Solution**: Use `["CMD-SHELL", "cmd | grep ..."]` for pipes/redirects

### Pitfall 5: Health endpoint requires auth
**Issue**: 401/403 errors in health check
**Solution**: Use unauthenticated health endpoint or add credentials

---

## Integration

### Skills-First Approach (v2.0+)

This skill is part of the **skills-first architecture** - loaded during Generation phase to add health checks after routing configuration.

### Related Skills
- `dokploy-compose-structure`: Service dependencies
- `dokploy-multi-service`: Complex dependency chains

### Invoked By
- `/dokploy-create` command: Phase 3 (Generation) - Step 3

### Order in Workflow (Progressive Loading)
1. `dokploy-compose-structure`: Create base structure
2. `dokploy-traefik-routing`: Add routing labels
3. **This skill**: Add health checks (Step 3)
4. `dokploy-cloudflare-integration`: Add CF integration (if applicable)
5. `dokploy-environment-config`: Configure environment
6. `dokploy-template-toml`: Create template.toml

See: `.claude/commands/dokploy-create.md` for full workflow
