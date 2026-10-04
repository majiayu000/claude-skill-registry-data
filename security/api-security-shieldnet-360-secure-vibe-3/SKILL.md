---
id: api-security
version: "1.3.0"
title: "API Security"
description: "OWASP API Top 10 for HTTP, GraphQL, and gRPC endpoints: input validation, route rate limiting, mass assignment, response caching, and gateway-versus-service control placement. Use when generating or reviewing HTTP handlers, GraphQL resolvers, gRPC service methods, or any API endpoint change."
category: prevention
severity: high
applies_to:
  - "when generating HTTP handlers"
  - "when generating GraphQL resolvers"
  - "when generating gRPC service methods"
  - "when reviewing API endpoint changes"
languages: ["*"]
token_budget:
  minimal: 1300
  compact: 1700
  full: 2700
rules_path: "checklists/"
related_skills: ["auth-security", "error-handling-security", "secure-code-review", "secret-detection", "ssrf-prevention", "websocket-security"]
last_updated: "2026-07-03"
sources:
  - "OWASP API Security Top 10 2023"
  - "OWASP Authentication Cheat Sheet"
  - "OAuth 2.0 Security Best Current Practice (RFC 9700)"
---

# API Security

## Rules (for AI agents)

### ALWAYS
- Require authentication on every non-public endpoint. Default to authenticated; opt
  out for genuinely public routes by explicit annotation.
- Consult `auth-security` for **who the caller is and what they may touch**. It owns
  the credential (algorithm pinning, expiry, lifetime, session, CSRF) and the
  permission (object-level BOLA/IDOR checks, multi-key routes, streaming subjects,
  function-level role gating). Any endpoint that reads or writes a resource by id
  needs it; this skill covers everything else about the endpoint.
- Validate all request inputs against an explicit schema (JSON Schema, Pydantic,
  Zod, validator/v10 struct tags). Reject early; never propagate untrusted input
  deeper.
- Enforce rate limits at the route level for authentication endpoints, password reset,
  and any expensive operation.
- Consult `error-handling-security` for what an error response may carry. It owns the
  boundary between what crosses to the client and what stays in the log, including
  presence-of-record disclosure (`User not found` vs `Invalid credentials`).
- Include `Cache-Control: no-store` on responses containing personal or sensitive
  data.

### NEVER
- Use sequential integer IDs in URLs for resources accessible across tenants. Use
  UUIDs or unguessable opaque IDs.
- Mass-assign request bodies directly to ORM models (`User(**request.json)`) — this
  enables privilege escalation when the model has admin fields the user shouldn't
  control.
- Key a rate-limit / lockout counter on a **client-controllable header** (leftmost
  `X-Forwarded-For`, `X-Real-IP`, `Forwarded`) — rotating it yields a fresh bucket per
  request and defeats the limit. Derive the client IP from the trusted-proxy hop count
  (or key on the authenticated user), and fail closed on limiter error.
- Use `HTTP GET` for any state-changing operation — GET should be safe and
  idempotent.
- Rely on **network position** (IP allowlist, VPN, private subnet, "internal
  only", a WAF/edge rule) as the *only* control on a sensitive endpoint.
  Reachability is not authentication: the moment there's an SSRF, a compromised
  internal host, a tenant on the network, or a boundary change, an
  unauthenticated "internal" endpoint (`permission_classes = [AllowAny]`,
  no `RequireAuth`) is wide open. Enforce auth/authz at the service itself,
  behind any network control.
- Place security controls (auth, field-stripping, CSRF, rate-limit, input
  validation) only at a gateway / BFF / proxy while the backend service is
  **also directly reachable**. An attacker calls the service directly and
  bypasses every proxy-layer control — controls must live at the service that
  owns the data. (A common variant: the gateway checks that a JWT is *present*
  but the service never checks the caller's *role* or *object-level ownership* —
  the service reads the subject id from the body/path/query and trusts it.)

### KNOWN FALSE POSITIVES
- Public marketing-site endpoints serving anonymous traffic legitimately have no auth
  and no rate limits beyond the load balancer.
- Sequential IDs in paths are fine for genuinely public, non-tenant-scoped resources
  (e.g. blog post slugs, public product catalog items).
- Health-check endpoints (`/healthz`, `/ready`) intentionally bypass auth.
- A network control (mTLS service mesh, NetworkPolicy, private ingress) is fine
  as **defense-in-depth** — the anti-pattern is only when it's the *sole* control
  and the service itself authenticates nothing.
- Mutual-TLS / SPIFFE workload identity between services **is** authentication
  (a cryptographic caller identity), not mere network position — mTLS-authenticated
  service-to-service calls are fine even on a private network.

## Context (for humans)

The OWASP API Top 10 differs from the web Top 10 mostly because APIs have weaker
defaults: they often skip CSRF, they expose object IDs directly, and they tend to
trust developer-provided client-side state. This skill codifies the most common
high-impact mistakes.

A recurring architectural failure is **trusting the perimeter instead of the
service**: a BFF/gateway enforces auth, strips fields, and checks CSRF, while the
core service is also directly reachable and authenticates nothing because it's
"internal". Anyone who can reach the core service — via SSRF, a foothold inside
the allowlisted network, or simply a public DNS name that resolves to the same
backend — bypasses every perimeter control. Network position is a mitigation, not
an authentication boundary; the owning service must enforce auth/authz itself.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `checklists/auth_patterns.yaml`
- `checklists/input_validation.yaml`
- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-introduction/).
- [RFC 9700 — OAuth 2.0 Security BCP](https://datatracker.ietf.org/doc/html/rfc9700).
