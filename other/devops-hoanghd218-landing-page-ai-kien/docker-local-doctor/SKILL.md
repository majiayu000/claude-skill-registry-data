---
name: docker-local-doctor
description: Run comprehensive health check on docker-local environment - diagnose configuration, services, and connectivity
---

# Docker-Local Doctor Skill

## Overview

This skill performs a comprehensive health check of the docker-local environment, diagnosing:
- System requirements
- Docker configuration
- Service health
- Network connectivity
- Project configurations
- Potential conflicts

## Activation

Use this skill when:
- User reports issues with their environment
- Setting up a new machine
- After updates or changes
- Periodic health verification
- Before creating new projects

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

## Process

### 1. Run Docker-Local Doctor

```bash
# Full diagnostic
docker-local doctor

# This checks:
# - Docker version and daemon
# - Docker Compose version
# - PHP and Composer versions
# - Configuration files
# - Container health
# - Network connectivity
# - DNS resolution
# - SSL certificates
```

### 2. Check System Requirements

```bash
# Docker version (24.0+)
docker --version

# Docker Compose (2.20+)
docker compose version

# PHP (8.2+)
php --version

# Composer (2.6+)
composer --version
```

### 3. Verify Configuration

```bash
# Check config exists
ls -la ~/.config/docker-local/

# View configuration
docker-local config

# Verify projects directory
ls -la ~/projects/
```

### 4. Test Services

```bash
# Check all containers
docker-local status

# Test database connectivity
docker exec mysql mysqladmin ping -h localhost -u root -psecret 2>/dev/null && echo "MySQL: OK"
docker exec postgres pg_isready -U laravel 2>/dev/null && echo "PostgreSQL: OK"
docker exec redis redis-cli ping 2>/dev/null && echo "Redis: OK"
```

### 5. Check Network

```bash
# Verify Docker network
docker network ls | grep laravel-dev

# Test DNS resolution (if configured)
ping -c 1 mysql.localhost 2>/dev/null && echo "DNS: OK"

# Check Traefik
curl -sk https://traefik.localhost 2>/dev/null && echo "Traefik: OK"
```

### 6. Audit Project Configurations

```bash
# Check all projects for conflicts
docker-local env:check --all

# This checks:
# - Database names (unique per project)
# - Redis DB numbers (no overlap)
# - Cache prefixes (unique)
# - MinIO buckets (unique)
# - Reverb credentials (unique)
```

### 7. Check Certificates

```bash
# Verify SSL certificates exist
ls -la ~/.config/docker-local/certs/

# Check certificate validity
openssl x509 -in ~/.config/docker-local/certs/localhost.pem -noout -dates 2>/dev/null
```

## Diagnostic Report Format

```
Docker-Local Health Check
=========================

System Requirements:
  [OK] Docker 24.0.7 (required: 24.0+)
  [OK] Docker Compose 2.24.5 (required: 2.20+)
  [OK] PHP 8.3.0 (required: 8.2+)
  [OK] Composer 2.7.1 (required: 2.6+)

Configuration:
  [OK] Config directory exists
  [OK] config.json valid
  [OK] .env file present
  [OK] Projects directory exists

Services:
  [OK] Docker daemon running
  [OK] php container healthy
  [OK] mysql container healthy
  [OK] postgres container healthy
  [OK] redis container healthy
  [OK] traefik container healthy
  [OK] nginx container healthy

Network:
  [OK] laravel-dev network exists
  [OK] Traefik responding
  [OK] SSL certificates valid

Projects:
  [OK] blog - no conflicts
  [OK] api - no conflicts
  [WARN] shop - Redis DB overlap with 'blog'

Recommendations:
  - Fix Redis DB conflict in ~/projects/shop/.env
```

## Common Issues Detected

### Version Mismatch
```
[FAIL] Docker 23.0.0 (required: 24.0+)
```
**Fix:** Update Docker to latest version

### Missing Configuration
```
[FAIL] config.json not found
```
**Fix:** Run `docker-local init`

### Service Not Running
```
[FAIL] mysql container not running
```
**Fix:** Run `docker-local up`

### Project Conflicts
```
[WARN] Redis DB conflict between projects
```
**Fix:** Update .env with unique REDIS_*_DB values

### Certificate Expired
```
[WARN] SSL certificate expired
```
**Fix:** Run `docker-local init --certs`

## Resolution Commands

After diagnosis, provide specific fix commands:

```bash
# Reinitialize environment
docker-local init

# Restart services
docker-local restart

# Fix DNS
sudo docker-local setup:dns

# Regenerate certificates
docker-local init --certs

# Clean and restart
docker-local clean
docker-local up
```

$ARGUMENTS
