---
name: env-file-generator
description: Generate properly structured .env environment files with common variables, documentation comments, and secure placeholder patterns. Triggers on "create .env file", "generate environment variables", "env file for", "dotenv template".
---

# Environment File Generator

Generate properly structured `.env` files with documented variables, secure placeholders, and environment-specific configurations.

## Output Requirements

**File Output:** `.env`, `.env.example`, `.env.local`, `.env.production`
**Naming Convention:** `.env.{environment}` for specific environments
**Format:** KEY=value pairs, one per line

## When Invoked

Immediately generate a complete `.env.example` file (safe to commit) with placeholder values and documentation. Note which values need real secrets.

## Env File Syntax Rules

### Basic Format
```bash
# Comment explaining the variable
VARIABLE_NAME=value
```

### Conventions
- SCREAMING_SNAKE_CASE for variable names
- No spaces around `=`
- Quote values with spaces: `APP_NAME="My Application"`
- No quotes needed for simple values: `PORT=3000`
- Comments with `#` at start of line
- Group related variables with blank lines and section headers

### Value Types
```bash
# Strings (quote if contains spaces or special chars)
APP_NAME="My App Name"
SIMPLE_STRING=myvalue

# Numbers (no quotes needed)
PORT=3000
TIMEOUT=30

# Booleans (lowercase strings)
DEBUG=true
ENABLE_FEATURE=false

# URLs (quote recommended)
DATABASE_URL="postgresql://user:pass@localhost:5432/db"
API_ENDPOINT="https://api.example.com/v1"

# Secrets (use placeholder in .env.example)
API_KEY=your_api_key_here
SECRET_KEY=generate_a_secure_key_here
```

## Standard Templates

### Web Application (Node.js/React)
```bash
# ===========================================
# Application Configuration
# ===========================================

# Application
NODE_ENV=development
APP_NAME="My Application"
APP_URL=http://localhost:3000
PORT=3000

# Debug & Logging
DEBUG=true
LOG_LEVEL=debug

# ===========================================
# Database Configuration
# ===========================================

# PostgreSQL
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/myapp_dev"
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
DB_USER=postgres
DB_PASSWORD=postgres

# Connection Pool
DB_POOL_MIN=2
DB_POOL_MAX=10

# ===========================================
# Redis / Cache
# ===========================================

REDIS_URL="redis://localhost:6379"
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

CACHE_TTL=3600

# ===========================================
# Authentication
# ===========================================

# JWT
JWT_SECRET=your_jwt_secret_here_min_32_chars
JWT_EXPIRES_IN=7d
JWT_REFRESH_EXPIRES_IN=30d

# Session
SESSION_SECRET=your_session_secret_here

# ===========================================
# External Services
# ===========================================

# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=my-app-bucket

# Email (SMTP)
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=587
SMTP_USER=your_smtp_user
SMTP_PASSWORD=your_smtp_password
EMAIL_FROM="noreply@example.com"

# ===========================================
# Third-Party APIs
# ===========================================

# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxx

# OAuth Providers
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# ===========================================
# Feature Flags
# ===========================================

FEATURE_NEW_UI=false
FEATURE_BETA_FEATURES=false
```

### Python/Django Application
```bash
# ===========================================
# Django Configuration
# ===========================================

# Core Settings
SECRET_KEY=your-secret-key-here-make-it-long
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Application
DJANGO_SETTINGS_MODULE=config.settings.development
WSGI_APPLICATION=config.wsgi.application

# ===========================================
# Database
# ===========================================

DATABASE_URL="postgres://postgres:postgres@localhost:5432/django_dev"

# Or individual settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# ===========================================
# Cache & Sessions
# ===========================================

REDIS_URL="redis://localhost:6379/0"
CACHE_BACKEND=django.core.cache.backends.redis.RedisCache

SESSION_ENGINE=django.contrib.sessions.backends.cache

# ===========================================
# Email
# ===========================================

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_username
EMAIL_HOST_PASSWORD=your_password
DEFAULT_FROM_EMAIL="noreply@example.com"

# ===========================================
# Static & Media Files
# ===========================================

STATIC_URL=/static/
MEDIA_URL=/media/

# AWS S3 (for production)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=my-bucket
AWS_S3_REGION_NAME=us-east-1

# ===========================================
# Security
# ===========================================

CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
CSRF_TRUSTED_ORIGINS="http://localhost:3000"

# ===========================================
# Celery
# ===========================================

CELERY_BROKER_URL="redis://localhost:6379/1"
CELERY_RESULT_BACKEND="redis://localhost:6379/2"
```

### Docker / Microservices
```bash
# ===========================================
# Container Configuration
# ===========================================

# Docker
COMPOSE_PROJECT_NAME=myproject
DOCKER_BUILDKIT=1

# Registry
REGISTRY_URL=ghcr.io
IMAGE_TAG=latest

# ===========================================
# Service Ports
# ===========================================

API_PORT=8080
WEB_PORT=3000
DB_PORT=5432
REDIS_PORT=6379
RABBITMQ_PORT=5672
RABBITMQ_MANAGEMENT_PORT=15672

# ===========================================
# Service Configuration
# ===========================================

# API Service
API_HOST=0.0.0.0
API_WORKERS=4
API_TIMEOUT=30

# Database
POSTGRES_DB=appdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_password_here

# Redis
REDIS_PASSWORD=

# RabbitMQ
RABBITMQ_DEFAULT_USER=rabbit
RABBITMQ_DEFAULT_PASS=rabbit_password_here

# ===========================================
# Observability
# ===========================================

# Logging
LOG_LEVEL=info
LOG_FORMAT=json

# Metrics
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001

# Tracing
JAEGER_AGENT_HOST=jaeger
JAEGER_AGENT_PORT=6831
```

## Security Guidelines

### In .env.example (safe to commit)
```bash
# Use placeholder values that are clearly not real
API_KEY=your_api_key_here
SECRET_KEY=replace_with_secure_random_string
DATABASE_PASSWORD=change_this_password
```

### Never Commit
```bash
# Real secrets - add to .gitignore
.env
.env.local
.env.*.local
```

### Secret Generation Notes
Include comments for generating secrets:
```bash
# Generate with: openssl rand -hex 32
JWT_SECRET=your_secret_here

# Generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DJANGO_SECRET_KEY=your_secret_here
```

## Validation Checklist

Before outputting, verify:
- [ ] All variable names are SCREAMING_SNAKE_CASE
- [ ] No real secrets in .env.example
- [ ] Placeholder values are obvious (contain "your_", "_here", etc.)
- [ ] Related variables are grouped with section headers
- [ ] Comments explain non-obvious variables
- [ ] URLs are properly quoted
- [ ] Boolean values are lowercase strings

## Example Invocations

**Prompt:** "Create .env.example for a Next.js app with Prisma and Stripe"
**Output:** Complete `.env.example` with database, auth, and Stripe sections.

**Prompt:** "Generate env file for Django REST API"
**Output:** Complete `.env.example` with Django-specific settings and security config.

**Prompt:** "Environment variables for docker-compose microservices setup"
**Output:** Complete `.env` with service ports, database credentials, and container config.
