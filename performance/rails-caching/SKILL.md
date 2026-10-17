---
name: rails-caching
description: "Use when designing, reviewing, debugging, or changing Rails caching across low-level values, fragments, HTTP responses, cache stores, keys, freshness, invalidation, stampede control, warming, capacity, and failure behavior."
license: MIT
---

# Rails Caching Engineering

## Purpose
Treat caching as a correctness and systems-design boundary, not merely a performance switch.

`rails-performance` establishes the measurement and bottleneck discipline. This skill owns the caching contract itself:
- what may be cached;
- who may observe it;
- how stale it may be;
- how it is keyed and versioned;
- how it becomes invalid;
- what happens on miss or store failure;
- how concurrent recomputation is controlled;
- how the store behaves across processes and deployments.

Core flow:
measure cost -> define freshness/correctness -> choose cache layer -> design key/version -> define invalidation -> define miss/failure behavior -> bound stampede/capacity -> test isolation -> observe hit/miss/invalidation -> re-measure

## Activate when
- adding or changing Rails low-level, fragment, view, or HTTP caching;
- changing cache keys, namespaces, versions, or expiration;
- reviewing tenant/user/authorization isolation of cached data;
- investigating stale, incorrect, cross-user, or cross-tenant cached responses;
- reviewing cache invalidation after model/domain changes;
- diagnosing cache stampede, thundering-herd, hot-key, or eviction problems;
- configuring or reviewing Solid Cache;
- introducing cache warming or precomputation;
- changing cache stores, serialization, namespaces, or deployment topology;
- deciding whether a value should be cached at all;
- defining behavior when the cache is unavailable or inconsistent.

Do not activate solely because an endpoint is slow. First use `rails-performance` to establish whether caching is justified and which boundary owns the cost.

## Repository inspection
Inspect:
1. Ruby/Rails/runtime versions and the cache APIs available there;
2. configured cache store(s), namespaces, environment settings, and serializers;
3. existing cache key/version conventions;
4. model/domain ownership and update paths that can invalidate values;
5. authentication, authorization, and tenant boundaries;
6. fragment/response/low-level caching already in use;
7. background jobs or callbacks that perform warming/invalidation;
8. multi-process, multi-host, replica, or region topology;
9. deployment/versioning behavior;
10. metrics/logging for hit rate, miss rate, latency, evictions, errors, and stampede symptoms;
11. tests for cache behavior and isolation;
12. storage capacity, TTL, eviction, and serialization constraints.

Do not invent a new cache store or invalidation subsystem before inspecting the repository's current caching boundary.

## Cache suitability
Cache only when the workload and semantics justify it.

Before caching answer:
- what work is expensive?
- what freshness is acceptable?
- can stale data violate authorization, tenant isolation, financial correctness, or other invariants?
- can the value be reconstructed safely?
- what is the invalidation source of truth?
- what happens when the cache misses?
- what happens when the store is unavailable?
- what is the storage/serialization cost?

Prefer fixing an incorrect query, missing index, excessive object loading, or unnecessary computation before adding a cache when that change removes the underlying waste without stale-state semantics.

## Cache layers
Choose the layer that matches the contract:

- request/HTTP cache: cache the response when the entire representation can be shared safely;
- fragment cache: cache a presentation fragment with explicit dependency/version semantics;
- low-level/application cache: cache a computed or read-oriented value behind an explicit key contract;
- precomputed value: materialize expensive results when recomputation latency or load requires it.

Do not move a value to a broader cache layer merely because it has a higher hit-rate potential. Broader scope increases correctness and invalidation risk.

## Cache key contract
A cache key is part of the data contract.

Include every dimension required to distinguish valid results, such as:
- tenant/account;
- authenticated principal or authorization scope when applicable;
- locale/region;
- resource identity;
- query/filter/version inputs;
- feature/configuration version when output depends on it;
- representation/schema version when serialized shape changes.

Never place raw secrets or unnecessary sensitive values into keys or logs.

Keys should be deterministic, bounded, namespaced, and compatible with repository conventions.

Use the `cache-key-isolation` pattern for explicit identity/isolation review.

