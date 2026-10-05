---
name: distributed-caching-design
description: "The default, because it fails open: when the cache is unavailable, reads still"
---

# Distributed Caching Design (Verbose)

## Core Patterns

### Cache-Aside

The default, because it fails open: when the cache is unavailable, reads still
succeed against the source of truth, just slower.

```python
def get_product(product_id: int) -> dict:
    key = f"product:{product_id}:v4"
    cached = cache.get(key)
    if cached is not None:
        return json.loads(cached)

    row = db.fetch_product(product_id)
    if row is None:
        cache.setex(key, 60, NEGATIVE)       # cache the absence, briefly
        return None

    cache.setex(key, jitter(600), json.dumps(row))
    return row


def update_product(product_id: int, changes: dict) -> None:
    db.update_product(product_id, changes)
    cache.delete(f"product:{product_id}:v4")   # delete, do not update
```

Two details carry most of the weight.

**Delete rather than update on write.** Writing the new value into the cache looks
more efficient and introduces a permanent-staleness race:

```
T0  Writer A: db.update(price=10)
T1  Writer B: db.update(price=20)
T2  Writer B: cache.set(price=20)
T3  Writer A: cache.set(price=10)   ← older value wins, and never expires
```

Deleting removes the entry regardless of ordering; the next read re-derives from
the database. The window shrinks from "until TTL" to "one request."

**Order matters.** Write the database first, then invalidate. Invalidating first
leaves a gap in which a concurrent reader repopulates the cache from the pre-write
state and re-arms the stale entry for a full TTL.

### Write-Through and Write-Behind

| | Cache-aside | Write-through | Write-behind |
|---|---|---|---|
| Cache down → reads | Slow, correct | Slow, correct | Slow, correct |
| Cache down → writes | Unaffected | **Blocked** | **Blocked / lost** |
| Staleness window | Up to one request | None | None |
| Write latency | DB only | DB + cache | Cache only |
| Durability risk | None | None | Unflushed writes lost |
| Cold cache | Miss storm | Miss storm | Miss storm |

Write-through eliminates the staleness window by making the cache part of the
write path — which is exactly its cost. The cache stops being a pure optimization
and becomes a dependency of correctness: a Redis failover now causes write errors,
not just a latency bump. Adopt it when a stale read is genuinely unacceptable and
you are prepared to run the cache at database-grade availability.

Write-behind buys the lowest write latency by acknowledging before durability. Any
buffered-but-unflushed window is data you will lose on an unclean shutdown. It is
correct for view counters and click streams, wrong for anything financial.

### Invalidation: TTL Is Not a Strategy

TTL bounds how long you serve a wrong answer; it does not prevent one. With a
600-second TTL and no explicit invalidation, every reader sees a stale price for up
to ten minutes after a change, and no amount of tuning removes that — shortening the
TTL trades correctness against origin load linearly.

The workable posture is layered:

1. **Explicit invalidation on write** provides correctness.
2. **TTL** is a backstop for the invalidations you missed, plus a memory-bound.
3. **A version segment in the key** handles schema changes wholesale.

```python
PRODUCT_SCHEMA_VERSION = 4          # bump on any serialization change
key = f"product:{product_id}:v{PRODUCT_SCHEMA_VERSION}"
```

Bumping that constant retires the entire old keyspace at deploy time. The
alternative — `SCAN`-and-delete across a live keyspace — is slow, partial, and
tends to run exactly when the system is already under stress.

For derived data with many dependencies, tag-based invalidation beats enumerating
keys. Maintain a generation counter per entity and fold it into the key:

```python
gen = cache.get(f"gen:category:{category_id}") or 0
key = f"listing:{category_id}:page{page}:g{gen}"
# invalidate every page of a category with one INCR
cache.incr(f"gen:category:{category_id}")
```

Old entries become unreachable immediately and age out on their own TTL.

### Cache Stampede

A single popular key expires and every concurrent request for it misses
simultaneously. The origin receives N identical queries where it previously
received zero; if N is large enough the database saturates, latency rises,
in-flight requests pile up, and the system does not recover on its own even after
the value is recomputed. This is the failure that turns a cache from an
optimization into an outage amplifier.

**Single-flight / request coalescing** — exactly one caller recomputes:

```python
def get_with_lock(key, loader, ttl=300):
    v = cache.get(key)
    if v is not None:
        return v

    lock_key = f"lock:{key}"
    token = uuid.uuid4().hex
    if cache.set(lock_key, token, nx=True, ex=10):   # atomic; one winner
        try:
            v = loader()
            cache.setex(key, jitter(ttl), v)
            return v
        finally:
            release_if_owner(lock_key, token)        # compare-and-delete

    for _ in range(20):                              # losers wait for the winner
        time.sleep(0.05)
        v = cache.get(key)
        if v is not None:
            return v
    return loader()                                  # winner died; degrade gracefully
```

The lock must have its own expiry and be released only by its owner, or one crashed
holder blocks the key until the lock TTL elapses.

**Probabilistic early expiry (XFetch)** — spread recomputation over time instead of
serializing on a lock. Each reader independently rolls the dice, with probability
rising as the entry nears expiry:

