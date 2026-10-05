---
name: core/selector-tracing
description: >-
  Use when diagnosing Store selector performance with traceSelectors,
  including cache hits, invalidations, cadence, aggregates, and lifetime
  summaries across Store families.
type: sub-skill
requires:
  - core
triggers:
  - selector tracing
  - selector performance diagnosis
  - selector trace summary
  - selector cache hit
  - selector invalidation
  - selector cadence
---
# Selector tracing — evidence-oriented performance diagnosis

Diagnose recomputation, output-cache reuse, invalidation, scheduling, and duration.
Public reference: `@themislib/themis/docs/SELECTORS.md` → Selector Tracing
Diagnostics. Runtime/types are evidence, not a second public API.

## Scope and safety rules

- Tracing is an opt-in diagnostic and is disabled by default in every build. Enable it only
  for a focused reproduction, then remove it or set it back to `false`.
- Tracing never provides selector argument values, selector result values, or
  Redux state values. Do not ask a user to capture them from logs, infer them
  from path names, or paste them into a report.
- Treat `selectorSource` as callback identity only. It is limited to the first
  five source lines and 500 characters; it is not a state snapshot.
- Trace counts describe the observed Store instance and selector identity. Do
  not compare counts from unrelated runs or Store instances without recording
  that boundary.
- Prefer the smallest event-category set that answers the question. A broad
  `true` preset is useful for a short reproduction, not a permanent setting.

## Configure the Store

Tracing is configured as the third constructor argument of `Store`,
`ReactStore`, or `StreamingStore`; pass `undefined` for middleware when there is
no middleware configuration.

```ts
const store = new Store(reducers, undefined, {
  traceSelectors: {
    traceExecution: true,
    traceInvalidation: true,
    traceResults: true,
    minDurationMs: 2,
    minRecomputationCount: 3,
    summaryEnabled: true,
  },
});
```

Accept only `undefined`, `false`, `true`, or one flat object; nested objects,
arrays, and unknown properties are rejected. The eleven fields are:

- Six independent boolean categories, default `false`: `traceExecution`,
  `traceCache`, `traceInvalidation`, `traceArguments`, `traceResults`, `traceCadence`.
- Inclusive numeric thresholds, default `0`: `minDurationMs`,
  `minRecomputationCount`, `minCacheMissCount`.
- `summaryEnabled` (boolean, default `false`) allocates the collector for period
  aggregates and lifetime snapshots; `summaryIntervalMs` defaults to `1000`.
- All numeric fields must be finite and non-negative.

`true` enables all six categories with zero thresholds, **not** summaries or a
summary timer. `undefined`/`false` disable categories and aggregation. Set
`summaryEnabled: true` explicitly for aggregates; details and cadence can run
without it. Summary-only configuration collects work/cache/reason/outcome data
without enabling detail categories.

## Store-owned logging streams

