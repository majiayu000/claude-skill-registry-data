---
name: systems
description: "Distributed-systems foundations: queues, events, locks, idempotency, consistency, retries, breakers. Use when work spans services, queues, or failure-prone networks."
---

# systems

Design for failure: at-least-once delivery, idempotent receivers, bounded retries, explicit consistency choices.

## Activate when

- Adding queues (Kafka/RabbitMQ/SQS), events, webhooks, or cross-service calls.
- Debugging duplicates, lost messages, or cascading failures.

## Do NOT activate for

- Single-process logic (see architecture/modularity).

## Procedure

1. Delivery: assume at-least-once; make every consumer idempotent (idempotency keys, dedupe tables) and every producer retry-safe.
2. Consistency: state the guarantee per workflow (strong vs eventual) and where users can observe staleness.
3. Coordination: distributed locks with fencing/leases for truly exclusive work; prefer partitioning (`SKIP LOCKED`-style claim) over global locks.
4. Resilience: timeouts on every call, retries with jitter + budgets (never unbounded), circuit breakers around failing dependencies, bulkheads for critical paths.
5. Backpressure: bounded queues, caller-visible shedding (429/queue-depth metrics), chunked background work.
6. Verify: duplicate-delivery test, consumer-restart test, dependency-down test, and a load test showing where the system sheds first.

## References
- Related: `../../backend/concurrency/`, `../../backend/transactions/`, `../../architecture/observability/`.
