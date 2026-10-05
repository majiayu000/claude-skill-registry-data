---
name: padosoft-durable-effects
description: >-
  Use this skill when work leaves the request and happens later — a background job, a queue, a worker, a
  webhook consumer, a scheduled task, a retry — and whenever the user reports that something ran twice, that
  a job was processed by two workers, that a retry charged or sent a second time, that a cancelled job still
  reported success, that a worker hung or exited with a late error, or that a job vanished. It covers lease
  and fencing semantics, exactly-once effects, terminal states, cancellation, and what a durable queue needs
  that an in-memory one does not. Do not use it to choose a queue technology, to tune throughput or worker
  counts, or for request-scoped transactions (padosoft-atomic-invariants covers those).
license: MIT
compatibility: >-
  Stack-agnostic. Examples assume a relational store behind the queue, because that is where the fencing and
  serialisation semantics become explicit.
metadata:
  version: 0.2.0
  author: Padosoft
  summary: A queue moves work, not effects — claim the effect atomically before performing it.
  profiles: api, data
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: queue, worker, lease, idempotency, exactly-once, webhook, retry, cancellation, fencing
---

# Durable effects

A queue moves *work*. It does not move **effects**. Everything below is a way a system with a correct queue
still charges twice, ships twice, or reports success for something it killed.

**The rule: claim the effect atomically before performing it, and make every terminal outcome a state you
can read back.**

---

## 1. Delivery is not the problem. The effect is

```text
signature verified  →  still not idempotent
lease reclaimed     →  still not exactly-once
retry with the same key → still a second charge, unless something refused it
```

A valid retry carries a valid signature and runs capture, fulfilment or entitlement again. Verification and
idempotency are **two separate prior checks**, and only one of them protects the effect.

**Claim a logical effect key atomically before running the effect**: treat the same event as a duplicate,
and reject a *different* event that reuses the key. In a multi-replica deployment the unique constraint in
the durable store is the boundary — not a check in application code, and not a cache.

## 2. Reclaiming a lease is a race you can lose quietly

A stale processing claim has to be reclaimable after a crash, or a dead worker blocks the queue forever. But
the previous holder may have completed the external side effect **in the moment before it died**.

The ledger can stop the duplicate *state transition*. Only an idempotency key on the external side makes the
external operation safe across that reclaim. If the downstream system has no such key, say so out loud: the
system is at-least-once, and the design has to tolerate it.

## 3. A lease is owned, and ownership can be lost

| Event | Correct outcome |
|---|---|
| Handler still running, lease near expiry | renew **with the exact fencing token** |
| Renewal fails | abort the handler, report *lease lost* |
| Lease lost | **not** an acknowledgement and **not** a failure — a third outcome |
| Job force-killed by an operator | a durable `cancelled` state, lease cleared, late acknowledgements rejected |

Marking a killed job `done` hides the abort and lets reporting claim success. Cancellation is its own
terminal state, scoped to the tenant, and the worker's cooperative abort is a separate step that the queue
mutation must not imply.

Polling for cancellation is not enough on a long job: the visibility timeout can expire while the handler is
still working, and another worker picks up the same job.

## 4. Stopping is harder than starting

- **Clearing a timer does not cancel an in-flight request.** A pending receive or renew is still awaiting a
  remote response, so a worker that closes its server after one pass gets an unhandled rejection later.
  Track an active flag, **check it after every await**, and catch post-stop queue errors so shutdown
  produces a fenced result instead of background noise.
- **Killing a shell child is not killing the process tree** it spawned.
- **Retries need a terminal policy.** An unbounded retry is an outage amplifier; a retry that gives up
  silently is data loss. Name the maximum, name where an exhausted job goes, and make that queue observable.

## 5. Durable means the store, not the label

- **A durable queue on top of a volatile store is volatile.** The guarantee belongs to what persists the
  message, not to the interface in front of it.
- **A pub/sub notification channel is not a queue.** It is useful for low-latency fan-out and it loses
  messages across a disconnect, with a payload limit on top. Persist first, then notify, and reconcile.
- **Bootstrap needs serialisation.** A conditional `CREATE TABLE IF NOT EXISTS` makes one statement
  repeatable; it does not make a multi-step bootstrap safe when two fresh replicas start at once. Take a
  transaction-scoped advisory lock and do the whole schema step inside it.
