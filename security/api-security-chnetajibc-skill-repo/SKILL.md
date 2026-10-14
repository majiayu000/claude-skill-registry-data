---
name: api-security
description: "Secure APIs as hard gate: BOLA, authn/authz, property-level authz, consumption limits, SSRF, misconfig, inventory. Ask: can A access Bs object? Can low-privilege hit admin?"
---

# api-security

Every endpoint answers: who can call this, on whose objects, with what fields, at what cost.

## Activate when

- Designing, implementing, or reviewing any API; adding endpoints, fields, webhooks, or integrations.

## Do NOT activate for

- Non-API app code (see secure-baseline); identity mechanics (see authentication).

## Inspection

Inventory routes with methods, auth requirements, object scoping, accepted fields, and cost profile (compute, I/O, third-party calls).

## Decision rules

- BOLA first: every object access scoped to the caller; test user-A vs user-B on each endpoint.
- Function-level: role checks on every route including admin/internal ones; no security by obscurity.
- Property-level: mass-assignment allowlists per role; sensitive fields never writable/readable by default.
- Consumption: rate limits + cost caps on expensive endpoints; pagination bounded; no unbounded exports.
- SSRF: no server-side fetches of user URLs without allowlist + no-metadata-IP egress; validate webhooks with signatures.
- Hygiene: security headers, CORS allowlisted, error responses uniform, deprecated versions inventoried and sunset.

## Procedure

1. Threat-list the new surface (spoofing, tampering, repudiation, info disclosure, DoS, elevation) in one pass.
2. Implement authz + validation + limits before business logic; deny by default.
3. Write the attacker tests: cross-user, low-privilege-admin, over-posting, quota-busting, SSRF probe.
4. Verify: attacker matrix green, headers audited, inventory updated, findings mapped to OWASP API Top 10.

## Failure modes

- Auth on most routes but not export/admin/debug ones; client-enforced roles; verbose errors leaking internals; unlimited pagination; SSRF via webhook URLs or image fetches.

## Escalation

Deep auth design → authentication/authorization; full audit → security/secure-baseline.

## References

- Related: `../authentication/`, `../authorization/`, `../validation/`, `../rate-limiting/`, `../../security/secure-baseline/`.
