---
name: laravel-telescope
description: "Use when analyzing Laravel Telescope requests from URL and DB. Loads Telescope entries, matches the same request in database tables, and proposes practical optimizations."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- If the current project uses Laravel, also apply `@rules/laravel/laravel.md`, `@rules/laravel/architecture.md`, `@rules/laravel/filament.md`, and `@rules/laravel/livewire.md`

---

## Purpose

Use this skill when you need to investigate a specific Laravel Telescope request, read its runtime data, find the same request directly in the Telescope database tables, and propose actionable optimizations.

The goal is practical diagnosis from real telemetry, not generic performance advice.

---

## When to use

Use this skill when the task asks for any of the following:

- analyze output from a Telescope URL
- inspect one concrete Telescope request in detail
- map a Telescope UI request to DB records
- verify request behavior from `telescope_entries` and related tables
- propose optimization opportunities based on observed request/query/job/cache/log data

---

## When not to use

Do not use this skill when:

- the project does not use Laravel Telescope
- no Telescope URL, request id, or filter context is available
- the user only wants generic Laravel performance tips without Telescope evidence

If Telescope UI or DB access is missing, continue with static analysis and clearly state limitations.

---

## Expected inputs

The skill can work with:

- Telescope URL (preferred)
- request UUID / entry UUID
- environment access (local, staging, production read-only)
- DB credentials for Telescope storage
- logs or screenshots exported from Telescope

The skill should proceed with whatever is available and not block on perfect input.

---

## Required workflow

Follow these steps in order.

### 1. Parse the Telescope target from URL

- Extract environment, host, path, query params, and request identifier from the provided URL.
- Identify whether the URL points to requests, exceptions, queries, jobs, cache, dumps, or logs.
- Capture all filters (time window, status code, tag, batch, family hash, etc.) because they affect record matching.

### 2. Read the same request in Telescope UI data

- Inspect request metadata: method, URI, controller/action, authenticated user, response status, duration, memory, and timestamp.
- Collect related tabs when available: queries, jobs, cache operations, events, dumps, logs, exceptions.
- Build a short "request profile" before proposing any fix.

### 3. Fetch the same request directly from DB

Prefer DB-backed verification over UI-only conclusions.

Use Telescope tables and relationships, typically:

- `telescope_entries`
- `telescope_entries_tags`
- `telescope_monitoring` (if used)

For suggested SQL patterns, see `references/sql-patterns.md`.

### 4. Correlate UI and DB records

Confirm that the DB row is the same request shown in UI by matching:

- `uuid`
- timestamp proximity
- method + URI
- status code
- tags / family hash
- related child entries (query, cache, job, exception)

If correlation is ambiguous, explicitly state what is missing.

### 5. Analyze bottlenecks from evidence

Evaluate observed data and highlight concrete problems, for example:

- N+1 query behavior
- slow SQL with missing or poor index usage
- repeated cache misses / no cache strategy
- excessive synchronous work in request cycle
- heavy serialization or payload size issues
- noisy logging causing overhead
- repeated failing jobs/events chained to the same request

### 6. Propose optimizations with impact and risk

For every recommendation include:

- what to change
- why it helps
- expected impact (latency, DB load, memory, throughput)
- implementation risk or side effects
- verification plan (how to measure after change)

When a recommendation **changes or refactors a query**, apply `@rules/sql/optimalize.md` "Performance Non-Regression on Query Changes": capture the query's current cost from the Telescope evidence (duration, rows, repeated executions) as the baseline, and require the changed query to be equal or faster. If the proposed change would be slower than the observed original, do not present it as an improvement — state why it is slower, list the remaining optimization options (or that none exist and why), and the trade-off that justifies it.

Keep suggestions scoped to observed telemetry, not hypothetical architecture rewrites.

---

## Output format

Use the template defined in `templates/analysis-report.md`.

---

## Behavior rules

The skill must:

- prefer evidence from Telescope data over assumptions
- match UI request with DB request whenever possible
- clearly separate confirmed findings from hypotheses
- avoid recommending changes without measurable validation
- keep output concise and implementation-oriented

The skill must not:

- invent UUIDs, timings, or DB rows
- claim DB correlation without explicit match criteria
- suggest destructive DB operations without justification

---

## References

- references/sql-patterns.md
- references/example-prompts.md

---

## Success criteria

A good result from this skill should:

- correctly identify the target Telescope request
- correlate UI and DB records with explicit evidence
- detect meaningful performance or reliability issues
- provide prioritized, testable optimization actions
- document limitations when runtime access is incomplete

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
