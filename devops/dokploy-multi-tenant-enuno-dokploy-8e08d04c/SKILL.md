---
name: dokploy-multi-tenant
description: "Multi-tenancy patterns for Dokploy templates with network isolation: separate docker networks per tenant, shared infrastructure, and tenant-specific configuration."
version: 1.0.0
author: Home Lab Infrastructure Team
---

# Dokploy Multi-Tenant Patterns

## When to Use This Skill

- When deploying multiple instances of the same template
- When different clients/projects need isolated deployments
- When user asks about "multi-tenant" or "tenant isolation"
- When planning organization-wide deployments

## When NOT to Use This Skill

- For single-instance deployments
- For application-level multi-tenancy (built into app)

## Prerequisites

- Understanding of Docker networking
- Clear tenant identification strategy
- Knowledge of shared vs dedicated resources

---

## Multi-Tenancy Strategy: Network Isolation

This implementation uses **separate Docker networks per tenant** with **shared infrastructure**:

```
┌────────────────────────────────────────────────────────────────┐
│                     Shared Infrastructure                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Traefik    │  │  Monitoring  │  │   Logging    │         │
│  │  (dokploy)   │  │  (shared)    │  │  (shared)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                                                       │
│         │ dokploy-network                                       │
└─────────┼──────────────────────────────────────────────────────┘
          │
    ┌─────┴─────┬─────────────┬─────────────┐
    │           │             │             │
┌───┴───┐   ┌───┴───┐     ┌───┴───┐     ┌───┴───┐
│Tenant1│   │Tenant2│     │Tenant3│     │TenantN│
│  net  │   │  net  │     │  net  │     │  net  │
│       │   │       │     │       │     │       │
│ ┌───┐ │   │ ┌───┐ │     │ ┌───┐ │     │ ┌───┐ │
│ │App│ │   │ │App│ │     │ │App│ │     │ │App│ │
│ │DB │ │   │ │DB │ │     │ │DB │ │     │ │DB │ │
│ └───┘ │   │ └───┘ │     │ └───┘ │     │ └───┘ │
└───────┘   └───────┘     └───────┘     └───────┘
```

**Characteristics:**
- Each tenant has isolated Docker network
- Tenant services cannot communicate with other tenants
- All tenants share Traefik via dokploy-network
- Each tenant has dedicated domain/subdomain

---

## Core Patterns

### Pattern 1: Tenant Network Naming

```yaml
networks:
  ${TENANT_ID}-net:
    driver: bridge
  dokploy-network:
    external: true
```

**Naming Convention:**
- Format: `${tenant_id}-${app_name}-net` or `${tenant_id}-net`
- Examples: `acme-corp-net`, `client-a-net`, `project-123-net`

### Pattern 2: Tenant Domain Strategy

**Subdomain per Tenant:**
```yaml
# tenant1.example.com
# tenant2.example.com
labels:
  - "traefik.http.routers.${TENANT_ID}.rule=Host(`${TENANT_ID}.${BASE_DOMAIN}`)"
```

**Custom Domain per Tenant:**
```yaml
# app.tenant1.com
# app.tenant2.com
labels:
  - "traefik.http.routers.${TENANT_ID}.rule=Host(`${TENANT_DOMAIN}`)"
```

**Path-Based Tenancy (Not Recommended):**
```yaml
# example.com/tenant1
# example.com/tenant2
labels:
  - "traefik.http.routers.${TENANT_ID}.rule=Host(`${DOMAIN}`) && PathPrefix(`/${TENANT_ID}`)"
```

### Pattern 3: Tenant-Specific Environment

```yaml
services:
  app:
    environment:
      TENANT_ID: ${TENANT_ID:?Set tenant identifier}
      TENANT_NAME: ${TENANT_NAME:?Set tenant name}
      TENANT_DOMAIN: ${TENANT_DOMAIN:?Set tenant domain}
```

### Pattern 4: Isolated Volumes per Tenant

```yaml
volumes:
  ${TENANT_ID}-app-data:
    driver: local
  ${TENANT_ID}-postgres-data:
    driver: local
```

**Naming Convention:**
- Format: `${tenant_id}-${service}-${type}`
- Examples: `acme-corp-postgres-data`, `client-a-app-uploads`

---

## Complete Example: Multi-Tenant Template

### docker-compose.yml

```yaml
services:
  app:
    image: myapp:1.0.0
    restart: always
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      # Tenant identification
      TENANT_ID: ${TENANT_ID:?Set tenant identifier}
      TENANT_NAME: ${TENANT_NAME:-${TENANT_ID}}

      # Domain
      APP_DOMAIN: ${TENANT_DOMAIN:?Set tenant domain}
      APP_URL: https://${TENANT_DOMAIN}

      # Database
      DATABASE_URL: postgresql://${DB_USER:-app}:${DB_PASS}@postgres:5432/${DB_NAME:-app}

      # Security
      SECRET_KEY: ${SECRET_KEY:?Set secret key}
    networks:
      - ${TENANT_ID}-net
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.${TENANT_ID}-app.rule=Host(`${TENANT_DOMAIN}`)"
      - "traefik.http.routers.${TENANT_ID}-app.entrypoints=websecure"
      - "traefik.http.routers.${TENANT_ID}-app.tls.certresolver=letsencrypt"
      - "traefik.http.services.${TENANT_ID}-app.loadbalancer.server.port=8080"
      - "traefik.docker.network=dokploy-network"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  postgres:
    image: postgres:16-alpine
    restart: always
    volumes:
      - ${TENANT_ID}-postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${DB_NAME:-app}
      POSTGRES_USER: ${DB_USER:-app}
      POSTGRES_PASSWORD: ${DB_PASS:?Set database password}
    networks:
      - ${TENANT_ID}-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app} -d ${DB_NAME:-app}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

volumes:
  ${TENANT_ID}-postgres-data:
    driver: local

networks:
  ${TENANT_ID}-net:
    driver: bridge
  dokploy-network:
    external: true
```

