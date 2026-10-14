---
name: performance-optimization
description: Measure-first approach — profile before optimizing, Core Web Vitals, bundle analysis, database query optimization. Prevents premature optimization while catching real performance issues.
---

# Performance Optimization

## Problem it solves

Performance work is often done wrong:
- Premature optimization: making code complex for speed gains that don't matter
- Guessing at bottlenecks instead of measuring them
- Optimizing the wrong things (hot path vs cold path)
- Shipping known-slow code without profiling
- Missing performance budgets entirely
- Micro-optimizations that add complexity for 1% gains

## Protocol

### 1. Measure first, optimize second

Never optimize without profiling data:
1. **Establish a baseline** — measure current performance (response time, throughput, memory, bundle size)
2. **Set a target** — what needs to improve and by how much?
3. **Profile to find the bottleneck** — don't guess, use tools
4. **Optimize the bottleneck** — only what the profile identified
5. **Measure again** — did it actually improve? By how much?

If you cannot measure the improvement, you haven't optimized — you've just made the code more complex.

### 2. What to measure

| Area | Tool / Method | Key metrics |
|------|--------------|-------------|
| API response time | Profiler, APM, load testing | P50/P95/P99 latency, throughput |
| Database queries | Query analyzer, EXPLAIN | Query time, rows scanned, indexes used |
| Frontend bundle | Bundle analyzer | Total size, per-package size, duplicate deps |
| Frontend rendering | Browser DevTools, Lighthouse | FCP, LCP, TTI, CLS |
| Memory | Heap profiler | Allocation rate, GC pauses, leak detection |
| Build time | Build tool timings | Incremental vs full build, cache hit rate |

### 3. Optimization priority

Optimize in this order (highest impact first):
1. **Algorithmic** — O(n^2) → O(n log n) or O(n). Biggest gains.
2. **Caching** — Memoize, cache database results, CDN for static assets
3. **I/O** — Batch database queries, reduce network calls, use connection pooling
4. **Memory** — Avoid unnecessary allocations, reuse objects, lazy loading
5. **Micro-optimizations** — Loop unrolling, inline functions, bit twiddling (last resort, smallest gains)

### 4. Performance budgets

Set budgets for key metrics and enforce them in CI:

| Metric | Budget | Action |
|--------|--------|--------|
| API P95 latency | <500ms | Alert if exceeded |
| Bundle size | <200KB JS, <50KB CSS | Fail build if exceeded |
| LCP | <2.5s | Fail build if exceeded |
| Database query time | <100ms per query | Flag for review |

### 5. Premature optimization prevention

Before spending time on optimization, ask:
- **Is this on the hot path?** — Code executed once per request is rarely worth optimizing
- **What's the user-impact?** — Will they notice the improvement?
- **What's the complexity cost?** — Is the simpler-but-slower version good enough?
- **Is there data?** — Do you have a profile showing this is a bottleneck?

If the answer is "no" to any of these, don't optimize yet.

## Detection triggers

Activate when:
- User says "optimize", "make faster", "improve performance", "slow"
- Response times are high or increasing
- Bundle size is growing
- Database queries are slow
- A profile or benchmark is available
- Setting up performance monitoring

## When NOT to use

- Prototyping or exploration (optimize later)
- One-off scripts or internal tools
- When correctness is still being established (fix bugs first, then optimize)
- User explicitly says "just make it work, don't optimize"

## Cross-references

- **code-review** — The performance axis of review should flag obvious bottlenecks and premature optimization.

- **code-simplification** — Optimization often complicates code. Balance performance gains against simplicity.

- **incremental-implementation** — Each slice should meet performance targets before the next slice starts.

- **test-driven-development** — Performance tests should be part of the test suite. Include benchmarks for hot paths.

- **ci-cd-automation** — Performance budgets should be enforced in CI. Add benchmark comparison jobs to the pipeline.

- **follow-existing-patterns** — Performance optimizations should match the project's existing approach (caching strategy, query patterns, etc.).

- **anti-premature-termination** — "Optimized" is not done until you can show the measured improvement.
