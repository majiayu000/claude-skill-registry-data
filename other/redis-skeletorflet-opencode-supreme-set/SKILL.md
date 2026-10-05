---
name: redis
description: Redis — data structures, caching patterns, pub/sub, Redis Stack, Lua scripting.
---

## redis

### Data Structures
- Strings: `SET key value`, `GET key`, `INCR`, `SETEX` with TTL.
- Lists: `LPUSH`, `RPUSH`, `LPOP`, `LRANGE` for queues.
- Hashes: `HSET`, `HGETALL`, `HINCRBY` for objects.
- Sets: `SADD`, `SMEMBERS`, `SINTER`, `SUNION` for relationships.
- Sorted Sets: `ZADD`, `ZRANGE`, `ZRANK`, `ZREVRANGE` for leaderboards.
- Streams: `XADD`, `XREAD`, `XREADGROUP`, `XACK` for event sourcing.

### Caching Patterns
- Cache-aside: app checks cache first, falls back to DB, writes to cache.
- Write-through: app writes to cache first, cache syncs to DB.
- Write-behind: async batch write to DB for high throughput.
- Use `SET NX` for distributed locks; `EXPIRE`/`TTL` for auto-eviction.
- Eviction policies: LRU, LFU, TTL, random, noeviction.

### Pub/Sub
- `PUBLISH channel message` — fire-and-forget messaging.
- `SUBSCRIBE channel` / `PSUBSCRIBE pattern*` for pattern subscriptions.
- Use Redis Streams instead for persistent message delivery.

### Redis Stack
- `FT.CREATE idx ON hash PREFIX 1 "doc:" SCHEMA title TEXT WEIGHT 5.0` — RediSearch.
- `JSON.SET`, `JSON.GET` — native JSON document store.
- `TS.CREATE`, `TS.ADD` — time-series data with retention policies.
- `GRAPH.QUERY` — property graph queries with Cypher syntax.

### Lua Scripting
- `EVAL "return redis.call('GET', KEYS[1])" 1 key` — atomic server-side scripts.
- `SCRIPT LOAD` + `EVALSHA` for cached script execution.

### RedisInsight
- GUI: key browser, profiler, slow log analyzer, cluster topology.
