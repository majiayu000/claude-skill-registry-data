---
name: event-driven-architect
version: 1.0.0
description: Event-driven architecture — event/command taxonomy, Protobuf schemas, topic naming, mandatory outbox, partitioning, idempotency, DLQs, schema evolution. Broker-agnostic (NATS/Kafka/RabbitMQ). Use when designing event flows or auditing consistency.
---

# Event-Driven Architecture

Patterns for services that communicate via asynchronous events. **Broker-agnostic** at the conceptual level; defaults inline per use case (NATS for lightweight, Kafka for log-based replay, RabbitMQ for command queues). **Protobuf schemas** for events ([protobuf-architect](../../encoding/protobuf-architect/SKILL.md)) so contracts get the same `buf breaking` discipline as gRPC. **Outbox pattern is mandatory** for any write that emits an event. Schemas, SQL, and tooling shapes in [RECIPES.md](RECIPES.md); pinned brokers and client libs in [STACK.md](STACK.md).

## 1. Event vs message vs command — the three shapes

| Shape | Direction | Semantics | Example |
|---|---|---|---|
| **Event** | Past-tense, broadcast | "Something happened" — fact about the past, anyone can listen | `OrderPlaced`, `PaymentCaptured` |
| **Command** | Imperative, point-to-point | "Do this" — request to one specific handler | `CancelOrder`, `SendEmail` |
| **Message** | Generic envelope | Container for either — used when the distinction doesn't matter | (mostly an implementation detail) |

- **Events are immutable past-tense facts.** `OrderPlaced` was placed; nothing changes that. Subscribers react however they want.
- **Commands have one intended handler.** Multiple handlers reacting to a command is almost always wrong — it's an event in disguise. Rename it.
- **Naming:** events are `<Noun><PastVerb>` (`OrderPlaced`, `ShipmentDispatched`); commands are `<Verb><Noun>` (`PlaceOrder`, `SendShipment`).
- **Choose the shape per use case**, not per technology. Both Kafka and RabbitMQ can carry either; the discipline is in the schema and contract.

## 2. Schema — Protobuf

Per [protobuf-architect](../../encoding/protobuf-architect/SKILL.md): events are `.proto` messages, code-generated, validated by `protovalidate`, and protected from breaking changes by `buf breaking` in CI.

**Envelope contract** (every event):

- `event_id` — UUID v7, sortable + unique. Subscribers dedupe on it.
- `occurred_at` — RFC 3339 timestamp. Replay tools sort by this.
- `aggregate_id` — the entity the event is about. Drives partitioning.
- `schema_version` — integer; bump on additive changes inside a topic version.

**Payload discipline:**

