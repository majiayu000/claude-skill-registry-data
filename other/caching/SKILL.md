---
name: caching
description: Use when adding or debugging a cache. Covers cache placement, invalidation strategies, stampede protection, TTL selection, and the consistency you are trading away.
metadata:
  category: backend
  version: 1.0.0
  tags: [caching, redis, invalidation, performance, stampede]
---

# Caching

## Purpose

Add a cache with a clear invalidation story, or find out why the existing one is serving stale data. A cache is a second source of truth; introducing one is a consistency decision, not just a performance one.

## When to Use

- A read path is slow and the data is read far more often than it is written.
- An upstream dependency is expensive, rate-limited, or unreliable.
- Debugging stale reads, cache stampedes, or unexplained memory growth.

## Capabilities

- Cache placement: client, CDN, application, database.
- Strategies: cache-aside, read-through, write-through, write-behind.
- Invalidation: TTL, explicit, event-driven, versioned keys.
- Stampede protection: locking, early recomputation, request coalescing.
- Negative caching and hot-key mitigation.

## Inputs

- The read/write ratio and the cost of the uncached path.
- How stale the data is allowed to be — in seconds, agreed with the product owner.
- Cardinality of the key space and expected memory footprint.

## Outputs

- A key schema, a TTL, and an invalidation trigger for each cached entity.
- Stampede protection on any key expensive enough to matter.
- A hit-rate metric, because a cache you do not measure is a cache you do not understand.

## Workflow

1. **Prove the need** — Measure the uncached path first. A cache in front of a missing index is a permanent workaround for a five-minute fix.
2. **Decide the staleness budget** — Ask what breaks if a user sees data five seconds old. The answer determines the TTL and whether you need explicit invalidation.
3. **Design the key** — Include everything that varies the result: tenant, locale, permission scope. A key that omits a dimension leaks data between users.
4. **Choose invalidation** — TTL alone for tolerant data. TTL plus explicit deletion on write for data that must be fresh. Versioned keys when deletion is unreliable.
5. **Protect against stampedes** — When a hot key expires, every concurrent request misses simultaneously and hits the origin at once. Use a lock or single-flight.
6. **Measure** — Hit rate, latency at each layer, and eviction rate. Falling hit rate with rising memory means the key space is too large.

## Best Practices

- Cache the expensive computation, not the whole response. Response-level caching multiplies the key space by every variant.
- A cache key missing the tenant or the user's permission scope is a data-leak vulnerability, and it will be found by a customer.
- Never cache with an unlimited TTL and rely on invalidation alone. Invalidation fails; the TTL is the safety net.
- Set memory limits and an eviction policy explicitly (`allkeys-lru`). A Redis instance with no `maxmemory` will be killed by the OOM killer.
- Do not cache errors indefinitely, but do cache "not found" briefly — otherwise a bad ID becomes an origin DoS.
- Warm caches before cutting traffic over. A cold cache under full load is an outage.

## Examples

**Single-flight cache-aside, preventing a stampede:**

```python
async def get_pricing(tenant_id: str, sku: str) -> Pricing:
    key = f"pricing:v3:{tenant_id}:{sku}"

    if (cached := await redis.get(key)) is not None:
        return Pricing.model_validate_json(cached)

    # Only one caller per key computes; the rest wait for the result.
    lock_key = f"{key}:lock"
    if await redis.set(lock_key, "1", nx=True, ex=10):
        try:
            pricing = await compute_pricing(tenant_id, sku)      # expensive
            await redis.set(key, pricing.model_dump_json(), ex=300)
            return pricing
        finally:
            await redis.delete(lock_key)

    # Lost the race: wait briefly for the winner, then fall back to computing.
    for _ in range(20):
        await asyncio.sleep(0.05)
        if (cached := await redis.get(key)) is not None:
            return Pricing.model_validate_json(cached)

    return await compute_pricing(tenant_id, sku)
```

## Notes

- The `v3` in the key is a schema version. When the cached shape changes, bump it — this invalidates the whole namespace atomically without a scan-and-delete.
- Adding jitter to TTLs (`ex=300 + random.randint(0, 60)`) prevents a cohort of keys written together from expiring together.
- A 95% hit rate sounds excellent, but if the 5% of misses are all on the single hottest key, the origin still sees the full load. Look at misses per key, not just the aggregate.
