---
name: rails-event-driven-messaging
description: Use when Rails/Ruby applications publish, consume, route, replay, evolve, or operate asynchronous events, commands, queues, brokers, or streams.
license: MIT
---

# Event-Driven Architecture & Messaging Engineering

## Purpose

Treat asynchronous messaging as an executable platform contract rather than a transport detail.

A reliable event-driven system makes message identity, schema, ownership, partitioning/order, delivery, acknowledgement, retry, dead-letter, replay, observability, and capacity explicit.

Core flow:

classify message
-> identify producer/consumer ownership
-> define envelope and schema
-> choose delivery and ordering semantics
-> choose partitioning/consumer model
-> define handler boundary
-> define retry/dead-letter/replay
-> instrument message lifecycle
-> size broker/consumer capacity
-> test duplicates/failures/compatibility
-> operate and evolve safely

Compose this skill with:

- rails-distributed-systems for distributed ownership and consistency;
- rails-api-integration for synchronous integration contracts;
- rails-active-job for Rails queue execution;
- rails-database-engineering for durable inbox/outbox state;
- rails-observability for message lifecycle diagnostics;
- rails-production-runtime for worker/process topology;
- ruby-concurrency for bounded consumer concurrency;
- rails-security for trust and secret boundaries;
- rails-test-engineering for deterministic message tests.

## Activate when

- publishing domain/integration events;
- consuming messages from queues, brokers, or streams;
- designing topics, queues, routing keys, partitions, or consumer groups;
- choosing ordering or parallel-consumption semantics;
- evolving event/message schemas;
- introducing dead-letter queues or poison-message handling;
- building replay or backfill tooling;
- reviewing consumer lag, throughput, or broker capacity;
- adding message tracing/correlation;
- defining event envelopes and metadata;
- changing retry/acknowledgement behavior;
- migrating between message transports;
- designing event-driven workflows.

Do not activate merely because a background job exists. Use this skill when the message itself is an architectural integration boundary.

## Repository inspection

Inspect:

1. Ruby/Rails/runtime versions;
2. queue/broker/stream technology and adapter;
3. message transport guarantees: delivery, ordering, retention, visibility/ack;
4. producer/consumer ownership and service boundaries;
5. event/message schemas and serializer/versioning convention;
6. topic/queue/routing-key/partition conventions;
7. consumer-group or worker topology;
8. retry, dead-letter, replay, and poison-message tooling;
9. outbox/inbox/idempotency implementations;
10. correlation/tracing and structured logging;
11. worker concurrency, database pools, and provider limits;
12. deployment/rolling-release compatibility;
13. security/authentication/encryption at the messaging boundary;
14. existing fixtures, contract tests, and integration tests.

Do not assume Kafka-style semantics, FIFO semantics, visibility timeouts, or exactly-once guarantees unless the actual transport/version documents and configuration support them.

## Decision rules

1. Classify the change: message taxonomy, envelope, and schema evolution; topology, consumer groups, handlers, and acknowledgement; retry, dead-letter queue, and replay; or observability, capacity, security, rollout, and testing.
2. Load the matching reference below before changing behavior; a new consumer needs both the topology and the failure-and-replay reference.
3. Give every message a stable message identity and make every handler idempotent against it.

## Critical invariants

- A replay should not accidentally trigger user-visible effects twice.
- Do not retry a poison message forever.
- Use the transport-specific acknowledgement contract; never invent "ack after enqueue" semantics without verifying what durability that represents.
- Support old/new schema coexistence and keep handlers compatible until old messages are drained or explicitly migrated.
- Do not use a schema registry as permission to make incompatible changes.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change defines a message type, alters the envelope, or evolves a message schema | [references/message-contracts.md](references/message-contracts.md) | Message taxonomy; Envelope contract; Schema evolution | `event-envelope`, `event-schema-evolution`, `message-delivery-contract` |
| a change alters topics/queues/routing keys/partitions, consumer groups, handler boundaries, or acknowledgement | [references/topology-and-consumers.md](references/topology-and-consumers.md) | Topic, queue, routing-key, and partition design; Consumer groups and parallelism; Handler boundary; Acknowledgement | `consumer-group-partitioning`, `message-handler-boundary` |
| a change alters consumer retries, the dead-letter queue, poison-message handling, replay, or backfill | [references/failure-and-replay.md](references/failure-and-replay.md) | Retry policy; Dead-letter queues and poison messages; Replay and backfill | `dead-letter-replay` |
| a change affects message telemetry, broker capacity, consumer authorization, deployment ordering, or messaging tests | [references/operations-and-testing.md](references/operations-and-testing.md) | Message observability; Capacity and backpressure; Security; Rolling deployments; Testing | `message-observability`, `broker-capacity`, `event-consumer-authorization-contract` |

