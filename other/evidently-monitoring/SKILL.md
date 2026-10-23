---
name: evidently-monitoring
description: "Use Evidently OSS (100+ evaluation metrics, declarative testing API) to detect data drift, target drift, and model-performance regression, wired into CI as a gate (a Report run with include_tests) and into production monitoring as a continuous check; reports as HTML + JSON for both human review and pipeline assertions. Includes a drift-alert triage playbook: classify the fired alert's signal, rank root-cause hypotheses (upstream schema change, pipeline bug, training-serving skew, seasonality, genuine population shift), and pick rollback, retrain, quarantine, or alert re-tuning. Use when you need a drift or quality gate, a scheduled monitoring job, or a structured triage of a fired drift alert, for a tabular ML model. Built on the Evidently API specifically: for DeepChecks-based validation suites use deepchecks-tests instead."
metadata:
  keywords: "evidently, data-drift, model-monitoring, drift-detection, production-monitoring"
  version: "1.3.8"
---

# evidently-monitoring

Evidently is *"an open-source Python library with over 40+ million
downloads. It provides 100+ evaluation metrics, a declarative testing
API, and a lightweight visual interface"* per [Evidently docs].

## When to use

- Pre-deployment gate: assert no data/target drift between
  candidate-model evaluation set and the production reference.
- Production monitoring: scheduled job comparing yesterday's traffic
  vs the reference window.
- Triage tool: when a model misbehaves in prod, run an Evidently
  Report comparing the bad period to a known-good window.

## How to use

1. `pip install evidently` into the CI or monitoring environment (Step 1).
2. Load a pinned reference dataset and the current dataset as pandas
   DataFrames (Step 2).
3. Run `Report([DataDriftPreset()])` with
   `run(reference_data=, current_data=)` and `save_html` for review (Step 3).
4. For a CI gate, add `include_tests=True`, read `.dict()["tests"]`, and
   `raise SystemExit` on any `FAIL`/`ERROR` (Step 4).
5. Add `RegressionPreset` / `ClassificationPreset` when `prediction` +
   `target` columns exist, to catch performance regression (Step 5).
6. Wrap the gated Report in a daily scheduled job comparing yesterday's
   traffic to the pinned reference, notifying on-call on failure (Step 6).
7. Tune the per-column drift method (`psi`, etc.) and severity tiers so
   critical drift blocks and minor drift only alerts (Step 4).

## Step 1 - Install

```bash
pip install evidently
```

See the canonical install page at
https://docs.evidentlyai.com/docs/setup/installation for the current
install options (`pip install evidently`, plus the `evidently[llm]` extra).

## Step 2 - Reference + current datasets

The standard pattern compares two datasets:

- **Reference** - known-good baseline (e.g., training data, last
  validated production window).
- **Current** - what you're checking (candidate model eval set, or
  current production traffic).

```python
import pandas as pd

reference_df = pd.read_parquet("reference.parquet")
current_df = pd.read_parquet("current.parquet")
```

## Step 3 - Run a drift Report

```python
from evidently import Report
from evidently.presets import DataDriftPreset

# The current API takes the preset list positionally; run() with keyword
# args is unambiguous about which dataset is which (per [Evidently Report]).
report = Report([DataDriftPreset()])
my_eval = report.run(reference_data=reference_df, current_data=current_df)
my_eval.save_html("drift_report.html")
```

Result: HTML dashboard + structured JSON. Per [Evidently docs], the
preset bundles per-feature drift detection with sane defaults.

## Step 4 - Gate CI on the drift tests

In the current Evidently API there is no separate `TestSuite` class. You
enable per-column pass/fail **tests** by passing `include_tests=True` to the
`Report`, then read each test's status from the result, per
[Evidently Report]:

```python
from evidently import Report
from evidently.presets import DataDriftPreset

# include_tests=True turns the preset's per-column drift metrics into
# pass/fail tests alongside the metrics.
report = Report([DataDriftPreset()], include_tests=True)
my_eval = report.run(reference_data=reference_df, current_data=current_df)

# .dict() exposes top-level "metrics" and "tests" only - there is NO
# top-level "status" key. Gate on any test that did not pass.
result = my_eval.dict()
failed = [t for t in result["tests"] if t.get("status") in ("FAIL", "ERROR")]
if failed:
    raise SystemExit(
        f"Evidently drift gate failed: {len(failed)} test(s); see drift_report.html"
    )
```

Evidently's drift detection supports several statistical methods (`psi`,
`wasserstein`, `ks`, `chisquare`, `jensenshannon`); PSI is conventional for
tabular production drift. Configure the method and threshold per column on
the preset or the dataset's data definition, per [Evidently drift preset].

## Step 5 - Model-performance presets

```python
from evidently.presets import RegressionPreset, ClassificationPreset

# Regression
report = Report([RegressionPreset()])
report.run(reference_data=ref, current_data=cur).save_html("regression.html")

# Classification
report = Report([ClassificationPreset()])
report.run(reference_data=ref, current_data=cur).save_html("classification.html")
```

Requires both `prediction` and `target` columns in both DataFrames.

## Step 6 - Schedule in production

```python
# Daily monitoring job
import datetime
from pathlib import Path

today = datetime.date.today().isoformat()
current_df = load_production_window(start=today, days=1)
reference_df = load_reference_window()

report = Report([DataDriftPreset()], include_tests=True)
result = report.run(reference_data=reference_df, current_data=current_df)
result.save_html(Path(f"monitoring/{today}.html"))

if any(t.get("status") in ("FAIL", "ERROR") for t in result.dict()["tests"]):
    notify_oncall(f"Data drift detected on {today}")
```

Pair with a scheduler (Airflow / Prefect / cron / Argo Workflows).

## Step 7 - Triage a fired drift alert

