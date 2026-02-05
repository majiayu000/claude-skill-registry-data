---
name: dokploy-environment-config
description: "Environment variable patterns for Dokploy templates including required vs optional syntax, secrets, connection strings, and configuration organization."
version: 1.0.0
author: Home Lab Infrastructure Team
---

# Dokploy Environment Configuration

## When to Use This Skill

- When defining environment variables for Dokploy templates
- When deciding between required and optional variables
- When configuring database connection strings
- When organizing environment sections
- When user asks about "environment variables" or "secrets"

## When NOT to Use This Skill

- For template.toml variables (use dokploy-template-toml)
- For Traefik configuration (use dokploy-traefik-routing)

## Prerequisites

- Application documentation (required env vars)
- Understanding of docker-compose variable syntax
- Knowledge of sensitive vs non-sensitive data

---

## Core Patterns

### Pattern 1: Required Variables (`:?` syntax)

Variables that MUST be set - deployment fails without them:

```yaml
environment:
  DOMAIN: ${DOMAIN:?Set your domain (e.g., example.com)}
  DATABASE_PASSWORD: ${DATABASE_PASSWORD:?Set a secure database password}
  SECRET_KEY: ${SECRET_KEY:?Set a secret key for session encryption}
```

**Syntax**: `${VAR_NAME:?Error message}`
- If VAR_NAME is unset or empty, shows error message and fails
- Use for: domains, passwords, API keys, secrets

### Pattern 2: Optional Variables (`:-` syntax)

Variables with sensible defaults:

```yaml
environment:
  LOG_LEVEL: ${LOG_LEVEL:-info}
  WORKERS: ${WORKERS:-4}
  CACHE_TTL: ${CACHE_TTL:-3600}
  DEBUG: ${DEBUG:-false}
```

**Syntax**: `${VAR_NAME:-default_value}`
- If VAR_NAME is unset or empty, uses default_value
- Use for: tuning parameters, feature flags, optional settings

### Pattern 3: Internal Constants

Values that shouldn't change:

```yaml
environment:
  # Database host is always the service name
  PGHOST: postgres
  REDIS_HOST: redis

  # Ports are fixed in the container
  PGPORT: "5432"
  REDIS_PORT: "6379"
```

### Pattern 4: Computed Values

Variables derived from other variables:

```yaml
environment:
  APP_URL: https://${DOMAIN}
  DATABASE_URL: postgresql://${DB_USER}:${DB_PASS}@postgres:5432/${DB_NAME}
  MONGO_URL: mongodb://mongodb:27017/${MONGO_DB:-appdb}
```

---

## Environment Variable Categories

### Category 1: Domain & URLs

```yaml
environment:
  # Primary domain (required)
  DOMAIN: ${DOMAIN:?Set your domain}

  # Derived URLs
  APP_URL: https://${DOMAIN}
  PUBLIC_URL: https://${DOMAIN}
  CORS_ORIGIN: https://${DOMAIN}
  ALLOWED_HOSTS: ${DOMAIN}
```

### Category 2: Database Configuration

**PostgreSQL:**
```yaml
environment:
  POSTGRES_DB: ${POSTGRES_DB:-appdb}
  POSTGRES_USER: ${POSTGRES_USER:-appuser}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set database password}

  # For app service connecting to postgres
  DATABASE_URL: postgresql://${POSTGRES_USER:-appuser}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB:-appdb}
  # OR individual variables
  DB_HOST: postgres
  DB_PORT: "5432"
  DB_NAME: ${POSTGRES_DB:-appdb}
  DB_USER: ${POSTGRES_USER:-appuser}
  DB_PASS: ${POSTGRES_PASSWORD}
```

**MongoDB:**
```yaml
environment:
  MONGO_INITDB_DATABASE: ${MONGO_DB:-appdb}

  # For app service
  MONGO_URL: mongodb://mongodb:27017/${MONGO_DB:-appdb}
  MONGO_DB: ${MONGO_DB:-appdb}
```

**Redis:**
```yaml
environment:
  # For app service
  REDIS_URL: redis://redis:6379
  REDIS_HOST: redis
  REDIS_PORT: "6379"
```

### Category 3: Security & Secrets

```yaml
environment:
  # Session/cookie security
  SECRET_KEY: ${SECRET_KEY:?Set a secret key}
  COOKIE_SECRET: ${COOKIE_SECRET:?Set cookie secret}

  # JWT/Auth
  JWT_SECRET: ${JWT_SECRET:?Set JWT secret}

  # API keys (user-provided)
  API_KEY: ${API_KEY:?Set API key}
```

### Category 4: External Services (Cloudflare R2)

