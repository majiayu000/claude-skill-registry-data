---
name: concurrency
description: "Concurrency: async vs sync, pools, timeouts, retries, circuit breakers, bounded concurrency. No unbounded fan-out."
---

# concurrency

Concurrency is bounded by design: pools, timeouts, and backpressure — never unbounded fan-out.

## Activate when

- Async code, worker pools, parallel fan-out, or any shared mutable state across tasks/threads.

## Do NOT activate for

- Language primitives themselves (see languages/*); cross-service resilience topology (see distributed/systems).

## Inspection

Find shared state, blocking calls inside async paths, pool sizes, timeout/retry settings, and what happens at 10× load.

## Decision rules

- Async for I/O-bound, threads/processes for CPU-bound; never blocking calls on event loops (offload or use async drivers).
- Bounded everything: pool sizes, queue depths, in-flight counts; backpressure (shed/slow) instead of unbounded growth.
- Timeouts on every call; retries only idempotent ops with jitter + budgets; breakers around repeatedly failing dependencies.
- Shared state minimized: message-passing/channels preferred; locks small, ordered consistently, never held across I/O.

## Procedure

1. Diagram the concurrency (tasks, shared state, pools, timeouts).
2. Bound and time-box each layer; add backpressure with visible signals (429/queue metrics).
3. Stress it: 10× load, slow-dependency, and chaos (kill workers mid-flight) tests.
4. Verify: no unbounded growth under load, graceful degradation demonstrated, race detector/sanitizer clean where available.

## Failure modes

- Unbounded goroutine/task spawn; blocking DB driver on async loop; retry storms; lock-order deadlocks; shared cache without invalidation.

## Escalation

Runtime specifics → languages/go, languages/rust, languages/python; topology → distributed/systems.

## References

- Related: `../transactions/`, `../caching/`, `../../architecture/error-handling/`.
