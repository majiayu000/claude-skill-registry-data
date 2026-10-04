---
model_tier: medium
name: performance
description: "Use when optimizing application performance — caching strategies, eager loading, query optimization, Redis patterns, or background job design."
domain: engineering
workspaces:
  - engineering
packs:
  - engineering-base
---

# performance

## When to use

Use when optimizing slow endpoints, designing caching, or improving query performance.

Do NOT use when:
- Database schema design (use `database` skill)
- Queue job creation (use `jobs-events` skill)

## Procedure: Optimize performance

### Step 0: Identify the bottleneck

1. Don't optimize prematurely — measure first.
2. Use `DB::enableQueryLog()` or Telescope to find slow queries.
3. Check for N+1 queries on list endpoints.
4. Search for existing cache services in the project.

**Performance complexity is a claim, and a claim needs evidence.** No cache
layer, no denormalised column, no materialised view, no read replica ships on
"this will be slow" — it ships on a profile, a query log, or a timing that names
the bottleneck. The added complexity is permanent (invalidation bugs, stale
reads, a second source of truth); the speedup is hypothetical until measured.
State the measurement in the change, or do not add the mechanism.

**Carve-out — this does not override the `scale-discipline` floor.** Where that
pack is installed, R-A2 *mandates* an index on every FK and every WHERE / ORDER
BY column, and R-A4 governs duplicated data by waiver. Those are structural
defaults that ship with the query, not optimisations awaiting a profiler; the
evidence gate above applies to *added mechanisms* (caches, denormalisation,
replicas, bespoke indexes beyond parity), never to the floor's baseline.

### Step 1: Apply the right fix

| Bottleneck | Fix |
|---|---|
| N+1 queries | Eager loading with `with()` |
| Slow queries | Add indexes, optimize (see `database` skill) |
| Repeated expensive queries | Cache with TTL |
| Blocking API calls | Queue as background job |
| Large datasets | Paginate, chunk, cursor |
| Missing counts | `withCount()` instead of loading relations |

### Step 2: Verify

Re-measure after fix. Check that cache invalidation works correctly.

## Conventions

→ See guideline `php/performance.md` for caching patterns, Redis, response time targets.

## Output format

1. Optimized code with before/after performance comparison
2. Caching strategy or query optimization applied

## Gotcha

- Cache invalidation bugs are worse than slow queries — don't add caching everywhere.
- Eager loading N+1 is the #1 win — always check list endpoints.
- Don't cache ORM collections/entities with loaded relations (Eloquent, Doctrine, Prisma) — too large.
- Always include tenant ID in cache keys (multi-tenant).

## Do NOT

- Do NOT cache without tenant isolation in multi-tenant contexts.
- Do NOT use `get()` or `all()` on large tables — paginate or chunk.
- Do NOT add indexes blindly — analyze query patterns first.

## Auto-trigger keywords

- performance
- caching
- eager loading
- query optimization
- Redis