### template.toml

```toml
# Multi-Tenant Application Template
# Each deployment creates an isolated tenant environment

[variables]
tenant_id = "${username}"  # User provides tenant identifier
tenant_domain = "${domain}"
db_password = "${password:32}"
secret_key = "${base64:64}"

[[config.domains]]
serviceName = "app"
port = 8080
host = "${tenant_domain}"

[config.env]
# ===========================================
# Tenant Configuration
# ===========================================
TENANT_ID = "${tenant_id}"
TENANT_NAME = "${tenant_id}"
TENANT_DOMAIN = "${tenant_domain}"

# ===========================================
# Database
# ===========================================
DB_NAME = "app"
DB_USER = "app"
DB_PASS = "${db_password}"
POSTGRES_DB = "app"
POSTGRES_USER = "app"
POSTGRES_PASSWORD = "${db_password}"

# ===========================================
# Security
# ===========================================
SECRET_KEY = "${secret_key}"
```

---

## Deployment Strategies

### Strategy 1: Subdomain Tenants

Each tenant gets `tenant.example.com`:

```toml
# Dokploy deployment for Tenant "acme"
[config.env]
TENANT_ID = "acme"
TENANT_DOMAIN = "acme.example.com"
```

**DNS Setup:**
```
*.example.com → Your Dokploy server
```

### Strategy 2: Custom Domain Tenants

Each tenant brings their own domain:

```toml
# Dokploy deployment for Tenant with custom domain
[config.env]
TENANT_ID = "acme"
TENANT_DOMAIN = "app.acmecorp.com"
```

**DNS Setup (per tenant):**
```
app.acmecorp.com CNAME your-dokploy-server.example.com
```

### Strategy 3: Project-Based Tenants

Each project is a tenant:

```toml
[config.env]
TENANT_ID = "project-123"
TENANT_DOMAIN = "project-123.projects.example.com"
```

---

## Resource Sharing vs Isolation

### Shared Resources (Cost Effective)

| Resource | Shared | Notes |
|----------|--------|-------|
| Traefik | Yes | Single instance routes all tenants |
| Monitoring | Yes | Central Prometheus/Grafana |
| Logging | Yes | Central logging stack |
| SSL Certs | Yes | LetsEncrypt for all |

### Isolated Resources (Security/Performance)

| Resource | Isolated | Notes |
|----------|----------|-------|
| Docker Network | Yes | Tenant-specific network |
| Database | Yes | Dedicated database per tenant |
| Volumes | Yes | Tenant-specific volumes |
| CPU/Memory | Optional | Use resource limits |

---

## Quality Standards

### Mandatory Requirements
- [ ] Tenant ID used in network name
- [ ] Tenant ID used in volume names
- [ ] Unique router names per tenant
- [ ] Tenant domain configured
- [ ] Isolated networks (no cross-tenant access)

### Naming Conventions
- Network: `${tenant_id}-net` or `${tenant_id}-${app}-net`
- Volume: `${tenant_id}-${service}-data`
- Router: `${tenant_id}-${service}`

---

## Common Pitfalls

### Pitfall 1: Duplicate router names
**Issue**: Two tenants with same router name conflict
**Solution**: Include tenant ID in all router names

### Pitfall 2: Shared volumes
**Issue**: Tenants overwrite each other's data
**Solution**: Include tenant ID in volume names

### Pitfall 3: Cross-tenant network access
**Issue**: Tenants can access each other's services
**Solution**: Each tenant on separate network

### Pitfall 4: Hardcoded tenant ID
**Issue**: Can't deploy multiple instances
**Solution**: Use `${TENANT_ID}` variable everywhere

---

## Migration: Single to Multi-Tenant

To convert existing single-tenant template:

1. **Add TENANT_ID variable:**
```toml
[variables]
tenant_id = "${username}"
```

2. **Update network name:**
```yaml
networks:
  ${TENANT_ID}-net:  # Was: app-net
    driver: bridge
```

3. **Update volume names:**
```yaml
volumes:
  ${TENANT_ID}-postgres-data:  # Was: postgres-data
    driver: local
```

4. **Update router names:**
```yaml
labels:
  - "traefik.http.routers.${TENANT_ID}-app.rule=..."  # Was: app
```

5. **Add tenant domain:**
```yaml
environment:
  TENANT_DOMAIN: ${TENANT_DOMAIN:?Set tenant domain}
```

---

## Integration

### Skills-First Approach (v2.0+)

This skill is part of the **skills-first architecture** - an advanced pattern loaded when multi-tenant architecture is specifically required (not part of standard workflow).

### Related Skills
- `dokploy-compose-structure`: Network patterns
- `dokploy-traefik-routing`: Domain routing
- `dokploy-environment-config`: Tenant variables
- `dokploy-multi-service`: Multi-service dependency patterns

### Invoked By
- **Special case**: When user explicitly requests multi-tenant architecture
- Not part of standard `/dokploy-create` workflow
- Can be manually invoked for advanced use cases

### Usage Notes
- This is an **advanced pattern skill** for specific multi-tenant scenarios
- Standard single-tenant templates use the regular `/dokploy-create` workflow
- Use this skill when building SaaS platforms or multi-tenant applications

See: `/dokploy-create` for standard workflow, this skill for multi-tenant variants
