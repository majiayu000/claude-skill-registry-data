---
name: performance-review
description: Provides performance optimization guidelines for profiling, caching, memory management, and concurrency. Use when optimizing slow code, fixing memory leaks, improving throughput, or conducting performance reviews.
---

# Performance Review Skill

## When to Use

- Code performance optimization
- Memory leak fixes
- Throughput improvements
- Performance review requests
- Bottleneck analysis

## Performance Analysis Workflow

```
Profiling → Identify bottlenecks → Optimize → Verify
```

## Checklist

### Algorithm & Data Structures

- [ ] Time complexity analysis (Big-O)
- [ ] Appropriate data structure selection
- [ ] Remove unnecessary operations

### Memory

- [ ] Minimize memory allocation
- [ ] Object reuse (pooling)
- [ ] Cache-friendly access patterns

### Concurrency

- [ ] Minimize lock contention
- [ ] Leverage async I/O
- [ ] Thread pool optimization

### Caching

- [ ] Appropriate cache strategy
- [ ] Cache invalidation policy
- [ ] Cache hit rate monitoring

## Reference Documents (Import Syntax)
@./reference/performance.md
@./reference/memory.md
@./reference/concurrency.md
@./reference/monitoring.md

## Caution

> "Premature optimization is the root of all evil" - Donald Knuth
>
> Always confirm bottlenecks through profiling before optimizing.
