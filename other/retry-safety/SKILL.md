---
name: retry-safety
version: 0.2.0
license: MIT
description: Use when a diff carries side effects - database writes, migrations, file mutations, network calls, payments, queue messages - to check whether running it twice is safe. Also when reviewing retry logic, crash recovery, or anything a scheduler, queue, or impatient caller might re-run. Silent when the diff touches no side-effecting surface. Read-only review. Applying the fixes belongs to expedite.
---

# retry-safety

Fire the same ticket twice and the kitchen must not charge the table twice. Timeouts, crashes, queue redeliveries, and impatient callers re-run operations constantly. The only question is whether the second run finishes the remainder or doubles the damage.

**Core principle:** the standard is idempotent read-modify-write at the side-effecting edge. The operation reads current state before writing, so a re-run over work already done completes the remainder and changes nothing else. Anything short of that needs a named reason it is still safe.

**Read-only.** This is a review lens. Fixing is a separate engagement: hand the finished report to [expedite](../expedite/SKILL.md), which works the backlog in leverage order. When the diff touches no side-effecting surface, say so in one line and stop.

## The sweep

For each side-effecting edge in the diff, simulate two failure shapes: the whole operation retried after a timeout, and a crash halfway followed by a re-run.

| Surface | The double-run hazard |
|---------|----------------------|
| Database writes | duplicate rows, double-applied increments, constraint violations on the second pass |
| Migrations | re-running a completed step corrupts or aborts (see the migration section) |
| File and data writes | appends that double, partial files clobbered, temp files orphaned |
| Network mutations | the remote applied the first call and the retry applies it again (no idempotency key) |
| Payments and external calls | double charge, double email, double webhook - the ones users notice |
| Queues and events | redelivery is at-least-once almost everywhere, and consumers assume exactly-once |
| Caches and counters | increments and TTL refreshes that drift under replay |

A transaction is not an answer by itself: the transaction makes one attempt atomic, and then the caller retries the whole transaction.

## Migrations carry a second hazard

Beyond re-run safety, a migration lives through a deploy window where old code runs against the new schema and new code runs against old data, and a partial failure leaves the two inconsistent. Flag a migration that:

- is non-reversible with no stated recovery path
- adds NOT NULL or another constraint to a populated table without a default or backfill
- renames or drops a column or table that instances still running mid-rollout depend on
- swaps or inverts an enum or ID mapping
- breaks foreign-key or cascade integrity

The fix arrow is expand-migrate-contract: add the column nullable, backfill, then add the constraint, so old and new code coexist through the rollout.

## Report contract

Same spine as the shared [audit report format](../../../docs/audit-report-format.md) so findings compose into one backlog and feed [expedite](../expedite/SKILL.md). Severity is the cost of the second run: **critical** (double charge, double payment, silent corruption) / **high** (duplicate effects a user sees: emails, webhooks, doubled rows) / **medium** (corruption someone can repair by hand, or a hazard that needs a narrow crash window) / **low** (cosmetic duplication). Effort is the fix cost: **S** (under 30 min) / **M** (under half a day) / **L** (multi-day).

```markdown
# retry-safety report: <scope> (<date>)

## Verdict
One paragraph, or the single line "no side-effecting surface in this diff".

## Findings
Grouped by severity, descending. Each:
### [SEVERITY] Short imperative title
- **Surface:** which side-effecting edge
- **Where:** file:line
- **Second run does:** the concrete double-apply, duplicate, or corruption
- **Fix:** the state check or idempotency key that makes the re-run finish the remainder
- **Effort:** S / M / L

## Backlog
Findings re-sorted by leverage (impact relative to effort), numbered,
one line each: `N. [SEVERITY/EFFORT] title (surface)`.
Cheap high-impact items float to the top regardless of severity.
```

## Common mistakes

- "It's in a transaction, so it's safe." Atomic per attempt is not idempotent across attempts.
- Assuming exactly-once delivery from a queue that promises at-least-once. Read the broker's contract, not the happy path.
- Checking only the clean retry and skipping the crash-halfway-then-rerun shape. Partial state is where the corruption lives.
- Treating idempotency keys on payments and external mutations as a nice-to-have. They are the fix, not an enhancement.
- Flagging read-only code. No side effects means no finding. One line and out.

---

The retry standard and the migration deploy-window lens are adapted from the correctness reviewer in [alp-river](https://github.com/alp82/alp-river) (MIT, Alper Ortac).
