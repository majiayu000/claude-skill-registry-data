---
name: authorization
description: "Authorization: RBAC/ABAC, object- and property-level checks on every path. Deny by default; test cross-user access."
---

# authorization

Deny by default; every path checks; every check is tested cross-user.

## Activate when

- Adding or reviewing permissions, roles, object-level or field-level access, multi-tenant scoping.

## Do NOT activate for

- Identity proof itself (see authentication); Spring wiring (see frameworks/spring-security).

## Procedure

1. Model: RBAC roles plus ABAC attributes where context matters; object-level (this record?) AND property-level (this field?) checks on every path — including batch, export, webhook, and admin paths.
2. Enforce server-side only; client checks are UX, not security. Most-specific-first rules with a deny tail.
3. Test as an attacker: unauthenticated, low-privilege, cross-user, cross-tenant probes per endpoint; IDOR matrix green before merge.
4. Tenant isolation: scope every query; support/impersonation access audited (see saas/multitenancy-billing).
5. Verify: probe results recorded, no fail-open defaults, authorization errors free of enumeration oracles.

## Failure modes

- Checks on most routes but not export/admin/debug/batch paths; client-enforced roles; fail-open defaults after refactor; tenant scoping dropped in a new query; error messages distinguishing 'no such object' from 'forbidden'.

## Escalation

- Full audit → security/secure-baseline; Spring wiring → frameworks/spring-security.
