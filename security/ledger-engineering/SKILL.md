---
name: ledger-engineering
description: Build append-only ledgers and audit trails — double-entry where money moves, immutability, reconciliation.
version: 1
triggers: ledger, double entry, audit trail, append-only, bookkeeping system, reconciliation
category: Money & markets
blurb: Build append-only ledgers and audit trails — double-entry where money moves, and reconciliation.
archetype: knowledge
example: Design a ledger that an auditor can trust.
---

# Ledger Engineering

Facts are append-only. Balances are derived. If money moves, both sides are recorded. If it can be edited, it isn't a ledger — it's a liability.

## When to use
- Money-like ledgers (expense/income, portfolios, credits).
- Audit trails for any state that must be provably truthful.
- Bookkeeping-adjacent tooling (exporting clean data to beancount-style systems).

## Method
1. **Append-only by design**: events are immutable; corrections are new reversing/adjusting entries referencing the originals; no UPDATE/DELETE on posted facts. Retention per policy; legal holds respected.
2. **Money discipline**: **double-entry** for anything monetary (sum = zero per transaction); integer minor units or exact decimals — floats are forbidden; currency explicit per entry; FX rates recorded at event time.
3. **Structure**: accounts → entries → transactions (atomic groups); stable IDs; every event carries timestamp, actor, source.
4. **Derived state**: balances and reports are projections (recomputable, checkpointed) — never authoritative over the log; periodic checkpoint hashes for tamper evidence.
5. **Reconciliation**: ledger ↔ bank/processor/external statements on a cadence; discrepancies get a workflow (found → investigated → resolved with record); no silently closed months.
6. **Reporting**: period summaries; audit queries answer "who changed what, when, why"; tax-ready exports for the accountant (ACB-style lot tracking where applicable).
7. **Security**: encryption at rest; scoped access; backups **restore-tested** (restore = replay the log and verify invariants).

## Quality gates
- [ ] Balance invariant tests in the suite (sums, double-entry).
- [ ] No mutation code paths on posted entries (verified).
- [ ] Reconciliation cadence running with resolution records.
- [ ] Restore drill done (replay verified).

## Red lines
- Never edit history; no float money; no unreconciled period closed silently.

## Related
`payments-and-billing` · `knowledge-graph-engineering` (provenance) · `tax-planning` (clean data for the accountant).
