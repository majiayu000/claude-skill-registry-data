---
name: api-security
description: Systematically test REST and GraphQL APIs for the OWASP API Security Top 10 (2023) on authorized targets — object- and function-level authorization (BOLA/BFLA), broken authentication, object-property-level authz (mass assignment / excessive data exposure), unrestricted resource consumption, SSRF, improper inventory (shadow/legacy versions), and unsafe third-party consumption. Use whenever the user is testing an API, has an OpenAPI/Swagger/Postman spec, mentions REST/GraphQL endpoints, API versioning, API keys/JWT, or asks to assess an API's attack surface.
license: Apache-2.0
metadata:
  layer: specialist
  status: under-review
  coverage: api-security
---

# API Security Hunter (OWASP API Top 10 · 2023)

APIs fail differently from web pages: the vulnerabilities are mostly **authorization and
inventory**, not injection. Scanners miss them because they need to understand *what the
object is* and *who should reach it*. Work the spec, not the payload list.

Prerequisite: authorization context (in-scope program/engagement) and the user's **own**
accounts/tokens. Cross-tenant proof uses own-account objects only. See `docs/SAFETY.md`.

## Inputs (gather first)
- Base URL(s) and any spec: OpenAPI/Swagger JSON, Postman collection, GraphQL schema or
  introspection. If none, build an endpoint inventory with `js-recon`/`js-audit`.
- Two of the user's own accounts (A, B) with different roles if roles exist.
- Auth mechanism: session cookie, Bearer/JWT, API key (header vs query), mTLS.

## Workflow
1. **Inventory & map (API9 first).** Enumerate every path, method, parameter, and version.
   Look for **shadow/legacy** surface: `/v1` beside `/v2`, `/internal`, `/debug`,
   `/actuator`, `/swagger`, staging hosts, deprecated-but-live endpoints. Build a table:
   endpoint · method · auth-required · object id location (path/body/query/GraphQL arg) ·
   role required.
2. **Classify objects & identities.** For each endpoint note what object it returns and
   which field identifies the caller. Header-asserted identity (`X-User-Id`,
   `X-Account`) is a claim — test whether the server actually binds it.
3. **BOLA — object-level (API1, the #1 class).** For each object-bearing endpoint, swap
   A's object id for B's (path, body, GraphQL `node(id:)`, batch `ids=`). Confirm with a
   **positive control**: A must succeed on A's own object, or a 4xx proves nothing.
4. **BFLA — function-level (API5).** Can a low-role user call high-role functions? Try
   admin/management methods and method-swaps (GET→PUT/DELETE) as role B.
5. **Broken auth (API2).** Token lifecycle: expiry honored? refresh reuse? JWT `alg:none`
   / RS256→HS256 / `kid` tricks (report only if the server accepts the forged token).
   Credential-stuffing and OTP endpoints — note rate-limit gaps but don't brute live.
6. **Object-property level (API3).** Excessive data exposure (response returns fields the
   UI hides — PII, internal flags) and mass assignment (send `role`, `isAdmin`,
   `verified`, `balance` the client never sends; own account; check what stuck; revert).
7. **Resource consumption (API4).** Pagination without caps, expensive GraphQL queries,
   deep nesting / query batching / aliasing amplification, large `limit`. Demonstrate
   with a bounded request — never a DoS.
8. **SSRF (API7)** on URL-accepting fields → hand off to `bb-ssrf`.
9. **Unsafe third-party consumption (API10)** — the API blindly trusts an upstream it
   calls; look for response-reflection and redirect-following.

## GraphQL specifics
Introspection on? Enumerate types/mutations. BOLA via opaque `node` ids; batching/alias
bypass of per-request limits; mutations that leak invite/collaborator data. Hand deep
GraphQL work to `bb-graphql`.

## Decisions requiring judgment
- Shadow/legacy endpoint found but in-scope? Re-check scope before testing it.
- Response exposes extra fields — is it PII/sensitive (report) or benign (note)?
- Resource-consumption proof: show the cost, stop well short of impact.

## Evidence vs hypothesis
Record each confirmed issue to `schemas/finding.schema.json`. BOLA/BFLA need the foreign
2xx **with the other object's body** plus the green positive control. "Endpoint has no
visible authz" without a cross-account read is a hypothesis, not a finding.

## Tools (check availability; none bundled)
- Spec-driven: import OpenAPI/Postman into a proxy (Burp/ZAP) if present; otherwise curl
  loops over the spec.
- Enumeration: `ffuf`/`feroxbuster` for versions/paths; `kiterunner` for API routes.
- GraphQL: `graphql-cop`, `clairvoyance` (schema recovery) — if installed.
- Always: confirm the tool exists (`command -v`) before relying on it; fall back to curl.

## Failure handling
If the spec is absent, derive the surface from JS (`js-audit`). If a tool is missing,
state it and use the manual curl equivalent. If every id swap 404s with clean fabrication
responses, record TESTED-NEGATIVE with the pattern.

## Output
An endpoint inventory table + per-issue finding records + a prioritized list. Calibrate
severity with `bb-disclosures`/`h1-reports`; escalate via `bb-chains`; write up with
`bb-report`.

## Acceptance criteria (for `validated`)
- POS: given a spec, produces the inventory table and runs the BOLA matrix with positive
  controls. NEG: declines to call a header-identity bug confirmed without a bound-identity
  test. SAFE: never brute-forces live auth, never DoS for API4, cross-tenant proof is
  own-account only. INC: id-swap 400/500 without a positive control → inconclusive.

## References
OWASP API Security Top 10 (2023). Siblings: `js-audit`, `bb-graphql`, `bb-authz`,
`bb-ssrf`, `bb-pii`, `idor-runner`.
