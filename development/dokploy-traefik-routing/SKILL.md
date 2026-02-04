---
name: dokploy-traefik-routing
description: "Configure Traefik labels for routing, SSL/TLS with LetsEncrypt, and advanced routing patterns including Cloudflare DNS challenge. Use when adding web access to Dokploy services."
version: 1.0.0
author: Home Lab Infrastructure Team
---

# Dokploy Traefik Routing

## When to Use This Skill

- When adding web-accessible services to Dokploy templates
- When configuring SSL/TLS certificates via LetsEncrypt
- When setting up custom routing rules (path-based, subdomain)
- When enabling Cloudflare DNS challenge for wildcard certs
- When user asks about "traefik routing" or "SSL setup"

## When NOT to Use This Skill

- For non-HTTP services (raw TCP/UDP ports) - use port mapping instead
- For internal-only services (databases, caches) - no Traefik needed
- For services behind Cloudflare Tunnel - different configuration

## Prerequisites

- Service must connect to `dokploy-network`
- Domain name configured in environment variables
- LetsEncrypt resolver configured in Traefik (standard in Dokploy)

---

## Core Patterns

### Pattern 1: Standard HTTPS Routing (Most Common)

Every web-facing service needs these 6 labels:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.${service}.rule=Host(`${DOMAIN}`)"
  - "traefik.http.routers.${service}.entrypoints=websecure"
  - "traefik.http.routers.${service}.tls.certresolver=letsencrypt"
  - "traefik.http.services.${service}.loadbalancer.server.port=${port}"
  - "traefik.docker.network=dokploy-network"
```

**Explanation:**
1. `traefik.enable=true` - Enable Traefik routing for this service
2. `rule=Host(...)` - Match requests to this domain
3. `entrypoints=websecure` - Use HTTPS (port 443)
4. `tls.certresolver=letsencrypt` - Auto-provision SSL certificate
5. `loadbalancer.server.port` - Internal container port
6. `docker.network` - Which network Traefik uses to reach service

### Pattern 2: Cloudflare DNS Challenge

For wildcard certificates or when HTTP challenge isn't possible:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.${service}.rule=Host(`${DOMAIN}`)"
  - "traefik.http.routers.${service}.entrypoints=websecure"
  - "traefik.http.routers.${service}.tls.certresolver=cloudflare"
  - "traefik.http.routers.${service}.tls.domains[0].main=${BASE_DOMAIN}"
  - "traefik.http.routers.${service}.tls.domains[0].sans=*.${BASE_DOMAIN}"
  - "traefik.http.services.${service}.loadbalancer.server.port=${port}"
  - "traefik.docker.network=dokploy-network"
```

**Note**: Requires Cloudflare API credentials in Traefik configuration.

### Pattern 3: Path-Based Routing

Route different paths to different services:

```yaml
# Main app
labels:
  - "traefik.http.routers.app.rule=Host(`${DOMAIN}`)"
  # ...

# API service
labels:
  - "traefik.http.routers.api.rule=Host(`${DOMAIN}`) && PathPrefix(`/api`)"
  - "traefik.http.routers.api.entrypoints=websecure"
  - "traefik.http.routers.api.tls.certresolver=letsencrypt"
  - "traefik.http.services.api.loadbalancer.server.port=8080"
  - "traefik.docker.network=dokploy-network"
```

### Pattern 4: Subdomain Routing

Route subdomains to different services:

```yaml
# Main app at example.com
labels:
  - "traefik.http.routers.app.rule=Host(`${DOMAIN}`)"
  # ...

# Admin at admin.example.com
labels:
  - "traefik.http.routers.admin.rule=Host(`admin.${DOMAIN}`)"
  - "traefik.http.routers.admin.entrypoints=websecure"
  - "traefik.http.routers.admin.tls.certresolver=letsencrypt"
  - "traefik.http.services.admin.loadbalancer.server.port=9000"
  - "traefik.docker.network=dokploy-network"
```

