---
name: caching-strategies
description: Deep reference for caching — what to cache, cache-aside vs read/write-through/write-behind, TTLs with jitter, eviction (LRU/LFU/FIFO), invalidation, and surviving stampedes (thundering herd / dogpile). Worked examples and a runnable jitter check.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# Caching Strategies

Caching is the cheapest order-of-magnitude performance win available, and the fastest way to serve
*confidently wrong* data. The hard part was never reading from a cache — it's **invalidation**,
**consistency under concurrency**, and **what happens the moment the cache is cold or wrong**. This
skill is the deep reference: the patterns, the decisions, the trade-offs, and the failure modes that
page you at 3am. Heavy detail lives in `references/`; copy-paste material in `examples/`; a runnable
check in `scripts/`.

## Mental model

A cache is a **bet**: you trade memory and a correctness risk for latency and load reduction. Every
caching decision is answering four questions, in order:

| Question | What it decides |
|---|---|
| What is hot and tolerant of staleness? | *whether* to cache at all |
| How does data get *into* the cache? | the **read/write pattern** (cache-aside, write-through…) |
| How does stale data get *out*? | **TTL + invalidation** |
| What happens on a miss storm or a dead cache? | **stampede control + fallback** |

If you can't answer the third and fourth questions before you ship, you don't have a caching
strategy — you have a future incident. Decide the invalidation plan *first*.

## 1. What to cache

Cache data that is **read-often, expensive to produce, and tolerant of some staleness**. Good
candidates: rendered product pages, the result of an expensive aggregation, a third-party API
response, a permission lookup hit on every request. Bad candidates: a user's current account balance,
a one-time-read report, anything where serving a 30-second-old value is a correctness or compliance
bug.

Quantify it before caching. The benefit is roughly `hitRate × costPerMiss`. A 50% hit rate on a 200ms
query is enormous; a 50% hit rate on a 2ms query is noise that you've paid for with a consistency
risk. Measure hit rate in production — a cache below ~80% hit rate for point lookups usually means the
key space is too sparse or the TTL is too short.

## 2. Read & write patterns

The pattern is *how data flows between your app, the cache, and the source of truth*. Pick one
deliberately per dataset.

- **Cache-aside (lazy loading)** — the default. App checks cache; on miss, loads from the source and
  populates the cache. Simple, resilient (a dead cache just means slow, not broken), but the first
  read of every key is a miss.
- **Read-through** — the cache library itself loads from the source on a miss. Same shape as
  cache-aside but the loading logic lives behind the cache abstraction.
- **Write-through** — writes go to cache *and* source synchronously. Cache is always fresh; writes
  are slower.
- **Write-behind (write-back)** — writes hit the cache and are flushed to the source asynchronously.
  Fast writes, but you risk data loss on a crash before flush.

Full comparison with sequence diagrams and when each one bites:
[references/cache-patterns.md](references/cache-patterns.md).

```js
// Cache-aside — the 90% pattern. Note the explicit TTL and miss-population.
async function getProduct(id, { cache, db, ttl = 300 }) {
  const key = `product:${id}`;
  const hit = await cache.get(key);
  if (hit !== null && hit !== undefined) return JSON.parse(hit);   // cache hit

  const product = await db.getProduct(id);                          // miss -> source of truth
  if (product) await cache.set(key, JSON.stringify(product), { ex: ttl });
  return product;
}
```

## 3. TTL, eviction & jitter

A cache is finite, so entries leave in two ways: **TTL expiry** (time-based) and **eviction** (space
pressure). Tune both.

- **TTL** bounds staleness. Short TTL = fresher + more misses; long TTL = fewer misses + staler data.
- **Eviction policy** decides who gets dropped when memory is full: **LRU** (evict least recently
  used — the sane default), **LFU** (least frequently used — better for skewed popularity), **FIFO**
  (rarely what you want). See `references/eviction-and-ttl.md`.
- **TTL jitter is mandatory at scale.** If you populate 10,000 keys in a batch with a fixed 300s TTL,
  they all expire in the same second and stampede the database together. Add randomness so expiries
  spread out.

```js
// Add ±10% jitter so a batch of keys never expires in lockstep.
function jitteredTtl(baseSeconds, jitterRatio = 0.1) {
  const delta = baseSeconds * jitterRatio;
  const offset = (Math.random() * 2 - 1) * delta;          // uniform in [-delta, +delta]
  return Math.max(1, Math.round(baseSeconds + offset));
}
// jitteredTtl(300) -> ~270..330, never the same instant across a batch
```

