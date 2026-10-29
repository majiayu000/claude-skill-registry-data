---
name: latency-critical-systems
description: "Use when working on latency-sensitive Laravel paths — realtime dashboards, streaming, queues, caches, or execution gateways — where p95 latency and data freshness matter."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/sql/optimalize.md` for every query on the hot path (N+1, eager loading, index usage, batching)
- Apply `@rules/laravel/laravel.md` for framework-level structure and caching choices
- Apply `@rules/laravel/queue-debouncing.md` when smoothing bursty queue work
- Measure, do not guess — every claim about latency must come from a real readback.
- Never trade correctness for speed (see Guardrails).

## Modes

This skill runs in one of two modes, selected by the caller via `MODE` (default `tune`):

- **`tune` (default)** — full latency work: instrument the hot path, rewrite queries and caches, change queue, worker, and broadcast configuration, and read the numbers back from the running system. Every section below behaves as written unless it is explicitly flagged for `MODE=cr`.
- **`cr` (read-only lens — invoked by `@skills/code-review/SKILL.md`, `code-review-github`, `code-review-jira`, and `code-review-bugsnag` when the diff touches a latency-critical surface)** — **never modify project code or configuration, never author a test, never stage / commit / push, never run fixers or checkers, and never chain a follow-up review.** Scope the analysis to the lines added or modified by the PR diff and return the findings as markdown only, carrying the reproducer fields the CR folds into its standard Critical / Moderate buckets.
Every instruction below that would touch a file or a running system — instrument, cache, batch, replicate, split, throttle, stream, or any other such verb — is emitted as a written proposal carrying a concrete snippet, never applied to the project.

> **What this lens owns in a CR:** the latency budget of the changed path and the freshness of the data it serves — whether the path the diff adds or changes carries a stated p50 / p95 / p99 target, whether the hot path is mapped rather than assumed, whether a cached or broadcast read carries a freshness age and a staleness window, whether a fast cache hit is allowed to masquerade as live data, and whether backpressure bounds queue depth instead of letting lag compound.
> It **defers how much a loop holds at once and the per-item work inside it** — unbounded materialisation, offset paging over a set being written, and one HTTP call / notification / job / cache write per element — to the walk *Bulk Data & Batch Processing (issue #223)* (`@rules/code-review/general.md`). It **defers the performance of a query and its plan** — N+1, index usage, rows examined, `EXPLAIN` shape, and the non-regression gate on a rewritten query — to the *N+1 queries* walk of `@rules/code-review/core-analysis.md` and, on MySQL, to the advisory `casey` report (`@skills/mysql-problem-solver/SKILL.md`). It never raises a finding either of those owns.
> Both boundaries divide the *dimensions* of a hot-path change, never its lines: a `foreach` issuing a query per row on a queue path carries the batching finding from the walk and the query-plan finding from that lens, and this lens speaks on the same change only when it also leaves the path with no stated budget or no freshness window — a different defect, never the batching or the query plan restated.
> The lens judges the runtime the project already has. **Never raise a finding whose only fix is to adopt infrastructure the project does not run** — Octane, Horizon, Reverb, a read replica, or a websocket layer: the runtime is a project decision, not a defect on the diff.
> **Nothing runs in `MODE=cr`, so this skill's *Verification — real readbacks* measurements are unavailable.** Judge what the diff and the project state about the budget and the freshness, and raise a **missing** budget, mapping, or readback as the finding — never assert a latency figure this review did not take.

## Scope
Engineering approach for latency-sensitive Laravel paths: realtime dashboards,
streaming, ingest workers, queues, caches, and execution gateways where p95
latency and freshness matter. This skill is engineering-focused; it does not
authorize live trading or financial advice.

## Use when
- A page, API route, broadcast, or dashboard must hit a latency target (p95/p99).
- Queue lag, cache staleness, or freshness age is a visible problem.
- Streaming / websocket freshness or execution-gateway timing is in scope.
- You are deciding where to cache, batch, replicate, or move compute.

## 1. Split the metrics

Do not collapse everything into "fast." Track separately:

- p50, p95, p99 latency (one slow tail dominates user perception);
- throughput (requests/jobs per second);
- freshness age (how old the displayed data is);
- queue depth and queue wait time;
- cache hit rate;
- provider/external API response time;
- browser render time;
- correctness under load;
- failure and retry behavior.

Capture them with real tools: response timing headers, `Horizon` metrics,
`Redis` `INFO`/`MONITOR`, slow-query log, and Laravel Telescope for per-request
timing breakdowns.

## 2. Map the hot path

Write the path from event to visible state, then measure each segment:

```text
source event -> provider API -> ingest job -> queue (Redis/Horizon) -> cache (Redis)
-> Octane worker / route -> broadcast (websocket) -> Livewire/browser render -> user
```

For each segment record where time goes. The bottleneck is usually one segment,
not the whole chain — instrument before optimizing.

## 3. Optimization order

Apply in this order; stop when the target is met.

1. **Remove unnecessary round trips.** Collapse repeated queries; resolve N+1
   with eager loading (`with(...)`, `withCount(...)`) per `@rules/sql/optimalize.md`.
   N+1 on a hot path is the single most common latency killer.
2. **Cache stable reads with freshness metadata.** Use `Cache::remember()` /
   `Cache::flexible()` against Redis for reads that tolerate a known staleness
   window. Store the computed-at timestamp alongside the value.

   ```php
   $stats = Cache::remember('dashboard:stats', 30, fn () => [
       'computed_at' => now(config('app.timezone'))->toIso8601String(),
       ...$this->orderRepository->getCountAndTotal()->toArray(),
   ]);
   ```

3. **Batch small calls and writes.** Combine per-row queries into bulk
   operations (`whereIn`, `upsert`, single keyed read) rather than looping. For
   bursty event streams, debounce/coalesce queued work per
   `@rules/laravel/queue-debouncing.md` so one job processes a window of events.
4. **Move compute closer to the data or user.** Push aggregation into SQL
   (`@rules/sql/optimalize.md`) instead of hydrating models in PHP; serve reads
   from a DB read replica where the connection supports it.
5. **Split hot and cold paths.** Keep the request fast: do the minimum
   synchronously, dispatch the rest to a queue. Run hot routes under **Laravel
   Octane** so the framework stays booted between requests.
6. **Apply backpressure before queues grow unbounded.** Cap concurrency with
   Horizon `maxProcesses` / rate limiting; shed or defer load when queue depth
   crosses a threshold rather than letting lag compound.
7. **Stream only when it improves freshness.** Use broadcasting / websockets
   (Reverb / Echo) to push fresh data instead of client polling — but only where
   freshness genuinely improves the experience.
8. **Add canaries** for stale cache, degraded providers, and growing queue depth.

## 4. Verification — real readbacks

Never claim a latency win from a label; read it back from the running system:

- **HTTP timing & headers** — measure the route; add a `Server-Timing` header or
  read response time from logs / Telescope.
- **Cache state** — confirm hit rate via Redis (`INFO stats`) and verify the
  freshness timestamp stored with cached values.
- **Queue state** — check Horizon for wait time, depth, and failed jobs; confirm
  the hot path is not blocked behind a slow queue.
- **Query plans** — run `EXPLAIN` on the hot query (see `@rules/sql/optimalize.md`)
  to confirm index usage after a rewrite.
- **Freshness** — read the provider/source timestamp and the displayed value;
  confirm the gap is within the agreed staleness window.
- **Browser** — verify actual UI freshness (Livewire poll/broadcast updates), not
  just server numbers.

For execution-adjacent paths, also verify source-data age, provider status, and
kill-switch / degraded-mode behavior before calling the path ready.

## Guardrails

- Do not optimize latency by dropping required validation or authorization.
- Do not hide stale data behind fast cache hits — surface freshness age; never
  let a fast cache hit masquerade as live data.
- Do not claim millisecond behavior from client labels without measurement.
- Do not gate risky changes loosely: execution-impacting, destructive-migration,
  or customer-facing deploys need an explicit approval gate and a rollback path.
- Keep secrets and private payloads out of logs and benchmark artifacts.

## Done when
- Each tracked metric (p50/p95/p99, throughput, freshness, queue depth, cache
  hit rate) has a real, measured value — before and after.
- The hot path is mapped and the actual bottleneck segment is identified.
- Optimizations were applied in order and each win is confirmed by a readback
  (Telescope/Horizon/Redis/EXPLAIN/browser), not assumption.
- Validation, authorization, and freshness honesty are intact; risky deploys are
  gated.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
