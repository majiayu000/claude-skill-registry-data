---
name: ruby-concurrency
description: Use when Ruby/Rails code performs concurrent work, shares mutable state across threads, uses queues or executors, uses Fibers, or has race conditions, deadlocks, thread-safety, or ordering hazards.
license: MIT
---

# Ruby Concurrency

## Purpose

Design and review concurrent Ruby/Rails code so execution model, ownership, synchronization, lifecycle, failure propagation, and resource limits are explicit.

Concurrency is not automatically parallel CPU execution. Identify the workload and bottleneck before selecting a primitive.

## Activate when

- `Thread`, `Queue`, `Mutex`, `Monitor`, or thread pools are introduced
- shared mutable state is accessed concurrently
- an intermittent race, ordering bug, deadlock, or starvation issue exists
- Rails jobs/services perform concurrent I/O
- database or HTTP connection pools constrain concurrency
- Fibers, schedulers, or async I/O are introduced
- thread safety of caches, registries, memoization, or clients is under review
- code relies on Ruby engine execution behavior

Do not activate merely because code is slow. Establish whether concurrency addresses the actual bottleneck.

## Repository inspection

Inspect:

1. Ruby engine and runtime version
2. existing thread, queue, pool, Fiber, job, and executor abstractions
3. ownership of shared mutable state
4. database connection-pool configuration
5. HTTP/client limits and timeouts
6. executor/thread lifecycle and shutdown behavior
7. existing synchronization conventions
8. tests covering ordering, retries, failure, and cleanup
9. deployment process/worker topology when relevant

Resolve runtime compatibility before relying on engine-specific behavior.

## Concurrency model selection

| Workload | Candidate |
|---|---|
| independent blocking I/O | bounded threads/thread pool |
| CPU-heavy Ruby work | processes or an appropriate external worker |
| producer/consumer | `Queue` or existing bounded queue |
| shared small mutable state | `Mutex`/ `Monitor` around the invariant |
| state-transition waiting | condition variable or existing coordination abstraction |
| asynchronous I/O | Fibers/scheduler only when supported |
| Rails background work | existing job/executor infrastructure |
| one-off parallel tasks | explicit start, wait, failure, and shutdown lifecycle |

Do not create a custom executor when the repository/framework already owns the concern.

## Core rules

### Ownership

Prefer single ownership of mutable state.

Document who creates, reads, mutates, and releases shared state.

### Synchronization

Protect an invariant, not an entire service.

Prefer a narrow critical section:

```ruby
mutex.synchronize { @balance += amount }
```

Keep critical sections small. Avoid database/network I/O while holding a lock.

### Lifecycle

Every worker/executor needs:

```text
create -> start -> perform -> observe failure -> stop/join -> release
```

Do not leave application-managed threads detached from shutdown.

### Failure propagation

Worker failures must be observable. Define whether the parent fails, remaining work stops, retries occur, or cleanup continues.

## Mutex, Monitor, and Queue

Use `Mutex` for narrow mutual exclusion. Use `Monitor` only when re-entrant coordination is actually required.

Use `Queue` for thread-safe producer/consumer coordination.

Avoid nested locks with inconsistent ordering, sleeping while locked, and calling unknown collaborators while locked.

For queues, define worker count, backpressure, shutdown/sentinel behavior, queue growth, and exception handling.

## Bounded concurrency

For blocking I/O, bound concurrency against:

- database connection pool
- HTTP connection limits
- external API rate limits
- memory per worker
- CPU availability
- remote service limits
- timeout duration

Never create one thread per unbounded input.

A larger worker count is not automatically faster.

## Rails-specific rules

Prefer Rails' existing job, executor, and lifecycle mechanisms over long-lived application-managed threads.

When Active Record is used concurrently:

- account for connection-pool capacity;
- follow the repository's connection-management conventions;
- do not assume a transaction in one thread covers work in another;
- use database constraints, atomic updates, transactions, or locking for persisted invariants;
- remember that an in-process `Mutex` cannot coordinate separate processes, workers, containers, or hosts.

For jobs, assume concurrent execution and retries. Make important state transitions idempotent.

## Database concurrency

Let the database own persisted invariants where appropriate:

- unique constraints for uniqueness
- atomic updates for counters
- transactions for related writes
- locking mechanisms when repository/database conventions require them
- optimistic locking when concurrent edits should be detected

Do not use Ruby synchronization to protect a cross-process database invariant.

## Fibers

