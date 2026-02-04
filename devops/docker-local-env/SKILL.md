---
name: docker-local-env
description: Check and manage .env configuration for docker-local projects - conflict detection, unique IDs, isolation settings
---

# Docker-Local Environment Skill

## Overview

This skill manages .env configuration for docker-local projects:
- Verify .env settings
- Detect conflicts between projects
- Generate unique isolation IDs
- Update existing configurations

## MANDATORY: Prerequisite Check

**Before ANY docker-local command, verify installation:**

```bash
which docker-local > /dev/null 2>&1
```

**If docker-local is NOT found:**
1. Stop and ask the user if they want to install it
2. If yes, install via: `composer global require mwguerra/docker-local`
3. Add to PATH: `export PATH="$HOME/.composer/vendor/bin:$PATH"`
4. Initialize: `docker-local init`
5. Verify: `which docker-local && docker-local --version`

## Understanding Environment Files

Docker-local uses **two separate .env files**:

| File | Purpose | Location |
|------|---------|----------|
| Docker .env | Container configuration | `~/.config/docker-local/.env` |
| Laravel .env | Application settings | `~/projects/<project>/.env` |

### Docker .env (Infrastructure)

Controls how containers are built:
```bash
PROJECTS_PATH=~/projects
MYSQL_PORT=3306
MYSQL_ROOT_PASSWORD=secret
XDEBUG_ENABLED=true
```

### Laravel .env (Application)

Controls how Laravel connects to services:
```bash
DB_HOST=mysql                 # Docker service name
DB_PORT=3306
REDIS_HOST=redis
MAIL_HOST=mailpit
```

**Key insight:** Services have different addresses:
- From host: `localhost:3306`
- From container: `mysql:3306`

## Environment Commands

### Check Current Project

```bash
# Verify .env configuration
docker-local env:check

# Checks:
# - Service hostnames (mysql vs localhost)
# - Required variables present
# - Redis DB numbers
# - Cache prefix
```

### Audit All Projects

```bash
# Check ALL projects for conflicts
docker-local env:check --all

# Detects:
# - Duplicate database names
# - Overlapping Redis DBs
# - Duplicate cache prefixes
# - Shared MinIO buckets
```

### Generate New .env

```bash
# Create new .env with unique IDs
docker-local make:env

# Generates:
# - Unique CACHE_PREFIX
# - Available REDIS_*_DB numbers
# - Unique REVERB credentials
# - Correct service hostnames
```

### Update Existing .env

```bash
# Update .env with current settings
docker-local update:env

# Preserves:
# - Custom settings
# - API keys
# - User modifications
```

## Isolation Settings

### Database Isolation

Each project gets its own database:
```bash
DB_DATABASE=myapp           # Main database
# Also created: myapp_testing
```

### Redis Isolation

Each project uses 3 Redis databases:
```bash
REDIS_CACHE_DB=0
REDIS_SESSION_DB=1
REDIS_QUEUE_DB=2
```

**Allocation pattern:**
| Project # | Cache | Session | Queue |
|-----------|-------|---------|-------|
| 1 | 0 | 1 | 2 |
| 2 | 3 | 4 | 5 |
| 3 | 6 | 7 | 8 |
| 4 | 9 | 10 | 11 |
| 5 | 12 | 13 | 14 |

### Cache Prefix Isolation

```bash
CACHE_PREFIX=myapp_
```

Prevents cache key collisions between projects.

### MinIO Bucket Isolation

```bash
AWS_BUCKET=myapp
```

Each project gets its own S3 bucket.

### Reverb/WebSocket Isolation

```bash
REVERB_APP_ID=123456
REVERB_APP_KEY=random-key
REVERB_APP_SECRET=random-secret
```

Each project gets unique WebSocket credentials.

## Conflict Detection

### Example Conflict Report

```
┌─ Environment Check: ~/projects/shop ─────────────────────────────┐

✓ Database Configuration
  DB_HOST: mysql (correct)
  DB_DATABASE: shop

✓ Redis Configuration
  CACHE_DB: 6
  SESSION_DB: 7
  QUEUE_DB: 8

⚠ CACHE_PREFIX Conflict
  Current: laravel_cache_
  Conflicts with: blog, api

  Fix: Change to 'shop_' in .env:
       CACHE_PREFIX=shop_

✓ MinIO Configuration
  Bucket: shop

└──────────────────────────────────────────────────────────────────┘
```

### Common Conflicts

#### Cache Prefix Conflict
```
⚠ CACHE_PREFIX conflict with 'other-project'
    Both use: laravel_cache_

Why: Cache data shared/corrupted between projects
Fix: CACHE_PREFIX=unique_project_name_
```

#### Redis DB Overlap
```
⚠ REDIS_CACHE_DB conflict
    Both projects use DB 0

Why: Cache data mixed between projects
Fix: Use next available set (3, 4, 5)
```

#### Database Name Collision
```
⚠ DB_DATABASE conflict
    Both projects use: laravel

Why: Data will be shared/overwritten
Fix: Use unique database name per project
```

## Required .env Variables

### Core Settings
```bash
APP_NAME=MyApp
APP_KEY=base64:...
APP_ENV=local
APP_DEBUG=true
APP_URL=https://myapp.test
```

### Database (MySQL)
```bash
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=myapp
DB_USERNAME=laravel
DB_PASSWORD=secret
```

### Database (PostgreSQL)
```bash
DB_CONNECTION=pgsql
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=myapp
DB_USERNAME=laravel
DB_PASSWORD=secret
```

### Redis
```bash
REDIS_HOST=redis
REDIS_PASSWORD=null
REDIS_PORT=6379
REDIS_CACHE_DB=0
REDIS_SESSION_DB=1
REDIS_QUEUE_DB=2
```

### Cache
```bash
CACHE_DRIVER=redis
CACHE_PREFIX=myapp_
```

### Mail
```bash
MAIL_MAILER=smtp
MAIL_HOST=mailpit
MAIL_PORT=1025
```

### S3/MinIO
```bash
FILESYSTEM_DISK=s3
AWS_ENDPOINT=http://minio:9000
AWS_ACCESS_KEY_ID=minio
AWS_SECRET_ACCESS_KEY=minio123
AWS_BUCKET=myapp
AWS_USE_PATH_STYLE_ENDPOINT=true
```

## Fixing Common Issues

### Wrong Database Host
```bash
# Wrong (from host perspective)
DB_HOST=localhost

# Correct (from container)
DB_HOST=mysql
```

### Missing Unique IDs
```bash
# Generate everything
docker-local make:env

# Or manually:
CACHE_PREFIX=myapp_
REDIS_CACHE_DB=3
REDIS_SESSION_DB=4
REDIS_QUEUE_DB=5
```

### Reset to Defaults
```bash
# Backup current .env
cp .env .env.backup

# Generate fresh .env
docker-local make:env

# Restore custom settings
# Manually copy API keys, etc. from backup
```

$ARGUMENTS
