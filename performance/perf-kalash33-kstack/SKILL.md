---
name: perf
description: |
  Profile, measure, optimize. Don't guess where the bottleneck is — measure it.
  Use when: "optimize", "slow", "performance", "profile", "latency",
  "make it faster", or when something takes too long.
---

# /perf — Performance Engineer

Measure first. Optimize second. Verify third.

## Process

1. **Baseline** — Measure current performance (time, memory, throughput)
2. **Profile** — Find the actual bottleneck (not where you think it is)
3. **Optimize** — Fix the bottleneck with minimal code change
4. **Verify** — Measure again. Did it actually improve?
5. **Document** — Record before/after for the PR

## Output

```
## Perf Report

### Baseline
- Response time: 450ms p95
- Memory: 128MB peak

### Bottleneck
- Database query in src/search.ts:42 — full table scan (380ms)

### Fix
- Added index on `users.email` column
- Response time: 45ms p95 (10x improvement)

### Verification
- Load test: 1000 req/s sustained, p99 < 100ms
```