```python
# delta = observed cost (seconds) of the last recompute; beta ≈ 1.0
if remaining_ttl < delta * beta * -math.log(random.random()):
    refresh_async(key)
return cached_value            # serve the still-valid value immediately
```

Nothing blocks, and the expensive keys — large `delta` — start refreshing earlier,
which is exactly the right bias.

**TTL jitter** is the cheap prerequisite for both. Keys written together with an
identical TTL expire together; `ttl * random.uniform(0.9, 1.1)` decorrelates them.

### Cache Penetration and Negative Caching

Requests for ids that do not exist miss the cache by definition and reach the
database every single time — a trivially cheap way for an attacker (or a buggy
client looping over ids) to bypass the cache entirely.

Cache the absence with a short TTL, and distinguish it from a cache miss in code:

```python
NEGATIVE = "\0none"

cached = cache.get(key)
if cached == NEGATIVE:
    return None                 # known-absent, do not touch the database
if cached is not None:
    return json.loads(cached)
```

Keep negative TTLs short (30–60s) so a newly created entity becomes visible
quickly. For very high-cardinality lookups, a Bloom filter of known-existent ids in
front of the cache answers "definitely absent" without a round trip.

### Multi-Level Caches

An in-process L1 in front of a shared L2 (Redis) removes the network hop for the
hottest keys — sub-microsecond instead of sub-millisecond.

| Level | Latency | Capacity | Coherence |
|---|---|---|---|
| L1 in-process | ~100 ns | MBs, per instance | **Not shared** |
| L2 shared (Redis) | 0.2–1 ms | GBs | Single view |
| Origin (DB) | 1–100 ms | Everything | Truth |

The cost is coherence: invalidating in Redis does nothing to the copy sitting in
each of your forty application processes. Either keep L1 TTLs very short (1–5s, and
accept that bounded staleness deliberately) or publish invalidations on a pub/sub
channel every instance subscribes to. Only put data in L1 whose staleness you have
explicitly reasoned about — feature flags and config, yes; account balances, no.

### Eviction and Sizing

Configure a memory ceiling and an eviction policy explicitly. In Redis,
`maxmemory-policy noeviction` means writes start failing with OOM when the ceiling
is hit — occasionally what you want for a queue, almost never for a cache. Prefer
`allkeys-lru`, or `volatile-lru` when the instance also holds keys that must not be
evicted.

Track evictions as a first-class metric. A rising eviction rate with a falling hit
rate means the working set no longer fits, and no TTL tuning will fix it.

## Common Anti-Patterns

❌ **Updating the cache in place on write.**
Concurrent writers interleave and the older value can win permanently.
✅ Delete the key; let the next read repopulate from the source of truth.

❌ **Invalidating before the database write commits.**
A concurrent reader repopulates from the old state and re-arms staleness for a
full TTL.
✅ Write the database, then invalidate.

❌ **Relying on TTL as the invalidation mechanism.**
Every reader gets a wrong answer for up to one TTL after every change, and the
only knob trades correctness against load.
✅ Explicit invalidation for correctness, TTL as a backstop.

❌ **One TTL constant everywhere, no jitter.**
Keys written together expire together and stampede together.
✅ Jitter every TTL; tier durations by volatility and recompute cost.

❌ **No stampede protection on expensive keys.**
✅ Single-flight locks or probabilistic early expiry on anything costly to build.

❌ **Application logic that assumes a hit.**
`cache.get(...)` returning `None` should never be an error path — a cold or failed
cache must degrade to slow, not to broken.
✅ Every read path works with a permanently empty cache.

❌ **Caching without a schema version in the key.**
A deploy that changes the serialized shape leaves old-format entries that
deserialize into exceptions.
✅ A version segment in the key, bumped with the shape.

❌ **Treating the cache as durable state.**
Session data or write-behind buffers with no backing store vanish on failover.
✅ Cache only what you can rebuild from an authoritative source.

❌ **Unbounded key cardinality.**
Keying on raw query strings or full filter permutations fills memory with entries
read exactly once and drives the hit rate to nothing.
✅ Normalize and hash the inputs; cap the parameter space you cache.

## Caching Design Checklist

- [ ] Write strategy chosen deliberately; failure mode understood and documented
- [ ] Invalidation on write is a delete, issued after the database commit
- [ ] Key format includes entity type, id, and a schema version segment
- [ ] Key cardinality bounded; unbounded inputs normalized or hashed
- [ ] Every TTL jittered; durations tiered by volatility and recompute cost
- [ ] Stampede protection (single-flight or early expiry) on expensive keys
- [ ] Negative results cached with a short TTL, distinguishable from a miss
- [ ] Every read path correct and available with a permanently empty cache
- [ ] Client timeouts on cache calls shorter than the origin call they replace
- [ ] L1 in-process entries limited to data whose staleness is acceptable
- [ ] `maxmemory` and an eviction policy set explicitly, not left at defaults
- [ ] Hit rate, eviction rate, and origin load tracked per key class
- [ ] Cache flush and cold-start behavior load-tested, not assumed
- [ ] Nothing stored in the cache that cannot be rebuilt from the source of truth
