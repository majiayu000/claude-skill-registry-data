---
name: performance-optimization
description: Use when performance requirements exist, users report slowness, monitoring shows a regression, or profiling identifies a bottleneck across frontend, backend, queries, databases, or resource usage. Do not use for speculative optimization without a measurable problem or target.
license: MIT
---

# Performance Optimization

Measure before optimizing. A performance change is a hypothesis until the
same measurement, under comparable conditions, shows a meaningful improvement
without a correctness regression.

## When to use

- A requirement defines a latency, throughput, resource, bundle, or response
  budget.
- Users, tests, or monitoring report slow behavior or a regression.
- Profiling identifies CPU, memory, I/O, query, rendering, network, or bundle
  cost.
- A feature will handle materially larger data or traffic than existing code.

Do not use this skill to make code "faster" without evidence. Use
`systematic-debugging` when the primary problem is unexplained behavior, and
use `code-simplification` when clarity, not measured performance, is the goal.

## Optimization loop

```text
MEASURE → IDENTIFY → HYPOTHESIZE → CHANGE ONE THING → MEASURE AGAIN → GUARD
```

### 1. Define the target and baseline

Record the user-visible or system metric, threshold, workload, environment,
sample size, and command or profiler used. Prefer a representative workload.
Use project-defined budgets; do not invent a target because a familiar metric
has a convenient threshold.

Repeat noisy measurements and record variance. For user-facing web work,
field data and controlled synthetic measurements answer different questions;
use the repository's existing monitoring and browser/testing setup when
available.

### 2. Find the actual bottleneck

Follow the symptom to the narrowest measurable seam:

- Load or navigation: request waterfall, server time, bundle size, render
  blocking resources, image dimensions, and cache behavior.
- Slow interaction: long tasks, repeated renders, layout work, serialization,
  or synchronous computation.
- Slow API or job: tracing, CPU, memory, external calls, queueing, and
  database timings.
- Slow query: query plan, row estimates, indexes, connection wait, payload
  size, and pagination.
- Memory growth: retained references, unbounded collections, cache size, and
  lifecycle cleanup.

Do not infer a bottleneck from a code smell alone. Capture the evidence that
distinguishes the leading hypothesis from its alternatives.

### 3. Make a narrow change

Choose the smallest reversible change that addresses the measured bottleneck.
Common candidates include batching or joining repeated queries, bounding
fetches, correcting an index based on a query plan, reducing unnecessary
render work, splitting rarely used code, optimizing resource dimensions, or
adding a cache only when its key, staleness, invalidation, and stampede behavior
are defined.

Check correctness while optimizing:

- A cache key must include every input that changes the result, including
  tenant, locale, identity, permissions, and feature flags where applicable.
- Do not cache values whose staleness violates correctness.
- Do not add an index, pool capacity, concurrency, or retry merely because it
  sounds faster; measure its read, write, saturation, and failure costs.
- Preserve pagination, authorization, validation, ordering, and required work.

### 4. Verify, keep, or revert

Re-measure with the same command, workload, conditions, and budget as the
baseline. Compare the result with run-to-run variance, not just the mean.
Keep a change only when:

- The relevant metric improves beyond noise or meets the stated target.
- Existing correctness checks remain green.
- Resource and operational costs are acceptable.

Revert a change that is neutral, worse, unmeasurable, or dependent on weakened
tests. Log both kept and reverted experiments so failed ideas are not repeated.

### 5. Guard against regression

Add the smallest useful guard: a performance budget, benchmark, query-plan
check, resource limit, alert, trace, or field metric. Guard the metric that
motivated the work, not every available number. If a guard fires, establish a
fresh baseline before proposing another optimization.

## Output

Return a concise record of:

- Symptom, target, workload, baseline, and measurement conditions.
- Bottleneck evidence and the rejected or remaining hypotheses.
- The change, before/after numbers, variance, and correctness evidence.
- Guard added, experiments reverted, and residual risks.

If profiling or representative data is unavailable, report the limitation and
do not claim a performance improvement.

## Upstream basis

Adapted for this harness-agnostic repository from
[addyosmani/agent-skills performance-optimization](https://github.com/addyosmani/agent-skills/tree/6ca0cd7db39b41b1c37e26d335c507ee92382c6d/skills/performance-optimization),
licensed under MIT.
