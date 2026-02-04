---
name: tailscale-deploy
description: |
  Deploy F# applications with Tailscale sidecar for private network access.
  Use when: "deploy", "production", "Tailscale", "docker-compose", "Docker",
  "Portainer", "private network", "deployment", "ship it", "go live",
  "home server", "self-host", "container", "release".
  Creates docker-compose.yml with app + Tailscale sidecar for secure access.
  No public ports, no authentication needed - Tailscale handles it.
allowed-tools: Read, Edit, Write, Grep, Bash
---

# Tailscale Sidecar Deployment

## When to Use This Skill

Activate when:
- User requests "deploy to production", "set up Tailscale"
- Need to create Docker deployment configuration
- Setting up private networking for F# application
- Deploying to Portainer or home server
- User mentions "docker-compose", "deployment", or "Tailscale"

## Prerequisites

- Docker and Docker Compose installed
- Tailscale account (https://tailscale.com)
- F# application with Dockerfile (multi-stage build)
- Target deployment server (Linux recommended)

## Architecture

```
Internet
    ↓ (blocked - no public ports)
Tailscale Network (WireGuard encrypted)
    ↓
Tailscale Sidecar Container
    ↓ (internal network)
F# Application Container
```

**Key Benefits:**
- No public ports exposed
- No authentication needed (Tailscale handles it)
- Access from any device on your Tailnet
- Encrypted WireGuard connections
- Device authorization at network level

## docker-compose.yml

**Location:** Project root

```yaml
version: '3.8'

services:
  # F# Application
  app:
    build: .
    container_name: my-fsharp-app
    restart: unless-stopped
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ASPNETCORE_URLS=http://+:5000
    volumes:
      # Persist SQLite database and files
      - ./data:/app/data
    networks:
      - app-network
    depends_on:
      - tailscale
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s

  # Tailscale Sidecar
  tailscale:
    image: tailscale/tailscale:latest
    container_name: my-fsharp-app-tailscale
    hostname: my-fsharp-app
    restart: unless-stopped
    environment:
      - TS_AUTHKEY=${TS_AUTHKEY}
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_HOSTNAME=my-fsharp-app
      - TS_ACCEPT_DNS=true
      - TS_USERSPACE=false
    volumes:
      - tailscale-data:/var/lib/tailscale
      - /dev/net/tun:/dev/net/tun
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "tailscale", "status"]
      interval: 30s
      timeout: 5s
      retries: 3

networks:
  app-network:
    driver: bridge

volumes:
  tailscale-data:
```

**Configuration Notes:**
- `hostname` - Name that appears in Tailscale admin console
- `TS_HOSTNAME` - DNS name on Tailnet (access via `http://my-fsharp-app`)
- `TS_AUTHKEY` - One-time auth key from Tailscale admin
- `/dev/net/tun` - Required for Tailscale networking
- `cap_add` - Required Linux capabilities for VPN

## Environment Configuration

### .env File

**Location:** Project root (same directory as docker-compose.yml)

```bash
# Tailscale authentication key
TS_AUTHKEY=tskey-auth-xxxxxxxxxxxxx

# Application settings (optional)
ASPNETCORE_ENVIRONMENT=Production
```

**Important:**
- Add `.env` to `.gitignore` (never commit secrets)
- Auth key is one-time use
- Generate new key for each deployment

### Generate Tailscale Auth Key

1. Go to https://login.tailscale.com/admin/settings/keys
2. Click "Generate auth key"
3. **Settings:**
   - ✅ Reusable (if deploying multiple times)
   - ✅ Ephemeral (device removed when container stops)
   - Set expiration (recommend 90 days)
4. Copy key to `.env` file

## Deployment Steps

### Local Development Testing

```bash
# 1. Build application
dotnet build

# 2. Build Docker image
docker build -t my-fsharp-app:latest .

# 3. Start stack
docker-compose up -d

# 4. Check logs
docker-compose logs -f

# 5. Verify Tailscale connection
docker exec my-fsharp-app-tailscale tailscale status

# 6. Access application
# Open browser: http://my-fsharp-app (from any device on Tailnet)
```

### Production Deployment (Portainer)

**Option 1: Using Portainer UI**

1. Login to Portainer (usually `http://server:9000`)
2. Go to **Stacks** → **Add stack**
3. **Name:** `my-fsharp-app`
4. **Build method:** Web editor
5. Paste `docker-compose.yml` content
6. **Environment variables:**
   - Add: `TS_AUTHKEY` = `tskey-auth-xxxxx`
7. Click **Deploy the stack**

**Option 2: Using Git Repository**

1. Push docker-compose.yml to Git repository
2. In Portainer: **Stacks** → **Add stack**
3. **Build method:** Repository
4. Enter Git URL and branch
5. Set environment variables
6. Enable **Automatic updates** (optional)
7. Click **Deploy the stack**

### Verify Deployment

```bash
# Check container status
docker ps

# Check app logs
docker logs my-fsharp-app

# Check Tailscale logs
docker logs my-fsharp-app-tailscale

# Verify Tailscale connection
docker exec my-fsharp-app-tailscale tailscale status

# Check health
docker inspect my-fsharp-app | grep -A 5 Health

# Test app endpoint
curl http://localhost:5000/health  # From server
curl http://my-fsharp-app/health    # From Tailnet device
```

## Accessing the Application

### From Tailnet Devices

**Any device on your Tailnet can access:**
```
http://my-fsharp-app
http://my-fsharp-app:5000
```

**Install Tailscale on devices:**
- Desktop: https://tailscale.com/download
- Mobile: App Store / Google Play
- Login with same Tailscale account

### From Server (Local)

```bash
# Use localhost
curl http://localhost:5000

# Or use Tailscale hostname
curl http://my-fsharp-app:5000
```

## Updating the Application

### Update Code and Redeploy

```bash
# 1. Pull latest code
git pull origin main

# 2. Rebuild Docker image
docker-compose build

# 3. Restart containers
docker-compose up -d

# 4. Check logs
docker-compose logs -f app
```

### In Portainer

1. Go to **Stacks** → your stack
2. Click **Editor**
3. Click **Update the stack**
4. Select **Re-pull image and redeploy**
5. Click **Update**

## Troubleshooting

### Tailscale Connection Issues

```bash
# Check Tailscale status
docker exec my-fsharp-app-tailscale tailscale status

# Check Tailscale logs
docker logs my-fsharp-app-tailscale

# Verify /dev/net/tun exists
ls -la /dev/net/tun

# Restart Tailscale container
docker restart my-fsharp-app-tailscale

# Check network capabilities
docker exec my-fsharp-app-tailscale ip addr show
```

**Common Issues:**

| Issue | Solution |
|-------|----------|
| `/dev/net/tun` not found | Host needs TUN/TAP support: `modprobe tun` |
| Permission denied | Container needs `NET_ADMIN` capability |
| Auth key expired | Generate new key in Tailscale admin |
| Can't reach app | Check app is running: `docker logs my-fsharp-app` |

### Application Issues

```bash
# Check app is running
docker ps | grep my-fsharp-app

# Check app logs
docker logs my-fsharp-app --tail 100

# Check app health
docker exec my-fsharp-app curl -f http://localhost:5000/health

# Check data volume
docker exec my-fsharp-app ls -la /app/data

# Restart app
docker restart my-fsharp-app
```

### Network Issues

```bash
# Check network exists
docker network ls | grep app-network

# Inspect network
docker network inspect app-network

# Check containers can communicate
docker exec my-fsharp-app-tailscale ping -c 3 my-fsharp-app
```

### Data Persistence Issues

```bash
# Check volume exists
docker volume ls | grep tailscale

# Check data directory
ls -la ./data

# Fix permissions (if needed)
sudo chown -R $(id -u):$(id -g) ./data
```

## Multiple Applications

Deploy multiple F# apps on same server:

```yaml
# app1/docker-compose.yml
services:
  app:
    container_name: todo-app
    # ... config
  tailscale:
    container_name: todo-app-tailscale
    hostname: todo-app
    environment:
      - TS_HOSTNAME=todo-app
    # ... config

# app2/docker-compose.yml
services:
  app:
    container_name: notes-app
    # ... config
  tailscale:
    container_name: notes-app-tailscale
    hostname: notes-app
    environment:
      - TS_HOSTNAME=notes-app
    # ... config
```

Access:
- `http://todo-app`
- `http://notes-app`

## Best Practices

### ✅ Do
- Use unique hostnames for each application
- Set auth key expiration (security)
- Use ephemeral keys for temporary deployments
- Monitor Tailscale connection health
- Keep Tailscale image updated
- Persist data in volumes (not containers)
- Use health checks
- Test locally before production deployment

### ❌ Don't
- Expose ports to public internet (defeats Tailscale purpose)
- Commit `.env` file to Git
- Reuse auth keys across environments
- Run without `NET_ADMIN` capability
- Forget to mount `/dev/net/tun`
- Skip health checks
- Deploy without testing locally first

## Security Considerations

**Tailscale Provides:**
- Network-level authentication (device authorization)
- WireGuard encryption
- Access control via Tailscale ACLs
- Automatic certificate management

**Application Still Needs:**
- Input validation (SQL injection, XSS prevention)
- Authorization (who can do what in the app)
- Secure data storage
- Audit logging

**Tailscale Admin:**
- Review connected devices regularly
- Disable/remove unused devices
- Use ACLs to restrict access by group
- Enable MFA for Tailscale account

## Verification Checklist

- [ ] `docker-compose.yml` created
- [ ] `.env` file created with `TS_AUTHKEY`
- [ ] `.env` added to `.gitignore`
- [ ] Tailscale auth key generated
- [ ] Application Dockerfile exists
- [ ] Data directory created
- [ ] Containers start successfully
- [ ] Tailscale shows connected
- [ ] Application accessible via Tailscale hostname
- [ ] Health checks passing
- [ ] Logs show no errors

## Related Skills

- **fsharp-feature** - Complete application to deploy
- **fsharp-backend** - Backend that gets deployed
- **fsharp-frontend** - Frontend that gets deployed

## Related Documentation

- `/docs/07-BUILD-DEPLOY.md` - Docker build and deployment guide
- `/docs/08-TAILSCALE-INTEGRATION.md` - Detailed Tailscale integration
- `CLAUDE.md` - Deployment model overview

## Additional Resources

- [Tailscale Documentation](https://tailscale.com/kb/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Portainer Documentation](https://docs.portainer.io/)
- [ASP.NET Core Deployment](https://docs.microsoft.com/en-us/aspnet/core/host-and-deploy/)
