---
name: rust-bounded-worker-queue
description: Design and validate a bounded worker queue with clear admission, cancellation, retry, fairness, and shutdown semantics.
---

# Rust Bounded Worker Queue

## Goal

Provide predictable concurrency and memory use for CPU-heavy or I/O-heavy work while making overload behavior explicit to callers.

## Inputs to inspect

Queue implementation, worker count, message size, service-time distribution, producer demand, retry policy and shutdown behavior.

## Workflow

1. Define queue capacity using expected item size, service-time distribution and acceptable queue delay; separate capacity from active worker count.
2. Specify admission behavior for full queues, including blocking, immediate rejection, deadline expiry or coalescing by task key.
3. Test fairness among producers, cancellation while queued versus running, worker panic/restart and tasks that exceed service deadlines.
4. Verify graceful shutdown stops new admission, drains or reports remaining work, and joins workers under an explicit deadline.
5. Measure throughput, p95/p99 queue age, memory high-water mark, rejected work and fairness under burst and sustained overload.

## Validation checklist

- [ ] Queue capacity and worker concurrency are independently configured and bounded.
- [ ] Rejected/expired/cancelled tasks are distinguishable from successful results.
- [ ] Worker failure cannot silently strand queue entries or lose task ownership.
- [ ] Shutdown semantics cover both queued work and in-flight work.

## Required output

A queue state machine, capacity rationale, admission/retry policy and burst/saturation/shutdown test report.

## Boundaries and failure handling

Do not default every producer to waiting forever for capacity; deadlines and overload semantics must be caller-visible.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
