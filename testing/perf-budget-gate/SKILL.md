---
name: perf-budget-gate
description: "Builds a unified release-readiness gate that aggregates verdicts from any combination of k6 / JMeter / Gatling / Locust load runners and Lighthouse CI Web Vitals, applies severity-aware pass/fail thresholds, and emits a single go / no-go decision with per-metric deltas vs the main-branch baseline. Posts the delta as a PR comment when the team has the integration set up. Use when authoring a CI step that gates a deployment on cross-runner perf compatibility."
---

# perf-budget-gate

## Overview

Modern teams measure perf at multiple layers:

| Layer        | Runner                                                                                |
|--------------|---------------------------------------------------------------------------------------|
| Backend load | `k6-load-testing`, `jmeter-load-testing`, and the Gatling / Locust references in `load-testing-overview` |
| Frontend     | `lighthouse-perf` - Web Vitals via Lighthouse CI       |

Each runner has its own pass/fail criterion. This gate **unifies** them into a
single go / no-go verdict with per-metric deltas vs. main, and emits a markdown
summary suitable for `$GITHUB_STEP_SUMMARY` or a PR comment.

This is the perf counterpart to `data-quality-gate`, `visual-baseline-gate`,
and `contract-compatibility-gate` - same artifact shape, different domain.

## When to use

- The team uses two or more perf runners and wants one CI gate.
- Per-PR perf delta vs. main is the team's regression-detection signal.
- Some metrics should be advisory rather than blocking - e.g. block on p95
  latency regression but warn on Lighthouse score drift.
- Per-metric ratchet behavior is needed (existing budget breaches
  grandfathered, new breaches block).

If the project has only one runner, defer this gate - use the runner's native
CI integration directly.

## How to use

1. Collect each runner's output artifact (k6 `summary.json`, Lighthouse
   `lhr-*.json`, and the rest) - the per-runner source map is in [references/ci-wiring-and-metric-sources.md](references/ci-wiring-and-metric-sources.md).
2. Flatten every runner's output into the unified metric record (below), one
   record per measured subject + metric.
3. Fetch the last green main-branch baseline and compute each record's delta.
4. Apply the gate decision rule to produce a single go / no-go verdict.
5. Emit the markdown + JSON artifact; a no-go exits non-zero and halts CI. Full
   CI wiring and per-metric budgets are in [references/ci-wiring-and-metric-sources.md](references/ci-wiring-and-metric-sources.md).

## The unified metric record

Flatten every runner's output into one shape:

```json
{
  "runner":   "k6",
  "subject":  "GET /api/orders",
  "metric":   "p95_latency_ms",
  "value":    320,
  "baseline": 280,
  "delta":    "+14.3%",
  "budget":   500,
  "status":   "pass",
  "severity": "blocker"
}
```

| Field      | Source |
|------------|--------|
| `runner`   | `k6` / `jmeter` / `gatling` / `locust` / `lighthouse`. |
| `subject`  | URL path / sampler name / story ID - what was measured. |
| `metric`   | `p95_latency_ms` / `error_rate` / `lcp_ms` / `inp_ms` / `cls`. |
| `value`    | Current run's value. |
| `baseline` | Last green main-branch run's value (from artifact storage / Grafana / Lighthouse CI server). |
| `delta`    | Percent change vs. baseline. |
| `budget`   | Configured threshold from the runner. |
| `status`   | `pass` / `fail` based on `value` vs `budget`. |
| `severity` | `blocker` / `warn`. |

## The gate decision rule

```python
def gate_decision(records, *,
                  block_on_regression_pct=10,   # block if any blocker regresses >10%
                  warn_on_regression_pct=3):    # warn if anything regresses >3%
    blockers = []
    warnings = []
    for r in records:
        if r["status"] == "fail" and r["severity"] == "blocker":
            blockers.append((r, "budget breach"))
        elif r["delta_pct"] > block_on_regression_pct and r["severity"] == "blocker":
            blockers.append((r, f"regression > {block_on_regression_pct}%"))
        elif r["delta_pct"] > warn_on_regression_pct:
            warnings.append((r, f"regression > {warn_on_regression_pct}%"))

    return {
        "verdict": "no-go" if blockers else "go",
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "blockers": blockers,
        "warnings": warnings,
    }
```

Two regression triggers:

- **Budget breach** - `value > budget` (absolute threshold).
- **Regression** - `delta_pct > N%` vs. baseline (relative).

Both matter: a metric within budget but trending up still warrants a warning.

## Emit the artifact

Markdown summary:

