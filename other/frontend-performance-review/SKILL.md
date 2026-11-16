---
name: frontend-performance-review
description: Review React or web UI implementation for user-visible performance issues. Use when building or optimizing React/Next.js pages, components, data fetching, or bundles.
---

# Frontend Performance Review

Prioritize measured user impact and avoid mechanical micro-optimization.

1. Trace the route/component render path and identify waterfalls, redundant requests, large bundles, expensive computations, and avoidable rerenders.
2. Check server/client boundaries, streaming, caching, hydration, image delivery, and code splitting as relevant to the framework.
3. Prefer parallel data loading when dependencies allow it; do not parallelize dependent operations.
4. Reduce client JavaScript and defer non-critical work without harming accessibility or correctness.
5. Inspect list rendering, memoization, state placement, and expensive visual updates only when evidence suggests they matter.
6. Establish before/after evidence with profiler, build output, network trace, or reproducible benchmark.
7. Check that optimization does not introduce stale data, race conditions, layout shift, or harder-to-maintain code.

Follow current project/framework documentation. Do not claim a speedup without comparable measurements. This skill is a review checklist, not a substitute for profiling.
