---
name: docker-local-troubleshoot
description: Diagnose and fix docker-local issues - container failures, connectivity problems, port conflicts, and configuration errors
---

# Docker-Local Troubleshooting Skill

## Overview

This skill helps diagnose and fix common docker-local issues including:
- Container failures and crashes
- Port conflicts
- Permission errors
- Network connectivity problems
- Database connection issues
- DNS and SSL problems

## Activation

Use this skill when:
- User reports Docker errors
- Services won't start
- Projects aren't accessible
- Database connections fail
- SSL/certificate issues
- General "it's not working" complaints

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

## Diagnostic Process

### 1. Quick Fix (Recommended First Step)

Use the `fix` command for automatic diagnosis and resolution:

```bash
# Run all checks and auto-fix what's possible
docker-local fix

# Target specific areas
docker-local fix --dns         # Only check/fix DNS issues
docker-local fix --docker      # Only check/fix Docker daemon
docker-local fix --services    # Only check/fix container services
docker-local fix --hosts       # Only check/fix /etc/hosts

# Additional options
docker-local fix --verbose     # Show detailed diagnostic info
docker-local fix --dry-run     # Show what would be fixed without making changes
```

The fix command automatically detects and resolves:
- Docker daemon not running
- Stopped containers
- Missing systemd-resolved configuration for *.test DNS
- Missing dnsmasq configuration
- /etc/hosts not configured

### 2. Gather Additional Information

```bash
# Check docker-local status
docker-local status

# View recent logs
docker-local logs --tail=50

# Check Docker system
docker info
docker system df
```

### 3. Common Issue Patterns

#### Docker Not Running
```
Error: Docker is not running
```

**Diagnosis:**
```bash
docker info 2>&1
systemctl status docker  # Linux
```

**Fix:**
```bash
# Linux
sudo systemctl start docker

# macOS
open -a Docker

# Windows (WSL2)
# Start Docker Desktop from Windows Start Menu
```

#### Port Already in Use
```
Error: Port 3306 already in use
```

**Diagnosis:**
```bash
# Find what's using the port
lsof -i :3306
netstat -tulpn | grep 3306

# Common ports to check:
# 80, 443 - Traefik/HTTP
# 3306 - MySQL
# 5432 - PostgreSQL
# 6379 - Redis
# 9000, 9001 - MinIO
# 1025, 8025 - Mailpit
```

**Fix:**
```bash
# Kill the process using the port
kill $(lsof -t -i:3306)

# Or change port in config
# Edit ~/.config/docker-local/config.json
```

#### Container Won't Start
```
Container php: Exited (1)
```

**Diagnosis:**
```bash
# Check logs for the failing container
docker-local logs php

# Check exit code
docker inspect --format='{{.State.ExitCode}}' php

# Exit codes:
# 0 - Normal stop
# 1 - Application error
# 137 - Out of memory (OOM killed)
# 139 - Segmentation fault
```

**Fix based on exit code:**
```bash
# Exit 1 - Check application logs
docker-local logs php --tail=100

# Exit 137 - Increase Docker memory
# Docker Desktop > Settings > Resources > Memory

# Restart the container
docker-local restart
```

#### Permission Denied
```
Error: Permission denied
```

**Diagnosis:**
```bash
# Check user permissions
id
groups

# Check project permissions
ls -la ~/projects/

# Check Docker socket
ls -la /var/run/docker.sock
```

**Fix:**
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Fix project permissions
sudo chown -R $USER:$USER ~/projects

# Fix socket permissions (temporary)
sudo chmod 666 /var/run/docker.sock
```

#### Cannot Connect to Database
```
SQLSTATE[HY000] [2002] Connection refused
```

**Diagnosis:**
```bash
# Check if database container is running
docker-local status

# Check database logs
docker-local logs mysql
docker-local logs postgres

# Test connection from inside container
docker exec php php -r "new PDO('mysql:host=mysql;dbname=laravel', 'laravel', 'secret');"
```

**Fix:**
```bash
# Ensure services are running
docker-local up

# Wait for database to be ready (health check)
docker-local status

# Check .env has correct host (mysql, not localhost)
# DB_HOST=mysql
```

#### DNS Not Resolving (*.test domains)
```
Could not resolve host: myapp.test
```

**Diagnosis:**
```bash
# Check if DNS is configured
ping myapp.test

# Check /etc/hosts
cat /etc/hosts | grep test

# Check dnsmasq (if used)
systemctl status dnsmasq  # Linux
```

**Fix:**
```bash
# Option 1: Setup DNS (recommended)
sudo docker-local setup:dns

# Option 2: Add to /etc/hosts
sudo docker-local setup:hosts

# Option 3: Manual hosts entry
echo "127.0.0.1 myapp.test" | sudo tee -a /etc/hosts
```

#### SSL Certificate Issues
```
SSL certificate problem: unable to get local issuer certificate
```

**Diagnosis:**
```bash
# Check SSL certificate status
docker-local ssl:status

# Check certificates exist
ls -la ~/.config/docker-local/certs/

# Check certificate validity
openssl x509 -in ~/.config/docker-local/certs/localhost.pem -noout -dates

# Test HTTPS
curl -vk https://localhost 2>&1 | head -20
```

**Fix:**
```bash
# Regenerate SSL certificates with mkcert
docker-local ssl:regenerate

# Or regenerate during init
docker-local init --certs

# Trust the certificate (browser)
# Import ~/.config/docker-local/certs/localhost.pem

# For mkcert users
mkcert -install
```

#### Projects Not Visible
```
No projects found in ~/projects
```

**Diagnosis:**
```bash
# Check projects directory
ls -la ~/projects/

# Check config
docker-local config | grep projects_path

# Verify project structure
ls -la ~/projects/myapp/artisan
```

**Fix:**
```bash
# Ensure projects are in correct location
mv /path/to/myapp ~/projects/

# Or update config
# Edit ~/.config/docker-local/config.json
# Change projects_path
```

### 4. Full Reset Procedure

If all else fails, perform a complete reset:

```bash
# Stop everything
docker-local down

# Remove all Docker resources
docker system prune -af
docker volume prune -f
docker network prune -f

# Remove docker-local config (backup first)
mv ~/.config/docker-local ~/.config/docker-local.backup

# Reinitialize
docker-local init

# Restart
docker-local up

# Restore projects (they're safe in ~/projects)
docker-local list
```

### 5. Useful Debugging Commands

```bash
# Shell into PHP container
docker-local shell

# Real-time Docker events
docker events

# Container resource usage
docker stats --no-stream

# Network inspection
docker network inspect laravel-dev

# Volume inspection
docker volume ls
docker volume inspect mysql_data

# Compose configuration check
docker compose -f ~/.config/docker-local/docker-compose.yml config
```

## Report Format

After troubleshooting, provide:

1. **Root Cause:** What caused the issue
2. **Solution:** Commands that fix it
3. **Prevention:** How to avoid in future
4. **Verification:** How to confirm it's fixed

```
Issue: MySQL container not starting

Root Cause: Port 3306 already in use by local MySQL installation

Solution:
  sudo systemctl stop mysql  # Stop local MySQL
  docker-local up            # Start docker-local

Prevention:
  - Use docker-local consistently
  - Or change MySQL port in ~/.config/docker-local/config.json

Verification:
  docker-local status        # Should show mysql: Running
  docker-local db:mysql      # Should open MySQL CLI
```

$ARGUMENTS
