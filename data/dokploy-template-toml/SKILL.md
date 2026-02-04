---
name: dokploy-template-toml
description: "Generate template.toml configuration for Dokploy templates with variables, domains, environment mappings, and file mounts. Use when finalizing Dokploy templates."
version: 1.0.0
author: Home Lab Infrastructure Team
---

# Dokploy Template TOML

## When to Use This Skill

- When creating template.toml for a new Dokploy template
- When configuring Dokploy variable generation (passwords, secrets)
- When setting up domain configuration for services
- When adding file mounts for configuration files
- When user asks about "dokploy variables" or "template configuration"

## When NOT to Use This Skill

- When working with docker-compose only (no Dokploy)
- For runtime configuration changes (modify environment vars instead)

## Prerequisites

- Completed docker-compose.yml file
- List of required/optional environment variables
- Domain configuration requirements
- Knowledge of secret generation needs

---

## Template.toml Structure

```toml
# Header comment with application info
# Application Name - Description
# https://github.com/example/application

[variables]
# User-provided and auto-generated variables
domain = "${domain}"
secret_key = "${base64:64}"
password = "${password:32}"

# Domain configuration for Traefik
[[config.domains]]
serviceName = "app"
port = 3000
host = "${domain}"

# Environment variables for all services
[config.env]
APP_DOMAIN = "${domain}"
APP_SECRET = "${secret_key}"

# Optional file mounts
[[config.mounts]]
serviceName = "app"
mountPath = "/app/config.json"
content = """
{
  "setting": "${variable}"
}
"""
```

---

## Core Patterns

### Pattern 1: Variable Definitions

```toml
[variables]
# User-provided domain (required)
domain = "${domain}"

# Random password generation
db_password = "${password:32}"      # 32-char alphanumeric
api_key = "${password:48}"          # 48-char alphanumeric

# Base64 secret generation
secret_key = "${base64:64}"         # 64-char base64 encoded
jwt_secret = "${base64:32}"         # 32-char base64 encoded

# UUID generation
instance_id = "${uuid}"             # Random UUID v4

# User inputs
admin_email = "${email}"            # User-provided email
username = "${username}"            # User-provided username

# Derived variables (string concatenation)
app_url = "https://${domain}"
db_url = "postgresql://user:${db_password}@postgres:5432/db"
```

**Supported Variable Types:**

| Syntax | Description | Example Output |
|--------|-------------|----------------|
| `${domain}` | User-provided domain | `example.com` |
| `${password:N}` | N-char random password | `aB3kL9mN...` |
| `${base64:N}` | N-char base64 secret | `dGhpcyBpcyBh...` |
| `${uuid}` | Random UUID v4 | `550e8400-e29b-41d4-a716-446655440000` |
| `${username}` | User-provided username | `admin` |
| `${email}` | User-provided email | `user@example.com` |

### Pattern 2: Domain Configuration

```toml
# Single domain
[[config.domains]]
serviceName = "app"
port = 3000
host = "${domain}"

# Multiple domains (different services)
[[config.domains]]
serviceName = "app"
port = 3000
host = "${domain}"

[[config.domains]]
serviceName = "api"
port = 8080
host = "api.${domain}"

# Admin subdomain
[[config.domains]]
serviceName = "admin"
port = 9000
host = "admin.${domain}"
```

**Important**: `serviceName` must match the service name in docker-compose.yml

### Pattern 3: Environment Variables

```toml
[config.env]
# Required variables (error if not set in compose)
APP_DOMAIN = "${domain}"
APP_SECRET = "${secret_key}"
DATABASE_PASSWORD = "${db_password}"

# Categories with comments
# ===========================================
# Database Configuration
# ===========================================
POSTGRES_DB = "appdb"
POSTGRES_USER = "appuser"
POSTGRES_PASSWORD = "${db_password}"

# ===========================================
# Application Settings
# ===========================================
APP_URL = "https://${domain}"
DEBUG = "false"

# ===========================================
# External Services (Cloudflare R2)
# ===========================================
S3_ENDPOINT = ""
S3_ACCESS_KEY_ID = ""
S3_SECRET_ACCESS_KEY = ""
S3_BUCKET = ""
S3_REGION = "auto"
```

### Pattern 4: File Mounts

