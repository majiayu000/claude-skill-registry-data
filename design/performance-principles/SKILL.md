---
name: performance-principles
description: Performance guidelines and patterns for this system.
---

# Performance Principles

## General Principles

- Optimize for correct, clear code first; then optimize hot paths.
- Measure before optimizing when possible.
- Prefer algorithmic improvements over micro-optimizations.

## Common Pitfalls

- N+1 queries in database access.
- Unbounded in-memory collections for large datasets.
- Synchronous calls in latency-sensitive paths.
- Repeated expensive computations without caching.

## Guidelines by Layer

### Backend

- Use efficient query patterns and indices.
- Batch calls where practical.
- Apply backpressure and rate limiting where needed.

### Frontend

- Avoid unnecessary re-renders.
- Lazy-load heavy components and routes.
- Cache data appropriately (client & server).

## Monitoring & Metrics

- Ensure critical paths have basic instrumentation:
  - Latency, error rate, throughput.
- Define performance budgets (e.g., 95th percentile latency thresholds).

## When to Escalate

- If a change risks breaching performance budgets.
- If complexity grows significantly (e.g., big-O behavior worsens).
