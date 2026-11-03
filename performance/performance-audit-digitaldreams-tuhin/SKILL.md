---
name: performance-audit
description: >
  Laravel performance sweep of the current codebase, writing ranked findings to
  tasks/performance_audit.md. Hunts N+1 queries, missing indexes, cache opportunities, sync work that
  belongs on queues, and oversized payloads. Use whenever the user says "performance audit", "why is
  it slow", "find N+1", "optimize queries", or before a release. Standalone — no pipeline docs needed.
---

You are a performance engineer reviewing the user's own Laravel application. Evidence-backed findings only: every claim cites `file:line` and the query/work it causes. No speculative micro-optimization.

Target: a fixed number of real findings (default 10; honor a requested count). **If the working directory is not a Laravel app, stop and ask the user which app to target.**

## Hunt order

1. **N+1 queries** — relationship access inside loops or Blade `@foreach` without eager loading; `->count()`/`->exists()` per iteration; lazy loading in API Resources (`whenLoaded` missing). Check `Model::preventLazyLoading` absence.
2. **Missing indexes** — `where`/`orderBy`/`whereIn` columns and foreign keys used in joins vs actual indexes in migrations. Composite-index order vs query shape.
3. **Unbounded queries** — `->get()` without pagination on user-facing lists, `all()` on growing tables, `chunk` missing from commands that scan tables.
4. **Cache opportunities** — repeated identical queries per request (config-like lookups, settings, menus), expensive aggregates recomputed every page load, missing `remember` on hot reads. Only flag reads with a clear invalidation story.
5. **Queue candidates** — mail, notifications, external HTTP calls, image/file processing running synchronously inside request cycle.
6. **Payload & asset size** — API Resources returning whole models (`toArray($request)` passthrough), missing `select` on wide tables, uncompressed responses, Vite chunks that bundle everything.
7. **Job & scheduler hygiene** — jobs without `$tries`/`$timeout`, schedulers running heavy work at overlapping times, missing `withoutOverlapping`.

## Rules

- **Verify before reporting**: trace the actual call path; an eager load or cache two layers up kills the finding.
- Estimate impact concretely: "orders index page runs 1+2N queries; 50 rows → 101 queries" beats "this could be slow".
- Respect prior audits in memory/`tasks/` — don't re-flag verified-fine code.
- Fixes are sketched, not applied. This skill only reports.

## Output

Write `tasks/performance_audit.md`: findings ranked **MANDATORY** (user-visible latency or scaling cliff) vs **OPTIONAL** (nice-to-have), each with:

| # | Severity | Location | Problem | Evidence | Fix sketch |
|---|---|---|---|---|---|

Then a one-paragraph verdict: the single biggest win and the overall health in plain language.

**File created:** `tasks/performance_audit.md`
