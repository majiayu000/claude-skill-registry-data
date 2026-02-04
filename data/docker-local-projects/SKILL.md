---
name: docker-local-projects
description: Manage Laravel projects with docker-local - list, create, clone, and open projects
---

# Docker-Local Projects Skill

## Overview

This skill manages Laravel projects within the docker-local environment:
- List all projects
- Create new Laravel projects
- Clone existing projects
- Open projects in browser/IDE
- Configure project settings

## Activation

Use this skill when:
- User wants to create a new Laravel project
- User needs to list their projects
- User wants to clone an existing repo
- User wants to open a project
- Managing project configurations

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

## Project Commands

### List Projects

```bash
# List all Laravel projects with status
docker-local list

# Output shows:
# NAME                 URL                                 STATUS
# blog                 https://blog.test                   ✓ accessible
# api                  https://api.test                    ○ DNS ok
# shop                 https://shop.test                   ✗ DNS not configured
```

### Create New Project

```bash
# Create with MySQL (default)
docker-local make:laravel myapp

# Create with PostgreSQL + pgvector
docker-local make:laravel myapp --postgres
```

**What gets created automatically:**
- Laravel project via Composer
- Database (MySQL or PostgreSQL) + testing database
- MinIO bucket for file storage
- Unique Redis DB numbers for cache/session/queue
- Unique cache prefix and Reverb credentials
- Configured `.env` with all Docker service connections

**Isolation settings created:**
```
Creating Laravel project: myapp
Database: MySQL
Redis DBs: cache=0, session=1, queue=2

✓ Project created successfully!
✓ MySQL database 'myapp' created
✓ MySQL database 'myapp_testing' created
✓ MinIO bucket 'myapp' created
✓ .env configured with complete isolation

Isolation settings (multi-project):
  ✓ Database: myapp (MySQL)
  ✓ Redis Cache DB: 0
  ✓ Redis Session DB: 1
  ✓ Redis Queue DB: 2
  ✓ Cache Prefix: myapp_
  ✓ MinIO Bucket: myapp
  ✓ Reverb App ID: 847291
```

### Clone Existing Project

```bash
# Clone from GitHub/GitLab
docker-local clone git@github.com:user/repo.git

# Clone with custom name
docker-local clone git@github.com:user/repo.git myapp
```

**Clone process:**
1. Clones repository to ~/projects/
2. Creates database
3. Installs dependencies
4. Generates unique isolation settings
5. Runs migrations

### Open Project

```bash
# Open current project in browser
docker-local open

# Open specific project
docker-local open myapp

# Open services
docker-local open --mail      # Mailpit
docker-local open --minio     # MinIO Console
docker-local open --traefik   # Traefik Dashboard
```

### Open in IDE

```bash
# Open in VS Code (default)
docker-local ide

# Open in PhpStorm
docker-local ide phpstorm

# Open specific project
docker-local ide code myapp
```

## Project Structure

Each project in ~/projects/ is automatically configured:

```
~/projects/
├── blog/                         → https://blog.test
│   ├── .env                      # Project-specific Laravel config
│   ├── app/
│   └── ...
├── api/                          → https://api.test
└── shop/                         → https://shop.test
```

## Project .env Configuration

Projects get these Docker-specific settings:

```bash
# Database - use Docker service names
DB_HOST=mysql                    # or 'postgres' for PostgreSQL
DB_PORT=3306                     # or 5432 for PostgreSQL
DB_DATABASE=myapp
DB_USERNAME=laravel
DB_PASSWORD=secret

# Redis - use Docker service name
REDIS_HOST=redis
REDIS_PORT=6379

# IMPORTANT: Unique isolation values
CACHE_PREFIX=myapp_
REDIS_CACHE_DB=0
REDIS_SESSION_DB=1
REDIS_QUEUE_DB=2

# Mail - use Mailpit
MAIL_HOST=mailpit
MAIL_PORT=1025

# MinIO/S3
AWS_ENDPOINT=http://minio:9000
AWS_ACCESS_KEY_ID=minio
AWS_SECRET_ACCESS_KEY=minio123
AWS_BUCKET=myapp
AWS_USE_PATH_STYLE_ENDPOINT=true
```

## Existing Project Migration

For projects not created by docker-local:

### 1. Copy Project
```bash
cp -r /path/to/project ~/projects/myapp
cd ~/projects/myapp
```

### 2. Create Database
```bash
docker-local db:create myapp
```

### 3. Update .env
```bash
# Edit .env with Docker service names:
DB_HOST=mysql        # NOT localhost
REDIS_HOST=redis     # NOT localhost
MAIL_HOST=mailpit    # NOT localhost
```

### 4. Set Unique Isolation
```bash
# Generate unique settings
docker-local make:env

# Or manually set:
CACHE_PREFIX=myapp_
REDIS_CACHE_DB=3   # Different from other projects
REDIS_SESSION_DB=4
REDIS_QUEUE_DB=5
```

### 5. Install & Migrate
```bash
docker exec -w /var/www/myapp php composer install
docker exec -w /var/www/myapp php php artisan migrate
```

## Check Project Configuration

```bash
# Verify current project .env
docker-local env:check

# Audit ALL projects for conflicts
docker-local env:check --all
```

**Conflict detection example:**
```
┌─ Cross-Project Conflicts ─────────────────────────────────────────┐
  ⚠ CACHE_PREFIX conflict with 'other-project'
    Both projects use: laravel_cache_

  Why: Cache data will be shared/corrupted between projects
  Fix: Change CACHE_PREFIX in one of the projects' .env files
```

## Best Practices

### Naming Conventions
- Use lowercase names
- Use hyphens for multi-word names: `my-blog`
- Keep names short but descriptive

### Before Creating Projects
- Ensure Docker is running: `docker-local status`
- Check for existing projects: `docker-local list`
- Verify DNS is configured: `docker-local doctor`

### After Creating Projects
- Verify accessibility: `docker-local open`
- Check .env configuration: `docker-local env:check`
- Run initial migrations: `docker-local db:fresh`

$ARGUMENTS
