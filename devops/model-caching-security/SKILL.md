---
name: model-caching-security
description: Review KV cache, prompt cache, and semantic cache implementations for cross-request context leakage, cache poisoning, sidecar timing attacks, and tenant isolation failures in shared inference infrastructure.
last_reviewed: 2026-04-30
---

# Model Caching Security

## First Principle

**Caching makes inference cheaper and faster — and turns every cache hit into a potential data channel between tenants.**

LLM inference caches (KV cache, prompt cache, semantic cache) store representations of prior context to accelerate repeated computations. In single-tenant deployments this is safe. In shared infrastructure — multi-tenant APIs, pooled inference workers, or semantic deduplication layers — cached context from one user's request can become observable or influenceable by another user's request. The performance optimization becomes a cross-tenant leakage vector.

## Attack Mental Model

1. **KV cache timing side-channel** — an attacker submits requests with varying prefixes and measures response latency. Cache hits produce faster responses; by probing systematically, an attacker can infer what content other users have recently submitted.
2. **Semantic cache poisoning** — a semantic cache returns the cached response for any query judged semantically similar to a cached query. An attacker crafts a query semantically similar to a sensitive query to receive another user's cached response.
3. **Sidecar cache injection** — an external caching sidecar (Redis, Memcached) that stores prompt-response pairs is insufficiently keyed. A crafted cache key collision routes one user's query to another user's cached response.
4. **Shared prefix pollution** — a long shared system prompt cached at the tenant level is evicted by a high-volume attacker flooding the cache, causing re-computation that reveals cache eviction behavior.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Cache keys include tenant, user, and session identity as mandatory dimensions — not optional metadata. |
| **Scope** | Cached context is never retrievable across tenant boundaries. Cache lookups return a miss — not an error — for cross-tenant key collisions. |
| **Isolate** | KV cache slots are not shared between tenants in shared inference infrastructure. Semantic cache entries are partitioned by tenant ID before similarity search. |
| **Enforce** | Cache timing response data is normalized or jittered to prevent timing side-channel inference. |

## MCS.1 Cache Key Isolation and Tenant Scoping

**The core vulnerability:** Caches keyed on prompt content alone are shared across all users who submit the same prompt. In a multi-tenant system, two users from different tenants with identical prompts collide to the same cache entry — leaking one tenant's response to another.

### Check

- Does every cache key (KV cache prefix hash, semantic cache query, sidecar cache key) include tenant ID as a mandatory non-optional component?
- Is the semantic cache similarity search scoped to the requesting tenant's partition — never querying across tenant boundaries?
- Can a cache eviction in one tenant's namespace be detected by another tenant through timing measurement?

### Action

- **Compose cache keys with mandatory tenant scope:**

```python
import hashlib

def build_cache_key(tenant_id: str, user_id: str, prompt: str, model_id: str) -> str:
    scoped = f"{tenant_id}:{user_id}:{model_id}:{prompt}"
    return hashlib.sha256(scoped.encode()).hexdigest()

# For semantic caches: scope similarity search by tenant partition
def semantic_cache_lookup(tenant_id: str, query_embedding: list[float]) -> str | None:
    # Filter to tenant partition BEFORE similarity search
    results = vector_store.search(
        query_embedding,
        filter={"tenant_id": tenant_id},  # enforced at datastore level
        top_k=1,
        threshold=0.95,
    )
    return results[0].cached_response if results else None
```

- **Partition semantic cache vector stores by tenant.** Do not use a single vector index with a metadata filter as your only isolation mechanism — metadata filters can be bypassed by index-level misconfiguration. Use separate index namespaces per tenant.
- **Enforce cache key namespace separation at the infrastructure level.** Use Redis key prefixes with ACL rules that prevent cross-namespace reads, or use separate cache instances per tenant tier.

### Failure Modes

- A system prompt cache is keyed only on the prompt hash. Two tenants with the same system prompt share a cache entry. Tenant B retrieves Tenant A's response when their system prompts coincidentally match.
- A semantic cache uses a shared vector index with a metadata `tenant_id` filter. A misconfigured query omits the filter; an attacker receives semantically similar responses from other tenants.

## MCS.2 Timing Side-Channel Mitigation

**The core vulnerability:** Cache hits complete faster than cache misses. An attacker who can measure response latency across a range of prompts can infer which prompts are cached — and thus reconstruct what other users have recently submitted.

### Check

- Is response latency normalized or jittered to prevent reliable discrimination between cache hits and cache misses?
- Are cache hit/miss metrics exposed through monitoring systems accessible to tenants (e.g., via public dashboards or response headers)?
- Does the system return `X-Cache: HIT` or similar headers that confirm caching behavior to clients?

### Action

- **Add response latency jitter to mask cache timing:**

```python
import random, asyncio

async def serve_with_jitter(response: str, cache_hit: bool) -> str:
    if cache_hit:
        # Add jitter to cache hit responses to prevent timing discrimination
        await asyncio.sleep(random.uniform(0.05, 0.15))
    return response
```

- **Remove cache status headers from API responses.** Do not send `X-Cache`, `X-Cache-Status`, or similar headers to clients. These confirm cache behavior and enable probe attacks.
- **Rate-limit high-frequency identical-prefix probing.** An account that submits dozens of requests with the same prefix and varying suffixes within a short window is consistent with timing side-channel probing. Flag and throttle.

### Minimum Deliverable Per Review

- [ ] Cache key composition: tenant ID and user ID as mandatory components in all cache key schemes
- [ ] Semantic cache partitioning: per-tenant index namespaces, not shared index with metadata filter
- [ ] Cross-tenant collision test: verify same-prompt requests from two tenants return independent responses
- [ ] Response timing: jitter applied to cache hits; no cache status headers in API responses
- [ ] KV cache slot isolation: tenant isolation enforcement in shared inference worker configuration
- [ ] Monitoring access: cache hit-rate metrics not exposed to tenants

## Quick Win

**Audit your cache key construction today.** Find every place a cache key is built and verify `tenant_id` is a required, non-nullable component. A missing tenant dimension is a cross-tenant leakage waiting to happen.

## References

- Multi-tenant model isolation → [multi-tenant-model-isolation/SKILL.md](../multi-tenant-model-isolation/SKILL.md)
- Model serving security → [model-serving-security/SKILL.md](../model-serving-security/SKILL.md)
- Data leakage prevention → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
