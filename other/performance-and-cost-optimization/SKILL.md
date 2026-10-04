---
name: performance-and-cost-optimization
description: Use when setting latency budgets per request type, when tracking LLM cost per call type, when designing a caching strategy, when reviewing bundle size, when profiling a slow path, or when a service is approaching its latency or cost SLO.
---

# Performance and Cost Optimization

## Overview

Define what "fast enough" and "cheap enough" mean *before* optimizing anything. Output is `.forge/performance-budget.md` — latency budgets per request path, LLM cost budgets per call type, the caching strategy (key schema, TTLs, invalidation), frontend bundle budgets, and the profiling targets. Pairs with `observability` (the dashboards that measure compliance) and `scalability-analysis` (the growth projection that decides when to invest).

## When to Use

- A new service is being designed and there's no latency or cost target
- An LLM-heavy feature is shipping and per-call cost is unbounded
- The frontend bundle is growing organically and ship time is increasing
- A query or endpoint is approaching its SLO and the team is debating where to optimize
- Caching is being added ad-hoc with no key convention or invalidation story

## When NOT to Use

- A one-off script with no user-facing latency
- Pure refactoring or rename work with no perf surface
- "It feels slow" with no measurement — start with `observability` first

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Premature optimization is evil" | Setting budgets isn't optimizing — it's defining done. You can't tell what's premature without a target. |
| "LLM costs are fine for now" | Unbounded token usage scales linearly with users. The first viral spike turns a $50/day bill into a $5000/day bill overnight. |
| "We'll cache later" | Cache invalidation designed after the fact creates stale-data bugs you find in production. Design the invalidation strategy with the cache. |
| "Bundle size doesn't matter, our users have fast internet" | You don't know that. Mobile carriers, hotel wifi, rural backhaul, parking-garage signal — all real. |
| "Profile when it's slow" | "Slow" is a feeling. Without a budget, you'll profile randomly or never. |
| "Auto-scaling fixes performance" | Auto-scaling fixes capacity, not per-request latency. A slow request stays slow under any cluster size. |

## Red Flags

- An endpoint in production with no latency SLO and no dashboard
- An LLM call with no `max_tokens`, no model selection rationale, and no cost tracking
- A cache layer with no documented TTL or invalidation event
- A frontend route loading >500KB of initial JS
- A backend hot path that has never been profiled
- A "background job" that takes >30s with no chunking or progress reporting
- Optimization work happening before measurement
- An LLM prompt that grows unbounded with conversation history

## Core Process

### Step 1: Define latency budgets per request type

In `.forge/performance-budget.md`:

| Path type | p95 budget | p99 budget | Source of truth |
|---|---|---|---|
| Interactive UI action (click → visible response) | 200ms | 500ms | Frontend RUM |
| Public API read | 500ms | 1s | Backend traces |
| Public API write | 800ms | 2s | Backend traces |
| Search / aggregation | 1s | 3s | Backend traces |
| Background job | 30s | 5min | Job runner |
| Email / webhook delivery | 5min | 30min | Queue worker |

Adjust per project, but write the numbers down. Every hot path gets a budget.

### Step 2: Set LLM cost budgets per call type

For every LLM call in the system, document:
- Model selection rationale (why Sonnet vs Haiku vs local)
- Input token cap (truncate or summarize context past N tokens)
- Output token cap (`max_tokens` always set)
- Cost target per call (e.g., "<$0.01 for the autocomplete call, <$0.05 for the summary call")
- Cost-per-user-per-day budget (the rate-limit threshold)
- Caching strategy if the same prompt recurs (prompt cache, response cache, or both)

Append to `.forge/performance-budget.md`.

### Step 3: Design caching strategy

For every cache layer:
- **Key schema** — explicit, deterministic, includes version (`v1:user:{id}:profile`)
- **TTL** — short for frequently-changing data (60s), long for slowly-changing (1h), forever for immutable (with versioned keys)
- **Invalidation events** — which mutations bust which cache keys, documented as a table
- **Negative caching** — cache "not found" for short TTL to absorb thundering-herd lookups
- **Stale-while-revalidate** for read-heavy paths where eventual consistency is acceptable
- **Failure mode** — what happens when the cache is down (fall through to source, or fail closed)

A cache without a documented invalidation event is a stale-data bug waiting to ship.

### Step 4: Set frontend bundle budgets

- Initial JS for any user-facing route: **<200KB gzip**.
- Initial CSS: <50KB.
- LCP-impacting resources (above-the-fold images): preloaded, properly sized.
- Code-split per route. Lazy-load heavy components (charts, editors, maps).
- Bundle analyzer in CI; budget breach blocks the build.

### Step 5: Identify profiling targets

For each service:
- Top 3 endpoints by traffic — profiled with production-shaped data
- Top 3 endpoints by latency — flame graphs captured, reviewed
- Top 3 database queries by cost — `EXPLAIN` plans attached to `.forge/database-design.md`
- Any code path inside a `setInterval`, `setTimeout`, or render loop

Profile *before* optimizing. Optimization without a baseline is decoration.

### Step 6: Define cost-tracking dashboards (cross-ref `observability`)

- Per-endpoint cost per request (compute + DB + cache + LLM + egress)
- Cost-per-active-user per day
- LLM spend per feature per day
- Top 10 most-expensive users per week (for usage-based pricing or abuse detection)

## Verification

- [ ] `.forge/performance-budget.md` written
- [ ] Every hot-path endpoint has a documented p95 and p99 latency budget
- [ ] Every LLM call type has model rationale, `max_tokens`, and cost target
- [ ] Every cache layer has documented key schema, TTL, and invalidation events
- [ ] Frontend bundle is <200KB initial JS per route (CI-enforced)
- [ ] Top traffic and top latency endpoints have been profiled with flame graphs
- [ ] Cost-per-user-per-day dashboard exists and has an alert threshold
- [ ] No LLM prompt grows unbounded with user input or conversation length
