---
name: defense-in-depth
description: Use when a critical invariant matters. Single-layer protection is a tech-debt smell.
---

# Defense in Depth

When an invariant matters — security, data integrity, money, identity — one layer of protection is not enough. The point is not paranoia. The point is that any single layer can be wrong, bypassed, or skipped, and the next layer catches it.

## Iron Law

**For invariants that must hold, enforce them at every layer that touches the data.** Front-end validates, API validates, DB constrains, audit logs catch.

## Red Flags

- "I already check this in the UI."
- "The API caller would never send that."
- "We trust the upstream service to validate."
- "The DB schema allows it but the app won't write it."
- One single check at one single layer, with the system relying on it.

Each of those is one bug, one bypassed front-end, one rogue script, one curl command away from disaster.

## Where the layers live

For a typical request flow, the layers are roughly:

1. **Client / UI** — guides the user, catches typos, gives fast feedback.
2. **Network boundary** — gateway / WAF, authentication, rate limit.
3. **Application layer** — business rules, authorization, validation.
4. **Persistence layer** — schema constraints, foreign keys, triggers.
5. **Audit / monitor layer** — logs, anomaly detection, replay-able trail.

The same invariant should be expressible at multiple layers, with different jobs:
- UI = **usability** (don't waste user's time)
- API = **correctness** (don't trust the caller)
- DB = **integrity** (don't trust the app)
- Audit = **detection** (catch when the others failed)

## Worked examples

### User input validation
- UI: regex on the input field, red border on invalid.
- API: server-side validation, return 400 on bad input.
- DB: `CHECK` constraint, `NOT NULL`, `UNIQUE` indexes.
- Audit: log all rejections; alert on a spike.

UI alone? Anyone with curl bypasses it. API alone? A migration script writes bad data and the schema accepts it. DB alone? Users get cryptic errors instead of guided feedback. **All four** — each catches a class the others miss.

### Authorization
- UI: hide buttons the user can't use (UX).
- API: re-check authz on every endpoint (the only one that actually protects).
- Service / domain: check permission inside business logic, in case API forgot.
- DB: row-level security as a final backstop where supported.

### Money / accounting
- API: validate amounts, currencies, sign.
- Domain: double-entry bookkeeping (sum of credits == sum of debits).
- DB: invariant constraints, transactional consistency.
- Reconciliation: nightly job that re-derives balances from journal.

## Defense in depth is NOT

- **Redundant code**. Each layer is a different check by a different actor for a different reason.
- **An excuse to skip root-cause fixes** — see [[root-cause-tracing]]. Layers catch when one fails; they don't justify leaving one broken.
- **Paranoia about everything**. Reserve it for things that must not fail: auth, money, identity, data integrity.

## When one layer IS enough

For low-stakes, internal, easily-recoverable operations, one well-placed check may be fine:
- Internal tools used by trusted operators
- Display formatting (wrong format = ugly screen, not a breach)
- Caches and derived data (can be regenerated)

The test: *if this check is bypassed, what's the worst that happens?* If the answer is "ugly UI" — one layer's fine. If it's "we ship the wrong charge to the wrong user" — every layer.

## How to choose where to add layers

1. Identify the invariant. State it precisely. ("No user can read another user's orders.")
2. List the layers that touch the data on the path.
3. For each layer, ask: can it enforce the invariant? Cheaply? Without false positives?
4. Add enforcement at every layer where the answer is yes.
5. Audit: log the path so violations are detectable even if all layers fail.

## MUST

- MUST enforce critical invariants at the persistence layer (it's the layer hardest to bypass).
- MUST enforce at the API layer for any rule the DB can't express.
- MUST NOT rely on the client for any security or correctness invariant.
- MUST add audit / logging for high-stakes operations, even if all gates pass.

## Cross-references

- [[root-cause-tracing]] — defense in depth complements, never replaces, fixing the source bug.
- [[systematic-debugging]] — when a layer catches a bug, debug to find which earlier layer should have caught it sooner.
- [[verification-before-completion]] — verify each added layer actually enforces the invariant (write the bypass test).
