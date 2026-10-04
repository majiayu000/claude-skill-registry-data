---
name: performance-reliability
description: Use for latency, throughput, concurrency, queues, retries, third-party APIs, uploads, large data, or production reliability; require measurement, bounded work, backpressure, idempotency, and failure-mode evidence rather than optimistic scale claims.
---
# Performance / Reliability

1. Measure current behavior before optimizing when feasible.
2. Bound lists, queries, uploads, tokens, concurrency, retries, queue depth, and request duration.
3. Use timeouts and exponential backoff with jitter; enforce a total retry budget.
4. Prevent retry amplification across SDK + app + gateway layers.
5. Make side effects idempotent before automatic retry/failover.
6. Add circuit breakers or cooldowns for repeatedly failing external dependencies.
7. Prefer graceful degradation/backpressure/load shedding over cascading failure.
8. Test local/fake-provider concurrency and failure behavior before stressing paid/free upstream APIs.
9. Record measured `performance` evidence for performance-sensitive tasks.
