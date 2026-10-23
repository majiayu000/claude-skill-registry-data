---
name: e2e-suite-budget
description: "Caps E2E suite size by computing per-test ROI - (regressions caught × value) ÷ (runtime × flake rate × maintenance) - then ranks every end-to-end test and recommends which bottom-decile ones to retire, move to a lower layer, or fix. Use when CI is slow or E2E-dominated, flaky failures are rising, or quarterly to keep suite size within maintenance capacity. For strategic unit:service:UI layer ratios use test-pyramid-balancer, for the minimal per-deploy critical-path gate use smoke-suite-gate, and for quarantining flaky tests use flaky-test-quarantine; this prunes low-signal tests by ROI."
---

# e2e-suite-budget

## Overview

This skill computes per-test ROI and recommends which tests to
retire / move to a lower layer / fix.

## When to use

- E2E suite has grown past 50-100 tests.
- CI time is dominated by E2E (slow CI pipeline).
- Flake rate >5%; team is fatigued.
- Team wants to reduce test maintenance burden or decide which tests to remove.
- Quarterly: scheduled budget review.

## How to use

1. Gather the E2E inventory - per test, pull runtime, flake rate, regressions caught, maintenance PR count, and a 1-5 value tier (Step 1).
2. Validate inputs - confirm every test has runtime and flake data; flag and exclude gaps (Step 1a).
3. Compute per-test ROI = (regressions caught × value) / (runtime × flake rate × maintenance) (Steps 2-3).
4. Rank every test ascending by ROI and take the bottom decile as the action list (Step 4).
5. Decide per bottom-decile test: retire, move to a lower layer, or fix the flake (Step 5).
6. Enforce the absolute budget - once the suite exceeds the cap, adding a new E2E test must retire an existing one (Step 6).
7. Re-run quarterly, and reactively after any flake spike (Step 7).

## Step 1 - Inputs

Per-E2E-test, the agent / skill needs:

- **Runtime:** average per-test duration (from CI).
- **Flake rate:** % of CI runs where the test failed then passed
  on retry (from CI history per `junit-xml-analysis` in the
  qa-test-reporting plugin, Step 3).
- **Regression-catch count:** how many real bugs this test caught
  in the last N months (from incident postmortems referencing the
  test, or git-blame on the failing-then-fixed pattern).
- **Maintenance cost:** PR count modifying the test in last N
  months (proxy for fragility).
- **Value tier:** 1-5; assigned by team (5 = critical journey).

## Step 1a - Validate inputs

Before scoring, verify data completeness:

- Every test ID present in `stats` must have a `runtime_min` value; flag any missing as **SKIP - no runtime data**.
- Flag any test with a missing or null `flake_rate` as **NEEDS MANUAL REVIEW** and exclude from automated scoring until resolved.
- Confirm `maintenance` and `regressions` files share the same set of test IDs as `stats`; log any mismatches.
- Sanity-check the ROI distribution after scoring (Step 3): if >50% of tests score 0.0, the `regressions` data is likely missing or incomplete - warn before generating recommendations.

## Step 2 - ROI formula

```
ROI = (regressions_caught × value_tier) / (runtime_min × (1 + flake_rate) × (1 + maintenance_count_norm))
```

Where:

- `regressions_caught` ≥ 0 (defaults to 0; can be fractional for
  "caught a near-miss").
- `value_tier` ∈ [1, 5].
- `runtime_min` is the test's average runtime in minutes.
- `flake_rate` ∈ [0, 1] (e.g., 0.05 = 5% flake).
- `maintenance_count_norm` is PRs touching the test in the window
  divided by the median for the suite (so a typical-maintenance
  test has factor ~1).

Higher ROI = more value per cost.

## Step 3 - Per-test scoring

```python
# per-test ROI scoring - implements the Step 2 formula
import json, sys
from collections import defaultdict

# Load per-test stats from CI history
stats = json.load(open(sys.argv[1]))  # {test_id: {runtime, flake_rate, ...}}
regressions = json.load(open(sys.argv[2]))  # {test_id: count}
value_tiers = json.load(open(sys.argv[3]))  # {test_id: tier}
maintenance = json.load(open(sys.argv[4]))  # {test_id: pr_count}
median_pr_count = sorted(maintenance.values())[len(maintenance) // 2] or 1

scores = {}
for tid, s in stats.items():
    rc = regressions.get(tid, 0)
    vt = value_tiers.get(tid, 3)
    rt = s['runtime_min']
    fr = s['flake_rate']
    mn = maintenance.get(tid, 0) / median_pr_count
    score = (rc * vt) / (rt * (1 + fr) * (1 + mn))
    scores[tid] = score

# Sort ascending - lowest ROI first
ranked = sorted(scores.items(), key=lambda x: x[1])
print(json.dumps(ranked))
```

## Step 4 - Output: bottom decile