```yaml
environment:
  # S3-compatible storage (Cloudflare R2)
  S3_ENDPOINT: ${S3_ENDPOINT:?Set Cloudflare R2 endpoint}
  S3_REGION: ${S3_REGION:-auto}
  S3_ACCESS_KEY_ID: ${S3_ACCESS_KEY_ID:?Set R2 access key ID}
  S3_SECRET_ACCESS_KEY: ${S3_SECRET_ACCESS_KEY:?Set R2 secret access key}
  S3_BUCKET: ${S3_BUCKET:?Set R2 bucket name}
  S3_FORCE_PATH_STYLE: "false"
```

### Category 5: Application Settings

```yaml
environment:
  # Feature flags
  DEBUG: ${DEBUG:-false}
  ENABLE_FEATURE_X: ${ENABLE_FEATURE_X:-true}

  # Performance tuning
  WORKERS: ${WORKERS:-4}
  MAX_CONNECTIONS: ${MAX_CONNECTIONS:-100}
  CACHE_TTL: ${CACHE_TTL:-3600}

  # Logging
  LOG_LEVEL: ${LOG_LEVEL:-info}
  LOG_FORMAT: ${LOG_FORMAT:-json}
```

### Category 6: Admin User (First Run)

```yaml
environment:
  ADMIN_USER: ${ADMIN_USER:-admin}
  ADMIN_PASSWORD: ${ADMIN_PASSWORD:?Set admin password}
  ADMIN_EMAIL: ${ADMIN_EMAIL:?Set admin email}
```

---

## Complete Examples

### Example 1: Simple Web App (Paaster)

```yaml
services:
  paaster:
    environment:
      # ===========================================
      # Domain Configuration
      # ===========================================
      PAASTER_DOMAIN: ${PAASTER_DOMAIN:?Set your domain}

      # ===========================================
      # Session Security
      # ===========================================
      COOKIE_SECRET: ${COOKIE_SECRET:?Set a secure random cookie secret}

      # ===========================================
      # MongoDB Connection
      # ===========================================
      MONGO_DB: ${MONGO_DB:-paasterv3}
      MONGO_URL: mongodb://mongodb:27017/${MONGO_DB:-paasterv3}

      # ===========================================
      # S3 Storage (Cloudflare R2)
      # Get from: Cloudflare Dashboard > R2 > Manage R2 API Tokens
      # Endpoint format: https://<ACCOUNT_ID>.r2.cloudflarestorage.com
      # ===========================================
      S3_ENDPOINT: ${S3_ENDPOINT:?Set Cloudflare R2 endpoint}
      S3_REGION: ${S3_REGION:-auto}
      S3_ACCESS_KEY_ID: ${S3_ACCESS_KEY_ID:?Set R2 access key ID}
      S3_SECRET_ACCESS_KEY: ${S3_SECRET_ACCESS_KEY:?Set R2 secret access key}
      S3_BUCKET: ${S3_BUCKET:?Set R2 bucket name}
      S3_FORCE_PATH_STYLE: "false"

  mongodb:
    environment:
      MONGO_INITDB_DATABASE: ${MONGO_DB:-paasterv3}
```

### Example 2: Complex Stack (Paperless-ngx)

```yaml
services:
  paperless:
    environment:
      # ===========================================
      # Application Settings
      # ===========================================
      PAPERLESS_SECRET_KEY: ${PAPERLESS_SECRET_KEY:?Set secret key}
      PAPERLESS_URL: https://${PAPERLESS_DOMAIN}
      PAPERLESS_ALLOWED_HOSTS: ${PAPERLESS_DOMAIN}
      PAPERLESS_CORS_ALLOWED_HOSTS: https://${PAPERLESS_DOMAIN}

      # ===========================================
      # Database (PostgreSQL)
      # ===========================================
      PAPERLESS_DBHOST: postgres
      PAPERLESS_DBPORT: "5432"
      PAPERLESS_DBNAME: ${POSTGRES_DB:-paperless}
      PAPERLESS_DBUSER: ${POSTGRES_USER:-paperless}
      PAPERLESS_DBPASS: ${POSTGRES_PASSWORD:?Set database password}

      # ===========================================
      # Cache (Redis)
      # ===========================================
      PAPERLESS_REDIS: redis://redis:6379

      # ===========================================
      # Document Processing
      # ===========================================
      PAPERLESS_OCR_LANGUAGE: ${OCR_LANGUAGE:-eng}
      PAPERLESS_TIKA_ENABLED: "1"
      PAPERLESS_TIKA_ENDPOINT: http://tika:9998
      PAPERLESS_TIKA_GOTENBERG_ENDPOINT: http://gotenberg:3000

      # ===========================================
      # Admin User (created on first run)
      # ===========================================
      PAPERLESS_ADMIN_USER: ${ADMIN_USER:-admin}
      PAPERLESS_ADMIN_PASSWORD: ${ADMIN_PASSWORD:?Set admin password}
      PAPERLESS_ADMIN_MAIL: ${ADMIN_EMAIL:?Set admin email}

  postgres:
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-paperless}
      POSTGRES_USER: ${POSTGRES_USER:-paperless}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set database password}
```