Fibers are cooperative execution and are not interchangeable with threads.

Before using them:

1. confirm runtime support;
2. identify the scheduler/evented I/O model;
3. confirm libraries cooperate;
4. define cancellation/error behavior;
5. keep execution-model boundaries explicit.

Do not introduce Fibers merely because they are lightweight.

## Race conditions

Look for check-then-act sequences:

```ruby
if cache[key].nil?
  cache[key] = expensive_load
end
```

If correctness depends on interleaving, establish an atomic/locked boundary or use a data structure with the required contract.

Test races with controlled interleavings rather than arbitrary sleeps.

## Deadlocks

Typical causes include inconsistent lock ordering, nested locks, waiting for workers while holding their required resource, and executor starvation.

For multiple locks, establish one acquisition order.

Diagnosis:

```text
blocked stacks
-> held/waited resources
-> wait-for graph
-> cycle
-> remove/reorder dependency
-> regression test
```

Do not "fix" deadlocks with larger timeouts or sleeps without identifying the cycle.

## Thread-safety review

Classify shared objects as:

```text
immutable
thread-confined
synchronized
atomic
process-local
externally synchronized
unsafe
```

Do not call an object thread-safe merely because of Ruby's GVL/GIL-like implementation detail. Establish safety from the object contract and access pattern.

## Testing

Prefer deterministic synchronization:

- barriers/latches where supported
- controlled queues
- injected collaborators
- explicit state transitions

Avoid `sleep` as the primary synchronization mechanism.

Test normal completion, concurrent updates, worker failure, shutdown, retries/idempotency, and bounded resource behavior.

A single successful stress run does not prove race or deadlock freedom.

## Performance

Measure before increasing concurrency.

Inspect throughput, latency, queue depth, lock contention, pool saturation, external limits, CPU, memory, and thread count.

Compare representative concurrent workloads with a sequential baseline.

## Anti-patterns / failure modes

- one thread per input item
- detached background threads
- global mutex around an entire service
- sleeping to fix races
- relying on the GVL for application correctness
- sharing non-thread-safe clients
- in-memory locks for cross-process invariants
- I/O inside locks
- inconsistent nested lock ordering
- swallowed worker exceptions
- unbounded queues
- custom executors replacing existing Rails/repository infrastructure
- Fibers without a compatible scheduler/I/O model
- increasing concurrency without measuring capacity

## Implementation procedure

1. Resolve Ruby engine/version and framework runtime.
2. Classify workload and actual bottleneck.
3. Identify ownership and shared invariants.
4. Prefer existing repository/framework concurrency infrastructure.
5. Select the smallest primitive that enforces the invariant.
6. Bound workers and queues against real resource limits.
7. Define lifecycle, failure propagation, and shutdown.
8. Add deterministic concurrency tests.
9. Measure representative performance when optimization is the goal.
10. Run focused and broader regression checks.
11. Inspect the final diff for leaked resources and unnecessary abstraction.

## Agent review checklist

- [ ] Ruby engine/version resolved
- [ ] workload/bottleneck identified
- [ ] ownership is explicit
- [ ] shared invariants identified
- [ ] concurrency primitive justified
- [ ] critical sections are minimal
- [ ] external I/O is not unnecessarily held under locks
- [ ] workers/queues are bounded
- [ ] failures are observable
- [ ] lifecycle is explicit
- [ ] Rails connection-pool implications checked
- [ ] cross-process invariants are not protected by in-process locks
- [ ] tests use deterministic synchronization
- [ ] retry/idempotency behavior checked
- [ ] performance measured when relevant
- [ ] focused/regression tests actually run

## Verification

Use repository-configured test/lint commands first.

For concurrent changes, run the focused concurrency test and affected test group. Run RuboCop when configured.

Never claim race freedom, deadlock freedom, or scalability from a single successful run.

## Source foundation

Repository-process guidance for AI coding agents based on Ruby/Rails concurrency engineering principles. It intentionally avoids assuming a particular Ruby engine, Rails version, executor library, or deployment topology. Repository evidence takes precedence.

## Book integration: *The Well-Grounded Rubyist*

Chapter 14 includes Ruby thread examples and shared-variable concerns. Treat it as introductory conceptual material only: it is based on Ruby 2.1 and does not define the complete behavior of current Ruby runtimes, servers, or concurrency libraries. Resolve the runtime and deployment model, make ownership/synchronization explicit, and validate race/failure behavior with tests.
