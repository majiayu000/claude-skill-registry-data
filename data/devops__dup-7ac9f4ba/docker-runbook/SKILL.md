---
name: docker-runbook
description: VaultCPA Docker operations guide including common commands, troubleshooting, deployment procedures, and container management. Use when working with Docker, deploying services, or debugging container issues.
allowed-tools: Read, Bash, Grep, Glob
---

# VaultCPA Docker Runbook

**Version:** 2.0
**Last Updated:** January 2026

This Skill provides operational guidance for managing VaultCPA's Docker infrastructure, including common commands, troubleshooting procedures, and deployment workflows.

## Table of Contents

1. [Quick Reference Commands](#quick-reference-commands)
2. [Service Architecture](#service-architecture)
3. [Starting & Stopping Services](#starting--stopping-services)
4. [Troubleshooting](#troubleshooting)
5. [Database Operations](#database-operations)
6. [Logs & Monitoring](#logs--monitoring)
7. [Deployment Procedures](#deployment-procedures)
8. [Health Checks](#health-checks)

---

## Quick Reference Commands

### Essential Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Restart a single service
docker-compose restart backend

# Rebuild and start
docker-compose up -d --build

# Stop and remove everything (including volumes)
docker-compose down -v
```

### Status Checks

```bash
# Check all service health
docker-compose ps

# Check specific service logs
docker-compose logs backend --tail=50

# Follow logs in real-time
docker-compose logs -f backend

# Check resource usage
docker stats

# Inspect a container
docker-compose inspect backend
```

### Shell Access

```bash
# Access backend container shell
docker-compose exec backend sh

# Access PostgreSQL CLI
docker-compose exec postgres psql -U vaultcpa_user -d vaultcpa

# Run command in container
docker-compose exec backend npm run migrate
```

---

## Service Architecture

### VaultCPA Container Stack

```
┌─────────────────────────────────────────────────────────────┐
│                         nginx (80/443)                       │
│                    Reverse Proxy & SSL                       │
└───────┬────────────────────────────────┬───────────────────┘
        │                                │
        ▼                                ▼
┌──────────────────┐            ┌──────────────────┐
│  frontend:3000   │            │  backend:3080    │
│  Next.js App     │◄───────────┤  Express API     │
└──────────────────┘            └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │  postgres:5432   │
                                │  PostgreSQL 15   │
                                └──────────────────┘
                                         △
                                         │
                                ┌──────────────────┐
                                │  pgadmin:8080    │
                                │  Database UI     │
                                └──────────────────┘
```

### Service Details

| Service   | Port  | Image/Build         | Health Check      | Depends On |
|-----------|-------|---------------------|-------------------|------------|
| postgres  | 5432  | postgres:15-alpine  | pg_isready        | -          |
| backend   | 3080  | ./server/Dockerfile | /health endpoint  | postgres   |
| frontend  | 3000  | ./Dockerfile        | /api/health       | backend    |
| pgadmin   | 8080  | dpage/pgadmin4      | -                 | postgres   |
| nginx     | 80/443| nginx:alpine        | /health endpoint  | all        |

### Network Configuration

```yaml
Network: vaultcpa-network (bridge)
Subnet: 172.20.0.0/16
Bridge: vaultcpa-br0
```

**Services communicate using service names:**
- Frontend → Backend: `http://backend:3080`
- Backend → Database: `postgresql://postgres:5432/vaultcpa`

---

## Starting & Stopping Services

### Development Startup

```bash
# Start all services in foreground (see logs)
docker-compose up

# Start in background (detached)
docker-compose up -d

# Start specific services
docker-compose up -d postgres backend

# Start with rebuild (after code changes)
docker-compose up -d --build

# Start with specific compose file
docker-compose -f docker-compose.dev.yml up -d
```

### Production Startup

```bash
# Use production compose file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Build fresh images
docker-compose build --no-cache

# Deploy with rebuild
docker-compose up -d --build --force-recreate
```

### Stopping Services

```bash
# Stop all services (preserve volumes)
docker-compose down

# Stop specific service
docker-compose stop backend

# Stop and remove volumes (DANGER - deletes data)
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

### Restarting Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Restart with new environment variables
docker-compose up -d --force-recreate backend

# Graceful restart (respects stop_grace_period)
docker-compose restart -t 30 backend
```

---

## Troubleshooting

### Service Won't Start

**Check logs first:**
```bash
docker-compose logs backend

# Look for error messages, stack traces
docker-compose logs backend --tail=100
```

**Common Issues:**

#### 1. Port Already in Use

```bash
# Error: "port is already allocated"

# Find process using port
lsof -i :3080  # macOS/Linux
netstat -ano | findstr :3080  # Windows

# Kill the process or change port in docker-compose.yml
ports:
  - "3081:3080"  # Host:Container
```

#### 2. Database Connection Failed

```bash
# Check if postgres is healthy
docker-compose ps

# Should show "healthy" status
# If not, check postgres logs
docker-compose logs postgres

# Common fixes:
# - Wait for postgres to finish initializing (30s)
# - Verify DATABASE_URL is correct
# - Check network connectivity

# Test connection manually
docker-compose exec backend sh
wget -O- postgres:5432  # Should connect
```

#### 3. Container Keeps Restarting

```bash
# Check restart count
docker-compose ps

# View recent logs
docker-compose logs backend --tail=50

# Common causes:
# - Application crash on startup
# - Missing environment variables
# - Failed health check
# - Port conflict

# Disable restart to see crash
# In docker-compose.yml: restart: "no"
docker-compose up backend  # Run in foreground
```

#### 4. Health Check Failing

```bash
# Check health check configuration
docker-compose inspect backend | grep -A 10 healthcheck

# Test health endpoint manually
docker-compose exec backend wget -O- http://localhost:3080/health

# Common issues:
# - Application not listening on correct port
# - Health endpoint not implemented
# - Database connection blocking startup

# Temporarily disable health check
# In docker-compose.yml: remove healthcheck section
```

#### 5. Build Failures

```bash
# Error during docker-compose build

# Clear build cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker-compose config

# Build with verbose output
docker-compose build --progress=plain backend

# Remove intermediate containers
docker system prune -a
```

---

## Database Operations

### Database Access

```bash
# PostgreSQL CLI
docker-compose exec postgres psql -U vaultcpa_user -d vaultcpa

# Run SQL query
docker-compose exec postgres psql -U vaultcpa_user -d vaultcpa -c "SELECT COUNT(*) FROM clients;"

# Execute SQL file
docker-compose exec -T postgres psql -U vaultcpa_user -d vaultcpa < backup.sql
```

### Migrations

```bash
# Run Prisma migrations (backend container)
docker-compose exec backend npm run migrate

# Or equivalently
docker-compose exec backend npx prisma migrate deploy

# Generate Prisma client
docker-compose exec backend npx prisma generate

# Check migration status
docker-compose exec backend npx prisma migrate status

# Open Prisma Studio
docker-compose exec backend npx prisma studio
```

### Backup & Restore

#### Database Backup

```bash
# Create backup
docker-compose exec -T postgres pg_dump -U vaultcpa_user vaultcpa > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup to container volume
docker-compose exec postgres pg_dump -U vaultcpa_user vaultcpa > /tmp/backup.sql

# Compressed backup
docker-compose exec -T postgres pg_dump -U vaultcpa_user vaultcpa | gzip > backup.sql.gz

# Automated daily backups (cron job)
0 2 * * * /usr/bin/docker-compose -f /path/to/docker-compose.yml exec -T postgres pg_dump -U vaultcpa_user vaultcpa | gzip > /backups/vaultcpa_$(date +\%Y\%m\%d).sql.gz
```

#### Database Restore

```bash
# Restore from backup
docker-compose exec -T postgres psql -U vaultcpa_user -d vaultcpa < backup.sql

# Restore from compressed backup
gunzip -c backup.sql.gz | docker-compose exec -T postgres psql -U vaultcpa_user -d vaultcpa

# Drop and recreate database first (DANGER)
docker-compose exec postgres psql -U vaultcpa_user -c "DROP DATABASE IF EXISTS vaultcpa;"
docker-compose exec postgres psql -U vaultcpa_user -c "CREATE DATABASE vaultcpa;"
docker-compose exec -T postgres psql -U vaultcpa_user -d vaultcpa < backup.sql
```

### Database Reset (Development Only)

```bash
# DANGER: This deletes all data!

# Stop backend to close connections
docker-compose stop backend

# Reset database
docker-compose exec postgres psql -U vaultcpa_user -c "DROP DATABASE vaultcpa;"
docker-compose exec postgres psql -U vaultcpa_user -c "CREATE DATABASE vaultcpa;"

# Restore schema
docker-compose exec -T postgres psql -U vaultcpa_user -d vaultcpa < vaultcpa_schema.sql

# Or run migrations
docker-compose exec backend npx prisma migrate deploy

# Restart backend
docker-compose start backend
```

---

## Logs & Monitoring

### Viewing Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend

# Follow logs (real-time)
docker-compose logs -f backend

# Last N lines
docker-compose logs --tail=100 backend

# Since timestamp
docker-compose logs --since="2024-01-01T00:00:00" backend

# Multiple services
docker-compose logs -f backend frontend

# Save logs to file
docker-compose logs backend > backend.log
```

### Log Filtering

```bash
# Search logs for errors
docker-compose logs backend | grep ERROR

# Count occurrences
docker-compose logs backend | grep ERROR | wc -l

# Show only errors and warnings
docker-compose logs backend | grep -E "ERROR|WARN"

# Timestamps
docker-compose logs -t backend
```

### Resource Monitoring

```bash
# Real-time resource usage
docker stats

# Specific container
docker stats vaultcpa-backend

# All containers with formatting
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# One-time snapshot
docker stats --no-stream
```

### Disk Usage

```bash
# Overall Docker disk usage
docker system df

# Detailed breakdown
docker system df -v

# Container sizes
docker-compose ps -a --format "table {{.Names}}\t{{.Size}}"

# Volume sizes
docker volume ls
docker volume inspect postgres_data
```

---

## Health Checks

### Service Health Status

```bash
# Check all service health
docker-compose ps

# Should show:
# NAME                STATUS                  HEALTH
# vaultcpa-postgres   Up (healthy)
# vaultcpa-backend    Up (healthy)
# vaultcpa-frontend   Up (healthy)
```

### Manual Health Checks

```bash
# PostgreSQL health
docker-compose exec postgres pg_isready -U vaultcpa_user

# Backend health (from host)
curl http://localhost:3080/health

# Backend health (from container)
docker-compose exec backend wget -O- http://localhost:3080/health

# Frontend health
curl http://localhost:3000/api/health

# All services via nginx
curl http://localhost/health
```

### Health Check Endpoints

**Backend `/health` Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "uptime": 12345,
  "database": "connected"
}
```

**Unhealthy Response:**
```json
{
  "status": "unhealthy",
  "error": "Database connection failed",
  "database": "disconnected"
}
```

---

## Deployment Procedures

### Development Deployment

```bash
# 1. Pull latest code
git pull origin main

# 2. Stop services
docker-compose down

# 3. Rebuild images
docker-compose build

# 4. Start services
docker-compose up -d

# 5. Run migrations
docker-compose exec backend npm run migrate

# 6. Verify health
docker-compose ps
curl http://localhost:3080/health
```

### Production Deployment (Zero Downtime)

```bash
# 1. Pull latest code
git pull origin main

# 2. Build new images (don't stop yet)
docker-compose build backend frontend

# 3. Run database migrations (if any)
docker-compose exec backend npx prisma migrate deploy

# 4. Restart services one by one
docker-compose up -d --no-deps --build backend
sleep 10  # Wait for health check
docker-compose up -d --no-deps --build frontend

# 5. Verify deployment
docker-compose ps
curl http://localhost/health

# 6. Check logs for errors
docker-compose logs --tail=50 backend
docker-compose logs --tail=50 frontend
```

### Rollback Procedure

```bash
# 1. Checkout previous version
git checkout <previous-commit-hash>

# 2. Rebuild and restart
docker-compose up -d --build --force-recreate

# 3. Rollback database migrations (if needed)
# This is tricky - best to have backup
docker-compose exec -T postgres psql -U vaultcpa_user -d vaultcpa < backup.sql

# 4. Verify rollback
docker-compose ps
curl http://localhost/health
```

### Environment Variable Updates

```bash
# 1. Update .env file
nano .env

# 2. Recreate containers (preserves volumes)
docker-compose up -d --force-recreate

# OR restart specific service
docker-compose up -d --force-recreate backend
```

---

## Common Scenarios

### Scenario 1: Backend Won't Connect to Database

**Symptoms:**
- Backend container restarting
- Logs show "ECONNREFUSED postgres:5432"

**Solution:**
```bash
# Check postgres is healthy
docker-compose ps postgres

# If not healthy, check logs
docker-compose logs postgres

# Verify DATABASE_URL
docker-compose exec backend env | grep DATABASE_URL

# Test network connectivity
docker-compose exec backend ping postgres

# Restart in correct order
docker-compose restart postgres
sleep 30  # Wait for postgres to be healthy
docker-compose restart backend
```

### Scenario 2: Out of Disk Space

**Symptoms:**
- Build failures
- "no space left on device"

**Solution:**
```bash
# Check Docker disk usage
docker system df

# Clean up stopped containers
docker container prune

# Clean up unused images
docker image prune -a

# Clean up volumes (CAREFUL - this deletes data)
docker volume prune

# Clean up everything (DANGER)
docker system prune -a --volumes

# Free up space on host
df -h  # Check disk usage
# Delete large log files, old backups, etc.
```

### Scenario 3: Slow Performance

**Solution:**
```bash
# Check resource usage
docker stats

# If high CPU/memory:
# - Check for infinite loops in application
# - Review database query performance
# - Check for memory leaks

# Increase Docker resources
# Docker Desktop → Settings → Resources
# - CPU: 4+ cores
# - Memory: 8+ GB

# Optimize database
docker-compose exec postgres psql -U vaultcpa_user -d vaultcpa -c "VACUUM ANALYZE;"
```

### Scenario 4: Network Issues

**Symptoms:**
- Services can't reach each other
- DNS resolution fails

**Solution:**
```bash
# Check network exists
docker network ls | grep vaultcpa

# Recreate network
docker-compose down
docker network rm vaultcpa-network
docker-compose up -d

# Test DNS resolution
docker-compose exec backend ping postgres
docker-compose exec backend nslookup postgres

# Check network configuration
docker network inspect vaultcpa-network
```

---

## Security Best Practices

### Container Security

```yaml
# In docker-compose.yml

services:
  backend:
    # Run as non-root user
    user: "1001:1001"

    # Prevent privilege escalation
    security_opt:
      - no-new-privileges:true

    # Read-only root filesystem (where possible)
    read_only: true
    tmpfs:
      - /tmp

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

### Secrets Management

```bash
# NEVER commit secrets to git
# Use .env files (in .gitignore)

# Rotate secrets regularly
# - JWT_SECRET
# - Database passwords
# - API keys

# Use Docker secrets (Swarm mode)
echo "my_secret_value" | docker secret create jwt_secret -

# Or use environment variable files
docker-compose --env-file .env.production up -d
```

---

## Maintenance Commands

```bash
# Update images
docker-compose pull

# Rebuild after updates
docker-compose up -d --build

# Check for outdated images
docker images | grep vaultcpa

# Remove old images
docker image prune -a --filter "until=24h"

# Backup volumes
docker run --rm -v postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data_backup.tar.gz /data

# Restore volumes
docker run --rm -v postgres_data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/postgres_data_backup.tar.gz --strip 1"
```

---

## Quick Troubleshooting Checklist

When something goes wrong:

- [ ] Check service status: `docker-compose ps`
- [ ] Check logs: `docker-compose logs <service>`
- [ ] Verify environment variables: `docker-compose config`
- [ ] Test health endpoints: `curl http://localhost:<port>/health`
- [ ] Check disk space: `docker system df`
- [ ] Verify network: `docker network inspect vaultcpa-network`
- [ ] Restart service: `docker-compose restart <service>`
- [ ] Check resource usage: `docker stats`
- [ ] Review recent changes: `git log --oneline -10`

---

**When using this Skill:**
1. Always check logs first when troubleshooting
2. Use health checks to verify service status
3. Back up database before major operations
4. Test deployment procedures in development first
5. Monitor resource usage regularly