```toml
# JSON configuration file
[[config.mounts]]
serviceName = "app"
mountPath = "/app/config.json"
content = """
{
  "domain": "${domain}",
  "secret": "${secret_key}",
  "database": {
    "host": "postgres",
    "port": 5432,
    "name": "appdb"
  }
}
"""

# INI/conf file
[[config.mounts]]
serviceName = "app"
mountPath = "/etc/app/settings.conf"
content = """
[general]
domain = ${domain}
debug = false

[database]
host = postgres
port = 5432
password = ${db_password}
"""

# YAML configuration
[[config.mounts]]
serviceName = "app"
mountPath = "/app/config.yaml"
content = """
server:
  host: 0.0.0.0
  port: 3000
  domain: ${domain}

security:
  secret_key: ${secret_key}
"""
```

---

## Complete Examples

### Example 1: Simple Web App (Paaster)

```toml
# Paaster - End-to-end encrypted pastebin
# https://github.com/WardPearce/paaster

[variables]
domain = "${domain}"
cookie_secret = "${base64:64}"

[[config.domains]]
serviceName = "paaster"
port = 3000
host = "${domain}"

[config.env]
# ===========================================
# Application Domain
# ===========================================
PAASTER_DOMAIN = "${domain}"

# ===========================================
# Security
# ===========================================
COOKIE_SECRET = "${cookie_secret}"

# ===========================================
# MongoDB Configuration
# ===========================================
MONGO_DB = "paasterv3"

# ===========================================
# Cloudflare R2 Storage
# Get from: Cloudflare Dashboard > R2 > Manage R2 API Tokens
# Endpoint format: https://<ACCOUNT_ID>.r2.cloudflarestorage.com
# ===========================================
S3_ENDPOINT = ""
S3_ACCESS_KEY_ID = ""
S3_SECRET_ACCESS_KEY = ""
S3_BUCKET = ""
S3_REGION = "auto"
```

### Example 2: Git Service with Database (Forgejo)

```toml
# Forgejo - Self-hosted Git forge
# https://forgejo.org/

[variables]
domain = "${domain}"
postgres_password = "${password:32}"
secret_key = "${base64:64}"
internal_token = "${base64:48}"
jwt_secret = "${base64:48}"

[[config.domains]]
serviceName = "forgejo"
port = 3000
host = "${domain}"

[config.env]
# ===========================================
# Domain Configuration
# ===========================================
FORGEJO__server__DOMAIN = "${domain}"
FORGEJO__server__ROOT_URL = "https://${domain}/"

# ===========================================
# Database Configuration
# ===========================================
FORGEJO__database__DB_TYPE = "postgres"
FORGEJO__database__HOST = "postgres:5432"
FORGEJO__database__NAME = "forgejo"
FORGEJO__database__USER = "forgejo"
FORGEJO__database__PASSWD = "${postgres_password}"

# PostgreSQL credentials
POSTGRES_USER = "forgejo"
POSTGRES_DB = "forgejo"
POSTGRES_PASSWORD = "${postgres_password}"

# ===========================================
# Security Keys
# ===========================================
FORGEJO__security__SECRET_KEY = "${secret_key}"
FORGEJO__security__INTERNAL_TOKEN = "${internal_token}"
FORGEJO__oauth2__JWT_SECRET = "${jwt_secret}"

# ===========================================
# Optional: SSH Configuration
# ===========================================
SSH_PORT = "2222"
```

### Example 3: Complex Stack (Paperless-ngx)

```toml
# Paperless-ngx - Document management system
# https://docs.paperless-ngx.com/

[variables]
domain = "${domain}"
postgres_password = "${password:32}"
secret_key = "${base64:64}"
admin_user = "${username}"
admin_password = "${password:16}"
admin_email = "${email}"

[[config.domains]]
serviceName = "paperless"
port = 8000
host = "${domain}"

[config.env]
# ===========================================
# Database Configuration
# ===========================================
POSTGRES_DB = "paperless"
POSTGRES_USER = "paperless"
POSTGRES_PASSWORD = "${postgres_password}"

# Paperless database settings
PAPERLESS_DBHOST = "postgres"
PAPERLESS_DBNAME = "paperless"
PAPERLESS_DBUSER = "paperless"
PAPERLESS_DBPASS = "${postgres_password}"

# ===========================================
# Application Settings
# ===========================================
PAPERLESS_SECRET_KEY = "${secret_key}"
PAPERLESS_URL = "https://${domain}"
PAPERLESS_ALLOWED_HOSTS = "${domain}"
PAPERLESS_CORS_ALLOWED_HOSTS = "https://${domain}"

# ===========================================
# Admin User (created on first run)
# ===========================================
PAPERLESS_ADMIN_USER = "${admin_user}"
PAPERLESS_ADMIN_PASSWORD = "${admin_password}"
PAPERLESS_ADMIN_MAIL = "${admin_email}"

# ===========================================
# Document Processing
# ===========================================
PAPERLESS_OCR_LANGUAGE = "eng"
PAPERLESS_TIKA_ENABLED = "1"
PAPERLESS_TIKA_ENDPOINT = "http://tika:9998"
PAPERLESS_TIKA_GOTENBERG_ENDPOINT = "http://gotenberg:3000"

# ===========================================
# Redis
# ===========================================
PAPERLESS_REDIS = "redis://redis:6379"
```

