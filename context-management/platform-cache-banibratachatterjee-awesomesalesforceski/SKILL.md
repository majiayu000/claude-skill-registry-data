---
name: platform-cache
description: "Use when designing or reviewing Salesforce Platform Cache usage in Apex, including org cache versus session cache, cache-aside patterns, invalidation, and safe key design. Triggers: 'Platform Cache', 'Cache.Org', 'Cache.Session', 'cache-aside', 'cache invalidation'. NOT for durable configuration storage or for caching user-specific sensitive data."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Scalability
  - Reliability
tags:
  - platform-cache
  - cache-org
  - cache-session
  - cache-aside
  - invalidation
triggers:
  - "when should I use Platform Cache in Apex"
  - "Cache.Org versus Cache.Session decision"
  - "cache invalidation strategy for Salesforce"
  - "cache-aside pattern in Apex"
  - "platform cache for reference data lookups"
inputs:
  - "data being cached and how often it changes"
  - "whether the data is org-wide, session-specific, or transaction-local only"
  - "fallback behavior on cache miss or eviction"
outputs:
  - "Platform Cache design recommendation"
  - "review findings for cache safety, key design, and invalidation gaps"
  - "cache-aside Apex scaffold with invalidation notes"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when query load or repeated reference-data lookup is the real bottleneck and Platform Cache is under consideration. The goal is to choose the right cache scope, treat cache contents as disposable, and design fallback and invalidation behavior so the system remains correct even when the cache is empty or evicted.

## Before Starting

- Is the data org-wide reference data, session-scoped user context, or only transaction-local and better handled in-memory?
- What happens if the cache misses or is evicted early?
- How will cached values be invalidated when source configuration or data changes?

## Core Concepts

### Platform Cache Is For Recomputable Data

Cached values should be safe to lose. Platform Cache improves performance, but it is not durable storage. Design every cache read with a fallback path back to SOQL, metadata, or an external system of record.

### Org Cache And Session Cache Solve Different Problems

Org cache is shared and appropriate for non-sensitive reference data used broadly across users. Session cache is better for per-user, per-session context that is safe to keep transiently. Transaction-local caching is a separate concern and is often just an in-memory Apex pattern rather than Platform Cache at all.

### Cache Keys Need Intentional Namespacing

Without a clear key convention, collisions and accidental overwrite become operational bugs. Keys should encode enough context to distinguish object, use case, locale, or other relevant dimensions.

### Invalidation Is Part Of The Feature

Cache-aside without invalidation becomes stale-data-as-a-service. Invalidation can be explicit on config change, version-key based, or tied to scheduled refresh logic, but it must exist.

## Common Patterns

### Cache-Aside Wrapper

**When to use:** Reference data is expensive to load repeatedly but safe to recompute.

**How it works:** Read from cache first, fall back to source of truth on miss, then repopulate the cache.

**Why not the alternative:** Sprinkling direct cache calls across many services makes invalidation chaotic.

### Org Cache For Shared Reference Data

**When to use:** Many users need the same slow-changing data such as picklist mappings or integration config derivatives.

**How it works:** Use a wrapper around `Cache.Org` with a namespaced key and TTL.

### Session Cache For Non-Sensitive User Context

**When to use:** Session-specific derived data helps reduce repeated work for one user.

**How it works:** Use `Cache.Session` only when session context exists and the data is safe for transient user-level storage.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Shared reference data used by many users | Org cache | Reuse across sessions and users |
| Per-user non-sensitive session context | Session cache | Scoped to the user session |
| Data must survive eviction or act as a source of truth | Do not rely on Platform Cache | Cache is an optimization, not storage |
| Same-object lookups only within one transaction | Transaction-local in-memory caching | Simpler than Platform Cache |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] Cached data is safe to recompute and safe to lose.
- [ ] Org cache is not used for user-specific or sensitive data.
- [ ] Cache keys are namespaced and consistent.
- [ ] Fallback behavior on cache miss is correct and tested.
- [ ] Invalidation or versioning strategy is documented.
- [ ] Cache wrappers centralize access instead of scattering raw cache calls.

## Salesforce-Specific Gotchas

1. **Platform Cache is not durable storage** — every cache read needs a miss path.
2. **Org cache is shared broadly** — do not place user-specific or sensitive data there.
3. **Session cache is not the same thing as async-safe state** — background jobs generally should not depend on session-scoped cache behavior.
4. **A cache hit can hide stale-data bugs** — invalidation strategy matters as much as the cache call itself.

## Output Artifacts

| Artifact | Description |
|---|---|
| Cache design review | Findings on scope choice, key design, eviction safety, and invalidation |
| Cache decision table | Recommendation for org cache, session cache, or no Platform Cache |
| Cache-aside scaffold | Wrapper pattern with key namespacing and fallback behavior |

## Related Skills

- `apex/apex-cpu-and-heap-optimization` — use when the issue is CPU or heap waste inside the transaction, not repeated data access across transactions.
- `apex/governor-limits` — use when the broader problem is query and transaction budgeting.
- `apex/custom-metadata-in-apex` — use when configuration belongs in metadata rather than in a transient cache.
