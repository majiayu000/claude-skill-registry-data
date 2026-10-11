---
name: redis
description: Redis — data structures, keyspace, persistence, clustering, pub/sub.
---

# Redis Reference

## When to Load
Load when the project uses Redis (signal: `redis`, `ioredis`, `redis-py`, `REDIS_URL`, `redis:` in docker-compose, Laravel `CACHE_DRIVER=redis`).

## CLI Connection

```bash
redis-cli -h "${REDIS_HOST:-localhost}" -p "${REDIS_PORT:-6379}" -a "$REDIS_PASSWORD"
# with TLS (Redis 6+):
redis-cli -h "$REDIS_HOST" -p "${REDIS_PORT:-6380}" --tls -a "$REDIS_PASSWORD"
# using URL:
redis-cli -u "$REDIS_URL"
```

Key inspection commands:
```bash
redis-cli INFO server            # version, uptime, mode
redis-cli INFO memory            # used_memory, maxmemory, fragmentation
redis-cli INFO stats             # ops/sec, hits, misses
redis-cli --latency              # rolling latency histogram
redis-cli --bigkeys              # scan for large keys (use on low-traffic periods)
redis-cli MONITOR                # real-time command stream (dev only; high overhead)
```

## Data Structures

| Type | Use when | Key commands |
|------|----------|-------------|
| String | Counters, cached values, sessions, feature flags | `GET`, `SET`, `INCR`, `SETNX`, `GETSET` |
| Hash | Object fields; partial updates without serializing whole object | `HGET`, `HSET`, `HMGET`, `HINCRBY` |
| List | Queues (FIFO/LIFO), activity feeds, message buffers | `LPUSH`, `RPOP`, `BRPOP`, `LRANGE`, `LLEN` |
| Set | Unique membership, tags, social graph intersections | `SADD`, `SMEMBERS`, `SINTER`, `SDIFF` |
| Sorted Set | Leaderboards, rate-limit windows, priority queues | `ZADD`, `ZRANGE`, `ZRANK`, `ZRANGEBYSCORE` |
| Bitmap | Compact boolean arrays (e.g., daily active users by index) | `SETBIT`, `GETBIT`, `BITCOUNT`, `BITOP` |
| HyperLogLog | Cardinality estimation with ~0.81% error, fixed 12 KB | `PFADD`, `PFCOUNT`, `PFMERGE` |
| Stream | Persistent, ordered event log; consumer groups | `XADD`, `XREAD`, `XGROUP CREATE`, `XACK` |

## Keyspace Design

- Always prefix keys with a namespace: `user:{id}:profile`, `session:{token}`, `ratelimit:{ip}:{minute}`
- Use `:` as separator (convention); avoid spaces and special chars
- Set a `TTL` on every cached key — never let cache grow unboundedly
- Avoid very large keys (> 1 MB) or very large values; split or compress
- Key cardinality: `user:*` patterns are fine; avoid `*` scans in production — use `SCAN` with `MATCH` and `COUNT`

## Persistence

| Mode | Guarantees | Use when |
|------|-----------|----------|
| No persistence | None (data lost on restart) | Pure cache, ephemeral queues |
| RDB (snapshot) | Point-in-time snapshot at intervals | Low RPO tolerance; fast restarts |
| AOF (append-only file) | Logs every write; `fsync` policy controls durability | Higher durability; larger disk use |
| RDB + AOF | Best of both | Production with data that must survive restarts |

AOF `fsync` options: `always` (safest, slowest), `everysec` (default, 1 s data loss risk), `no` (OS decides).

## Eviction Policies

Set `maxmemory` and `maxmemory-policy` in `redis.conf` or at runtime:

| Policy | Behaviour |
|--------|-----------|
| `noeviction` | Returns error when memory full (default) |
| `allkeys-lru` | Evict least recently used from all keys |
| `volatile-lru` | Evict LRU from keys with TTL only |
| `allkeys-lfu` | Evict least frequently used (Redis 4+) |
| `volatile-ttl` | Evict key with shortest TTL first |

For a pure cache: use `allkeys-lru` or `allkeys-lfu`.

## Clustering & High Availability

| Mode | Topology | When |
|------|----------|------|
| Standalone | Single node | Dev / low-traffic |
| Sentinel | 1 primary + N replicas + sentinel processes | HA without sharding |
| Cluster | 16384 hash slots across N primaries | Horizontal scale + HA |

- Cluster mode does not support multi-key commands across slots unless keys share a hash tag: `{user:123}:profile` and `{user:123}:sessions` land on the same slot
- Replica lag is async; reads from replicas may be stale — use `WAIT` command for synchronous replication confirmation

## Pub/Sub vs Streams

| Feature | Pub/Sub | Streams |
|---------|---------|---------|
| Message persistence | None (fire-and-forget) | Yes — messages stored in log |
| Consumer groups | No | Yes — each group reads independently |
| At-least-once delivery | No | Yes — `XACK` acknowledgement |
| Backpressure | No | Yes — `MAXLEN` trim |

Use Streams for durable event queues; use Pub/Sub for lightweight real-time notifications only.

## Common Gotchas

| Gotcha | Fix |
|--------|-----|
| `KEYS *` blocks the event loop | Use `SCAN` with `MATCH` and `COUNT 100` |
| Large `HGETALL` on a hash with thousands of fields | Use `HSCAN` or restructure |
| No TTL on session keys → memory leak | Set TTL on every write; use `OBJECT IDLETIME` to audit |
| `SETNX` + `EXPIRE` is not atomic | Use `SET key value NX EX seconds` (single command) |
| Cluster: cross-slot multi-key operations fail | Use hash tags `{...}` to co-locate related keys |
| AOF rewrite pauses | Schedule `BGREWRITEAOF` during low-traffic windows |
