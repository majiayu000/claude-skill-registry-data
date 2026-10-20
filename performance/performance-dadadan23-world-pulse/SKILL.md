---
name: "performance"
description: 'Optimize application performance through async patterns, caching strategies, profiling, and resource management. Use when diagnosing slow endpoints, implementing caching layers, profiling CPU/memory bottlenecks, optimizing database queries, or setting up performance monitoring.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Performance

> **Purpose**: Optimize application speed, throughput, and resource usage for production loads. 
> **Strategy**: Profile first, optimize bottlenecks, measure impact. 
> **Note**: For language-specific implementations, see [C# Development](../../development/csharp/SKILL.md) or [Python Development](../../development/python/SKILL.md).

---

## When to Use This Skill

- Diagnosing slow application endpoints
- Implementing caching strategies
- Profiling CPU or memory bottlenecks
- Optimizing database query performance
- Setting up performance monitoring and alerting

## Prerequisites

- Application running in a profiling-capable environment
- Access to monitoring tools

## Decision Tree

```
Performance concern?
+- Not yet measured? -> Profile FIRST (don't guess)
| +- .NET -> dotnet-trace / BenchmarkDotNet
| +- Python -> cProfile / py-spy
| - Node.js -> clinic.js / --prof
+- Slow API response?
| +- Database query? -> EXPLAIN ANALYZE -> add index
| +- External service? -> Add caching + async calls
| - Computation? -> Optimize algorithm or add memoization
+- High memory usage?
| +- Large collections? -> Stream/paginate instead of loading all
| - Memory leaks? -> Profile allocations, check dispose patterns
+- Concurrency bottleneck?
| +- I/O bound? -> async/await (don't block threads)
| - CPU bound? -> Parallel processing / background workers
- Quick wins? -> See Quick Wins table below
```

## Quick Wins

| Optimization | Impact | Effort |
|--------------|--------|--------|
| **Enable Response Compression** | 70-90% size reduction | Low |
| **Add Database Indexes** | 10-100x query speed | Low |
| **Implement Caching** | 50-99% latency reduction | Medium |
| **Use Async I/O** | 5-10x throughput | Medium |
| **Fix N+1 Queries** | 10-1000x DB performance | Medium |

---

## Performance Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Premature Optimization** | Optimize before profiling | Profile first, optimize bottlenecks |
| **Over-Caching** | Cache everything | Cache strategically based on access patterns |
| **Blocking I/O** | Synchronous network calls | Use async/await |
| **No Pagination** | Load all results | Paginate large datasets |
| **Missing Indexes** | Full table scans | Add indexes on frequently queried columns |
| **N+1 Queries** | Loop over queries | Use JOINs or batch loading |

---

## Optimization Checklist

**Before Production:**
- [ ] Profile application under realistic load
- [ ] Add database indexes on frequently queried columns
- [ ] Implement caching for expensive operations
- [ ] Enable response compression
- [ ] Fix N+1 query problems
- [ ] Use connection pooling
- [ ] Implement async I/O where applicable
- [ ] Paginate large result sets
- [ ] Set up monitoring and alerts
- [ ] Conduct load testing
- [ ] Set performance budgets
- [ ] Optimize static asset delivery

---

## Resources

**Profiling Tools:**
- **.NET**: BenchmarkDotNet, dotTrace, PerfView
- **Python**: cProfile, py-spy, Scalene
- **Node.js**: clinic.js, 0x, Chrome DevTools
- **Java**: JProfiler, VisualVM

**Load Testing:**
- [k6](https://k6.io) - Modern load testing
- [Apache JMeter](https://jmeter.apache.org) - Industry standard
- [Gatling](https://gatling.io) - Scala-based testing

**Guides:**
- [Web Performance Working Group](https://www.w3.org/webperf/)
- [High Performance Browser Networking](https://hpbn.co)

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md)

**Last Updated**: January 27, 2026

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`run-benchmark.ps1`](scripts/run-benchmark.ps1) | Run benchmarks (.NET/Python/Node) with baseline comparison | `./scripts/run-benchmark.ps1 [-Baseline baseline.json]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cache stampede on expiry | Use cache-aside with staggered TTL or background refresh |
| Memory leak in production | Profile with dotMemory/py-spy, check for unbounded collections |
| High latency spikes | Check GC pauses, database connection pool, and external service timeouts |

## References

- [Profiling Caching Db](references/profiling-caching-db.md)
- [Optimization Techniques](references/optimization-techniques.md)