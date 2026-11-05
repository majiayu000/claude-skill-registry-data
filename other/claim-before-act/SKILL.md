---
name: claim-before-act
description: Use whenever a read-then-write decides WHICH CALLER ACTS — an idempotency claim, a lease, a dedupe marker, a reclaim of an expired or failed row, an approval slot. The write must be a compare-and-swap on the exact row you read (or a serializable transaction); an unconditional update by id lets two racers both win. Triggers on lib/ai/tools/tool-idempotency.ts, lib/services/action-attempts.ts, and any create -> P2002 -> update sequence.
triggers: read-then-write, idempotency claim, lease, dedupe marker, reclaim, expired row, failed row, approval slot, compare-and-swap, serializable transaction, two racers, p2002
---

# Claim before act

## The defect this encodes

2026-09-15, PR #2338 (the durable ActionAttempt contract, built to end
double-sends): the reclaim of an expired or FAILED attempt was

```
findUnique(where: { operationKey })      // both callers read the same reclaimable row
update(where: { id }, data: { state: "EXECUTING", attemptNo: n + 1 })   // both updates succeed
```

Two identical calls arriving after the same expiry both received
`kind: "claimed"` and both would have sent the Telegram. Caught only by
review (Codex P1). The fix was one WHERE clause and one branch:

```
const r = await prisma.actionAttempt.updateMany({
  // every field the DECISION read: identity, version, state — and the
  // deadline the "expired" verdict came from (a renewal changes only that)
  where: { id: existing.id, attemptNo: existing.attemptNo, state: existing.state, holdUntil: existing.holdUntil },
  data:  { ...fresh, attemptNo: existing.attemptNo + 1 },
});
if (r.count === 1) return { kind: "claimed", ... };
const winner = await prisma.actionAttempt.findUnique({ where: { id: existing.id } });
return { kind: "duplicate", state: winner.state, ... };   // the loser never acts
```

## The rule

**A read-then-write that decides who acts is a compare-and-swap, never an
update by id.**

1. Pin the write to EVERY field the decision read — the version-ish fields
   the other branch would have changed (`attemptNo`, `state`, `updatedAt`)
   AND the field the verdict came from: if you decided "expired" from
   `holdUntil` / `expiresAt`, pin that deadline too. A settle changes
   `state`; a reclaim bumps `attemptNo`; a renewal changes only the
   deadline — and a swap that did not pin it still matches the stale
   observation and lets the reclaimer act (Codex review of #2343). A
   monotonic version column covers all three at once, if you have one.
2. `count === 1` wins. `count === 0` re-reads the winner's row and reports
   it (a duplicate with the REAL state) — no retry loop, no second swap.
3. If the store cannot express the swap, use a serializable transaction
   with `SELECT ... FOR UPDATE` — not a hope that two calls are far apart.
4. The unique-key path is the same shape: `create` -> `P2002` -> read the
   existing row -> decide -> swap. The `P2002` catch alone only serializes
   the FIRST claim, not the reclaim.

## The canary (positive-control-first applies)

Two arms, because a mocked `{ count }` cannot see a field missing from the
predicate:

- **Against a real store (preferred):** two callers share one stale read;
  between the first caller's read and its swap, the second RENEWS only the
  deadline (no state or version change). Exactly one acts. A swap that omits
  the deadline lets both act here — that is the case the mocked arm is blind to.
- **Against a mocked store:** assert the swap's WHERE names every field the
  decision read (`id`, `attemptNo`, `state`, `holdUntil`), then the race:
  first swap `{ count: 1 }`, second `{ count: 0 }` -> exactly one `claimed`
  and one `duplicate` carrying the winner's state. Dropping a field from the
  predicate must fail the first assertion, not pass silently.

Then plant the defect (swap -> update by id, `count >= 0`, or a predicate
without the deadline) and watch the canary go red; #2338's did.

## When NOT to use

Writes where every caller is allowed to act (append-only logs, counters,
telemetry). The rule is about EXCLUSIVITY, not about every update.

Related: `assert-the-consumer` (a state field is set only by the code
that saw the write succeed) · `positive-control-first`.