### Example 3: Git Service (Forgejo)

```yaml
services:
  forgejo:
    environment:
      # ===========================================
      # Server Configuration
      # ===========================================
      FORGEJO__server__DOMAIN: ${FORGEJO_DOMAIN}
      FORGEJO__server__ROOT_URL: https://${FORGEJO_DOMAIN}/
      FORGEJO__server__SSH_DOMAIN: ${FORGEJO_DOMAIN}
      FORGEJO__server__SSH_PORT: ${SSH_PORT:-2222}

      # ===========================================
      # Database (PostgreSQL)
      # ===========================================
      FORGEJO__database__DB_TYPE: postgres
      FORGEJO__database__HOST: postgres:5432
      FORGEJO__database__NAME: ${POSTGRES_DB:-forgejo}
      FORGEJO__database__USER: ${POSTGRES_USER:-forgejo}
      FORGEJO__database__PASSWD: ${POSTGRES_PASSWORD:?Set database password}

      # ===========================================
      # Security
      # ===========================================
      FORGEJO__security__SECRET_KEY: ${SECRET_KEY:?Set secret key}
      FORGEJO__security__INTERNAL_TOKEN: ${INTERNAL_TOKEN:?Set internal token}
      FORGEJO__oauth2__JWT_SECRET: ${JWT_SECRET:?Set JWT secret}

      # ===========================================
      # Service Settings
      # ===========================================
      FORGEJO__service__DISABLE_REGISTRATION: ${DISABLE_REGISTRATION:-false}
      FORGEJO__service__REQUIRE_SIGNIN_VIEW: ${REQUIRE_SIGNIN:-false}

  postgres:
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-forgejo}
      POSTGRES_USER: ${POSTGRES_USER:-forgejo}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set database password}
```

---

## Sensitive Data Guidelines

### Always Required (`:?`)
- Domain names
- Database passwords
- Secret keys / JWT secrets
- API keys and tokens
- Admin passwords
- S3/R2 credentials

### Usually Optional (`:-`)
- Usernames (with sensible default)
- Database names
- Feature flags
- Tuning parameters
- Log levels

### Never in Environment
- Private keys (use mounted secrets)
- Large certificates (use volume mounts)
- Multi-line configurations (use file mounts)

---

## Quality Standards

### Mandatory Requirements
- [ ] All required vars use `:?` with clear error message
- [ ] All optional vars use `:-` with sensible default
- [ ] Environment sections have category comments
- [ ] Database passwords marked as required
- [ ] Secret keys marked as required
- [ ] Internal service hosts use service names

### Organization Standards
- Group variables by category
- Add comment headers for each category
- Document where to obtain external credentials
- Use consistent naming (UPPER_SNAKE_CASE)

---

## Common Pitfalls

### Pitfall 1: Missing error message
**Issue**: `${VAR:?}` gives unclear error
**Solution**: Always add descriptive message: `${VAR:?Set your domain}`

### Pitfall 2: Using IP addresses
**Issue**: Service IPs change on restart
**Solution**: Use service names: `postgres`, `redis`, `mongodb`

### Pitfall 3: Hardcoded secrets
**Issue**: Secrets visible in repository
**Solution**: Use variables: `${PASSWORD:?Set password}`

### Pitfall 4: Missing quotes on ports
**Issue**: YAML interprets as number
**Solution**: Quote port strings: `DB_PORT: "5432"`

---

## Integration

### Skills-First Approach (v2.0+)

This skill is part of the **skills-first architecture** - loaded during Generation phase to configure environment variables before creating template.toml.

### Related Skills
- `dokploy-template-toml`: Variable generation in template.toml
- `dokploy-security-hardening`: Secret management
- `dokploy-cloudflare-integration`: R2 credentials

### Invoked By
- `/dokploy-create` command: Phase 3 (Generation) - Step 5

### Order in Workflow (Progressive Loading)
1. `dokploy-compose-structure`: Create base structure
2. `dokploy-traefik-routing`: Add routing labels
3. `dokploy-health-patterns`: Add health checks
4. `dokploy-cloudflare-integration`: Add CF integration (if applicable)
5. **This skill**: Configure environment variables (Step 5)
6. `dokploy-template-toml`: Create template.toml

See: `.claude/commands/dokploy-create.md` for full workflow
