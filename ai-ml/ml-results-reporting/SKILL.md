---
name: ml-results-reporting
description: "Use when reporting or plotting machine-learning or AI-research results: benchmark tables, model comparisons, ablations, training curves, RL returns across seeds, scaling-law fits, LLM eval scores, pass@k, calibration plots. Enforces seeds and run counts, robust aggregates (IQM) with bootstrap intervals, eval standard errors, paired comparisons, equal tuning budgets, and no bolding a winner without evidence."
license: CC-BY-4.0
---

# Reporting ML results

A leaderboard number is an estimate from a finite set of seeds and a finite
set of eval items. Report it so a reader can tell a real gap from noise.

## Rules

1. **Say what varies.** For every number: how many seeds/runs, what the seed
   controls (init, data order, environment), how many eval items, and the
   decoding settings (temperature, top-p, k, prompt version).
2. **Eval standard error.** Accuracy p on n independent items has
   SE ≈ √(p(1−p)/n). At p = 0.71, n = 1,000: SE ≈ 1.4 pp, so a 95% interval
   is about ±2.8 pp. Items grouped (several questions per passage, several
   tests per problem) need clustered standard errors, which are larger.
3. **Compare paired.** Two models on the same items: compute per-item
   differences and report the mean difference with its interval. Paired
   intervals are usually much narrower than the two separate ones; overlap of
   separate intervals is not the test.
4. **Aggregate across runs and tasks robustly.** With few runs, report the
   interquartile mean (IQM: mean of the middle 50% of run-task scores) with a
   stratified bootstrap confidence interval, alongside per-task results.
   Means are dominated by outlier tasks; medians ignore most of the data.
   Performance profiles (fraction of runs above each score) show the whole
   distribution. The `rliable` library implements these.
5. **Show the runs.** With 3–10 seeds, plot every seed (dots or thin lines)
   with the aggregate on top. A band alone hides a bimodal outcome (some
   seeds diverge).
6. **Equal budgets, stated.** Report the hyperparameter search budget (trials,
   GPU-hours) for every method, tuned baselines included. A method tuned for
   200 trials vs a baseline at defaults is a budget comparison. Expected
   best-validation-score-vs-budget curves make this visible; their simple
   estimator is biased at small budgets, so report the number of trials
   behind each point.
7. **No test-set selection.** Checkpoints, prompts and hyperparameters are
   chosen on validation data. Say which split selected what.
8. **Bold only what is distinguishable.** Bold the best entry only if its
   paired difference from the runner-up excludes zero at the stated level;
   otherwise bold every entry whose difference from the best is not
   distinguishable from zero, or none. "Not distinguishable" is not "tied":
   the interval may still allow a gap that matters. Across several
   benchmarks or metrics, adjust for the number of comparisons (e.g.
   Bonferroni-adjusted intervals; say which) or label the bolding
   exploratory.
9. **Training curves state their axes and smoothing.** x in steps, tokens or
   FLOPs (say which); smoothing named ("EMA, α = 0.9; raw in light colour");
   band named ("min–max over 5 seeds").
10. **Scaling-law plots.** Log–log axes labelled as such, fitted form and
    fit interval stated, and extrapolated points drawn as forecast, not as
    measurements.
11. **Projections are not distances.** Label t-SNE/UMAP/PCA plots as
    projections and do not read cluster gaps as similarity measurements.
12. **Contamination and versions.** State the benchmark version, any known
    overlap with training data, and the evaluation harness version.

## Table template

| Model | Accuracy (%) | Δ vs baseline (pp, paired 95% CI) | Seeds | Tuning trials |
|---|---|---|---|---|
| Baseline | 68.9 | — | 5 | 50 |
| Ours | 71.3 | +2.4 (+0.9 to +3.9) | 5 | 50 |

Caption: "MMLU-style eval, 1,000 items, greedy decoding, prompt v4. Accuracy
is the mean over seeds; Δ is the mean per-item paired difference with a
bootstrap interval over items and seeds."

## Good / bad

Bad: "Our method achieves SOTA (**71.3** vs 70.9)" from one seed each.
Good: "71.3 vs 70.9 (paired Δ +0.4 pp, 95% CI −1.1 to +1.9; 5 seeds): the
difference is not distinguishable from zero, and the interval still allows
up to 1.9 pp either way, so this is not evidence the two are equal."

Bad: RL return curve, mean of 3 seeds, band unlabelled, smoothed with an
unknown window.
Good: each seed in a thin line, IQM in bold, band "95% stratified bootstrap
CI", smoothing stated.

## ieeVisualizer mapping

- Per-seed results: `scatter` on a category x-axis (method), or one `line`
  per seed via `series`.
- Curves with an interval: `timeseries` template (2.0.0) with numeric time
  and a unit (`steps`) and `intervals=[{"lower": ..., "upper": ..., "kind":
  "confidence", "level": 0.95}]` from your own bound columns, or a `band`
  mark directly. The kind and level are required and shown in the legend;
  say n (seeds) and the method in the caption.
- Log–log: `axes.x.scale = "log"`, `axes.y.scale = "log"`; non-positive values
  are refused (`log_scale_nonpositive`).
- Extrapolations: separate dataset with `role="forecast"`; always drawn
  distinctly.
- AI-research templates (training curves with seed variance, scaling fits,
  calibration, confusion matrices) are planned, not on `main`.

## Checklist

- [ ] Seeds, eval items, decoding settings and prompt version stated.
- [ ] Every score has an interval with kind and method.
- [ ] Comparisons are paired and show the interval of the difference.
- [ ] Aggregates across tasks use IQM (or justify the mean) with bootstrap CIs.
- [ ] Individual runs are visible.
- [ ] Tuning budgets equal or stated.
- [ ] Selection used validation data only.
- [ ] Bold marks only distinguishable winners.
- [ ] Smoothing, axes units, log scales and extrapolations labelled.

Adapted in part from Agarwal et al. 2021 and Dodge et al. 2019 / Tang et al.
2020 (all CC BY 4.0); changed: condensed into rules, examples invented.
Sources and licences: `SOURCES.md`.
