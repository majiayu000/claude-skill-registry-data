---
name: rails-distributed-systems
description: Use when Rails/Ruby systems cross process, service, host, queue, or datastore boundaries and correctness depends on delivery semantics, consistency, coordination, or failure recovery.
license: MIT
---

# Distributed Systems & Service Architecture

## Purpose

Treat every cross-process or cross-service workflow as a failure boundary.

The design must make ownership, communication, delivery semantics, consistency, retries, idempotency, recovery, observability, and rollout compatibility explicit.

Core flow:

classify boundary
-> define ownership and invariants
-> define message/API contract
-> choose delivery semantics
-> choose consistency model
-> isolate side effects
-> define retry/deduplication/recovery
-> observe state transitions
-> test failure and replay
-> roll out compatibly

This skill composes with:

- rails-api-integration for synchronous APIs/webhooks;
- rails-event-driven-messaging for message envelopes, broker topology, schema evolution, dead-letter/replay, and messaging capacity;
- rails-active-job for asynchronous execution;
- rails-database-engineering for transaction/constraint/locking boundaries;
- ruby-concurrency for in-process coordination;
- rails-observability for correlation and state-transition diagnostics;
- rails-production-runtime for process topology and shutdown behavior;
- rails-security for trust boundaries and credentials.

## Activate when

- splitting a monolith into services or bounded components;
- designing service ownership or a service boundary;
- publishing domain/integration events;
- using queues, brokers, streams, or asynchronous delivery;
- implementing outbox or inbox/deduplication processing;
- reviewing at-least-once or at-most-once delivery;
- coordinating changes across independent datastores;
- designing eventual consistency or read-model propagation;
- implementing sagas or compensating actions;
- introducing a distributed lock/lease;
- handling duplicate, delayed, reordered, or lost messages;
- defining cross-service retries or failure recovery;
- reviewing distributed transaction assumptions;
- planning rolling deployment across service versions.

Do not activate merely because two Ruby classes communicate. The boundary must cross an independent execution, persistence, or trust domain.

## Repository inspection

Inspect:

1. Ruby/Rails versions and process model;
2. application/service ownership boundaries;
3. databases, schemas, replicas, and transaction semantics;
4. Active Job/queue/broker adapter and delivery guarantees;
5. outbound HTTP/event transport and timeout/retry rules;
6. existing idempotency, deduplication, or uniqueness constraints;
7. event/message schemas and versioning;
8. correlation identifiers and tracing conventions;
9. worker concurrency and downstream capacity;
10. deployment/rolling-release topology;
11. failure/retry/dead-letter/replay tooling;
12. operational state/reconciliation jobs;
13. security/authentication between services;
14. tests for duplicate, delayed, reordered, failed, and replayed work.

Never invent a distributed mechanism when an existing database transaction, unique constraint, job primitive, or local abstraction already owns the invariant.

## Boundary classification

Classify the interaction:

### Synchronous service API

A caller waits for a response.

Primary concerns: contract compatibility, timeout, authentication, retries, and partial failure.

Compose with `rails-api-integration`.

### Asynchronous command

One component requests work and completion occurs later.

Primary concerns: delivery, retry, deduplication, acknowledgement, and status visibility.

Compose with `rails-active-job` and delivery patterns.

### Event publication

A producer announces committed state or a domain fact.

Primary concerns: atomic publication, schema evolution, ordering, replay, and consumer independence.

Use the outbox boundary when database commit and publication must be coupled.

### Cross-service workflow

A business operation spans independent transaction boundaries.

Primary concerns: partial success, compensating actions, workflow state, timeouts, and recovery.

Use a saga only when the workflow truly crosses independent transaction owners.

### Shared coordination resource

Multiple processes must coordinate access to one resource.

Prefer a database constraint or atomic state transition when sufficient. A distributed lock is a coordination primitive, not a substitute for ownership or idempotency.

## Failure model

Explicitly model:

- producer crash before commit;
- producer commit before publish;
- publish timeout after broker accepted;
- consumer crash before side effect;
- consumer crash after side effect before acknowledgement;
- duplicate delivery;
- delayed/reordered delivery;
- dependency outage;
- poison message;
- schema incompatibility;
- deployment overlap;
- stale lock holder;
- partial saga completion.

For each failure, define whether the system retries, deduplicates, compensates, reconciles, dead-letters, or requires operator intervention.

## Decision rules

1. Classify the boundary and model its failures above, then name the owner of each invariant before choosing a mechanism.
2. Load the matching reference below before changing behavior: ownership and delivery semantics (outbox, inbox, retries, consistency), coordination (sagas, distributed locks, multi-region), or ordering, replay, observability, rollout, and testing.
3. Prefer a database constraint or atomic state transition over a distributed lock when it is sufficient.

## Critical invariants

