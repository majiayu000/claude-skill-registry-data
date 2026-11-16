---
name: book--designing-data-intensive-applications--nano
description: >-
  DDIA (Martin Kleppmann) — Minimal rules — essential one-liners only. Use when asked to apply DDIA principles or review code against DDIA standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Designing Data-Intensive Applications by Martin Kleppmann

## When to use

Use when data correctness, durability, or distributed write semantics matter more than local code style.

## Primary bias to correct

Hidden data contracts are still contracts.

## Decision rules

- State the source of truth, consistency expectation, durability point, visibility point, retry semantics, and evolution path for every important data change.
- Choose data models, storage, indexes, replication, partitioning, transactions, queues, streams, and APIs from workload, access pattern, consistency, reliability, maintainability, and operational cost.
- Treat caches, indexes, projections, search copies, denormalized data, and materialized views as derived data with staleness, lag visibility, repair, and rebuild paths.
- Make retried, replayed, queued, batch, stream, and event-driven work idempotent or transactional; reject casual exactly-once claims.
- Treat schemas, encodings, service APIs, messages, logs, and events as versioned contracts that must survive old code, old data, rolling upgrades, and in-flight messages.
- Assume distributed uncertainty: crashes, partial writes, timeouts, duplicate messages, reordered events, stale replicas, lag, clock error, pauses, stale leaders, and unknown success.
- Match replication, partitioning, isolation, transactions, and coordination to the invariant; do not rely on follower freshness, quorum formulas, weak isolation, wall-clock order, or ad hoc leadership without proof.

## Trigger rules

- When adding retries, jobs, consumers, queues, CDC, event sourcing, or stream processing, prove duplicate, replay, ordering, side-effect, and recovery safety.
- When changing schemas, APIs, messages, events, enum values, or status meanings, plan backward and forward compatibility plus migration, bootstrap, or rebuild paths.
- When reading from replicas or partitioning data, define staleness, routing, hot-key, ordering, rebalancing, and cross-partition behavior.
- When using locks, leases, timestamps, leadership, majorities, or coordination services, define the fault model, quorum/session semantics, stale-authority behavior, and fencing.

## Final checklist

- Clear owner and source of truth?
- Explicit consistency, durability, visibility, and staleness semantics?
- Safe under retry, replay, duplicate delivery, reordering, and unknown success?
- Compatible across old data, old code, new code, and messages in flight?
- Isolation, replication, partitioning, transactions, and coordination checked against actual invariants?