```markdown
# Perf Budget Gate - verdict: NO-GO

**Blockers: 2**

| Runner     | Subject              | Metric            | Current | Baseline | Δ      | Budget | Status |
|------------|----------------------|-------------------|--------:|---------:|-------:|-------:|--------|
| k6         | POST /api/orders     | p95 latency       | 620ms   | 280ms    | +121% | 500ms  | FAIL   |
| lighthouse | /dashboard           | LCP               | 3200ms  | 2100ms   | +52%  | 2500ms | FAIL   |

**Warnings: 3**

| Runner     | Subject              | Metric            | Current | Baseline | Δ     |
|------------|----------------------|-------------------|--------:|---------:|------:|
| k6         | GET /api/orders      | p95 latency       | 240ms   | 220ms    | +9%   |
| lighthouse | /                    | INP               | 180ms   | 150ms    | +20%  |
| locust     | GET /search          | p95 latency       | 410ms   | 380ms    | +8%   |
```

Plus a JSON sibling for downstream tooling:

```json
{
  "verdict": "no-go",
  "blocker_count": 2,
  "warning_count": 3,
  "blockers": [...],
  "warnings": [...]
}
```

A no-go verdict exits non-zero - CI halts.

## Worked example

Run the gate on one build: read the k6 and Lighthouse artifacts, flatten each
into records, apply the rule, print the verdict, and exit with its code.

```python
# scripts/run_perf_gate.py
import json, csv, sys, os
from pathlib import Path

records = []

# Source: k6 summary.json
k6_path = Path("k6-summary.json")
if k6_path.exists():
    s = json.loads(k6_path.read_text())
    p95 = s["metrics"]["http_req_duration"]["values"]["p(95)"]
    error_rate = s["metrics"]["http_req_failed"]["values"]["rate"]
    records += [
        {"runner": "k6", "subject": "global", "metric": "p95_latency_ms",
         "value": p95, "budget": 500, "severity": "blocker",
         "status": "fail" if p95 > 500 else "pass"},
        {"runner": "k6", "subject": "global", "metric": "error_rate",
         "value": error_rate, "budget": 0.01, "severity": "blocker",
         "status": "fail" if error_rate > 0.01 else "pass"},
    ]

# Source: Lighthouse CI lhr-*.json
for lhr in Path(".lighthouseci/").glob("lhr-*.json"):
    r = json.loads(lhr.read_text())
    url = r["finalUrl"]
    lcp = r["audits"]["largest-contentful-paint"]["numericValue"]
    inp = r["audits"]["interaction-to-next-paint"]["numericValue"]
    cls = r["audits"]["cumulative-layout-shift"]["numericValue"]
    records += [
        {"runner": "lighthouse", "subject": url, "metric": "lcp_ms",
         "value": lcp, "budget": 2500, "severity": "blocker",
         "status": "fail" if lcp > 2500 else "pass"},
        {"runner": "lighthouse", "subject": url, "metric": "inp_ms",
         "value": inp, "budget": 200, "severity": "blocker",
         "status": "fail" if inp > 200 else "pass"},
        {"runner": "lighthouse", "subject": url, "metric": "cls",
         "value": cls, "budget": 0.1, "severity": "blocker",
         "status": "fail" if cls > 0.1 else "pass"},
    ]

# Apply gate
blockers = [r for r in records if r["status"] == "fail" and r["severity"] == "blocker"]
verdict = "no-go" if blockers else "go"

print(f"# Perf Budget Gate - verdict: {verdict.upper()}")
for r in blockers:
    print(f"- {r['runner']} :: {r['subject']} :: {r['metric']} = {r['value']} (budget {r['budget']})")

sys.exit(0 if verdict == "go" else 1)
```

## Anti-patterns

| Anti-pattern                                                     | Why it fails                                                       | Fix |
|------------------------------------------------------------------|---------------------------------------------------------------------|-----|
| Hardcoded budgets in the gate script                              | Budgets evolve; updating requires code review.                     | Externalize to `.perf-budgets.yml` consumed by the gate. |
| Comparing against the previous run, not the main baseline         | Drift compounds; the team approves a 5% regression every PR.       | Compare against the last-known-green main commit. |
| Block on every metric                                             | The gate becomes "the perf gate that always fails."                 | Block on the team's documented NFRs only; everything else is `warn`. |
| Skipping baseline storage                                          | First-run-after-budget-update has nothing to compare against.       | Persist baseline JSON as a build artifact uploaded on every main-branch run. |
| Asserting on Lighthouse score (categories:performance)             | The score conflates LCP/INP/CLS; one bad Web Vital tanks the score uninterpretably. | Assert on individual Web Vitals; category score is supplementary. |

## References

- Per-runner source artifacts, per-metric budgets, and the full CI wiring:
  [references/ci-wiring-and-metric-sources.md](references/ci-wiring-and-metric-sources.md).
- `data-quality-gate`, `visual-baseline-gate`,
  `contract-compatibility-gate` - sibling gates with the same artifact shape.
- `non-functional-requirement-extractor` - upstream skill that produces the
  threshold-bound budgets this gate enforces.
