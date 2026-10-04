---
name: perf-audit
description: End-to-end performance audit composite — baseline the slow metric, profile to find the real hotspot, implement the smallest targeted fix, re-benchmark to confirm improvement, capture in ADR. Use when users report slowness, CI shows runtime regression, or before a release. Never optimize without profiling first.
triggers:
  - perf audit
  - performance audit
  - slow build
  - slow tests
  - performance regression
  - optimize performance
  - profile this
---

# perf-audit

Profile before you optimize. Never guess hotspots.

## Phases

### Phase 1 — Baseline
Measure current performance and record the numbers (test suite runtime, build time, bundle size, API latency, DB query time). These go into the reconciliation block as before-state.

### Phase 2 — Profile (mandatory before fixing)
Locate the top 1-3 hotspots using the appropriate tool for the stack (flame graph, bundle analyzer, `EXPLAIN ANALYZE`, verbose test reporter). Do NOT skip this phase and jump to a fix based on intuition.

### Phase 3 — Fix (smallest change, biggest hotspot)
Apply one fix per PR. If the fix would touch >5 files or >150 LOC → stop and escalate to `/research-and-decide`.

Common patterns: memoize pure functions in hot loops, lazy-load eager imports, add DB indexes, replace sync I/O with async, deduplicate test setup.

### Phase 4 — Validate
Re-run the same benchmarks from Phase 1 under the same conditions. Confirm improvement is >5% (above the noise floor). If <5% → the fix may not be worth the change risk; revert and document.

### Phase 5 — Capture
Write an ADR with context (which metric, by how much), decision, before/after numbers, and revisit trigger.

## Reconciliation

```
PERF AUDIT — <scope>

Phase 1 Baseline:  <metric>: <before value> ✅
Phase 2 Profile:   Hotspot: <file/function/query> ✅
Phase 3 Fix:       <change applied> | (escalated to /research-and-decide) ✅
Phase 4 Validate:  <metric>: <before> → <after> (<delta>%) ✅
Phase 5 Capture:   ADR <path> ✅ | (skipped: below noise floor)
```

## Failure / Stop Conditions

- Phase 2: profiling tools unavailable → baseline with available metrics, note gap in ADR, continue.
- Phase 3: fix scope exceeds 5 files / 150 LOC → stop, escalate to `/research-and-decide`.
- Phase 4: no measurable improvement → revert, mark "investigated, no action" in ADR, stop.
- Never ship a fix whose only evidence is subjective. Require numbers.
