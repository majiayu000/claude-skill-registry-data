---
name: docker-local-status
description: Check docker-local environment status - all services, containers, and project accessibility
---

# Docker-Local Status Skill

## Overview

This skill checks the complete status of the docker-local development environment, including:
- Docker daemon status
- Container states
- Service health
- Project accessibility
- Network connectivity

## Activation

Use this skill when:
- User wants to know if Docker is running
- User asks about service status
- User needs to verify their environment
- Troubleshooting connectivity issues

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

### 1. Check Docker Installation

```bash
# Verify docker-local is installed
which docker-local

# Check Docker daemon
docker info > /dev/null 2>&1 && echo "Docker is running" || echo "Docker is NOT running"
```

### 2. Check Environment Status

```bash
# Full status report
docker-local status

# This shows:
# - All container states
# - Health check status
# - Port bindings
# - Uptime
```

### 3. Check Container States

```bash
# List all docker-local containers
docker compose -f ~/.config/docker-local/docker-compose.yml ps -a

# Or using docker-local
docker-local status
```

### 4. Verify Services

Check each service individually if needed:

```bash
# Check specific logs
docker-local logs mysql
docker-local logs postgres
docker-local logs redis
docker-local logs traefik
docker-local logs nginx
docker-local logs mailpit
docker-local logs minio
```

### 5. Check Project Accessibility

```bash
# List all projects with their status
docker-local list

# This shows:
# - Project name
# - URL (https://project.test)
# - Status (accessible, DNS ok, not configured)
```

### 6. Test Connections

```bash
# Test database connections
docker exec mysql mysqladmin ping -h localhost -u root -psecret

# Test Redis
docker exec redis redis-cli ping

# Test PostgreSQL
docker exec postgres pg_isready -U laravel
```

## Expected Output

A healthy environment shows:
- All containers in "Up" state
- Health checks passing (healthy)
- Projects accessible via *.test domains
- Database connections working

## Common Issues

### Docker Not Running
```
Docker is NOT running
```
**Solution:** Start Docker Desktop (macOS/Windows) or `sudo systemctl start docker` (Linux)

### Containers Not Started
```
Container php: Exited
```
**Solution:** Run `docker-local up` to start containers

### Port Conflicts
```
Error: Port 3306 already in use
```
**Solution:** Stop the conflicting service or change the port in config

### DNS Not Configured
```
Status: DNS not configured
```
**Solution:** Run `sudo docker-local setup:dns` or add entries to /etc/hosts

## Output Format

Report the status in a clear format:

```
Docker-Local Status
==================

Docker Daemon: Running
Environment: Up

Services:
  - php:      Running (healthy)
  - mysql:    Running (healthy)
  - postgres: Running (healthy)
  - redis:    Running (healthy)
  - traefik:  Running (healthy)
  - nginx:    Running (healthy)
  - mailpit:  Running (healthy)
  - minio:    Running (healthy)

Projects:
  - blog:  https://blog.test  (accessible)
  - api:   https://api.test   (accessible)
```

$ARGUMENTS