## Versioning and deployment
Prefer deterministic versioning over ad-hoc mass deletion where the repository's cache model supports versioned keys.

Consider old/new application overlap:
- old workers may write old values;
- new readers may expect new shape;
- rolling deployment can produce mixed versions;
- serialized cached values may outlive the release that created them.

When representation or calculation semantics change, invalidate or version the affected key space intentionally.

Do not assume a cache flush is an acceptable deploy primitive. It can create a miss storm and erase unrelated warm state.

## Freshness and invalidation
Every non-trivial cache needs an explicit freshness contract.

Distinguish:
- expiration: value becomes invalid after time;
- event-driven invalidation: value becomes invalid after a domain change;
- versioned invalidation: changed inputs produce a new key/version;
- manual purge: operator-controlled removal with an explicit reason.

Prefer invalidation tied to the authoritative state transition rather than scattered controller callbacks.

Use the `cache-invalidation-contract` pattern for non-trivial dependencies.

A short TTL is not a substitute for correct invalidation when stale data is unsafe.

## Miss behavior
Define what happens on a cache miss.

Normal miss:
read source -> compute/materialize -> store -> return

For expensive values also define:
- whether concurrent misses may recompute;
- whether stale data may be served;
- maximum wait/recompute budget;
- behavior when the source or cache store fails.

A cache miss must preserve the underlying data contract. Do not return an invalid success result merely because the cache is empty.

## Stampede and hot keys
Cache stampede is a concurrency/capacity problem.

Use the `cache-stampede-control` pattern when concurrent recomputation is measured or the contract requires bounded recomputation.

Candidate controls include:
- stale-while-revalidate;
- bounded recomputation;
- request coalescing;
- prewarming;
- bounded locking;
- expiration jitter.

Choose the simplest mechanism that satisfies freshness and load requirements.

Do not add distributed locks because stampede is theoretically possible. Measure contention and cost first.

## Cache warming
Prewarming can trade deployment/load latency for background work.

Before warming define:
- which keys matter;
- expected hit-rate benefit;
- source-of-truth cost;
- concurrency/batch limit;
- failure/retry behavior;
- expiration timing;
- whether warming can overload the source database/API.

Warm only high-value keys backed by evidence. Avoid eager warming of unbounded key spaces.

## Failure behavior
A cache is normally an optimization boundary, so distinguish cache failure from source-of-truth failure.

Where correctness permits, cache-store failure should degrade to the underlying source with bounded extra load.

Where the cache is part of a required correctness or session contract, the failure semantics must be explicit instead of silently bypassing the boundary.

Never cache exceptions or authorization failures as successful values.

Use the `cache-failure-boundary` pattern when the store failure mode affects user-visible behavior.

## Capacity and eviction
Treat cache storage as finite capacity.

Inspect:
- item size and serialization cost;
- TTL distribution;
- eviction policy;
- hot keys;
- namespace growth;
- value cardinality;
- network round trips;
- memory/CPU cost;
- cross-tenant key distribution.

A high hit rate can still be unhealthy if a small hot-key set creates contention or value size overwhelms the store.

Do not blindly increase TTL to improve hit rate; freshness and capacity may worsen.

## Security and isolation
Cached data can outlive the request that created it.

Verify:
- authorization-sensitive values are isolated;
- tenant/user dimensions are encoded when required;
- private responses are not exposed through shared caching;
- secrets/tokens are never cached unnecessarily;
- invalidation occurs when access rights change;
- cache logs and diagnostics do not expose payloads.

Coordinate with `rails-security` and `rails-security-engineering` for trust/tenant boundaries.

## Observability
At minimum, make the cache diagnosable without logging sensitive payloads.

Useful signals:
- hit/miss rate;
- get/set latency;
- store errors;
- evictions;
- entry size where measurable;
- hot-key concentration;
- stampede/recompute count;
- invalidation count/lag;
- source fallback rate.

Keep metric dimensions bounded. Do not use raw cache keys or user-generated identifiers as unbounded labels.

Coordinate with `rails-observability` for instrumentation and `rails-incident-engineering` for operational diagnosis.

## Testing
Cache tests should prove semantics, not implementation details.

