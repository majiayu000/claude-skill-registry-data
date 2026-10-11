---
name: caching
description: Caching — in-memory, distributed, CDN, invalidation, TTL.
---

## Cache Tiers

| Tier | Type | Latency | Scope | Examples |
|------|------|---------|-------|---------|
| L1 | In-memory (process) | <1ms | Single instance | Node.js Map, Python dict, Guava Cache |
| L2 | Distributed | 1–10ms | All instances | Redis, Memcached, Hazelcast |
| L3 | CDN | 5–50ms | Global edge | Cloudflare, Fastly, CloudFront |
| L4 | DB query cache | varies | DB layer | PostgreSQL result cache, MySQL query cache |

Read from L1 first; fall through to L2, then origin. Write invalidation must propagate through all tiers.

## When to Cache

- Expensive DB queries (aggregations, joins across large tables)
- External API responses (weather, exchange rates, third-party lookups)
- Computed aggregates (leaderboards, dashboards, reports)
- Session and auth tokens
- Rendered HTML fragments or full pages (SSR)
- Infrequently changing config or feature flags

Do not cache: user-specific mutable data without scoping by user ID, financial transactions, anything that must be strongly consistent.

## TTL Strategy

| Data Type | Recommended TTL | Rationale |
|-----------|----------------|-----------|
| Real-time feeds | 30s – 2m | Balance freshness vs. load |
| API third-party | 1m – 5m | Respect upstream rate limits |
| Session data | 15m – 1h (sliding) | Security + convenience |
| Computed aggregates | 5m – 30m | Rebuild cost justifies staleness |
| Static reference data | 1h – 24h | Rarely changes |
| CDN / public assets | 1d – 1y + immutable | Content-addressed URLs |

Use event-driven invalidation (not TTL) when data changes are known immediately (e.g., user profile update).

## Invalidation Patterns

| Pattern | How it works | Best for |
|---------|-------------|---------|
| TTL expiry | Entry removed after fixed time | Tolerable staleness |
| Explicit delete-on-write | App deletes cache key on mutation | Strong consistency needs |
| Cache-aside (lazy) | Read miss → load from DB → populate cache | General purpose |
| Write-through | Write to cache and DB atomically | Read-heavy, low write latency tolerance |
| Write-behind (write-back) | Write to cache; async flush to DB | Write-heavy, eventual consistency OK |
| Tag-based invalidation | Keys tagged; invalidate by tag | Content with multiple dependencies |

Cache-aside is the safest default. Write-through and write-behind require careful failure handling.

## Cache Key Design

- Prefix by domain: `user:profile:{id}`, `product:detail:{sku}`
- Include schema version when the value structure may change: `v2:user:profile:{id}`
- Scope by tenant in multi-tenant systems: `{tenant}:user:profile:{id}`
- Never embed PII (email, SSN, phone) in cache keys — keys may appear in logs
- Use deterministic serialization for composite keys (sort query params alphabetically)

## Thundering Herd Prevention

When a popular cache entry expires, many requests can hit the origin simultaneously.

- **Probabilistic early expiration (PER):** re-compute the cache value slightly before expiry based on a random probability — no locks required
- **Mutex / single-flight:** first request acquires a lock and populates the cache; others wait and read the result
- **Stale-while-revalidate:** serve the stale value immediately; refresh asynchronously in the background

## Cache Warming

- Pre-populate critical hot paths on deploy (e.g., homepage data, top-N products)
- Run a warm-up job as part of the deployment pipeline before traffic shifts
- Use read-through warming: replay recent production traffic in staging to pre-fill cache
- Monitor cache hit rate after each deploy; alert if it drops below baseline

## Redis-Specific Guidelines

- Use `SCAN` with a cursor — never `KEYS` in production (blocks the event loop)
- Use pipelining (`pipeline()`) for bulk reads/writes to reduce round-trip overhead
- Set `maxmemory-policy allkeys-lru` so Redis evicts least-recently-used keys under memory pressure
- Use Redis Cluster or Sentinel for high availability — never treat Redis as durable storage
- Prefer atomic operations (`SETNX`, `INCR`, Lua scripts) over read-modify-write sequences to avoid race conditions
- Set explicit `TTL` on every key — unbounded keys are a memory leak
