---
name: api-versioning
description: >
  Find and attack old/shadow API versions that missed a fix — improper inventory management. Load
  when the API is versioned (/v1, /v2, /api/2021-01), on "old API", or after mapping the surface.
  Signals: version in path/header/subdomain, deprecated docs, mobile app using an older version.
domain: api
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: high
owasp_api: [API9:2023-Improper-Inventory-Management]
cwe: [CWE-1059]
tools: [burp, ffuf]
schema_version: 1
---

# API versioning attacks

## When it applies
The API exposes multiple versions and a vulnerability fixed in the current version still lives in
an older or undocumented one. Old versions rarely get the same auth, validation, or rate-limit hardening.

## Why it works
Teams patch the latest version and leave `/v1` (and `/beta`, `/internal`, dated versions) running
for backward compatibility. Those endpoints often skip a fix, lack a new authz check, or expose
fields later removed — same data, weaker guard.

## Method
1. **Enumerate versions**: swap the version in path (`/v1`↔`/v2`↔`/v3`), header
   (`Accept: application/vnd.api+json;version=1`, `X-API-Version`), or subdomain
   (`api-v1.`, `legacy.`). Fuzz with `ffuf`.
2. **Diff behaviour**: take a request that's now blocked/fixed on the current version and replay it
   against older ones — missing auth, mass assignment (→ `api-mass-assignment`), BOLA
   (→ `api-bola`), verbose fields, or no rate limit.
3. **Mine sources for old versions**: mobile apps, JS bundles, wayback, and public API docs often
   reference deprecated versions still live.
4. **Re-test every known bug per version** — a fix in v2 is often absent in v1.

## Gotchas
- A 404 on `/v1` root doesn't mean v1 is gone — test specific known endpoints under it.
- Header/media-type versioning is easy to miss vs path versioning — enumerate all three.
- Old versions may lack rate limits, enabling brute force the new one blocks.

## Verify success
A vulnerability reproducible on an older/undocumented API version that is patched or better-guarded
on the current one.

## References
OWASP API Security Top 10 (2023) API9; API inventory/versioning guidance.
