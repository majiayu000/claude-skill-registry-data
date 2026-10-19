---
name: api-fuzzing
description: >
  Discover and fuzz API endpoints, methods, params, and versions systematically. Load when you
  have an API base but not its full surface, an OpenAPI/Swagger/Postman spec, or "map/fuzz the
  API". Signals: /api, /v1, swagger.json, GraphQL, mobile backend, undocumented routes.
domain: api
type: technique
stability: learning
modes: [bugbounty]
severity: info
owasp_api: [API9:2023-Improper-Inventory-Management]
cwe: [CWE-1059]
tools: [ffuf, kiterunner, arjun, burp]
schema_version: 1
---

# API discovery & fuzzing

## When it applies
You need the API's real surface before attacking it: hidden endpoints, accepted methods, extra
params, and old versions. Complete inventory is where BOLA/mass-assignment/auth bugs surface.

## Why it works
APIs expose far more than the client uses; specs, JS, and mobile apps reveal routes, and
version drift leaves un-patched endpoints. Enumerating the surface turns guesswork into targeted testing.

## Method
1. **Harvest from specs/clients**: OpenAPI/Swagger (`swagger.json`, `/api-docs`), Postman
   collections, GraphQL introspection, and endpoints in JS bundles / mobile apps.
2. **Route brute**: `kiterunner` (API-aware wordlists incl. methods) or `ffuf` against `/api/FUZZ`,
   `/v{1,2,3}/`; try each with GET/POST/PUT/PATCH/DELETE — method matters.
3. **Param discovery**: `arjun`/Burp param miner per endpoint to find hidden inputs (feed
   mass-assignment, injection, IDOR tests).
4. **Version & shadow**: enumerate `/v1../v3`, `/internal`, `/beta`; compare behaviour/auth across versions.
5. **Feed the results** into `api-bola`, `api-mass-assignment`, `api-auth-attacks`, injection.

## Gotchas
- Respect rate limits and scope — API fuzzing is noisy; throttle and stay on in-scope hosts.
- A route that 401s still counts — note it for auth testing; 404 vs 401 vs 403 map the surface.
- Method-fuzzing finds actions the client never issues (hidden admin verbs).

## Verify success
A materially larger, documented endpoint/param inventory (with methods/versions) ready for
vuln-class testing — including routes not in the official docs.

## References
OWASP API Security (API9); kiterunner; PortSwigger API testing guide.
