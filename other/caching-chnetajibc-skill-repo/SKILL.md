---
name: caching
description: "Caching: ETags, cache headers, revalidation, invalidation, bounded keys. Measure hit rates; avoid stale authz data."
---

# caching

Cache deliberately: what, where, for how long, and exactly how it invalidates.

## Activate when

- Adding caches (HTTP, CDN, application, query) or debugging staleness.

## Do NOT activate for

- Database tuning itself (see databases/*).

## Inspection

Find the read/write ratio, staleness tolerance per datum, and current invalidation paths (or their absence).

## Decision rules

- HTTP: ETags + conditional requests for versioned resources; `Cache-Control` explicit (never rely on defaults); revalidation for mutable, immutable+hashed for static.
- Application: cache computed results with TTLs tied to change frequency; keys bounded and namespaced; stampede protection (singleflight/locks) on hot misses.
- Never cache authorization decisions beyond their trust window; never cache per-user data under shared keys.
- Invalidation: write-through/write-behind/event-driven — chosen and documented, not hoped for. No cache without a named invalidation story.

## Procedure

1. Measure baseline latency + hit rate; set a target.
2. Implement cache + invalidation together (a cache PR without invalidation is incomplete).
3. Load-test hot paths including cold-start and thundering-herd cases.
4. Verify: hit rate improved, staleness bounded and tested (stale-authz test fails closed), invalidation demonstrated end to end.

## Failure modes

- Stale permissions/prices served; unbounded key growth; cache stampedes on expiry; private data in shared caches; TTLs nobody can explain.

## Escalation

Distributed invalidation → distributed/systems; CDN specifics via registry + documentation-search.

## References

- Related: `../rate-limiting/`, `../../databases/redis/`, `../../frontend/performance/`.
