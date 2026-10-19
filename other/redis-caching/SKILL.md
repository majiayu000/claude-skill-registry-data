---
name: redis-caching
description: >
  Design, implement, and optimize high-throughput Redis caching layers and in-memory
  data architectures. Use when selecting data structures (Strings, Hashes, Sets,
  Sorted Sets, Streams, Bitmaps), tuning eviction policies and TTL jitter, implementing
  Cache-Aside, Write-Through, or Write-Behind patterns, preventing cache stampedes
  with singleflight and probabilistic early expiration, executing distributed locks with Redlock,
  or optimizing memory footprint, pipelining, and transactions.
compatibility: >
  Agent Skills-compatible coding agents interfacing with Redis 6+ or Redis 7+ instances and clusters. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "redis, caching, distributed-cache, redlock, memory-optimization, key-value, databases"
  topics: "databases"
---

# Redis Caching & In-Memory Data Store Engineering

Redis is an in-memory key-value data structure store used as a distributed cache, message broker, and fast transient state store. Achieving high throughput and sub-millisecond latencies requires selecting the right data structures, designing robust expiration strategies, eliminating cache stampedes, and ensuring safe concurrency under failover.

## Purpose & Overview

This skill guides the design, operational tuning, and hardening of Redis caching systems. It covers data structure selection (Strings, Hashes, Sets, Sorted Sets, Streams, Bitmaps), eviction algorithms (`allkeys-lru`, `volatile-lru`, `volatile-lfu`), caching paradigms (Cache-Aside, Write-Through, Write-Behind), thundering herd mitigation (probabilistic early expiration / XFetch and singleflight), distributed locking with Redlock, pipelining, transactions, and memory optimization.

---

## Core Principles & Rules

1. **Always add jitter to cache TTLs**: Never set uniform expiration times across bulk keys. Randomize TTLs (e.g. `base_ttl + random_jitter`) to prevent simultaneous cache expirations and database thundering herds.
2. **Never run `KEYS *` or blocking commands in production**: `KEYS` blocks the single-threaded Redis event loop while traversing millions of keys. Always use cursor-based `SCAN`, `SSCAN`, `HSCAN`, or `ZSCAN` with bounded `COUNT`.
3. **Choose Hashes over Strings for objects**: Storing multi-field objects in Redis Hashes (`HSET`) avoids JSON serialization overhead, allows partial field updates (`HINCRBY`), and saves up to 50% RAM via memory-compact `ziplist`/`listpack` representations.
4. **Guard against cache stampedes**: For high-concurrency read-heavy keys, implement singleflight mutex locking or probabilistic early expiration (XFetch algorithm) before the key hard-expires in the primary cache.
5. **Release distributed locks safely via Lua scripts**: Never release a lock with a plain `DEL`. A delayed process may release a lock acquired by a newer process. Always use an atomic Lua script verifying ownership token equality.
6. **Set an explicit `maxmemory` and eviction policy**: Avoid unbounded memory growth that triggers OS OOM kills. Configure `maxmemory` and select `allkeys-lru` for general caching or `volatile-lru`/`volatile-lfu` when mixing volatile cache with persistent data.
7. **Pipeline independent batch operations**: Network roundtrips dominate Redis latency. Group multiple independent reads or writes into a single network packet using `pipeline()` rather than making sequential roundtrips.

---

## Standard Workflows & Procedures

### Workflow 1: Implementing the Cache-Aside Pattern with Jitter

1. Construct a namespaced key (`<namespace>:<entity>:<id>`).
2. Query Redis for the cached payload.
3. If cache hit: deserialize and return the value immediately.
4. If cache miss:
   - Acquire a singleflight group or lock to prevent concurrent redundant DB queries.
   - Fetch the authoritative state from the primary database.
   - Calculate jittered TTL: `ttl = BASE_SECONDS + rand(0, JITTER_SECONDS)`.
   - Store value in Redis using `SET key value EX ttl`.
   - Return fetched value.

### Workflow 2: Distributed Locking with Lease Renewal (Redlock Pattern)

