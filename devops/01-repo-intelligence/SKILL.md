---
name: repo_intelligence
description: Build evidence-based repo map with actual file paths, trust boundaries, and operational topology.
when_to_use:
  - First session on the repo
  - Before any production change
  - Diagnosing incidents or onboarding
---

# Repo Intelligence Protocol (RESTO BOT v3.3.0)

## Goal

Create an evidence-based map of the full system: components, routes, domains, auth boundaries, data flows, and operational controls.

## Extraction checklist (with file evidence)

### 1. Entry points and domains

- `api.srv1258231.hstgr.cloud` -> gateway (nginx) -> `/v1/*` routes
- `console.srv1258231.hstgr.cloud` -> n8n-main (BasicAuth + IP allowlist)
- `cms.srv1258231.hstgr.cloud` -> Strapi CMS (IP allowlist)
- `admin.srv1258231.hstgr.cloud` -> Admin Dashboard (BasicAuth + IP allowlist)
- `kiosk.srv1258231.hstgr.cloud` -> Kiosk App (public, rate-limited)
- Config: `project/docker-compose.hostinger.prod.yml` (Traefik labels)

### 2. Proxy chain

```text
Internet -> Traefik v3.6.6 (:80/:443) -> proxy network
  -> gateway (nginx:1.27) -> n8n-main (upstream, internal network)
  -> n8n-main -> console (direct Traefik route)
  -> cms -> Strapi (direct Traefik route)
  -> admin-dashboard (direct Traefik route)
  -> kiosk-app (direct Traefik route)
```

### 3. Auth mechanisms

- Gateway: `X-API-Token` header or Bearer token validated pre-proxy
- Console: BasicAuth + IP allowlist middleware chain
- CMS: IP allowlist (no BasicAuth on CMS itself)
- Admin Dashboard: BasicAuth + IP allowlist
- Query token: **disabled by default**

### 4. n8n topology

- Queue mode: `n8n-main` (webhook receiver) + `n8n-worker` (execution)
- Redis 7-alpine as Bull queue backend (AOF, 256MB, allkeys-lru)
- Worker concurrency: `QUEUE_BULL_MAX_CONCURRENCY` (default: 2)
- 54 workflow JSON files in `project/workflows/`

### 5. Data layer

- PostgreSQL 15-alpine with two databases: `n8n` and `strapi`
- Bootstrap: `project/db/bootstrap.sql`
- Init scripts: `project/db/init/01_apply_migrations.sh`, `02_create_strapi_db.sh`
- Migrations: `project/db/migrations/` (tracked in `schema_migrations` table)
- Schemas: `project/schemas/` mounted at `/opt/resto/schemas`

### 6. Frontend apps

- **inventory-cms/**: Strapi headless CMS for menu/inventory
- **admin-dashboard/**: Vite-based admin UI (VITE_DOMAIN, VITE_STRAPI_URL)
- **kiosk-app/**: Vite-based customer kiosk (VITE_DOMAIN, VITE_STRAPI_URL)

### 7. Ops primitives

- Compose: `project/docker-compose.hostinger.prod.yml`
- Scripts: `project/scripts/` (preflight, smoke, validate, deploy, rollback)
- CI/CD: 12 workflows in `project/.github/workflows/`, 4 composite actions
- Secrets: `project/secrets/` (postgres_password, n8n_encryption_key, redis_password, traefik_usersfile)
- VPS: `deploy@72.60.190.192`, project at `/opt/resto/current/`

### 8. MCP servers

- **ruflo** (Claude Flow v3.5.2): Multi-agent orchestration
- **n8n-mcp**: n8n workflow/execution management (needs API key)
- **strapi-mcp**: Strapi CMS content management (needs admin credentials)

## Required output

- Repo Map (bullets with file paths)
- Trust Boundary Diagram (ASCII)
- Public Surface Map (endpoints + methods + auth)
- Failure Impact Table (component -> failure -> user impact -> mitigation)
- Deploy and verify checklist