## Reference example

Domain events over Active Support notifications with a queue-backed subscriber: publishing is synchronous, effects are not.

```ruby
module Billing
  class Invoice
    def mark_paid!(at: Time.current)
      update!(paid_at: at)
      ActiveSupport::Notifications.instrument(
        "invoice.paid",
        invoice_id: id, account_id: account_id, paid_at: at
      )
    end
  end
end

Rails.application.config.to_prepare do
  ActiveSupport::Notifications.subscribe("invoice.paid") do |event|
    # Subscriber stays trivial; work is enqueued so publish() never blocks.
    InvoicePaidHandlerJob.perform_later(event.payload.slice(:invoice_id, :account_id))
  end
end
```

## Agent review checklist

- [ ] message classified as command/event/notification/retry
- [ ] envelope and identity defined
- [ ] producer/consumer ownership explicit
- [ ] schema versioning strategy explicit
- [ ] partition/routing key justified
- [ ] ordering scope explicit
- [ ] consumer-group parallelism bounded
- [ ] acknowledgement boundary explicit
- [ ] retry classification and budget explicit
- [ ] poison-message handling explicit
- [ ] dead-letter retention/replay policy explicit
- [ ] replay authorization and rate limit explicit
- [ ] correlation/causation propagated
- [ ] payload logging minimized
- [ ] broker/consumer capacity measured or bounded
- [ ] old/new rolling compatibility verified
- [ ] duplicate/failure/replay tests exist

## Anti-patterns

- treating a queue as a database;
- assuming exactly-once processing;
- generating new event identity on retry;
- mixing command and event semantics without a contract;
- using one global ordering key for the whole system;
- scaling consumers without checking partitions/database/API capacity;
- retrying poison messages indefinitely;
- dead-lettering without replay ownership;
- replaying without idempotent handlers;
- logging sensitive message payloads;
- destructive schema changes while old messages remain;
- acknowledging before durable work completion;
- allowing every application layer to depend directly on broker-specific APIs.

## Verification

For producers:

`domain commit -> message identity/schema -> publication -> observability`

For consumers:

`decode -> validate -> dedupe -> handler -> acknowledgement`

For failure handling:

`retry -> backoff -> dead-letter -> operator review -> controlled replay`

For capacity:

`arrival rate -> consumer throughput -> dependency capacity -> lag/backpressure`

Report schema compatibility, duplicate safety, delivery/ack semantics, replay behavior, observability, and capacity assumptions.

## Source foundation

- Rails Active Job: https://guides.rubyonrails.org/active_job_basics.html
- Rails Active Record Transactions: https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
- Rails Testing Applications: https://guides.rubyonrails.org/testing.html
- Ruby documentation: https://ruby-doc.org/
- Repository skills: rails-distributed-systems, rails-api-integration, rails-active-job, rails-observability, rails-production-runtime, ruby-concurrency, rails-security

## Event-driven messaging changes

For queue, broker, stream, event, and message changes:
- classify the message as command, event, notification, or retry/control message;
- resolve actual transport guarantees for delivery, ordering, retention, acknowledgement, and partitioning;
- define stable message identity, envelope metadata, schema version, correlation, and causation;
- preserve old/new message compatibility during rolling deployments and replay;
- choose routing/partition keys from ordering requirements and hot-key evidence;
- bound consumer concurrency against partitions, database pools, downstream API limits, CPU, and memory;
- make acknowledgement timing explicit and never acknowledge before required durable work;
- classify retryable versus permanent failures and terminate poison-message loops;
- define dead-letter ownership, retention, remediation, authorization, and controlled replay;
- preserve original message identity during retry/replay;
- instrument publish, queue age/lag, processing, retries, dead-letter, and replay state without logging sensitive payloads;
- test duplicate delivery, failures before/after side effects, schema compatibility, dead-letter routing, replay, ordering, and restart/rebalance behavior.
