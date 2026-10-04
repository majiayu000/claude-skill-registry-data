---
name: performance-optimization
description: Guidance for identifying bottlenecks, measuring impact, and making pragmatic performance improvements without cargo-cult optimization.
compatibility: opencode
metadata:
  audience: performance
  purpose: optimization-guidance
---
# Performance optimization

## Core approach

- Measure before and after when feasible.
- Focus on actual bottlenecks and workload behavior.
- Prefer clear changes with material impact over complex micro-optimizations.
- Keep maintainability in view while improving performance.

## Practical guidance

- Consider data volume, latency, allocation, concurrency, rendering cost, query shape, and caching behavior where relevant.
- Call out assumptions behind measurements and likely next bottlenecks.
