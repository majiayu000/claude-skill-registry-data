---
name: engine-frame-time-budget
description: Allocate and measure CPU/GPU frame budgets to find recurring stalls, overloaded systems, and latency regressions.
---

# Engine Frame Time Budget

## Goal

Turn a target frame rate into explicit budgets, measurements, and accountable subsystem limits.

## Inputs to inspect

Target frame rate, frame-time captures, engine phases, platform targets, GPU timings when available, and recent regressions.

## Workflow

1. Convert the target rate into a frame-time ceiling and define a separate budget for simulation, world streaming, rendering submission, UI, synchronization, and slack. Keep CPU and GPU timing domains distinct.
2. Capture representative scenes and worst-case transitions with warm-up and enough samples to report median, p95, p99, and maximum frame time.
3. Use instrumentation to separate active work from waits, locks, resource uploads, allocation spikes, shader compilation, and main-thread joins.
4. Rank costs by contribution to missed-frame events, then change one major factor at a time. Include a before/after trace and confirm the same workload was used.
5. Add a lightweight performance gate for stable critical paths and define an investigation threshold for regressions instead of failing on noisy single-run results.

## Validation checklist

- [ ] Metrics identify the sampling interval, build mode, machine, scene, and frame definition.
- [ ] CPU and GPU timings are not incorrectly summed when they overlap asynchronously.
- [ ] Tail latency and stutters are investigated even when average FPS looks healthy.
- [ ] Optimization does not remove correctness checks or shift the bottleneck into another unmeasured phase.
- [ ] The result includes a rollback or follow-up action if the target is still missed.

## Required output

Produce a budget table, trace references, current bottleneck, measured change, remaining headroom, and a repeatable profiling recipe.

## Boundaries and failure handling

Do not present average FPS alone as proof of smoothness; do not optimize a subsystem based solely on intuition.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
