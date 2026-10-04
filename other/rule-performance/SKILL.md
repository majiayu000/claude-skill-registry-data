---
name: rule-performance
description: MANDATORY when editing files matching ["api/src/**/*.py", "frontend/src/**/*.{ts,tsx}"]. Performance budgets, query discipline, caching, and rendering strategy
---

# Performance Rules

## Database Queries

ALWAYS specify exact relationships with `selectinload(Model.rel)` — NEVER use `selectinload("*")`. ALWAYS add indexes for columns used in filters, joins, and order-by. ALWAYS paginate list endpoints; NEVER return unbounded result sets. Prefer `.scalar_one_or_none()` over `.first()` for single-row lookups.

Correct:
```python
query = select(Opportunity).options(
    selectinload(Opportunity.current_opportunity_summary),
    selectinload(Opportunity.agency),
).limit(page_size).offset(offset)
```

Incorrect:
```python
# N+1 with wildcard eager load
select(Opportunity).options(selectinload("*"))
```

## N+1 Prevention

ALWAYS batch-fetch related rows in a single query. NEVER iterate a collection and re-query per item. Add a regression test for any endpoint where N+1 was fixed.

## Caching

ALWAYS use Next.js ISR (`export const revalidate = N`) for periodically-refreshed pages. ALWAYS use `force-dynamic` only when the page must be fresh per-request. ALWAYS set appropriate HTTP cache headers on API routes. NEVER cache responses containing PII.

## Frontend Rendering

ALWAYS prefer Server Components for data-fetching layers. ALWAYS split client bundles by route. ALWAYS lazy-load non-critical interactive components with `next/dynamic`. NEVER import heavy libraries (charts, editors, PDF) at the top of a server component.

## Payload Size

ALWAYS return only the fields the client needs. ALWAYS compress large list responses. NEVER embed base64 blobs in JSON responses — use presigned URLs.

## Budgets

Frontend route budgets (guidance): JS ≤ 200KB gzipped per route, LCP ≤ 2.5s on mid-tier mobile, CLS < 0.1. API p95 latency budget for list endpoints ≤ 500ms, detail endpoints ≤ 250ms. ALWAYS justify regressions in PR description.

## Background Work

ALWAYS move long-running or CPU-heavy work to background tasks (see `api-tasks.mdc`). NEVER block a request handler on an operation > ~1s.

---

## Related Rules

- **`api-database.mdc`** — indexes, query patterns, soft delete filters
- **`api-search.mdc`** — OpenSearch query performance
- **`api-tasks.mdc`** — background task offloading
- **`frontend-app-pages.mdc`** — ISR and dynamic classification
- **`frontend-components.mdc`** — server/client boundary
- **`accessibility.mdc`** — CWV alignment with a11y

## Specialist Validation

**Simple (add index, add pagination param):** None.
**Moderate (new list endpoint, new cache policy):** Invoke `performance-oracle` and `codebase-conventions-reviewer`.
**Complex (new caching tier, query refactor across multiple endpoints):** Invoke `performance-oracle`, `architecture-strategist`, and `kieran-python-reviewer` (or `kieran-typescript-reviewer`) in parallel.