Cover the applicable contract:
- hit and miss;
- key isolation;
- freshness/expiration;
- invalidation;
- version changes;
- authorization/tenant boundaries;
- concurrent miss behavior;
- store failure/fallback;
- serialization/deserialization;
- deployment compatibility where old/new processes overlap.

Prefer deterministic tests and repository-provided cache helpers.

## Reference example

A read-through cache entry with an explicit TTL and race-condition protection, keyed by the versioned record cache key.

```ruby
class InvoiceStats
  def self.for(account)
    Rails.cache.fetch(["invoice-stats/v2", account, account.invoices.maximum(:updated_at)],
                      expires_in: 15.minutes,
                      race_condition_ttl: 10.seconds) do
      {
        open_count: account.invoices.unpaid.count,
        overdue_cents: account.invoices.overdue.sum(:total_cents)
      }
    end
  end
end

# Key discipline:
#   - version the key namespace ("v2") so format changes cannot serve stale shapes
#   - embed the max(updated_at) so the entry self-invalidates on writes
#   - never cache a value whose authorization depends on the current viewer
```

## Agent review checklist
- [ ] workload and bottleneck evidence exists
- [ ] cache layer matches the sharing/freshness contract
- [ ] key contains required identity/version dimensions
- [ ] tenant/authorization isolation is explicit
- [ ] freshness semantics are documented
- [ ] invalidation owner is explicit
- [ ] miss behavior is correct
- [ ] stampede control is justified by evidence
- [ ] warming is bounded
- [ ] store failure semantics are explicit
- [ ] capacity/eviction effects are understood
- [ ] deployment overlap is safe
- [ ] observability avoids sensitive payloads
- [ ] deterministic tests cover the cache contract

## Anti-patterns
- caching before measuring the underlying cost;
- keys that omit tenant/user/authorization identity;
- TTL used as the only correctness mechanism for sensitive data;
- controller-by-controller invalidation for a domain-owned value;
- global cache flush on every deploy;
- unbounded cache warming;
- distributed locks for unmeasured stampede risk;
- caching exceptions or authorization failures as successful data;
- treating cache-store outages as indistinguishable from source-of-truth outages;
- unbounded cache metrics labels;
- declaring a cache correct from hit-rate alone.

## Verification
Verify both functional correctness and cache behavior.

Use this evidence format where relevant:
workload: ...
baseline: ...
cache_layer: ...
key_contract: ...
freshness: ...
invalidation: ...
hit/miss: ...
failure_behavior: ...
after: ...

Never claim that caching improved production performance without measurement or a structurally demonstrated reduction in repeated work.

## Rails 8 current framework considerations

- Solid Cache is the default cache store for new Rails 8 applications and uses database-backed storage. Inspect cache database ownership, capacity, isolation, and migration conventions before relying on it.
- Do not equate database-backed cache storage with authoritative application data; cache invalidation and failure semantics remain separate concerns.

## Source foundation
Primary Rails guidance:
- https://guides.rubyonrails.org/caching_with_rails.html

Repository composition:
- `rails-performance` skill
- `ruby-performance` skill
- `rails-observability` skill
- `rails-security` skill
- `rails-security-engineering` skill
- `rails-active-job` skill
- `cache-boundary` pattern
- `cache-stampede-control` pattern

## Rails caching changes

For caching changes:
- establish the workload and bottleneck before introducing a cache;
- inspect the existing cache store, key/version conventions, invalidation mechanisms, authorization/tenant boundaries, deployment topology, and cache tests;
- define the cache layer and sharing scope explicitly;
- treat the key as a correctness/security contract and include every required identity/version dimension;
- define freshness and invalidation from the authoritative state transition instead of relying on scattered callers;
- reason about old/new application overlap and cached serialization across deployments;
- bound stampede, warming, eviction, and source fallback behavior;
- classify cache-store failure separately from source-of-truth failure;
- never cache secrets, authorization failures, or exceptions as successful values;
- keep cache metrics low-cardinality and payload-free;
- test hit/miss, isolation, invalidation, versioning, concurrency, failure, and deployment compatibility as applicable;
- require measured or structurally demonstrated evidence before claiming caching improved performance.
