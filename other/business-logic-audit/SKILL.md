---
name: business-logic-audit
description: "Reviews existing business code (billing, multi-tenancy, state machines, inventory, GL postings, audit logs, etc.) for missing real-world edge cases. Severity-graded findings — invariant violations, race conditions, missing idempotency, currency precision bugs, audit gaps, jurisdiction issues."
---

# /business-logic-audit

Audit a feature or module for the edge cases that break in production. Different from `/review-pr` (which reviews diffs) — this skill walks code that's already shipped and looks for the failure modes the original implementer missed.

## When to use

- Before scaling a feature to higher traffic / bigger customers / new regions.
- After an incident touched a business invariant.
- Before a SOC 2 / PCI / HIPAA audit.
- When taking ownership of someone else's code that handles money or regulated data.
- When a competitor's incident shows a class of failure you haven't checked for.

## Operating method

### 1. Lock down scope

Ask:

- **What feature / module / domain?** Be specific — "the checkout flow," "subscription billing," "inventory reservation," "multi-tenant search."
- **What's the worst-case failure?** Lost charge, double charge, leaked tenant data, audit fail, etc. We'll prioritize the audit around it.
- **What's the deployment context?** Dev / staging / prod. Some checks (rate limits, tax) only matter in prod.

### 2. Walk the relevant edge-case checklist

For each finding, classify by category and severity. Categories below — pick the ones that apply.

#### Money handling

- [ ] All monetary values stored in minor units as integers. **Critical** if floats are used.
- [ ] Every monetary value has an explicit currency code. **High** if missing.
- [ ] Rounding rule documented at every site that rounds. **Medium**.
- [ ] FX rate snapshotted at transaction time. **High** for multi-currency.
- [ ] Refunds, adjustments, chargebacks are append-only. **Critical** if rows are mutated.
- [ ] Tax calculation through Stripe Tax / Avalara / TaxJar (not hand-rolled). **High** for non-US jurisdictions.
- [ ] Invoice numbers are sequential per legal entity, immutable once issued. **High**.

#### State machines

- [ ] Legal transitions defined in code (enum + guard) or DB constraint, not just UI. **High**.
- [ ] Every transition logged with actor + timestamp + before + after. **High**.
- [ ] Race conditions on transitions handled (row locks or unique constraints). **Critical** for concurrent scenarios.
- [ ] Reversible vs one-way transitions documented. **Medium**.
- [ ] State machine matches the real business workflow (no impossible states reachable). **High**.

#### Multi-tenancy

- [ ] Every business-data query filters by `tenant_id`. **Critical** if any miss.
- [ ] Cross-tenant access returns 404, not 403. **High** (existence-leak).
- [ ] At least one cross-tenant integration test exists. **High**.
- [ ] Tenant-scoped uniqueness (emails, slugs) enforced via composite unique index. **High**.
- [ ] Tenant export and delete flows exist. **Medium** (gating: B2B SaaS / GDPR-relevant).

#### Idempotency

- [ ] State-changing API endpoints accept `Idempotency-Key`. **Critical** for charge/refund/order endpoints.
- [ ] Server stores result per key for ≥ 24h, replays cached result on retry. **Critical**.
- [ ] Webhook receivers dedupe via stable event ID. **Critical**.
- [ ] Background jobs are idempotent at unit-of-work level. **High**.
- [ ] External-system writes (Stripe charge, email send) use provider idempotency keys. **High**.

#### Concurrency

- [ ] Optimistic locking (version column) on user-facing edits. **Medium**.
- [ ] Pessimistic locking on inventory / balance / queue work. **Critical** for inventory.
- [ ] No distributed-transaction-across-services. Use outbox pattern. **High**.
- [ ] Worker visibility timeout > longest expected job. **High**.

#### Audit & compliance

- [ ] Append-only audit log on regulated entities. **Critical** for financial / medical / customer-PII.
- [ ] Each audit entry: actor, UTC timestamp, entity ID, action, before, after, request ID. **High**.
- [ ] Retention policy documented per data class. **High**.
- [ ] Audit log access controlled — actors can't erase tracks. **Critical**.
- [ ] DSAR endpoint (GDPR) exists. **High** if EU users.
- [ ] Right-to-erasure cascades through all systems including backups. **High** if EU users.

#### API contracts

