---
name: multitenancy-billing
description: "Build SaaS tenancy and monetization: orgs/teams/roles, tenant isolation, Stripe billing, metering, entitlements, audit logs. Use for any multi-tenant or paid feature."
---

# multitenancy-billing

Tenants isolated by construction, money handled by Stripe, every grant auditable.

## Activate when

- Adding organizations, seats, roles, trials, subscriptions, usage limits, or per-tenant data.

## Do NOT activate for

- Single-tenant internals (see architecture/modularity).

## Procedure

1. Model: org → team → user → role → permission; tenant id on every row or separate schema per isolation tier (shared-schema with tenant id, or separate schema per isolation tier).
2. Enforce: server-side tenant scoping on every query; cross-tenant tests for each new endpoint; support access is impersonation-audited, never silent.
3. Bill: Stripe for subscriptions/invoices/trials; webhook handling idempotent with signature verification; metering pipeline decoupled from request path.
4. Gate: entitlements checked server-side; feature flags per plan; quotas with clear 429/upgrade paths; audit log for permission and billing events.
5. Operate: background jobs for email/notifications/dunning; data-export and tenant-deletion runbooks.
6. Verify: cross-tenant access tests fail closed, webhook replay is safe, trial→paid→cancel flows exercised end to end.

## References
- Related: `../../backend/authorization/`, `../../backend/api-security/`.
