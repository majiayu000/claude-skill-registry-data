---
name: perf-profile
description: Profile and optimize performance of a slow endpoint or component. Use when p99 exceeds 200ms or when asked to optimize.
---

# Performance Profiling

Profile and optimize: $ARGUMENTS

## Steps

1. Measure baseline (p50/p95/p99) using Grafana or k6
2. Read [profiling-guide.md](./profiling-guide.md)
3. Identify bottleneck: DB queries, computation, I/O, or memory
4. Apply appropriate optimization from [patterns.md](./patterns.md)
5. Measure again and compare
6. Document findings in a comment