- Do not assume exactly-once execution.
- An outbox does not provide exactly-once publication. Publishers may send the same logical event more than once.
- A distributed lock is a coordination primitive, not a substitute for ownership or idempotency.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change crosses a service or process boundary with messages, retries, or eventual consistency | [references/ownership-and-delivery.md](references/ownership-and-delivery.md) | Ownership and invariants; Delivery semantics; Outbox; Inbox and deduplication; Retries and backpressure; Consistency | `distributed-service-boundary`, `outbox-publication`, `inbox-deduplication`, `eventual-consistency` |
| a change coordinates multi-step workflows, introduces a distributed lock or lease, or spans regions | [references/coordination.md](references/coordination.md) | Sagas; Distributed locks; Multi-region deployments | `saga-orchestration`, `distributed-lock`, `multi-region-data-boundary` |
| a change depends on ordering or replay, or affects distributed telemetry, rollout compatibility, or tests | [references/ordering-rollout-testing.md](references/ordering-rollout-testing.md) | Ordering and replay; Observability; Rollout compatibility; Testing | `distributed-boundary-readiness` |

## Reference example

Idempotency at the edge plus an outbox row: the request may retry, the effect must not duplicate.

```ruby
class CreateCharge
  def initialize(request_id, account)
    @request_id = request_id
    @account = account
  end

  def call(amount_cents:)
    # First write records intent; the unique index makes retries converge.
    outbox = OutboxEvent.create_or_find_by!(
      request_id: @request_id,
      kind: "charge.created"
    ) { |event| event.payload = { account_id: @account.id, amount_cents: amount_cents } }

    if outbox.previously_new_record?
      ChargeProcessorJob.perform_later(outbox.id) # effect enqueued exactly once
    end
    Charge.find_by(request_id: @request_id)
  end
end
```

## Agent review checklist

- [ ] boundary crosses an independent process/service/persistence/trust domain
- [ ] authoritative owner and invariant are explicit
- [ ] delivery semantics are explicit
- [ ] exactly-once assumptions are rejected or justified
- [ ] idempotency/deduplication is durable
- [ ] outbox used when commit/publication atomicity is required
- [ ] inbox/deduplication used for duplicate delivery
- [ ] retry budget and backpressure are bounded
- [ ] consistency model is explicit
- [ ] saga exists only where multiple transaction owners require it
- [ ] compensation/recovery semantics are explicit
- [ ] distributed lock is justified over simpler primitives
- [ ] lock lease/fencing behavior is explicit when applicable
- [ ] multi-region ownership/residency/failover contracts are explicit when data spans regions
- [ ] ordering/replay semantics are explicit
- [ ] failure matrix is reviewed
- [ ] correlation/causation identifiers propagate
- [ ] old/new schema compatibility is considered
- [ ] failure/replay tests exist
- [ ] operational replay/reconciliation path is defined

## Anti-patterns

- assuming exactly-once delivery or execution;
- using local Mutex for cross-process correctness;
- using a distributed lock where a database constraint is sufficient;
- adopting multi-region topology without a residency, latency, or availability requirement single-region cannot meet;
- publishing an event after commit with no durable handoff;
- performing the same side effect from duplicate messages without deduplication;
- putting an entire distributed workflow inside one HTTP request;
- using a saga for a workflow one database transaction already owns;
- retrying at every layer without a combined budget;
- treating eventual consistency as an implementation detail when consumers observe stale state;
- acknowledging messages before required durable state;
- assuming message ordering without a transport/key guarantee;
- logging sensitive cross-service payloads;
- destructive message-schema changes during rolling deployment.

## Verification

Verify the owning boundary, not merely helper classes.

For an event publisher:

`transaction -> outbox -> publisher -> message contract`

For a consumer:

`delivery -> dedupe -> side effect -> acknowledgement`

For a saga:

`state machine -> step outcome -> compensation/recovery`

For a lock:

`acquire -> ownership -> lease/fencing -> release/expiry`

Report tested delivery semantics, duplicate behavior, failure paths, consistency, and rollout assumptions.

## Source foundation

- Rails Active Job: https://guides.rubyonrails.org/active_job_basics.html
- Rails Active Record Transactions: https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
- Rails Active Record Locking: https://api.rubyonrails.org/classes/ActiveRecord/Locking/Pessimistic.html
- Rails Testing Applications: https://guides.rubyonrails.org/testing.html
- Ruby documentation: https://ruby-doc.org/
- Repository skills: rails-api-integration, rails-active-job, rails-database-engineering, rails-observability, rails-production-runtime, rails-security, ruby-concurrency

## Distributed systems and service architecture changes

For changes crossing process, service, host, queue, broker, or independent datastore boundaries:
- classify the boundary and name the authoritative owner of each invariant;
- inspect API/message schemas, transaction ownership, delivery guarantees, retry/dead-letter behavior, and deployment topology;
- never assume exactly-once execution; make at-least-once duplicate behavior explicit;
- use a database constraint, atomic update, row lock, keyed queue, or single authoritative writer before introducing distributed coordination;
- use an outbox when database commit and message publication must be coupled without a distributed transaction;
- use durable inbox/deduplication for duplicate message delivery and reuse existing idempotent-job semantics for queued execution;
- define acknowledgement timing, replay, ordering, and poison-message behavior;
- bound retries/backpressure across all layers instead of multiplying retry loops;
- make eventual consistency visible through explicit pending/stale semantics and reconciliation where applicable;
- use sagas only when independent transaction owners require cross-step compensation/recovery;
- justify distributed locks over simpler primitives and define lease, ownership, expiry, and fencing behavior when stale holders can mutate state;
- propagate correlation/causation identifiers and record state transitions, not only exceptions;
- preserve old/new message compatibility during rolling deploys;
- test duplicate, delayed, reordered, failed, replayed, and partially completed workflows.
