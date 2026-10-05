---
name: microservices
description: Use when decomposing a system into services, or deciding whether to. Covers service boundaries, inter-service communication, distributed data, saga patterns, and the operational cost of the network.
metadata:
  category: backend
  version: 1.0.0
  tags: [microservices, distributed-systems, saga, boundaries]
---

# Microservices

## Purpose

Decide where service boundaries belong — and whether you need them at all. Splitting a system converts function calls into network calls, and every network call is a new failure mode you must design for.

## When to Use

- Considering extracting a service from a monolith.
- Defining boundaries for a system that will be built as services.
- Diagnosing a distributed system that has become a "distributed monolith".
- Designing a transaction that spans services.

## Capabilities

- Boundary identification along business capabilities and data ownership.
- Communication design: synchronous versus asynchronous, and when each is correct.
- Distributed data: the outbox pattern, sagas, eventual consistency.
- Resilience: timeouts, retries with backoff, circuit breakers, bulkheads.
- Observability: correlation IDs and distributed tracing.

## Inputs

- The current system and the concrete problem services are meant to solve.
- Team topology — services follow team boundaries whether you intend them to or not.
- Consistency requirements per operation.

## Outputs

- Service boundaries with owned data and a published contract.
- A communication pattern per interaction, chosen deliberately.
- Failure behavior for each cross-service call.

## Workflow

1. **Justify the split** — The valid reasons are independent deployability, independent scaling, and team autonomy. "Microservices are best practice" is not a reason.
2. **Draw boundaries around data** — A service owns its data exclusively. If two services need the same table, they are one service.
3. **Prefer asynchronous** — A synchronous call chain of five services has the availability of the least available one, multiplied. Events decouple.
4. **Design the failure** — For every synchronous call: timeout, retry policy, circuit breaker, and a defined degraded behavior.
5. **Solve distributed writes with the outbox** — Write the state change and the event in one local transaction; publish from the outbox. Two-phase commit across services is not available to you.
6. **Trace everything** — Correlation ID propagated through every hop. Without it, a distributed system is undebuggable.

## Best Practices

- Start with a modular monolith. Enforce module boundaries in code; extract a service only when a module has a genuinely different deployment or scaling need.
- Shared databases between services are the single most common way a microservice architecture becomes worse than the monolith it replaced.
- Retries without idempotency cause duplicate side effects. Retries without backoff cause outages. Both are required, together.
- A synchronous call inside a request path adds its latency and its failure probability to yours. Count the hops.
- Do not build a service per entity. `UserService`, `OrderService`, `ProductService` is a database schema wearing a network.
- Version events. An event schema is a contract with consumers you cannot deploy in lockstep with.

## Examples

**Transactional outbox — the state change and the event commit atomically:**

```sql
BEGIN;
  UPDATE orders SET status = 'paid' WHERE id = $1;

  INSERT INTO outbox (id, aggregate_id, type, payload, created_at)
  VALUES (gen_random_uuid(), $1, 'order.paid',
          jsonb_build_object('order_id', $1, 'amount_cents', $2, 'version', 1),
          now());
COMMIT;
```

A separate relay polls `outbox`, publishes to the broker, and marks rows as sent. If the publish fails, the row remains and is retried; if the transaction rolls back, no event is emitted. The state and the event can never disagree.

**Saga compensation for a booking spanning three services:**

```text
1. Reserve inventory   -> compensate: release inventory
2. Charge payment      -> compensate: refund payment
3. Confirm shipment    -> compensate: cancel shipment

Failure at step 3 runs compensations for 2 and 1, in reverse order.
Each compensation must be idempotent — it will be retried.
```

## Notes

- Eventual consistency is a product decision, not just a technical one. Someone must decide what a user sees during the window, and that decision belongs in the design document.
- Circuit breakers need a defined behavior when open: fail fast, serve stale, or degrade. An open breaker with no fallback is just a faster failure.
- If the team cannot operate one service well — no tracing, no alerting, no runbook — ten services will not go better.
