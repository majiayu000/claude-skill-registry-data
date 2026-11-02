---
name: rust-channel-backpressure
description: Audit Rust channel-based pipelines for queue growth, blocked producers, dropped messages, and shutdown behavior under load.
---

# Rust Channel Backpressure

## Goal

Make asynchronous and threaded pipelines remain bounded and observable when consumers are slower than producers.

## Inputs to inspect

Channel types and capacities, producer/consumer tasks, message semantics, cancellation paths, queue metrics and shutdown policy.

## Workflow

1. Map each channel edge with producer count, consumer count, queue capacity, message size, ordering needs and whether loss is acceptable.
2. Trace overload behavior for bounded/unbounded channels: producer blocking, try-send failures, drops, retries, and propagation of downstream errors.
3. Stress uneven producer/consumer rates, slow I/O, consumer panic/cancellation, and shutdown while messages remain queued.
4. Measure queue depth, oldest-message age, blocked duration and rejected/dropped messages; define which signals mean overload versus normal burst handling.
5. Choose an explicit policy per edge—await capacity, reject, coalesce, shed low-priority work or persist—and test graceful drain and abort behavior.

## Validation checklist

- [ ] Queues have deliberate capacity or a documented, measured reason to be unbounded.
- [ ] Dropped or rejected messages have explicit semantics and metrics.
- [ ] Shutdown cannot wait forever on a producer or consumer that has already failed.
- [ ] Retry policies do not create duplicate side effects or amplify overload.

## Required output

A channel-topology map, per-edge overload policy, saturation metrics, and load/shutdown test results.

## Boundaries and failure handling

Do not solve backpressure by simply increasing every queue; that can convert visible overload into memory growth and long-tail latency.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