`traceStreams.selectorDetail` carries configured per-event metadata;
`selectorCadence` carries scheduling events. The default logger renders them
immediately (`[themis] selector trace` and cadence labels below).
`selectorSummary` publishes lifetime snapshots each summary interval, even idle
ones; it is not the console's period-delta payload. All follow selector privacy.
For public stream types and separate `reduxAction` payload safety, follow
[Store-owned logging streams](../redux-action-logging/SKILL.md#store-owned-logging-streams).

For `loggerFactory` subscription cleanup/re-init, follow
[Logger factory lifecycle](../redux-action-logging/SKILL.md#logger-factory-lifecycle).
Period aggregate console output is runtime-owned and still occurs with a custom
factory; its separate interval contract is in [Aggregate summaries](#aggregate-summaries).

The legacy `store.traceSelectors()` compatibility method can activate the same
event preset in any build when construction used omitted or `false` tracing
options. A configured object remains authoritative; do not use the method to
override it.

## Read console aggregates as evidence

With `summaryEnabled: true`, each eligible non-empty period emits one
`console.info('[themis] selectors fired: N, recalculated: M', aggregate)`.
`N`/`M` total emitted rows' execution/recomputation counts. The aggregate is
`{ intervalMs, selectors }`; rows follow `SelectorTracePeriodSummary`:

| Field | Meaning |
| --- | --- |
| `selectorSource` | Safe callback source snippet used as selector identity. |
| `executionCount` | Execution samples collected during this interval. |
| `recomputationCount` | Recomputation count during this interval; an interval delta, not a lifetime total. |
| `invalidationReasons` | Counts for all four invalidation reason labels. |
| `resultOutcomes` | Counts for `initial`, `changed`, and `retained-reference`. |
| `arguments` | `{ count, changedCount }` for argument-related computations. |
| `duration` | `{ count, totalMs, averageMs, maximumMs }` for this interval. |
| `cache` | `{ requestCount, hitCount, missCount, hitRatio }` for this interval; ratio is `null` with no requests. |

Rows need one qualifying category: execution requires duration samples and both
period maximum duration/recomputation thresholds; cache requires requests and
the miss threshold. Comparisons are inclusive. `summaryEnabled` also makes
invalidation/result counts eligible; argument-only eligibility needs
`traceArguments`. Thresholds do not discard collected samples or lifetime data,
and another category can qualify a row. `minDurationMs` separately filters
execution detail events. Period rows omit paths, changed-path metadata, argument
types, output-cache status, and cumulative cache counters.

Use duration and recomputation counts together. A slow callback with few
recomputations suggests expensive selector work; a high period count suggests
an active update path or unstable selector inputs. Cache request, hit, and miss
metrics are interval deltas and describe direct output reuse, not callback
recomputation. The console aggregate has no per-selector labels or bold styling.

### Cadence records

- `SUBSCRIBE SELECTOR CADENCE` reports the current subscriber count.
- `SELECTOR CADENCE TICK` reports the tick timestamp and listener count.

These immediate messages distinguish scheduling pressure from computation, with
no state/selector values. RAF timestamps use normalized wall-clock time.

## Aggregate summaries

`store.getSelectorTraceSummary()` returns a deep-frozen, non-resetting lifetime
snapshot; it is empty when summaries are disabled or no data exists. Entries
contain source identity, work counts, invalidation/results, duration, and cache
metrics as above (no `arguments` group), plus duration `p95Ms`.
Totals/counts/averages/maxima are lifetime metrics; p95 uses only the latest
bounded ring of at most 64 durations, not exact lifetime tail latency.

Only `summaryEnabled: true` allocates the collector and, after `init()`, one
`summaryIntervalMs` timer. Each tick publishes a lifetime stream snapshot and
consumes/resets period deltas; console output is silent when no row qualifies.
Repeated `init()` does not duplicate timers. The initializer disposer or
`store.dispose()` stops the timer and clears pending period data. Re-init may
start a fresh timer; cadence remains immediate and separate.

## Store-family symmetry and lifecycle

All families share tracing options, events, summaries, privacy, and activation:

| Family | Public direct selector output |
| --- | --- |
| `Store` from `@themislib/themis/svelte-store` | Svelte `Readable` |
| `ReactStore` from `@themislib/themis/react-store` | Preact `ReadonlySignal` |
| `StreamingStore` from `@themislib/themis/streaming-store` | Kefir `Observable` |

Do not mix family-specific lifecycle patterns in one app.

Initialize before direct reactive selector calls; retain/call the `store.init()`
disposer when finished. Equivalent `store.dispose()` evicts direct outputs,
stops intervals, disposes cadence, and stops sagas.

## Default-off production behavior and privacy

Production supports explicit categories, legacy activation, and summaries just
like development; omission/`false` remain silent. Keep tracing off in normal
builds and remove temporary configuration afterward. The same
[Scope and safety rules](#scope-and-safety-rules) apply in every build.

## Common mistakes

- Do not expect `true` or category flags alone to collect aggregates or start a
  timer; explicitly set `summaryEnabled: true` and initialize the Store.
- Do not use nested/array options or unknown properties; use the flat
  [configuration](#configure-the-store) with finite, non-negative numeric fields.
- Do not treat row thresholds as global collection filters; another category can
  qualify a period row, and lifetime samples remain collected.
- Do not equate output-cache hits with callback recomputations, period console
  deltas with lifetime stream snapshots, or bounded-window p95 with exact lifetime latency.
- Do not call reactive selectors before init/after disposal or diagnose missing
  records then as tracing failures; use `.select(...)` for explicit state reads
  where the family lifecycle requires it.
- Do not add manual memoization/debounce/throttle layers before diagnosing the
  Store-owned cache and cadence.
- Never enrich traces with argument/result/state values; report only source
  identity, counts, durations, cache metrics, and fixed labels.

## Concise troubleshooting workflow

1. Confirm Store family/instance; configure minimally, initialize, and reproduce
   through the real selector path. Enable summaries for period/lifetime evidence.
2. Filter for `[themis] selectors fired:`; compare duration and recomputations,
   then invalidation, argument, and result counts, never underlying values.
3. Compare cache requests/hits/misses/ratios within the same Store/source boundary;
   new sources or unstable direct-call identity can explain misses.
4. Enable cadence if scheduling is suspected. Compare frozen lifetime snapshots
   before/after a change using bounded p95 appropriately; dispose and disable tracing.

## Evidence-oriented handoff

Report family/instance, options, initialization/disposal, reproduction boundary,
and relevant metadata/counts only, following [Scope and safety rules](#scope-and-safety-rules).
Record `git diff --check` for docs and focused tests/builds for runtime changes.

## See also

- `../debugging/SKILL.md` — Store lifecycle and runtime inspection boundaries.
- `../testing/SKILL.md` — focused selector and Store verification guidance.
- The selected Store-family selector skill — family-specific call modes.