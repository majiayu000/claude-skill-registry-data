---
name: cf-tunnel-deploy
description: Deploy local services to public internet via Cloudflare Tunnel with custom domain. Use when user wants to expose local Docker service to public, set up Cloudflare tunnel, configure cloudflared, or make local service accessible via custom domain. Handles DNS pollution issues, SSL configuration, and Docker Compose integration.
---

# Cloudflare Tunnel Deploy

Deploy local services to public internet using Cloudflare Tunnel with custom domain.

## Prerequisites

- Cloudflare account with a domain
- Docker installed
- `cloudflared` CLI installed locally

## Quick Start Workflow

### 1. Login to Cloudflare (one-time)

```bash
cloudflared tunnel login
```

This creates `~/.cloudflared/cert.pem`.

### 2. Create Named Tunnel

```bash
cloudflared tunnel create <tunnel-name>
```

This creates credentials file: `~/.cloudflared/<tunnel-id>.json`

### 3. Create Tunnel Config

Create `~/.cloudflared/config-<service>.yml`:

```yaml
tunnel: <tunnel-id>
credentials-file: /etc/cloudflared/<tunnel-id>.json
protocol: http2

ingress:
  - hostname: <subdomain>.<domain>
    service: http://host.docker.internal:<port>
    originRequest:
      connectTimeout: 180s
      noTLSVerify: true
  - service: http_status:404
```

### 4. Add DNS Route

```bash
cloudflared tunnel route dns -f <tunnel-id> <subdomain>.<domain>
```

### 5. Configure Cloudflare SSL (CRITICAL)

In Cloudflare Dashboard: `SSL/TLS` -> `Overview` -> Set to **Flexible** (not Full).

### 6. Add to Docker Compose

See [references/docker-compose.md](references/docker-compose.md) for template.

## Common Issues & Solutions

See [references/troubleshooting.md](references/troubleshooting.md) for:
- DNS pollution (198.18.x.x fake IPs)
- TLS handshake errors
- 404 from Cloudflare
- host.docker.internal not accessible

## Verification

```bash
# Check tunnel status
cloudflared tunnel list
cloudflared tunnel info <tunnel-name>

# Test via proxy (if DNS polluted locally)
curl -x http://127.0.0.1:<proxy-port> https://<subdomain>.<domain>/health
```