- **Minimal.** IDs and the few facts subscribers need — not the full aggregate state. Subscribers fetch via [sql-architect](../../databases/sql-architect/SKILL.md) repositories. Big payloads make schema evolution and replay expensive.
- **Field numbers reserved on delete** per [protobuf-architect §3](../../encoding/protobuf-architect/SKILL.md#3-field-numbering--reservation-discipline). Never reuse.
- **One file per resource's events** — `orders/v1/events.proto` holds every event the orders context emits.

Canonical schema in [RECIPES §1](RECIPES.md#1-canonical-event-schema).

## 3. Topic / subject naming

Hierarchical, snake_case, versioned. Pick a convention and enforce it.

```
<org>.<context>.<resource>.<version>.<event_name>
```

- Matches the Buf-style package path from protobuf-architect.
- **Version is part of the topic name**, not just the schema. New major version → new topic. Run in parallel until consumers migrate.
- **Lowercase + dots** (NATS, Pub/Sub) or **lowercase + underscores** (Kafka). Pick one for your broker and stick to it.
- **Document the catalog** somewhere queryable — Confluent Schema Registry, BSR, or a simple `events.md` in the repo.

Examples in [RECIPES §5](RECIPES.md#5-topic--subject-naming-reference).

## 4. Outbox pattern — mandatory for "DB write + event emit"

The dual-write problem: an HTTP handler writes a row and publishes an event. If the DB commits but the broker rejects, the event is lost — silent inconsistency. If the broker accepts but the DB rolls back, subscribers process a phantom event.

**Outbox fixes this with a single transactional write.**

1. Handler `BEGIN TX` → `INSERT INTO aggregate` → `INSERT INTO outbox` → `COMMIT`.
2. Separate publisher reads unpublished rows, sends them to the broker, marks them published.

- **Outbox is a regular table** in the same DB as the aggregate. The write is atomic with the business write.
- **Publisher is separate** — a goroutine, a sidecar, a cron, or **CDC** (Debezium reading Postgres WAL). CDC is the most robust; goroutine is fine for small services.
- **At-least-once delivery** — the same event can be republished if the publisher crashes between PUBLISH and UPDATE. Consumers must be idempotent (§6).
- **Outbox table grows** — partition or purge published rows older than 7–30 days.
- **Why mandatory:** there is no working pattern that avoids both the lost-event and phantom-event failure modes without the outbox. Anything else (publish-before-commit, publish-after-commit) is broken under failure.

Schema + publisher shapes in [RECIPES §2](RECIPES.md#2-outbox-table--publisher).

## 5. Ordering and partitioning

Event ordering is the single hardest part of event-driven systems. **Order is per-key, not global.**

- **Order is preserved within a partition / subject**, but not across partitions. Kafka partitions by message key; NATS via subject hierarchy; RabbitMQ via consistent-hash exchanges.
- **Partition key is the aggregate ID.** All events for `order_id=abc` land on the same partition, processed in order by one consumer. Different orders process in parallel.
- **Globally-ordered events are a smell.** If you "need" global order, you actually need a single consumer (and you've lost scaling), or you're modeling the domain wrong.
- **Consumers process one partition at a time per instance.** Concurrent processing within a partition breaks ordering. Most client libs handle this; verify your config.

## 6. Idempotency — consumer must dedupe

Brokers deliver at least once. Consumers see the same event more than once under network failure, restart, or rebalance.

- **Dedupe by `event_id`.** Each consumer keeps a small store (Redis with TTL, or a `processed_events` table) of recently-seen IDs. Reject duplicates.
- **Idempotent side effects** — design the handler so a duplicate is harmless: `INSERT ... ON CONFLICT DO NOTHING`, `UPDATE ... WHERE version = ?` (with optimistic concurrency).
- **TTL on dedupe store** — events older than the broker's retention can't be replayed anyway.
- **Exactly-once illusion**: idempotent consumer + at-least-once delivery = "effectively exactly-once" from the business perspective. Don't chase true exactly-once at the protocol level — far more expensive than just making consumers idempotent.

Concrete handler + dedupe table in [RECIPES §3](RECIPES.md#3-consumer-idempotency).

## 7. Dead-letter queues (DLQs)

Some events can't be processed — schema mismatch, downstream service down too long, business invariant violation. Don't let them block the partition.

- **Every consumer has a DLQ.** A topic / subject named `<original>.dlq` receives messages the consumer gave up on.
- **Retry policy first, DLQ second.** N attempts with exponential backoff (typical: 3 attempts), then DLQ.
- **DLQs are monitored.** Per [observability-architect](../../infra/observability-architect/SKILL.md): a Prometheus counter `<svc>_dlq_messages_total` with an alert on any non-zero value. A DLQ that quietly fills is a silent outage.
- **DLQ tooling** — operator scripts to inspect, replay, or discard. Both audited.

Retry policy + tool CLI shape in [RECIPES §4](RECIPES.md#4-dlq-topic--replay-tooling).

## 8. Backpressure

When the consumer can't keep up with the producer, the system needs to slow down — gracefully.

- **Prefetch / consumer concurrency limits.** Don't let one consumer instance buffer 10,000 in-flight messages.
- **Lag-based autoscaling.** Watch consumer-group lag; scale out the consumer pool when lag grows.
- **Reject upstream** when persistently overloaded — return `503 Service Unavailable` with `Retry-After` per [rest-api-architect §3](../../protocols/rest-api-architect/SKILL.md#3-status-codes). Better than building a backlog you can't drain.
- **No unbounded queues in memory.** A handler that reads from one topic and writes to another needs bounded size + a timeout.

Per-broker tuning knobs in [RECIPES §6](RECIPES.md#6-backpressure-tuning-per-broker).

## 9. Schema evolution

Per [protobuf-architect §4](../../encoding/protobuf-architect/SKILL.md#4-versioning) — additive changes stay in the version; breaking changes go to a new `vN`.

- **Additive:** new optional field, new enum value, new event type on a new topic. Safe.
- **Breaking:** field removal, type change, semantic change. Bump to `<topic>.v2`; both run side-by-side until consumers migrate.
- **`buf breaking` in CI** catches accidental breakage in the proto files. Per [protobuf-architect §8](../../encoding/protobuf-architect/SKILL.md#8-breaking-change-detection--buf-breaking-in-ci).
- **Consumer compatibility tests** — for each known consumer version, replay a sample event and assert it deserializes cleanly. Catches semantic-level breakage that's still wire-compatible.

## 10. Saga / orchestration / choreography

For multi-step workflows that span services. Two opposing patterns — comparison table in [RECIPES § 6](RECIPES.md#6-choreography-vs-orchestration).

- **Start with choreography** — events flowing service-to-service, each subscriber reacts. Simpler.
- **Promote to orchestration** (Temporal, Camunda, AWS Step Functions) when the flow is genuinely complex — 5+ services, branching, retries, compensation.
- **Compensation actions** for partial failures: `OrderCancelled` undoes `PaymentCaptured` via `RefundIssued`. Domain-level, not technical rollback.
- **Correlation ID** propagated through every event in a saga — ties the chain together ([observability-architect §5](../../infra/observability-architect/SKILL.md#5-correlation)).

## 11. Broker selection — when each fits

The pattern in §1–10 works on any modern broker. Full strengths/best-for table in [RECIPES § 7](RECIPES.md#7-broker-selection-reference). Defaults:

- **Lightweight: NATS JetStream** — single binary, conf-driven, easy to operate.
- **Log-based: Kafka** — when replay, retention, and analytics consumers matter.
- **Command queues / legacy fit: RabbitMQ** — when integration with non-Kafka non-NATS systems forces the choice.
- **Cloud-managed (SNS+SQS, Pub/Sub, Service Bus)** — when ops cost matters more than feature parity.

Pick once per system; switching mid-flight is expensive.

## 12. Cross-skill ties

- [protobuf-architect](../../encoding/protobuf-architect/SKILL.md) — event schemas + `buf breaking` discipline.
- [grpc-architect](../../protocols/grpc-architect/SKILL.md) — synchronous counterpart; when a call should be RPC vs event.
- [sql-architect](../../databases/sql-architect/SKILL.md) — outbox lives in your domain DB; same transactional discipline.
- [ddd-architect §6](../../design/ddd-architect/SKILL.md#6-domain-events) — domain events as the natural source of integration events.
- [observability-architect](../../infra/observability-architect/SKILL.md) — consumer lag, DLQ depth, processing latency are first-class metrics.
- [grafana-architect](../../infra/grafana-architect/SKILL.md) — per-consumer-group lag dashboards; DLQ alerts.
- [rest-api-architect §8](../../protocols/rest-api-architect/SKILL.md#8-idempotency--idempotency-key-mandatory) — the HTTP `Idempotency-Key` discipline is the same idea consumers need internally.