- [ ] Versioning strategy (URL or header). **Medium**.
- [ ] Idempotency keys on state-changing endpoints. **Critical** (also called out above).
- [ ] Cursor-based pagination on large/insert-heavy collections. **Medium**.
- [ ] Stable error codes alongside human messages. **Medium**.
- [ ] Rate limits per-key, per-tenant, per-IP. **High**.
- [ ] Sunset policy for deprecations (typically 12-month minimum). **Medium**.

#### Webhooks (outgoing)

- [ ] HMAC signing with rotatable secret. **Critical**.
- [ ] Retry with exponential backoff + dead-letter. **High**.
- [ ] Stable event IDs for receiver dedupe. **High**.
- [ ] Schema versioning + sunset policy. **Medium**.

#### Time

- [ ] Timestamps stored in UTC with timezone. **High**.
- [ ] DST-aware date math (no `+24h` hacks). **Medium**.
- [ ] Recurring schedules use rules (cron / RRULE), not pre-computed instances. **Medium**.
- [ ] "Now" injected for testability. **Low**.

#### File handling

- [ ] Type, size, content validated server-side. **High**.
- [ ] Virus scanning for user-uploaded files. **High** for public/shared files.
- [ ] Signed URLs for downloads; cookieless serving domain. **High**.
- [ ] Per-tenant quotas enforced before accepting upload. **Medium**.

#### Sessions & auth

- [ ] Session cookies `Secure`, `HttpOnly`, `SameSite=Lax`. **Critical** for web auth.
- [ ] CSRF protection on state-changing endpoints (or strict CORS for bearer-token APIs). **Critical**.
- [ ] Session revocation works server-side (logout invalidates the token). **High**.
- [ ] Idle timeout for sensitive flows. **Medium**.
- [ ] MFA available for admin / billing-owner roles. **High** for B2B SaaS.

#### ERP-specific (skip if N/A)

- [ ] Double-entry posting (debits = credits) enforced. **Critical**.
- [ ] Period-close lock prevents back-dated entries. **Critical**.
- [ ] 3-way match (PO + GRN + invoice) on payable. **High**.
- [ ] Inventory available count derived from on-hand − reserved − allocated. **Critical**.
- [ ] Reconciliation jobs run nightly, alert on mismatches. **High**.

#### Marketplace-specific (skip if N/A)

- [ ] KYC at seller onboarding. **Critical**.
- [ ] Sanctions screening on transactions. **Critical** for fintech.
- [ ] Payout hold for first-time sellers. **High**.
- [ ] Tax form generation (1099-K US) above threshold. **High** for US marketplace.

### 3. Verify, don't guess

For each item, **read the code** (or run a query, or check a config) before marking it. The `no-hallucination` rule applies — never claim "✅ this is implemented" without showing where.

For findings, cite the file and line range.

### 4. Severity grading

- **Critical** — invariant violation, money loss, data leak, regulatory breach. Fix before next release.
- **High** — likely incident under realistic load. Fix in current sprint.
- **Medium** — quality issue that compounds. Fix soon.
- **Low** — defense-in-depth. Track for later.

### 5. Compare to competitors (optional)

For categories where prior art is well-known (billing dunning, RBAC, search), include a one-line note: "Stripe handles failed payments via 4 retries / 15 days; we have 1 retry / immediate suspend, which is harsh for SMB customers."

If the user wants a deeper comparison, suggest running `/competitive-analysis` afterward.

## Output format

```
## Scope
- Feature audited: <name>
- Worst-case failure considered: <description>
- Files reviewed: <list with line ranges>

## Findings (severity-ordered)

### Critical (N)
1. <category> — <issue>. <file:line>. **Fix:** <one-paragraph fix>.
2. …

### High (N)
…

### Medium (N)
…

### Low (N)
…

## What's good (specific, not generic)
- <thing 1>
- <thing 2>

## Comparison to prior art (if relevant)
- <our pattern> vs <competitor pattern> — for context only.

## Recommended next action
1. <highest-leverage critical fix — start here>
2. …
```

## Boundaries

- **Verify every claim with code, query, or config.** Don't say "this is missing" without showing it's missing.
- **Don't audit categories that don't apply.** ERP-specific items on a SaaS app are noise.
- **Don't recommend infinite complexity.** Match recommendations to project stage (pre-launch, scaling, mature).
- **Cite competitor patterns when borrowing recommendations.** Don't say "industry standard is X" without naming who.
- **Flag legal questions for the user**, don't decide them. "Your retention period of 90 days may not meet US tax law's 7-year requirement — confirm with your accountant" is right; "you must use 7 years" is overreach.