- **Cross-replica retry cannot rely on a filesystem check.** Use a database primary key, insert atomically,
  and compare the stored digest on conflict.

## 5b. A batch with per-row outcomes

An import, an export, a bulk recalculation: one job, thousands of rows, each with its own fate. Five rules,
and the first one is where the data actually goes wrong.

- **Counters are derived, never incremented.** `increment()` on a progress counter from parallel chunks is
  a lost update on every collision, and the drift is invisible because the number still looks plausible.
  Recompute with one aggregate over the rows themselves — they are the source of truth — after each flush,
  each chunk, and each manual edit.
- **Validation is orchestrated by the base, not overridden by the concrete type.** Give it phases — the
  declarative rules, then per-field checks found by convention, then the cross-field hook — so a new import
  type can only fill in the parts, never replace the sequence and silently skip one.
- **The row processor returns an identifier or throws.** It does **not** record its own failure: the caller
  owns the outcome, marks the row and moves on. A processor that writes its own error state and returns
  normally makes a failed row indistinguishable from a successful one that produced nothing.
- **Progress is broadcast at a bounded rate**, not per row. A real-time event per row on a large file is a
  denial of service you wrote yourself.
- **Re-running protects what already completed.** Delete and re-parse only the rows that are not in a
  terminal state, skip the completed ones while parsing, and let the recount include them. Otherwise a
  re-validation silently undoes work somebody already reviewed.

## 6. Event streams and replay

- **An event id is not replay.** Persist the event *before* publishing the notification, subscribe before
  replaying, deduplicate across the overlap, and signal a missing or expired cursor explicitly instead of
  returning an empty result. Replay lowers recovery cost; it does not replace refetching authoritative
  state.
- **A server-sent stream is a transport, not a durable event source.** Reconnection converges from the
  authoritative projection, not from what the stream remembers.
- **Signature plus raw body plus clock.** A webhook signature is computed over the exact bytes received, so
  it must be verified before any parsing middleware rewrites them, and it needs a timestamp tolerance to
  stop replays of a genuinely signed request.

## 7. Worker identity

A worker that can take any job can take any tenant's job. Require an explicit verifier or a deployment
credential **before boot**, compare it in constant time, keep it out of diagnostics, and enforce the tenant
scope inside dequeue *and* again on acknowledge — see **`padosoft-tenant-isolation`**. A static token is a
visible bootstrap fallback, never the production answer.

---

## Gotchas

- **An in-memory queue test proves your control flow and nothing about the engine**: migration locks, lease
  fencing and serialisation failures only appear against the real store. See
  **`padosoft-evidence-boundaries`**.
- **A timeout is not a negative result.** The effect may have happened. Classify it as *unknown* and
  reconcile against authoritative state before mutating anything else.
- **Priority is not fairness.** A strict priority queue starves the low-priority tenant indefinitely; decide
  which one you meant.
- **Recovery must not depend on the thing that failed.** A cleanup job that only runs inside a healthy
  worker never runs on the day it is needed.
- **Emergency controls have to cross the worker boundary.** A kill switch the workers cannot observe is a
  switch for the dashboard.

## Checklist

- [ ] The effect key is claimed atomically **before** the effect, with duplicates and key-reuse both handled
- [ ] Signature/authenticity verified as a separate, prior check
- [ ] Lease renewal uses the fencing token; lease loss is its own outcome, not an ack and not a failure
- [ ] Cancellation is a durable state; late acknowledgements rejected
- [ ] Shutdown checks its active flag after every await, and catches post-stop errors
- [ ] Retry policy bounded, with a named destination for exhausted work
- [ ] The durable store is what persists the message; notifications are not the queue
- [ ] Bootstrap serialised under a transaction-scoped lock
- [ ] Replay: persist before publish, subscribe before replay, explicit missing-cursor signal
- [ ] Webhooks verified on the raw body, with a clock tolerance
- [ ] Worker identity required at boot; tenant scope enforced at dequeue and at ack
- [ ] The journey exercised against the real engine at least once

## Final report

```
Path: <producer> → <queue/store> → <worker> → <effect>
Effect key: <what is claimed, where, atomically?>   Duplicate handling: <…>
Lease: renew <…> · loss <…> · cancellation <state>
Retries: <max> → <destination>        Terminal states: <list>
Store: <durable? what persists the message>
Identity: worker <…> · tenant scope at dequeue/ack: yes | no
Proven against the real engine: yes | no
```