1. Generate a cryptographically random ownership token (`token = uuid4()`).
2. Attempt to acquire the lock: `SET resource_name token NX PX 10000` (10-second TTL).
3. If acquired:
   - Spawn a background heartbeat timer ("watchdog") to periodically extend lease if work exceeds expected duration.
   - Execute critical section.
   - On completion, terminate watchdog and execute atomic release Lua script.
4. If not acquired:
   - Retry with exponential backoff and jitter, or abort if non-blocking.

### Workflow 3: Memory Diagnostic & Optimization

1. Check overall memory stats: `INFO memory`.
2. Inspect individual key memory usage: `MEMORY USAGE <key>`.
3. Audit memory consumption distribution: `redis-cli --bigkeys` and `redis-cli --memkeys`.
4. Ensure small Hashes/Lists/Sets do not exceed configured `*-max-listpack-entries` / `*-max-ziplist-entries` thresholds to preserve compact memory encoding.

---

## Real-World Examples & Patterns

### 1. Cache-Aside with Singleflight & TTL Jitter (Python)

```python
import random
import time
import json
import redis
from typing import Optional, Callable, Any
from threading import Lock

class SingleFlight:
    """Ensures only one in-flight fetch executes per key across concurrent threads."""
    def __init__(self):
        self._locks: dict[str, Lock] = {}
        self._global_lock = Lock()

    def do(self, key: str, fn: Callable[[], Any]) -> Any:
        with self._global_lock:
            if key not in self._locks:
                self._locks[key] = Lock()
            lock = self._locks[key]

        with lock:
            return fn()

class CacheAsideService:
    def __init__(self, r: redis.Redis, base_ttl: int = 3600, jitter: int = 300):
        self.r = r
        self.base_ttl = base_ttl
        self.jitter = jitter
        self.sf = SingleFlight()

    def get_user_profile(self, user_id: str, fetch_from_db: Callable[[str], dict]) -> dict:
        cache_key = f"cache:user:{user_id}"

        # 1. Fast path: check cache
        cached = self.r.get(cache_key)
        if cached:
            return json.loads(cached)

        # 2. Thundering herd protection via singleflight
        def _fetch_and_cache() -> dict:
            # Re-check cache inside lock (double-checked locking)
            val = self.r.get(cache_key)
            if val:
                return json.loads(val)

            # Query database
            data = fetch_from_db(user_id)

            # Calculate jittered expiration (3600s + [0..300s])
            expire_seconds = self.base_ttl + random.randint(0, self.jitter)
            self.r.set(cache_key, json.dumps(data), ex=expire_seconds)
            return data

        return self.sf.do(cache_key, _fetch_and_cache)
```

### 2. Probabilistic Early Expiration (XFetch Algorithm)

Prevent cache stampedes on read-heavy hot keys by refreshing the cache before it expires based on computation delta and beta coefficient:

```python
import math

def should_refresh(ttl_remaining: float, delta_computation_time: float, beta: float = 1.0) -> bool:
    """
    XFetch algorithm:
    Refresh if: -delta * beta * ln(rand()) >= ttl_remaining
    """
    if ttl_remaining <= 0:
        return True
    r = random.random()
    if r == 0:
        return True
    return -(delta_computation_time * beta * math.log(r)) >= ttl_remaining
```

### 3. Distributed Lock Acquisition & Atomic Lua Release

```python
import uuid
import time
import redis

# Atomic release script: only delete if the value matches the caller's unique token
RELEASE_LOCK_LUA = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""

class DistributedLock:
    def __init__(self, r: redis.Redis, name: str, ttl_ms: int = 15000):
        self.r = r
        self.key = f"lock:{name}"
        self.ttl_ms = ttl_ms
        self.token = str(uuid.uuid4())
        self._release_script = self.r.register_script(RELEASE_LOCK_LUA)

    def acquire(self, blocking_timeout_sec: float = 5.0) -> bool:
        deadline = time.time() + blocking_timeout_sec
        while time.time() < deadline:
            # SET resource token NX PX ttl_ms
            if self.r.set(self.key, self.token, nx=True, px=self.ttl_ms):
                return True
            time.sleep(0.05 + random.uniform(0, 0.05)) # Jittered retry
        return False

    def release(self) -> bool:
        # Atomic check-and-delete
        result = self._release_script(keys=[self.key], args=[self.token])
        return result == 1
```

