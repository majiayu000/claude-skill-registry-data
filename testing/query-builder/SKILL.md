---
name: query-builder
description:  QueryBuilder integration canon — PaginateQueryParams, filters/gt/lt/period query string, mapping_filters joins, front filter-utils mirror. Use for INTEG PLAN/IMPLEMENT/QA/BUGFIX, new list endpoints with filters, relation__column joins, filter key matrix, dashboard filter wiring. Replaces external fec-web-acc reference project.
---

# QueryBuilder — INTEG canon ()

Self-contained skill for back↔front list/filter integration. **Do not open `/home/aero/PyProject/fec-web-acc`** — all patterns are here.

## When to use

- INTEG PLAN / IMPLEMENT / QA / BUGFIX for list + filters domains
- New `GET /api/v1/<resource>/list` with QueryBuilder
- Join filters: `relation__column` + `mapping_filters`
- Front: `lib/filters/` → query string mirror
- Dashboard: shared UI filters → N endpoints with different API keys

**Skip when:** portal-scoped CRUD without list filters (e.g. `/provider/slots`) — no QueryBuilder needed.

## Lazy load references

Read **only** shards needed for current subtask:

| Task | Read |
|------|------|
| Plan contract / filter matrix | `FILTER-KEY-MATRIX.md`, `QUERY-PARAMS.md` |
| BACK endpoint + joins | `PIPELINE.md`, `JOINS-AND-MAPPING.md`, `BACK-ENDPOINT.md` |
| FRONT filter-utils | `FRONT-FILTERS.md`, `QUERY-PARAMS.md` |
| Dashboard N API | `DASHBOARD-PATTERN.md`, `FILTER-KEY-MATRIX.md` |
| QA / wire verify | `INTEG-CHECKLIST.md` |
| Debug drift | `ANTI-PATTERNS.md`, `INTEG-CHECKLIST.md` |
| Context / history | `INTEGRATION-TIMELINE.md` |

##  file map

| Layer | Path |
|-------|------|
| Query params validators | `core/base/schema.py` — `PaginateQueryParams` |
| SQL pipeline | `core/base/query_builder.py` — `QueryBuilder.build()` |
| CRUD entry | `core/base/crud.py` — `build_query()` |
| Endpoint | `api/v1/endpoints/<entity>.py` — `mapping_filters` |
| Schemas | `app/<domain>/schema.py` — `IFilter`, `IRead` |
| Front API | `frontend/src/lib/api/<domain>.ts` |
| Front filters | `frontend/src/lib/filters/<domain>-filters.ts` |
| Query keys | `frontend/src/lib/query-keys/<domain>.ts` |
| Contract | `memory-bank/integration/contracts/<domain-slug>.md` |

## Fixed pipeline (never bypass)

```
HTTP query string
  → PaginateQueryParams (core/base/schema.py)
  → rows { model, column, value, path, join_type }
  → QueryContext
  → QueryBuilder.build() (core/base/query_builder.py)
  → crud.get_multi() — NO raw SQL in endpoint
```

## INTEG layer order

```
1. Contract (filter key matrix per endpoint)
2. BACK — mapping_filters + IFilter + pytest
3. FRONT — filter-utils + api types + vitest
4. Wire — §0.11 grep + contract test
```

## Quick param routing

| UI need | Query param | Example |
|---------|-------------|---------|
| enum / multiselect / join | `filters` JSON | `{"city__slug":["sochi"]}` |
| numeric range | `gt` / `lt` / `eq` JSON | `gt={"price__gte":5000}` |
| date range | `period` quoted string | `"2025-01-01:2025-12-31"` |
| text search | `search` | `search=rafting` |
| sort | `ascending` / `descending` | `descending=created_at` |

**Rule:** numbers in `gt`/`lt`, never in `filters`.

## Critical rule: one UI filter → many API keys

Same UI field may map to **different keys per endpoint**. Document in contract **before code**. One `buildXxxApiFilters` per endpoint variant — see `FILTER-KEY-MATRIX.md`.

## Memory-bank redirects

Legacy paths redirect here:
- `memory-bank/integration/reference/query-builder-template.md`
- `memory-bank/integration/reference/patterns-fec-web-acc.md`
- `memory-bank/integration/reference/reference-project-fec-web-acc.md`
