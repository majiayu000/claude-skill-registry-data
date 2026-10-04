---
name: redis
description: "Design Redis keys and caching with appropriate TTLs, data structures, and eviction behavior; inspect memory or pub/sub issues."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["redis", "cache", "ttl", "datastructures", "sessions", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Redis Caching & Data Structures AI Skill Guide

## Overview & Engine Architecture

Redis is an in-memory data structure server used for caches, session stores, rate limits, queues, and coordination. Commands operate on typed keys (string, hash, list, set, sorted set, stream). Agents always set TTLs on cache keys, avoid `KEYS *` in production, and treat Redis as volatile unless persistence is explicitly designed.

```
App clients
   -> Redis (single / Sentinel / Cluster)
        |- strings / hashes / lists / sets / zsets / streams
        |- TTL + eviction policy
        |- optional AOF/RDB persistence
```

## When to use this skill

- Cache-aside or read-through caching
- Rate limiting and ephemeral locks (with caveats)
- Leaderboards and time-ordered feeds (ZSET)
- Session storage with sliding expiration

## Operational directives

1. Namespace keys: `app:env:entity:id` (example `shop:prod:session:abc`).
2. Set TTL on every cache key; decide eviction policy deliberately (`allkeys-lru`, etc.).
3. Prefer `SCAN` over `KEYS`.
4. Use atomic constructs (`SET NX EX`, Lua, or Redlock carefully) for locks; document failure modes.
5. Do not store the only copy of critical business data solely in Redis unless persistence + backups are confirmed.

## Cache-aside pattern

```bash
# Pseudocode CLI equivalents for illustration
SET shop:prod:item:42 '{"id":42,"price":199}' EX 300
GET shop:prod:item:42
DEL shop:prod:item:42
```

Application flow: read cache -> on miss load DB -> SET with TTL -> return. On write: update DB then DELETE/UPDATE cache key.

## Useful structures

| Structure | Use | Example |
| --- | --- | --- |
| STRING | blobs, counters | `INCR rate:ip:1.2.3.4` + `EXPIRE` |
| HASH | object fields | `HSET user:1 name Ada` |
| ZSET | rankings / schedules | `ZADD lb 100 user:1` |
| LIST | simple queues | `LPUSH` / `BRPOP` |
| STREAM | consumer groups | `XADD` / `XREADGROUP` |

## Rate limit sketch (fixed window)

```bash
INCR ratelimit:user:9:2026-08-26T15:04
EXPIRE ratelimit:user:9:2026-08-26T15:04 60
# reject when count > threshold
```

Prefer token bucket / sliding window libraries in app code for fairness under burst.

## Best practices

- Cap payload sizes; huge values block the single-threaded event loop.
- Monitor `used_memory`, evictions, and hit rate.
- Separate DB indexes logically by purpose when sharing an instance (still prefer separate instances for noisy neighbors).
- In Cluster mode, understand hash tags for multi-key operations.

## Limitations

- Distributed locks are subtle; correctness needs fencing tokens for some workloads.
- Persistence settings trade durability for latency.
- Managed Redis (ElastiCache, Memorystore) changes networking and AUTH setup.

## Related skills

- `@postgresql` - system of record behind the cache
- `@kubernetes` - deploying Redis/Sentinel/Cluster operators
- `@opentelemetry` - tracing cache misses as latency sources