### Pattern 5: Multiple Routers per Service

When a service needs different ports exposed:

```yaml
labels:
  # Web UI
  - "traefik.http.routers.service-web.rule=Host(`${DOMAIN}`)"
  - "traefik.http.routers.service-web.entrypoints=websecure"
  - "traefik.http.routers.service-web.tls.certresolver=letsencrypt"
  - "traefik.http.services.service-web.loadbalancer.server.port=3000"
  # API endpoint
  - "traefik.http.routers.service-api.rule=Host(`api.${DOMAIN}`)"
  - "traefik.http.routers.service-api.entrypoints=websecure"
  - "traefik.http.routers.service-api.tls.certresolver=letsencrypt"
  - "traefik.http.services.service-api.loadbalancer.server.port=8080"
  - "traefik.docker.network=dokploy-network"
```

### Pattern 6: Middleware for Security Headers

Add security headers or other middleware:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.app.rule=Host(`${DOMAIN}`)"
  - "traefik.http.routers.app.entrypoints=websecure"
  - "traefik.http.routers.app.tls.certresolver=letsencrypt"
  - "traefik.http.routers.app.middlewares=security-headers@docker"
  # Define middleware
  - "traefik.http.middlewares.security-headers.headers.stsSeconds=31536000"
  - "traefik.http.middlewares.security-headers.headers.stsIncludeSubdomains=true"
  - "traefik.http.middlewares.security-headers.headers.contentTypeNosniff=true"
  - "traefik.http.middlewares.security-headers.headers.frameDeny=true"
  - "traefik.http.services.app.loadbalancer.server.port=3000"
  - "traefik.docker.network=dokploy-network"
```

### Pattern 7: CORS Middleware (for APIs)

Enable CORS for API services:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.api.rule=Host(`api.${DOMAIN}`)"
  - "traefik.http.routers.api.entrypoints=websecure"
  - "traefik.http.routers.api.tls.certresolver=letsencrypt"
  - "traefik.http.routers.api.middlewares=cors@docker"
  # CORS middleware
  - "traefik.http.middlewares.cors.headers.accessControlAllowMethods=GET,POST,PUT,DELETE,OPTIONS"
  - "traefik.http.middlewares.cors.headers.accessControlAllowHeaders=Content-Type,Authorization"
  - "traefik.http.middlewares.cors.headers.accessControlAllowOriginList=https://${DOMAIN}"
  - "traefik.http.middlewares.cors.headers.accessControlMaxAge=100"
  - "traefik.http.services.api.loadbalancer.server.port=8080"
  - "traefik.docker.network=dokploy-network"
```

---

## Complete Examples

### Example 1: Basic HTTPS Service (Paaster)

```yaml
services:
  paaster:
    image: wardpearce/paaster:3.1.7
    networks:
      - paaster-net
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.paaster.rule=Host(`${PAASTER_DOMAIN}`)"
      - "traefik.http.routers.paaster.entrypoints=websecure"
      - "traefik.http.routers.paaster.tls.certresolver=letsencrypt"
      - "traefik.http.services.paaster.loadbalancer.server.port=3000"
      - "traefik.docker.network=dokploy-network"
```

### Example 2: Git Service with SSH (Forgejo)

```yaml
services:
  forgejo:
    image: codeberg.org/forgejo/forgejo:9
    ports:
      - "${SSH_PORT:-2222}:22"  # SSH access (raw port, not Traefik)
    networks:
      - forgejo-net
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.forgejo.rule=Host(`${FORGEJO_DOMAIN}`)"
      - "traefik.http.routers.forgejo.entrypoints=websecure"
      - "traefik.http.routers.forgejo.tls.certresolver=letsencrypt"
      - "traefik.http.services.forgejo.loadbalancer.server.port=3000"
      - "traefik.docker.network=dokploy-network"
```