`scripts/ttl-jitter.mjs` is a runnable, self-testing version of this function.

## 4. Invalidation

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

TTL alone is *eventual* freshness. When correctness matters, invalidate **on write**:

- **Explicit bust** — on update, delete the key (`cache.del(key)`) so the next read repopulates. With
  cache-aside this is the standard move. Beware the race: delete *after* the DB commits, not before.
- **Write-through** — keep the cache correct on the write path so there's nothing to bust.
- **Versioned keys** — embed a version/etag in the key (`product:42:v7`); bumping the version
  instantly orphans all old entries without a scan.

The subtle bugs (delete-before-commit races, distributed invalidation lag, cache-vs-DB ordering) are
covered in `references/invalidation-and-stampede.md`.

## 5. Stampede control (thundering herd / dogpile)

When a hot key expires, every concurrent request misses at once and they *all* hit the source —
the **thundering herd**. A single popular key can take down a database this way. Mitigations:

- **Per-key locking (single-flight):** the first miss acquires a lock and recomputes; everyone else
  waits for the result instead of also recomputing.
- **Stale-while-revalidate:** serve the slightly-stale value while one background task refreshes it.
- **Early/probabilistic recomputation:** refresh a key *before* it expires, with probability rising
  as expiry approaches, so the herd never forms.
- **TTL jitter:** prevents *synchronized* expiry in the first place (see §3).

Detailed algorithms and pseudocode: `references/invalidation-and-stampede.md`.

## 6. HTTP caching

Not all caching is a key-value store. The HTTP layer gives you free caching via `Cache-Control`,
`ETag`, and `Last-Modified` — push work to the browser and CDN before it ever reaches your app. See
`examples/http-cache-headers.md` for a `Cache-Control` / `ETag` / `304 Not Modified` walkthrough.

## Common pitfalls (failure modes & edge cases)

- **No invalidation plan** — TTL-only freshness shipped where correctness was required. The classic
  "I updated it but it's still showing the old price for 5 minutes" bug.
- **Synchronized expiry** — fixed TTL on a batch of keys → herd at expiry. Always jitter.
- **Caching nulls badly** — either you don't cache "not found" (so every miss re-queries a row that
  doesn't exist — **cache penetration**) or you cache it forever (so a later insert is invisible).
  Cache negatives with a *short* TTL.
- **Unbounded cache / no eviction** — an in-process map with no size cap is a memory leak that ends in
  an OOM. Always bound size and set an eviction policy.
- **Delete-before-commit race** — busting the key before the DB transaction commits lets a concurrent
  read repopulate the cache with the *old* value. Bust after commit.
- **Stale-on-error** — refresh logic that overwrites a good cached value with an error/empty result.
  On a source failure, keep serving stale rather than caching the failure.
- **Cache key collisions** — forgetting a discriminator (locale, tenant, auth scope) in the key, so
  user A sees user B's cached personalized data. A security bug, not just a correctness one.
- **Thundering herd ignored** — works fine until the one hot key expires under load.

## When NOT to cache / trade-offs

Caching is not free — it adds a consistency risk, operational surface, and a second source of truth
to reason about. Skip or reconsider it when:

- **Strong consistency is required** (balances, inventory counts, anything legally/financially
  binding) — a stale read is a bug, not a latency win.
- **Low read-to-write ratio** — if data changes nearly as often as it's read, you'll spend more effort
  invalidating than you save on reads.
- **The source is already fast** — caching a 1ms lookup buys nothing and adds a failure mode.
- **Per-user, read-once data** — the entry is evicted before it's ever reused.

When you *do* cache, name the trade-off explicitly: you are choosing **availability and latency over
strict consistency** (an AP-leaning choice). Make the maximum staleness window a documented number,
not an accident of the TTL you happened to pick.

## Files in this package

- `references/cache-patterns.md` — cache-aside / read-through / write-through / write-behind, with flows
- `references/eviction-and-ttl.md` — LRU / LFU / FIFO, TTL tuning, jitter, negative caching
- `references/invalidation-and-stampede.md` — invalidation strategies, thundering herd, dogpile locks
- `examples/redis-cache-aside.js` — runnable cache-aside + single-flight against an in-memory fake
- `examples/http-cache-headers.md` — `Cache-Control`, `ETag`, and `304` revalidation
- `scripts/ttl-jitter.mjs` — runnable jittered-TTL helper with `--selftest`

Pairs with the `rest-api-design` skill (HTTP cache headers), the `database-scaling` skill (caching as a
read-load shield), and the `performance-engineer` agent.
