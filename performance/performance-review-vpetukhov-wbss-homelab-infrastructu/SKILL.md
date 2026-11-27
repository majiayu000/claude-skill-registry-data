---
name: performance-review
description: "Investigate .NET, EF Core, Blazor and MAUI performance using measured workloads and evidence-based tuning."
---

# Performance analysis
- Obtain baseline metrics and precise workload; distinguish response latency, DB, serialization, network and rendering.
- Diagnose trace/queries/CPU/allocations first. Don't recommend Span, pooling, caching or new technology until bottleneck is proven.
- Evaluate EF generated SQL, indexes, projections, pagination, N+1, connections and locking.
- Evaluate async throughput, ThreadPool starvation, synchronous blocking, HttpClient pools, cache-hit and queues.
- Blazor: component rerenders, virtualization and JS interop; MAUI: startup/layout/image allocations on devices.
- Recommend minimal 1–3 changes; define reproducible benchmark, acceptable regression and rollback; report before/after when executable.
