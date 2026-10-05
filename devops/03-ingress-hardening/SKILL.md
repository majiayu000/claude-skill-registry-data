---
name: ingress_hardening
description: Harden the full ingress chain - Traefik TLS/middlewares, Nginx gateway, and /v1 API contract.
when_to_use:
  - Editing gateway configs (infra/gateway/)
  - Editing Traefik labels in prod compose
  - Adding or modifying /v1 endpoints
  - TLS or routing issues
  - Locking down console/admin/cms
---

# Ingress Hardening (Traefik + Gateway + /v1 Contract)

## Current ingress chain

```text
Internet -> Traefik v3.6.6 (:80 -> :443 redirect)
  |
  +-- api.* -> api-public-chain (ratelimit 20/s burst 40 + security headers)
  |            -> gateway nginx:1.27 (:8080) -> n8n-main upstream
  |
  +-- api.*/v1/internal|admin -> api-internal-chain (IP allowlist + BasicAuth + headers)
  |
  +-- console.* -> console-chain (IP allowlist + BasicAuth + headers)
  |                -> n8n-main (:5678)
  |
  +-- cms.* -> cms-chain (IP allowlist + headers, no BasicAuth)
  |            -> Strapi (:1337)
  |
  +-- admin.* -> admin-dash-chain (IP allowlist + BasicAuth + headers)
  |              -> admin-dashboard (:80)
  |
  +-- kiosk.* -> kiosk-chain (ratelimit 30/s burst 60 + headers)
               -> kiosk-app (:80)
```

## Key files

- `project/docker-compose.hostinger.prod.yml` (Traefik labels, middleware chains)
- `project/infra/gateway/nginx.conf` (upstream routes, auth validation, /v1/* mapping)
- `project/infra/gateway/proxy_params` (proxy headers)
- `project/.env` (ADMIN_ALLOWED_IPS, TRAEFIK_TRUSTED_IPS)

## Traefik middleware chains

| Chain | Middlewares | Used by |
| --- | --- | --- |
| api-public-chain | ratelimit + security headers | api.* public routes |
| api-internal-chain | IP allowlist + BasicAuth + headers | /v1/internal, /v1/admin |
| console-chain | IP allowlist + BasicAuth + headers | console.* |
| cms-chain | IP allowlist + headers | cms.* |
| admin-dash-chain | IP allowlist + BasicAuth + headers | admin.* |
| kiosk-chain | ratelimit + headers | kiosk.* |

## Gateway /v1 contract rules

- No breaking changes to existing `/v1/*` routes
- Only additive changes unless deprecation plan exists
- Auth enforced BEFORE upstream calls
- No query-token auth unless explicitly enabled
- Rate limiting per IP (and optional per token)
- Request body size limits
- Method allowlist
- Timeouts: connect/read/send + upstream resilience
- Security headers at both Traefik and gateway level
- Token redaction in logs

## Required output

- Exact diff for gateway or compose config
- Updated smoke tests covering:
  - Valid auth -> 200
  - Missing/wrong auth -> 401/403
  - Disallowed methods -> 405
  - Rate limit behavior
- Rollback steps (revert config + reload)
- Post-deploy verification: TLS ok, routes ok, console protected