```markdown
## E2E suite budget - `<repo>` - Q2 2026

**Total E2E tests:** 142
**Total runtime:** 38 min (per CI run)
**Median flake rate:** 4.2%
**Bottom-decile (14 tests) recommended for action:**

| Test                                              | ROI | Runtime | Flake | Regressions caught | Value tier | Recommendation |
|---------------------------------------------------|----:|--------:|------:|-------------------:|-----------:|----------------|
| `archive-flow.spec.ts > old-orders`                | 0.0 |   2.1m  |  18%  |        0           |     2      | Retire - high flake, no signal in 6mo. |
| `legacy-checkout.spec.ts > deprecated-promo`       | 0.1 |   3.2m  |   8%  |        0           |     1      | Retire - feature deprecated. |
| `cart.spec.ts > add 1000 items`                    | 0.2 |   4.5m  |   2%  |        0           |     2      | Move to perf suite - not E2E concern. |
| `e2e-utils.spec.ts > date-formatting`              | 0.5 |   0.8m  |   1%  |        0           |     2      | Move to unit layer. |
| ... (10 more)                                       |     |         |       |                    |            |                |

### Estimated impact of acting on all 14

- Suite size: 142 → 128 (-14)
- Runtime: 38 min → 28 min (-10 min per CI run, ~26% reduction)
- Flake-related reruns: estimated -50%
- Maintenance load: -20% (these 14 had the highest PR-touch count)
```

## Step 5 - Categorize recommendations

| Class                | Action                                                 |
|----------------------|--------------------------------------------------------|
| `retire`              | Delete; covered by other tests OR feature deprecated. |
| `lower-layer`         | Rewrite at unit / integration; cheaper.                |
| `fix-flake`           | Tests catches bugs but flakes; investigate per `flaky-test-quarantine` (in the qa-flake-triage plugin). |
| `consolidate`         | Merge with sibling test that overlaps.                 |
| `keep-but-monitor`     | Low ROI but catches important regressions; tag for next-quarter review. |

The team picks the appropriate class per test; the skill recommends.

## Step 6 - Cap discipline

Set an **absolute budget**:

```yaml
# e2e-budget.yml
budget:
  max_tests: 100
  max_runtime_min: 30
  max_flake_rate: 0.03   # 3%
```

When the suite exceeds budget, the next sprint's "add new E2E
test" requires retiring / moving an existing one. Force the
trade-off.

## Step 7 - Cadence

| Cadence    | Trigger                                                 |
|------------|---------------------------------------------------------|
| Quarterly   | Scheduled review.                                       |
| Per-major-feature | New tests added; verify suite stays under budget.  |
| After flake spike | Reactive review; flake source likely a low-ROI test. |

## Worked example

A 40-test E2E suite, median maintenance = 2 PRs/quarter (so `maintenance_count_norm` = PRs ÷ 2). Scoring three representative tests:

| Test                                    | Regressions | Value | Runtime | Flake | PRs (norm) |  ROI |
|-----------------------------------------|------------:|------:|--------:|------:|-----------:|-----:|
| `checkout.spec.ts > guest-purchase`      |      4      |   5   |  2.0m   |   2%  |   2 (1.0)  | 4.9  |
| `admin-report.spec.ts > csv-export`      |      1      |   2   |  3.5m   |  10%  |   3 (1.5)  | 0.21 |
| `legacy-banner.spec.ts > dismiss-cookie` |      0      |   1   |  1.8m   |  20%  |   4 (2.0)  | 0.0  |

The ROI column above is computed with the Step 2 formula. Ranked ascending: dismiss-cookie (0.0) → csv-export (0.21) → guest-purchase (4.9). The bottom decile of 40 is the lowest 4 tests; the first two here fall in it.

Decisions:

- `dismiss-cookie` → **retire**: 0 regressions in the window, 20% flake, feature deprecated - pure cost.
- `csv-export` → **lower-layer**: catches a real regression but tier-2 value, and CSV formatting is cheaply covered by a unit test; rewrite there.
- `guest-purchase` → **keep**: highest ROI in the suite; critical journey, low flake, worth its runtime.

## Anti-patterns and Limitations

See [references/anti-patterns-and-limitations.md](references/anti-patterns-and-limitations.md) for common failure modes (missing regression data, auto-retiring without review, cherry-picking) and known constraints (difficulty gathering regression-catch data, heuristic formula tuning, "test of last resort" cases, migration cost).

## References

- [tp][tp] - Cohn's pyramid: UI tests "brittle, expensive to
  write, and time consuming to run."
- `test-pyramid-balancer` - 
  sibling: identifies the layer-balance issue this skill
  addresses tactically.
- `flaky-test-quarantine` - sibling: handles the flake side of low-ROI tests.
- `junit-xml-analysis` - upstream: provides per-test runtime + flake stats.
- `test-coverage-targeter` - complementary: identifies what to add at the unit layer when
  E2E tests get retired.

[tp]: https://martinfowler.com/bliki/TestPyramid.html
