---
name: cache-architect
description: "Advanced caching strategies, Redis architectural patterns, cache-aside, write-through, and cache stampede prevention."
---

# Advanced Caching Architecture Protocol

Design resilient, consistent, and performant caching tiers.

---

## 1. Cache-Aside Pattern (Standard)

1. Check cache for key. If hit, return data.
2. If miss, load from authoritative database, populate cache with explicit TTL, and return data.
3. On entity update: Invalidate the cache key immediately rather than attempting manual in-place patching.

---

## 2. Cache Stampede Prevention

When high-traffic keys expire, thousands of requests hit the database simultaneously:
1. Implement early probabilistic recomputation (XFetch algorithm) or distributed mutex locks.
2. Recompute the cache in the background right before official TTL expiration when read velocity spikes.
3. Add randomized TTL jitter so grouped keys do not expire simultaneously.