### Example 4: Service with Config File Mount

```toml
# ANyONe Protocol Relay
# https://github.com/anyone-protocol/ator-protocol

[variables]
relay_nickname = "${username}"
relay_contact = "${email}"
control_password = "${password:24}"
orport = "9001"
dirport = "9030"
controlport = "9051"
wallet_address = ""

[config.env]
ACCEPT_TOS = "1"
ANON_NICKNAME = "${relay_nickname}"
ANON_CONTACT = "${relay_contact}"
ANON_ORPORT = "${orport}"
ANON_DIRPORT = "${dirport}"
ANON_CONTROLPORT = "${controlport}"

[[config.mounts]]
serviceName = "anon-relay"
mountPath = "/etc/anon/anonrc"
content = """
# ANyONe Protocol Relay Configuration
# Auto-generated by Dokploy

# Relay Identity
Nickname ${relay_nickname}
ContactInfo ${relay_contact}

# Network Ports
ORPort ${orport}
DirPort ${dirport}
ControlPort ${controlport}

# Control Authentication
HashedControlPassword ${control_password}

# Relay Type (exit disabled by default)
ExitRelay 0

# Bandwidth Limits (optional)
# RelayBandwidthRate 1 MB
# RelayBandwidthBurst 2 MB
"""
```

---

## Quality Standards

### Mandatory Requirements
- [ ] All required variables defined in `[variables]`
- [ ] Domain configuration matches docker-compose service names
- [ ] Environment variables organized with category comments
- [ ] Sensitive values use auto-generation (password, base64)
- [ ] User-facing values use appropriate prompts (domain, email)

### Documentation Standards
- Add header comment with app name and link
- Comment each category in `[config.env]`
- Document where to get external credentials (R2, etc.)

### Security Standards
- Never hardcode passwords or secrets
- Use `${password:N}` for database passwords
- Use `${base64:N}` for encryption keys
- Leave external API keys blank for user input

---

## Common Pitfalls

### Pitfall 1: serviceName mismatch
**Issue**: Domain config doesn't work
**Solution**: `serviceName` must exactly match docker-compose service name

### Pitfall 2: Missing variable definitions
**Issue**: Variables referenced but not defined
**Solution**: Define all `${var}` references in `[variables]` section

### Pitfall 3: Password in plain text
**Issue**: Secrets visible in Dokploy UI
**Solution**: Use `${password:N}` or `${base64:N}` for auto-generation

### Pitfall 4: Wrong mount serviceName
**Issue**: Config file not mounted
**Solution**: Match serviceName to exact docker-compose service

---

## Integration

### Skills-First Approach (v2.0+)

This skill is part of the **skills-first architecture** - loaded progressively during the Generation phase as the final step before validation.

### Related Skills
- `dokploy-compose-structure`: Service names for domain config
- `dokploy-environment-config`: Environment variable patterns
- `dokploy-cloudflare-integration`: R2 configuration

### Invoked By
- `/dokploy-create` command: Phase 3 (Generation) - Step 6 (Final)

### Order in Workflow (Progressive Loading)
1. `dokploy-compose-structure`: Create compose file
2. `dokploy-traefik-routing`: Add routing
3. `dokploy-health-patterns`: Add health checks
4. `dokploy-cloudflare-integration`: Add CF config (if applicable)
5. `dokploy-environment-config`: Plan environment vars
6. **This skill**: Create template.toml (final generation step)

See: `.claude/commands/dokploy-create.md` for full workflow
