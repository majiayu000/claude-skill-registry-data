---
name: walk-forward-leakage-auditor
description: Audits time-based machine learning backtests, walk-forward validation, rolling retraining, forecasting evaluations, and temporal train/test pipelines for data leakage, faulty split logic, invalid feature timing, target leakage, calibration/tuning leakage, and misleading experiment comparisons. Use when agent needs to review or change walk-forward code, time-series ML experiments, trading backtests, forecasting notebooks, rolling CV logic, or any model evaluation where past-to-future chronology matters.
---

# Walk-Forward Leakage Auditor

## Core Principle

Before trusting  reported metric, state the temporal contract:

```text
For a prediction made at <decision_time>, allowed inputs are <data sources> as known no later than <cutoff_time>. The target covers <future horizon>. Training may use rows ending at <train_end>, validation/calibration may use rows <validation_window>, and final reported performance comes only from <test_window>.
```

If the project cannot state this contract, the evaluation is not yet auditable.

## Audit Workflow

1. Map the evaluation timeline.
   - Identify the prediction timestamp, label horizon, feature cutoff, train window, validation/calibration window, test/scoring window, embargo/gap, and retrain cadence.
   - Verify that every reported metric is computed only after the model, thresholds, transforms, and selection rules are frozen for that test window.

2. Trace data through the pipeline.
   - Follow raw data into features, labels, datasets, splits, fitted transforms, models, predictions, decisions, and metrics.
   - Verify that every fitted object is trained inside the fold/window where it is used.
   - Distinguish label construction from model features: label code may look forward, but label columns must be excluded from model inputs.

3. Inspect code and artifacts against the checklist below.
   - For each suspicious pattern, decide: leak, harmless by construction, or needs a test/guard.
   - Prefer concrete file/line evidence over broad claims.

4. Require a failable guard before trusting the result.
   - Add assertions for split ordering, no overlap, embargo, feature availability cutoff, fitted-transform scope, and comparable run controls.
   - Prefer a tiny synthetic fixture that fails if a future value leaks into a past prediction.
   - Rerun affected results after fixing leakage or faulty logic.

## Split Logic Checklist

Check:

- Train rows end before validation/test rows begin.
- Embargo/gap is at least as long as the label horizon or any overlapping feature lookback that can leak target information.
- Fold boundaries are based on event/prediction time, not row order after arbitrary filtering.
- Same entity/event cannot appear in both train and test when that creates leakage.
- Hyperparameter, threshold, feature-selection, and architecture choices do not use final test metrics.

Red flags:

- `train_test_split`, `KFold`, `StratifiedKFold`, `.sample(frac=...)`, or `shuffle=True`.
- Selecting "best" model/threshold by test Sharpe, test AUC, test return, or final leaderboard score.
- Reusing the same validation slice for early stopping, calibration, feature selection, and threshold selection without acknowledging optimism.

## Feature Timing Checklist

Check:

- Rolling, expanding, rank, z-score, and aggregation features are lagged to the prediction cutoff.
- Cross-sectional features only use constituents and data known at the prediction time.
- Joins to fundamentals, events, news, status, or labels use release/effective timestamps, not file dates or period end dates.
- Imputation does not backfill from future observations.

Red flags:

- `shift(-1)` or negative periods in feature code.
- `.rolling(...)` or `.expanding(...)` used on a feature without a following lag/shift.
- `bfill`, `fillna(method="bfill")`, interpolation across the train/test boundary.
- `merge_asof(..., direction="forward")`.
- Features named like `future_*`, `next_*`, `target_*`, `label_*`, `outcome_*`, `realized_*`, `exit_*`, or `pnl_*`.

## Fitted Transform Scope

Every fitted object must be fit inside the training fold/window:

- Scalers and normalizers.
- Imputers.
- Encoders.
- PCA/UMAP/SVD.
- Feature selectors.
- Target encoders and count/frequency encoders.
- Oversampling/SMOTE/class balancing.
- Calibrators.
- Threshold selectors.

Red flags:

- `fit_transform` on the full dataset before split.
- Global means/stds/min/max/quantiles used to normalize the full timeline.
- Calibration trained on test predictions.

## Label And Outcome Construction

Labels may use future data, but only inside label-generation artifacts that are excluded from model features. Check:

- Label columns are explicitly excluded by name or schema.
- Ambiguous/incomplete horizons are handled consistently.
- Rows near the dataset end are not scored when labels are unavailable unless running true live-mode inference.
- The target horizon cannot overlap the training window for the next fold without embargo.

## Backtest And Simulation Logic

Check:

- Decision prices, fills, spreads, borrow availability, liquidity, and latency are available at decision time or modeled realistically.
- Position sizing uses only pre-trade account state.
- Trade selection thresholds are fixed from training/validation, not final test performance.
- Metrics include costs/slippage when the claimed result depends on tradability.

## Comparable Experiment Checks

Fail a comparison when any of these differ unless the difference is the explicit treatment:

- Dataset version/hash/row count.
- Date range, cohort, universe, or entity membership.
- Target definition or horizon.
- Starting capital, budget, leverage, exposure, or cost model.
- Split policy, embargo, retrain cadence, and lookback.
- Metric definition, net/gross treatment, and aggregation level.

## Review Standard

Lead with concrete findings and file/line references. For each issue, include:

- What leaks or is logically faulty.
- Why it changes evaluation results.
- The minimal fix or guard.
- Whether the result should be rerun.

If no leak is found, say which checks were performed and name the remaining unverified assumptions.

## Common Fix Patterns

- Replace random splits with chronological splits or blocked/time-series CV.
- Fit scalers, imputers, encoders, feature selectors, calibration models, and threshold selectors inside each training window only.
- Add an embargo/gap when labels or feature windows can overlap the scoring horizon.
- Lag rolling/expanding features so the current prediction row cannot see its own outcome.
- Use backward/as-of joins with explicit timestamp tolerance for point-in-time data.
- Exclude labels, outcomes, future returns, post-event status fields, and model diagnostics from feature columns.
- Separate validation/calibration/tuning windows from final test windows.
- Save run metadata and fail comparisons when run controls differ.