### 4. Pipelining & High-Speed Batch Writes

```python
def batch_update_counters(r: redis.Redis, events: list[tuple[str, int]]):
    """Executes 1000 counter increments in a single network roundtrip."""
    pipe = r.pipeline(transaction=False) # Non-transactional pipeline for max throughput
    for metric_name, increment in events:
        key = f"metrics:{metric_name}"
        pipe.incrby(key, increment)
        pipe.expire(key, 86400) # 24h retention
    
    # Executes all queued commands in one batch
    results = pipe.execute()
    return results
```

### 5. Efficient Eviction & Memory Settings (`redis.conf`)

```text
# Limit max memory usage to 8 Gigabytes
maxmemory 8gb

# Evict least recently used keys among all keys when memory is full
maxmemory-policy allkeys-lru

# Number of sample keys to check for LRU approximation (default 5, 10 is near exact)
maxmemory-samples 10

# Memory optimization for Hashes (use compact listpack/ziplist up to thresholds)
hash-max-listpack-entries 512
hash-max-listpack-value 64
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Why It Fails | Remediated Practice |
|---|---|---|
| **Using `KEYS *` in application code** | Scans the entire keyspace synchronously, blocking all Redis operations and causing cascade timeouts. | Use cursor-based `SCAN` with bounded iterations for maintenance tasks. |
| **Uniform TTLs across cached items** | Keys cached during peak hour expire simultaneously, creating a cache stampede that overwhelms the database. | Add random jitter (+10-20%) to expiration TTLs. |
| **Releasing locks with simple `DEL`** | If a job takes longer than the lock TTL, another worker acquires the lock, and the first worker's `DEL` deletes the second worker's lock. | Always release locks using an atomic Lua script matching token identity. |
| **Default `noeviction` policy on cache instances** | When memory fills, Redis rejects write operations (`OOM command not allowed`) instead of pruning stale entries. | Set `maxmemory-policy allkeys-lru` or `allkeys-lfu` on caching instances. |
| **Large serialized JSON strings in single keys** | Reading or updating a single field requires downloading, parsing, and rewriting entire multi-megabyte payloads. | Use Redis Hashes (`HSET`/`HGET`/`HMGET`) to store granular fields. |
| **Ignoring network roundtrips in loops** | Issuing 500 individual `GET` or `SET` commands sequentially introduces 500 network roundtrips (100ms+ latency). | Batch operations with `MGET`, `MSET`, or Redis Pipelining. |

---

## Verification Checklist

- [ ] All cache keys have explicit TTLs configured with randomized jitter.
- [ ] No `KEYS` or blocking scan commands exist in application code paths.
- [ ] Read-heavy keys use singleflight or probabilistic early expiration to prevent stampedes.
- [ ] Distributed locks use `NX PX` with unique tokens and atomic Lua script releases.
- [ ] `maxmemory` and an appropriate eviction policy (`allkeys-lru` or `volatile-lru`) are set in `redis.conf`.
- [ ] Batch reads and writes use pipelining (`pipeline()`) or multi-key commands (`MGET`/`MSET`).
- [ ] Redis Hashes are preferred over serialized JSON strings for entity representation.
- [ ] Slow logs are enabled and monitored (`slowlog-log-slower-than 10000`).

---

## Tooling & Reference Guides

- **Clients**: `redis-py` (Python), `ioredis` (Node.js/TypeScript), `go-redis` (Go), `Jedis`/`Lettuce` (Java).
- **Diagnostics**: `redis-cli --bigkeys`, `redis-cli --memkeys`, `redis-cli monitor`, `redis-cli slowlog get 20`.
- **Benchmarking**: `redis-benchmark -q -n 100000 -c 50 -P 16`.
- **References**: [Redis Memory Optimization](https://redis.io/docs/management/optimization/memory-optimization/), [Distributed Locks with Redis (Redlock)](https://redis.io/docs/manual/patterns/distributed-locks/), [Redis Command Reference](https://redis.io/commands/).
