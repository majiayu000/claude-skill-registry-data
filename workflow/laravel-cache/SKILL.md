---
name: laravel-cache
description: "Use when writing or reviewing Laravel code that reads, writes, invalidates or locks through the cache: cache-aside reads, falsy values, stale-while-revalidate, atomic writes and locks, tags, flushing, failover. Version-sensitive APIs are marked and re-read against the installed framework."
---

# laravel-cache

Step 6 of the pipeline (`WORKFLOW.md`). The cache decisions that look harmless and fail under load or in
production: a falsy value read as a miss, two requests computing the same expensive value, a tag on a store
that ignores it, a flush that empties someone else's keys. Sits next to `skills/laravel-conventions` §12
(which only picks the store) and §4 (queries).

**Special status.** New block, 🟡: written from the framework's own documentation and the rule files the
Laravel team ships for its tooling, never run on real work in house. A base to confront with the first
real caching change, not settled doctrine. Several APIs here are recent (`flexible`, `memo`, `funnel`,
`failover`): re-read the page of the installed version before relying on one (`skills/source-freshness`).

## When
A `Cache::` call, the `cache()` helper, `once()`, a lock, a tag, a cache-store setting, or a "slow, let's
cache it" change.

## Steps
1. **Read through the store's own primitive, not a hand-written truthiness test.** `Cache::remember($key,
   $ttl, fn () => ...)` is the cache-aside read. The manual `get`, `if (! $value)`, `put` shape treats a
   legitimately cached `0`, `false` or empty array as a miss and recomputes it on every call.
   `rememberForever` is for values with an explicit invalidation path, never a default: without one it is a
   permanent stale answer. The store's read counts only `null` as a miss, so `0`, `false`, `""` and `[]`
   are hits when read through `get`, `has` or `remember`; the opposite trap is that a cached `null` is
   always a miss (step 12).
2. **`remember` does not stop two requests computing the same missing value.** It takes no lock: it reads,
   runs the closure on a miss, and writes, so concurrent callers each run the closure. When duplicate computation
   is expensive or unsafe, wrap the computation in a lock (step 5) or use stale-while-revalidate (step 3).
3. **Stale-while-revalidate is `Cache::flexible($key, [$fresh, $stale], fn () => ...)`.** Fresh window:
   served as is. Stale window: served stale and refreshed after the response by a deferred function that
   lives in the same process, not in a durable job. Past the stale window: recomputed synchronously for
   that caller. The refresh takes a store lock and rechecks the stored creation time before it writes, so
   only one refresh per key lands. Use it for hot keys where a slow recompute hurts; do not use it where serving a stale value
   is wrong (balances, permissions).
4. **Atomic conditional write is `Cache::add`**, which returns whether it wrote. A `has` followed by a `put`
   is a race. Like the other reads, `add` treats a stored `null` as absent.
5. **A lock when ownership matters**: `Cache::lock($name, $seconds)` with `get`, `block($wait)` (throws
   `LockTimeoutException` when it cannot acquire) or the closure forms that release for you. To release in
   another process, pass `$lock->owner()` to it and use `Cache::restoreLock($name, $owner)->release()`;
   `forceRelease()` ignores ownership and is an operator tool, not a code path. Locks need a store that
   supports them and every server must reach the same one. `Cache::funnel` caps concurrency (a limit, a
   release-after safety timeout, a block wait) and needs a lock-capable store: on any other store the call
   throws a bad-method-call exception. Without a failure closure it throws `LimiterTimeoutException` when the
   wait runs out; handle that case.
6. **Repeated reads of one key in a single request or job** go through `Cache::memo()->get(...)`, which holds
   resolved values in memory for that execution and forgets one on any write through it. `once()` memoizes a
   callback in process and never touches a store; use it for repeated computation, `memo()` for repeated reads.
7. **Tags only on a store that supports them.** The manual lists the file, database and DynamoDB drivers as
   unsupported (an extra `storage` driver named in an earlier version of this block is not in that list: 🟡,
   check the installed version). A tagged item is readable only with the same ordered tags it was stored
   with. Flushing several tags removes every item carrying any one of them. Confirm the store before designing invalidation around tags; on a store without tags,
   name the keys and `forget` them.
8. **Never `Cache::flush()` for an application-level reason.** It ignores the configured prefix and empties
   every key in a shared store, other applications' included. Invalidate by key or by tag.
9. **Invalidation is part of the change.** A new cached value names what makes it wrong (which write, which
   event) and where that is cleared. A cache with a TTL and no invalidation path is a stale-data bug with a
   delay. Key names are built in one place from the inputs that change the value, tenant and locale included,
   or two tenants share a key.
10. **Production uses a failover store deliberately.** The `failover` driver tries the next store when an
    operation on the current one throws; it does not consult a later store on an ordinary miss and does not
    replicate data (both negatives confirmed in the failover store's source: a first-store null is returned at once, and a write lands on the first healthy store only; failover is triggered by any thrown error, and the event fires once per newly failing store). It dispatches
    a `CacheFailedOver` event when it fails over: report it.
11. **A cache is not storage.** Anything that must survive eviction, restart or a store swap (a counter that
    bills, a one-time token with legal meaning) lives in the database. Test code uses the array store or a
    fake, never the production store. The array and null drivers exist for tests. The database store's flush deletes every row of the table, whatever the prefix, and its "forever" writes an expiry about ten years out.
12. **Never cache a legitimate `null`.** A closure that returns `null` is recomputed on every call, because
    the store cannot tell the value from an absent key. Cache a wrapper (an array with a found flag) or a
    sentinel for "known empty", then unwrap on read.
13. **Lock waits poll.** `block()` retries about every 250 ms by default and throws when the next attempt would pass the wait; a lock released in the closure forms is freed even when the closure throws. What an expiry of zero seconds means is up to the driver: set an explicit expiry. **Check the table driver has its table.** The database store needs its cache table (default migration or
    the table generator); a missing table fails at the first read, not at boot.

## Output / checkpoint
Every cached read uses a primitive from steps 1 to 6, every tag sits on a store that supports it, every cached
value has a named invalidation, and no code calls `flush()`. Checked at `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Apply to new and changed code only (`skills/code-baseline` §0). Do not add
a cache to fix a slow query before measuring it (`skills/laravel-conventions` §4). A project that already
standardises on one pattern keeps it.

