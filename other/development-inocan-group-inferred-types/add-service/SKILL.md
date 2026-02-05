---
name: add-service
description: Add a new Docker Compose service with automatic DNS configuration (OVH) and SSL certificates. Use when adding new web services to the homelab infrastructure.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash(python3:*), Bash(docker compose:*), Bash(docker-compose:*), Bash(sudo mkdir:*), Bash(sudo chown:*), Bash(curl:*), Bash(dig:*)
---

# Add Docker Service with DNS

This skill adds a new service to the Docker Compose homelab with:
1. Automatic DNS record creation via OVH API (if configured)
2. Service YAML file creation in services/
3. SSL certificate provisioning via Let's Encrypt
4. Service startup and verification

## Prerequisites

- `.env` file with `DOMAIN` configured
- OVH API credentials in `.env` (optional, for DNS automation)
- `scripts/ovh-dns.py` script available

## Required Information

Before adding a service, gather:
- **Service name**: e.g., `gitea`, `nextcloud`, `grafana`
- **Docker image**: e.g., `gitea/gitea`, `nextcloud:latest`
- **Subdomain**: e.g., `git` for git.${DOMAIN}
- **Internal port**: The port the container exposes (check Docker Hub)

## Step-by-Step Process

### 1. Read configuration

First, read the DOMAIN from .env:
```bash
source .env && echo "Domain: $DOMAIN"
```

### 2. Add DNS Record (if OVH configured)

```bash
python3 scripts/ovh-dns.py add <subdomain>
```

Verify DNS propagation:
```bash
python3 scripts/ovh-dns.py check <subdomain>
dig +short <subdomain>.${DOMAIN}
```

### 3. Create Service File

Create `services/<service-name>.yml`:

```yaml
# =============================================================================
# <Service Name> - <Brief Description>
# =============================================================================
# Usage: docker compose -f docker-compose.yml -f services/<service-name>.yml up -d
# =============================================================================

services:
  <service-name>:
    image: <docker-image>
    container_name: <service-name>
    logging:
      options:
        max-size: "10m"
        max-file: "3"
    environment:
      - PUID=${PUID:-1000}
      - PGID=${PGID:-1000}
      - TZ=${TZ:-Europe/Paris}
      - VIRTUAL_HOST=<subdomain>.${DOMAIN}
      - VIRTUAL_PORT=<internal-port>
      - LETSENCRYPT_HOST=<subdomain>.${DOMAIN}
      - LETSENCRYPT_EMAIL=${LETSENCRYPT_EMAIL}
    volumes:
      - /data/<service-name>:/config
    networks:
      - proxy-tier
    restart: unless-stopped
    depends_on:
      - letsencrypt-companion

networks:
  proxy-tier:
    external: true
```

### 4. Create Data Directory

```bash
sudo mkdir -p /data/<service-name>
sudo chown -R $(id -u):$(id -g) /data/<service-name>
```

### 5. Start Service

```bash
docker compose -f docker-compose.yml -f services/<service-name>.yml up -d
docker compose -f docker-compose.yml -f services/<service-name>.yml logs -f <service-name>
```

### 6. Verify SSL

Wait 1-2 minutes for Let's Encrypt, then:
```bash
source .env
curl -sI https://<subdomain>.${DOMAIN} | head -5
```

### 7. Update Documentation

If the service should be documented, add it to:
- `services/README.md` - Service catalog
- `CLAUDE.md` - Main documentation (if significant)

## Common Service Configurations

### LinuxServer.io Images (Radarr, Sonarr, Lidarr, etc.)
- Port: Usually 8989 (Sonarr), 7878 (Radarr), 8686 (Lidarr)
- Volumes: `/config` for settings
- Environment: PUID, PGID, TZ

### Services needing /data access
Add volume mapping:
```yaml
volumes:
  - /data/<service-name>:/config
  - /data/media:/data/media
  - /data/downloads:/data/downloads
```

## Troubleshooting

### DNS not resolving
- Wait 5-10 minutes for propagation
- Check with: `dig +short <subdomain>.${DOMAIN}`
- Verify record exists: `python3 scripts/ovh-dns.py list`

### SSL certificate not generated
- Check letsencrypt-companion logs: `docker compose logs letsencrypt-companion`
- Ensure DNS resolves to correct IP
- Verify VIRTUAL_HOST and LETSENCRYPT_HOST match

### Service not accessible
- Check service is running: `docker compose ps`
- Check service logs: `docker compose -f docker-compose.yml -f services/<name>.yml logs <service>`
- Verify VIRTUAL_PORT matches exposed port
- Ensure service is on proxy-tier network

## Rollback

If something goes wrong:
```bash
# Stop and remove service
docker compose -f docker-compose.yml -f services/<name>.yml down

# Remove DNS record (if created)
python3 scripts/ovh-dns.py delete <subdomain>

# Remove service file
rm services/<name>.yml
```