When the Step 6 job pages, triage the alert before acting - never jump straight
to retrain or rollback.

**Parse the alert envelope.** Read the JSON report (`report.dict()` returns the
run as a dictionary per
[Evidently output formats](https://docs.evidentlyai.com/docs/library/output_formats)).
Each column is scored by a drift method against a threshold; defaults are PSI
and Jensen-Shannon divergence at threshold 0.1, KS and chi-square at p-value
0.05, per
[Evidently customization docs](https://docs.evidentlyai.com/metrics/customize_data_drift).
Dataset-level drift triggers when the share of drifted columns reaches
`drift_share`: "By default, Dataset Drift is detected if at least 50% of
columns drift" per [Evidently drift preset]. Note which columns drifted and
which stat test fired.

**Classify the drift signal:**

| Signal | Look for |
|---|---|
| Broad feature drift (many columns) | Schema/ETL change or population shift |
| Single-column drift, especially an ID or timestamp | Pipeline bug or upstream encoding change |
| Target/prediction drift without feature drift | Concept drift or label-pipeline failure |
| Drift that aligns with calendar (weekend, holiday, season) | Seasonality - not a model failure |
| Drift only in serving data, not in a held-out eval set | Training-serving skew |

**Rank root-cause hypotheses** (default likelihood order in practice; adjust on
the signal evidence) and act per hypothesis:

1. **Upstream schema change** - a feed column renamed, retyped, or dropped.
   Diff the upstream schema against a reference snapshot; fix the feature
   pipeline; re-run the report before returning the model to live traffic.
2. **Pipeline bug** - a join key, fill-value, or preprocessing step changed.
   Check deploy timestamps against drift onset; roll back the coinciding
   deploy; quarantine predictions from the affected window; add a per-column
   CI drift gate for the affected column.
3. **Training-serving skew** - the live feature path diverges from the
   training path (different imputation or aggregation window). Align serving
   feature code with the training job, then regenerate the reference dataset
   from the corrected serving path.
4. **Seasonality** - known calendar or business-cycle effect. Corroborate with
   a year-over-year window or business calendar first; then widen the affected
   columns' thresholds (or switch stat test) via per-column configuration per
   [Evidently customization docs](https://docs.evidentlyai.com/metrics/customize_data_drift),
   and document the pattern as a known-good deviation.
5. **Genuine population shift** - the data-generating process changed (new
   product line, user segment, regulation). Retrain on a window that includes
   the new population; re-run the fairness gating workflow in
   `model-risk-evidence-matrix` on the retrained candidate (fairness metrics
   shift with population); update the reference dataset only after successful
   promotion.

**Triage discipline:**

- Cite the report data (columns, stat tests, onset timestamp) behind every
  hypothesis; no rollback or quarantine call without the columns and onset
  time that substantiate it.
- Never classify an alert as seasonality without corroborating evidence
  (year-over-year window, business calendar, or a prior documented pattern).
- Never retrain before ruling out hypotheses 1-3: retraining on drifted input
  without fixing the upstream cause embeds the bug in the new model.

## Worked example

A team ships a weekly retrain of a tabular fraud classifier and wants CI to
block a release whose input distribution has moved too far from the validated
baseline.

1. `reference.parquet` holds the last validated production week (~400k rows);
   `current.parquet` holds the candidate model's eval slice.
2. The CI step runs a gated drift Report:

```python
from evidently import Report
from evidently.presets import DataDriftPreset

report = Report([DataDriftPreset()], include_tests=True)
result = report.run(reference_data=reference_df, current_data=current_df)
result.save_html("drift_report.html")

failed = [t for t in result.dict()["tests"] if t.get("status") in ("FAIL", "ERROR")]
if failed:
    raise SystemExit(f"Evidently drift gate failed: {len(failed)} test(s)")
```

3. Two columns (`transaction_amount`, `merchant_country`) drift past their PSI
   threshold, so their tests report `FAIL`.
4. `raise SystemExit` fails the CI job; `drift_report.html` is uploaded as a
   build artifact showing the two drifted distributions.
5. The engineer confirms `merchant_country` gained a new region, widens that
   column's threshold (or retrains on data that includes it), and the re-run
   passes.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Use yesterday as reference (rolling window only) | Slow drifts go undetected (model degrades 1% per day for 100 days = 100% drift) | Pin a stable reference (Step 2) |
| Run only on training data | Training data is curated; never reflects real production distribution | Use real production samples (Step 6) |
| Default thresholds for all metrics | Defaults are textbook; production tolerance differs | Tune per-feature thresholds (Step 4) |
| Block deploy on every drift | High-traffic production shifts daily; team disables monitor | Severity tiers: critical drift blocks; minor drift alerts |
| Skip target/prediction drift | Concept drift (inputs stable, output behavior changed) goes undetected | Include the target/prediction column in the drift check (Steps 3-4) |

## Limitations

- 100+ metrics doesn't mean every domain. Healthcare/finance fairness
  metrics often need pairing with `fairlearn-fairness` skill.
- Memory: full preset on millions of rows can OOM. Sample to
  100k - 1M before passing.

## References

- [Evidently docs] - library overview, presets, install snippet
- [Evidently Report] - Report construction, `include_tests`, `run()`, and
  the `.dict()` result shape (top-level `metrics` + `tests`, per-test status)
- [Evidently drift preset] - DataDriftPreset and per-column drift method
  configuration
- The [Evidently docs] llms.txt index lists current canonical per-preset
  documentation: https://docs.evidentlyai.com/llms.txt

[Evidently docs]: https://docs.evidentlyai.com/
[Evidently Report]: https://docs.evidentlyai.com/docs/library/report
[Evidently drift preset]: https://docs.evidentlyai.com/metrics/preset_data_drift