## Origin
Rewritten from the Laravel 13 cache documentation (laravel.com/docs/13.x/cache, MIT-licensed framework docs,
read 2026-10-02: remember, flexible, memo, add, touch, locks and owner tokens, funnel, tags support list,
flush and prefix, failover) and the `caching` rule file of Laravel Boost (`laravel/boost`, MIT, cloned
2026-10-02: falsy values, the lock caveat on `remember`, `once` against `memo`). Mechanisms only, rewritten in
our words. Re-read 2026-10-20 against the 12.x cache page of the documentation repository (MIT, its `license.md`
read) and the cache repository, failover, lock and database-store classes of `laravel/framework` (MIT, LICENSE read): confirmed the null-only miss test,
no lock in `remember`, the lock and deferral inside `flexible`, `add`, locks and owner tokens, `funnel` failures, tag
support list, flush ignoring the prefix, failover event. Still unverified: `once()`, the `storage` driver's tag
support, the two failover negatives, and everything on the 13.x page (the 12.x page was read). Re-read 2026-10-20 against the 12.x cache page of the documentation repository (MIT, its `license.md` read) and the cache repository class of `laravel/framework` (MIT, LICENSE read): confirmed the null-only miss test, no lock in `remember`, the lock and deferral inside `flexible`, `add`, locks and owner tokens, `funnel` failures, the tag support list, flush ignoring the prefix, the failover event. Still unverified: the `storage` driver's tag support, the meaning of a zero-second lock expiry per driver, `once()` across long-running workers (the manual says only that results live for the request, per object instance), and the 13.x page (12.x was read). Version-sensitive: `flexible`, `memo`, `funnel`, `failover` and the `storage` driver depend on the
installed framework version.
