---
name: julien-infra-hostinger-docker
description: Docker management for Hostinger VPS srv759970 - container operations, image optimization, WordPress Docker, troubleshooting. Use for any Docker operation, container issues, or image management.
license: Apache-2.0
triggers:
  - docker
  - container
  - docker compose
  - optimize docker
  - container crash
  - docker logs
---

# Hostinger Docker Management

Docker infrastructure for srv759970.hstgr.cloud (30+ containers).

## Server Info

| Property | Value |
|----------|-------|
| **Host** | automation@69.62.108.82 |
| **Base path** | /opt/ |
| **Containers** | 30+ (ML apps, APIs, databases) |

---

## 1. Status & Monitoring

### Quick Status

```bash
ssh srv759970 'docker ps --format "table {{.Names}}\t{{.Status}}"'
ssh srv759970 'docker system df'
```

### Container Stats

```bash
ssh srv759970 'docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}\t{{.CPUPerc}}"'
```

### Logs

```bash
ssh srv759970 'docker logs container-name --tail 50'
ssh srv759970 'docker logs -f container-name'  # Follow
ssh srv759970 'docker logs container-name --tail 100 --timestamps'
```

---

## 2. Container Operations

### Start/Stop/Restart

```bash
ssh srv759970 'docker restart container-name'
ssh srv759970 'docker stop container-name'
ssh srv759970 'docker start container-name'
```

### Deploy Service

```bash
ssh srv759970 << 'EOF'
cd /opt/service-name
docker-compose down
docker-compose up -d
docker-compose logs --tail 20
EOF
```

### Force Recreate (for config changes)

```bash
ssh srv759970 'cd /opt/service && docker-compose down && docker-compose up -d --force-recreate'
```

### Execute Command in Container

```bash
ssh srv759970 'docker exec -it container-name bash'
ssh srv759970 'docker exec container-name ls /app'
ssh srv759970 'docker exec -u root container-name chown -R www-data:www-data /var/www/html'
```

---

## 3. WordPress Docker

### Containers

| Container | Port | Usage |
|-----------|------|-------|
| wordpress-site | 9xxx | WordPress + PHP |
| mysql-site | 3306 | Database |
| wp-cli-site | - | WP-CLI commands |

### Common Commands

```bash
# Status
ssh srv759970 'docker ps | grep wordpress'

# Logs
ssh srv759970 'docker logs wordpress-site --tail 50'

# Restart
ssh srv759970 'cd /opt/wordpress-site && docker-compose restart'

# WP-CLI
ssh srv759970 'docker exec wp-cli-site wp plugin list'
ssh srv759970 'docker exec wp-cli-site wp user list'

# Fix permissions
ssh srv759970 'docker exec -u root wordpress-site chown -R www-data:www-data /var/www/html'
```

---

## 4. Image Management

### List Images

```bash
ssh srv759970 'docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"'
```

### Cleanup

```bash
# Dangling images (safe)
ssh srv759970 'docker image prune -f'

# Old images (>30 days)
ssh srv759970 'docker image prune -a --filter "until=720h"'

# Unused volumes
ssh srv759970 'docker volume prune -f'
```

### Build & Deploy

```bash
ssh srv759970 << 'EOF'
cd /opt/service
docker-compose build --no-cache
docker-compose up -d --force-recreate
docker image prune -f
EOF
```

---

## 5. Troubleshooting

### ContainerConfig KeyError

```bash
docker-compose down && docker-compose up -d --force-recreate
```

### Network has active endpoints

```bash
# Skip down, use only:
docker-compose up -d --force-recreate
```

### Wrong CMD in container

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Container keeps restarting

```bash
# Check logs
docker logs container-name --tail 100

# Check exit code
docker inspect container-name | grep ExitCode

# Check memory limits
docker stats --no-stream container-name
```

### Permission denied (scp)

Use cat with heredoc instead:
```bash
ssh srv759970 "cat > /opt/service/Dockerfile" << 'EOF'
# Dockerfile content here
EOF
```

---

## 6. Optimization

### Multi-stage Dockerfile Template

```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

### Best Practices

1. Order layers: deps before code
2. Use multi-stage builds
3. Combine RUN commands
4. Add .dockerignore
5. Use --no-cache-dir for pip

---

## Quick Reference

```bash
# Status
ssh srv759970 'docker ps && docker system df'

# Restart service
ssh srv759970 'cd /opt/service && docker-compose restart'

# Logs
ssh srv759970 'docker logs container --tail 50'

# Cleanup
ssh srv759970 'docker image prune -f && docker volume prune -f'

# Full redeploy
ssh srv759970 'cd /opt/service && docker-compose down && docker-compose build --no-cache && docker-compose up -d'
```
