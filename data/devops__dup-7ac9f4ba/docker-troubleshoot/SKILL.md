---
name: docker-troubleshoot
description: Diagnose container failures, networking issues, permissions, and port conflicts
---

# Docker Troubleshooting Skill

## Overview

This skill helps diagnose and resolve common Docker issues:
- Container startup failures
- Networking problems
- Permission errors
- Port conflicts
- Data persistence issues
- Health check failures

## Process

### 1. Consult Documentation

Read relevant documentation:
- `17-troubleshooting.md` for common issues
- `15-port-conflicts.md` for port problems
- `16-restart-strategies.md` for restart issues

### 2. Diagnose Issue

Gather information:
```bash
# Check container status
docker compose ps -a

# View logs
docker compose logs servicename

# Check configuration
docker compose config

# Inspect container
docker inspect containername
```

### 3. Apply Solution

## Common Issues and Solutions

### Container Won't Start

**Diagnosis:**
```bash
docker compose logs servicename
docker inspect --format='{{.State.ExitCode}}' containername
```

**Solutions:**
- Check logs for error messages
- Verify configuration syntax
- Check dependencies are running
- Verify image exists

### Port Already in Use

**Diagnosis:**
```bash
lsof -i :3000
# or
netstat -tulpn | grep 3000
```

**Solutions:**
```bash
# Kill process
kill $(lsof -t -i:3000)

# Or change port in compose
ports:
  - "3001:3000"
```

### Permission Denied

**Diagnosis:**
```bash
docker compose exec app ls -la /app/data
```

**Solutions:**
```yaml
# Fix in compose
services:
  app:
    user: "1000:1000"

# Or fix in container
docker compose exec -u root app chown -R appuser:appgroup /app/data
```

### Data Disappearing

**Diagnosis:**
```bash
docker volume ls
docker compose config | grep -A5 "volumes:"
```

**Solutions:**
```yaml
# Use named volumes instead of anonymous
volumes:
  - postgres_data:/var/lib/postgresql/data  # Named (persists)
  # NOT: - /var/lib/postgresql/data  # Anonymous (deleted)
```

### Container Can't Reach Other Container

**Diagnosis:**
```bash
docker network inspect networkname
docker compose exec app ping db
docker compose exec app nslookup db
```

**Solutions:**
```yaml
# Ensure same network
services:
  app:
    networks:
      - backend
  db:
    networks:
      - backend

networks:
  backend:
```

### Health Check Failing

**Diagnosis:**
```bash
docker inspect --format='{{json .State.Health}}' containername | jq
```

**Solutions:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s  # Give time to start
```

### Out of Disk Space

**Diagnosis:**
```bash
docker system df
docker system df -v
```

**Solutions:**
```bash
# Clean unused resources
docker system prune -a --volumes
```

### Build Cache Issues

**Solutions:**
```bash
docker compose build --no-cache
docker builder prune -a
```

## Debugging Commands

```bash
# Shell into running container
docker compose exec app sh

# Shell into failed container
docker compose run --entrypoint sh app

# View resource usage
docker stats

# View container processes
docker compose top

# View real-time events
docker events

# Copy files from container
docker compose cp app:/app/logs ./logs
```

## Quick Diagnostic Checklist

1. **Check if container is running:** `docker compose ps`
2. **Check logs:** `docker compose logs servicename`
3. **Check network:** `docker network ls`
4. **Check volumes:** `docker volume ls`
5. **Check resources:** `docker stats`
6. **Validate config:** `docker compose config`
7. **Check disk space:** `docker system df`

## Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| "port is already allocated" | Port in use | Kill process or change port |
| "network not found" | Missing network | Create network or check name |
| "volume not found" | Missing volume | Create volume or check name |
| "no such service" | Service name typo | Check compose.yaml |
| "unauthorized" | Auth issue | `docker login` |
| "image not found" | Missing image | `docker compose pull` |
| "permission denied" | File permissions | Fix ownership/permissions |
| "out of memory" | Memory limit | Increase limit or optimize app |