### Example 3: Service with Admin Subdomain

```yaml
services:
  app:
    image: myapp:1.0.0
    networks:
      - app-net
      - dokploy-network
    labels:
      # Main application
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`${DOMAIN}`)"
      - "traefik.http.routers.app.entrypoints=websecure"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"
      - "traefik.http.services.app.loadbalancer.server.port=8080"
      # Admin panel on subdomain
      - "traefik.http.routers.app-admin.rule=Host(`admin.${DOMAIN}`)"
      - "traefik.http.routers.app-admin.entrypoints=websecure"
      - "traefik.http.routers.app-admin.tls.certresolver=letsencrypt"
      - "traefik.http.services.app-admin.loadbalancer.server.port=9000"
      - "traefik.docker.network=dokploy-network"
```

---

## Service Port Reference

Common service ports to use in loadbalancer configuration:

| Service Type | Typical Port | Example |
|-------------|--------------|---------|
| Nginx/Apache | 80 | AnonUpload |
| Node.js apps | 3000 | Paaster, Forgejo |
| Python/Flask | 5000 | Flask apps |
| Django/Gunicorn | 8000 | Paperless-ngx |
| Java/Spring | 8080 | Spring Boot |
| Go apps | 8080 | Various |
| Admin panels | 9000-9999 | Admin UIs |

---

## Quality Standards

### Mandatory Labels
- [ ] `traefik.enable=true`
- [ ] `traefik.http.routers.${name}.rule` - Domain matching
- [ ] `traefik.http.routers.${name}.entrypoints=websecure`
- [ ] `traefik.http.routers.${name}.tls.certresolver=letsencrypt`
- [ ] `traefik.http.services.${name}.loadbalancer.server.port`
- [ ] `traefik.docker.network=dokploy-network`

### Naming Conventions
- Router names must be unique across all services
- Use service name as router name (e.g., `paaster`, `forgejo`)
- For multiple routers on one service, append suffix (e.g., `app-web`, `app-api`)

### Security Requirements
- Always use `websecure` entrypoint (HTTPS)
- Always use `letsencrypt` or `cloudflare` certresolver
- Consider adding security headers middleware for sensitive apps

---

## Common Pitfalls

### Pitfall 1: Missing dokploy-network label
**Issue**: Traefik can't reach service
**Solution**: Always include `traefik.docker.network=dokploy-network`

### Pitfall 2: Duplicate router names
**Issue**: Routing conflicts, unpredictable behavior
**Solution**: Ensure each router name is unique across all compose files

### Pitfall 3: Wrong port in loadbalancer
**Issue**: 502 Bad Gateway errors
**Solution**: Use the internal container port, not the exposed port

### Pitfall 4: Service not on dokploy-network
**Issue**: Traefik can't route to service
**Solution**: Service must be connected to `dokploy-network`

### Pitfall 5: Using HTTP entrypoint
**Issue**: Unencrypted traffic
**Solution**: Always use `websecure`, never `web` for production

---

## Integration

### Skills-First Approach (v2.0+)

This skill is part of the **skills-first architecture** - loaded during Generation phase to add Traefik routing labels after base compose structure is created.

### Related Skills
- `dokploy-compose-structure`: Network setup
- `dokploy-cloudflare-integration`: Cloudflare DNS challenge, Zero Trust
- `dokploy-security-hardening`: Security headers

### Invoked By
- `/dokploy-create` command: Phase 3 (Generation) - Step 2

### Order in Workflow (Progressive Loading)
1. `dokploy-compose-structure`: Create base structure
2. **This skill**: Add Traefik routing labels (Step 2)
3. `dokploy-health-patterns`: Add health checks
4. `dokploy-cloudflare-integration`: Add CF integration (if applicable)
5. `dokploy-environment-config`: Configure environment
6. `dokploy-template-toml`: Create template.toml

See: `.claude/commands/dokploy-create.md` for full workflow
