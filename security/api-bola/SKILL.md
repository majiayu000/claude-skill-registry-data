---
name: api-bola
description: >
  Broken Object/Function Level Authorization in REST/JSON APIs (the #1 API risk). Load on any
  REST API with object ids in paths/bodies (/api/v1/users/123, /orders/{id}), Bearer auth,
  mobile-app backends, or admin vs user function separation. Signals: predictable ids, verbs
  that skip re-authorization, "role" enforced only in the UI.
domain: api
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp_api: [API1:2023-BOLA, API5:2023-BFLA]
cwe: [CWE-639, CWE-285]
tools: [burp, autorize, postman]
schema_version: 1
---

# Broken Object/Function Level Authorization (BOLA/BFLA)

## When it applies
An API exposes objects (BOLA) or privileged functions (BFLA) and enforces authorization
weakly. The API version of IDOR — but APIs multiply the surface (many endpoints, verbs,
versions, and a mobile client that trusts the server less than the web UI does).

## Why it works
APIs are stateless and object-centric; each endpoint must independently check "can this token
act on this object/function?". Teams centralize authentication but scatter (or forget)
authorization, and hide admin functions in the client instead of the server.

## Method
1. **BOLA**: with two tokens, request another user's object id on every endpoint & verb; also
   try guessing/incrementing ids and IDs leaked from list endpoints.
2. **BFLA**: take an admin-only call (from JS, mobile, or docs) and replay it with a low-priv
   token; try method swaps (GET→PUT/DELETE) and hidden verbs the UI never issues.
3. **Version & shadow endpoints**: `/api/v1/` may lack fixes present in `/v2/`; `/internal/`,
   `/debug/`, Swagger/OpenAPI docs reveal ungoverned routes.
4. **Automate** with Burp **Autorize** (low-priv token as the "enforcement" session) to flag
   every request that succeeds when it shouldn't.

## Gotchas
- 200 vs 403 is the tell, but some APIs return 200 with an empty body — diff the content.
- IDs as UUIDs still leak via list/search endpoints and other objects' relations.
- Rate-limit and WAF differ per API version — the vuln may only show on an older route.

## Verify success
A low-privilege (or cross-tenant) token successfully reads/modifies an object or invokes a
function reserved for another user/role.

## References
OWASP API Security Top 10 (2023) API1/API5; PortSwigger access-control labs.
