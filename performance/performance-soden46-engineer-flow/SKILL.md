---
name: performance
description: Diagnose and improve runtime performance including N+1 queries, slow queries, caching, latency, memory, throughput, and resource efficiency using framework-agnostic principles.
metadata:
  internal: true
---

# Performance

Use this skill when work involves latency, throughput, resource usage, query efficiency, rendering cost, memory pressure, or scaling bottlenecks.

This skill is technology agnostic.

## Measure First

Do not optimize solely from intuition.

Identify:

- the slow operation
- current baseline
- dominant cost
- expected improvement
- acceptable tradeoffs

Use measurements appropriate to the system.

## Common Bottlenecks

Investigate relevant:

- repeated database queries
- N+1 access
- unnecessary network calls
- repeated computation
- inefficient algorithms
- excessive serialization
- large payloads
- blocking I/O
- unnecessary rendering
- memory growth
- contention
- cache misses
- excessive file operations

Do not assume the database is always the bottleneck.

## Database Performance

Consider:

- query count
- query plans
- indexes
- join behavior
- selected columns
- pagination
- batch operations
- eager/bulk loading
- connection usage

Add indexes based on actual query patterns.

## Caching

Cache when:

- computation or retrieval is meaningfully expensive
- reuse is likely
- consistency requirements are understood

Define:

- cache key
- lifetime
- invalidation
- ownership
- failure behavior

Do not add caching merely to hide an inefficient design without understanding correctness implications.

## Memory

Avoid loading unbounded datasets into memory.

Prefer:

- streaming
- chunking
- pagination
- iterators
- bounded batches

when processing large data.

## Concurrency

Parallelism can improve throughput but may increase:

- contention
- memory usage
- rate-limit pressure
- database load
- ordering complexity

Use bounded concurrency.

## Verification

Compare before and after.

Verify:

- functional behavior remains correct
- measured metric improves
- resource usage remains acceptable
- no significant regression is introduced elsewhere

Performance work without measurement should be treated as a hypothesis, not a proven optimization.

## Framework Adaptation

Use native profiling, caching, ORM, worker, and runtime mechanisms from the detected project stack.

Do not invent framework-specific APIs.
