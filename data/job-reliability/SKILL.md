---
name: job-reliability
description: This skill should be used when the user mentions "background jobs", "queue", "worker", "dead letter", "DLQ", "retry", "at-least-once", "exactly once", "outbox", "idempotent consumer", "visibility timeout", "BullMQ", "Celery", "Sidekiq", "SQS", "Pub/Sub", "Kafka", or "RabbitMQ", or auditing background-job/message-consumer code for reliability. It provides at-least-once handling patterns, DLQ/backoff/visibility recipes per broker, and message-deduplication strategies.
---

# Job Reliability

## Purpose
Provide a standardized methodology for making background jobs and message consumers reliable under the delivery guarantee that nearly every queue actually offers: **at-least-once**. That guarantee has two consequences every consumer must handle: **duplicates** (the same message is delivered more than once) and **partial failure** (the worker crashes after doing the work but before acknowledging). Code that ignores either will silently double-charge, double-send, lose messages, or stall. This skill catalogs the gaps and the fixes, statically, from the worker source.

## The at-least-once contract
- **Duplicates are guaranteed, eventually.** A network blip, a redelivery after a visibility timeout, or a consumer restart re-delivers a message. → **Make consumers idempotent** (see `references/dedup-strategies.md`).
- **Ack means "I'm done," not "I received it."** Ack/commit the offset **after** the side effect succeeds, never before. Ack-then-work loses the message on a crash.
- **Poison messages exist.** A message that always fails must not retry forever, route it to a **dead-letter queue** after a bounded number of attempts.
- **Retries need backoff + jitter.** Immediate infinite retries create a thundering herd against a failing dependency.

## The reliability checklist (audit every consumer against this)

| Axis | The gap | The fix |
|---|---|---|
| Idempotency | Side effect runs again on redelivery (double charge/email) | Dedup store keyed by message-id/business key; check before acting |
| Ack ordering | Ack/commit **before** the work completes | Ack **after** success; nack/retry on failure |
| Dead-letter | Poison message retries forever or is dropped | DLQ / dead-set after N attempts; alert on it |
| Retry policy | No backoff, or fixed immediate retry | Exponential backoff **with jitter**, capped attempts |
| Visibility/redelivery | Work outlives the visibility timeout → concurrent redelivery | Timeout ≥ processing time, or extend/heartbeat |
| Atomic "work + ack" | Crash between work and ack | Idempotency makes the inevitable redelivery safe |
| Outbox | DB commit then publish (dual write), crash loses the event | Transactional outbox: write event in the same tx; a relay publishes |

## Ordering: the crux of correctness
The single most important line to read in any consumer is **where the ack/commit happens relative to the side effect**:
- `receive → ack → do work` : **loses** work on a crash after ack. Wrong for anything that matters.
- `receive → do work → ack` : at-least-once done right, a crash before ack redelivers, and idempotency absorbs the duplicate.
- `receive → do work → publish → ack`, where publish and a DB write must both happen: needs the **outbox**, or a crash between the two loses the event.

## The transactional outbox (when an event must not be lost)
Writing to the database **and** publishing to a broker are two systems, you cannot commit both atomically. If you `COMMIT` then publish, a crash in between loses the event; if you publish then commit, a rollback emits a phantom event. The fix: write the event row into an `outbox` table **in the same transaction** as the business change; a separate relay (poller or CDC/log-tailing) reads the outbox and publishes, marking rows sent. The publish becomes at-least-once (so consumers still dedup), but the event can never be lost.

## Additional Resources
### Reference Files
- **`references/queue-patterns.md`**: per broker (BullMQ, Celery, Sidekiq, RabbitMQ, AWS SQS, Google Pub/Sub, Kafka): the ack model, how to configure retries/backoff, the DLQ mechanism, visibility-timeout/redelivery handling, and the idiomatic idempotent-consumer shape, plus the transactional-outbox recipe.
- **`references/dedup-strategies.md`**: deduplication approaches: dedup stores (Redis `SET NX`, SQL unique constraint), message-id vs idempotency-key vs business-key dedup, dedup windows, and how to build an exactly-once **effect** on top of at-least-once delivery.
