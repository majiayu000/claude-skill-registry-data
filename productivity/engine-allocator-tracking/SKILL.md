---
name: engine-allocator-tracking
description: Add or audit allocator tagging and allocation tracing to attribute engine memory growth to subsystems and lifetimes.
---

# Engine Allocator Tracking

## Goal

Make significant memory allocations traceable without imposing unbounded logging overhead or changing allocation semantics.

## Inputs to inspect

Allocator wrappers, subsystem boundaries, resource ownership types, build configurations, telemetry and memory regressions.

## Workflow

1. Define a small stable taxonomy for subsystem, allocation class, lifetime expectation and ownership source; avoid per-object labels with unbounded cardinality.
2. Identify allocation APIs and paths that bypass the engine allocator, and state explicitly which memory pools are outside instrumentation scope.
3. Choose sampling or event aggregation based on overhead requirements, ensuring allocation/free pairing and realloc semantics remain consistent.
4. Exercise repeated create/destroy, scene reload and failure paths; verify outstanding bytes and counts return to expected levels after teardown.
5. Measure instrumentation overhead and add thresholds for unexplained subsystem growth or outstanding allocations in controlled tests.

## Validation checklist

- [ ] Allocation and free accounting handles reallocations and failed allocations correctly.
- [ ] Tags are stable enough to compare across builds and avoid sensitive payload contents.
- [ ] Instrumentation overhead and missing coverage are disclosed.
- [ ] Teardown tests distinguish expected persistent caches from unintended survivors.

## Required output

A tag taxonomy, instrumentation-coverage map, subsystem allocation report and repeatable leak/growth check.

## Boundaries and failure handling

Do not store raw user data in allocation labels or claim complete tracking when system/driver allocations are unobserved.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
