---
name: uncertainty-display
description: "Use whenever a figure or sentence shows an estimate, forecast, sample-based rate, model metric or average over seeds: decides whether and how to show uncertainty (error bars, bands, fan charts, quantile dotplots, hypothetical outcome plots), and makes every interval state its kind, level, n and method. Also use when someone asks whether two error bars overlapping means anything."
license: CC-BY-4.0
---

# Showing uncertainty

An estimate without its uncertainty invites the reader to treat it as exact.
An interval without a label is worse: SD and SE differ by a factor of √n,
and a 95% CI is about ±2 SE (1.96 for a normal approximation), so the same
data can give three very different bars and the reader cannot tell which
they are looking at.

## Rule 1: every interval states five things

1. **Kind**: standard deviation, standard error, confidence interval,
   credible interval, prediction interval, min–max, or quantile range.
2. **Level**: 50%, 80%, 95%; or "±1 SD".
3. **n and the unit of replication**: 5 training seeds; 212 orders; 14
   weeks. Not "n = 3 runs" when the runs share a seed.
4. **Method**: normal approximation, Wilson, bootstrap (percentile, stratified),
   posterior from model X.
5. **What it is about**: the mean, a single future week, the difference.

Caption pattern: "Shaded: 80% prediction interval for weekly orders from
forecast model v3 (trained to 28 Sep 2026). Points: observed."

## Rule 2: uncertainty is computed by analysis, never by the figure

The plotting layer draws intervals it is given. It does not widen, symmetrise,
smooth or invent them. If no interval exists, the figure says "no uncertainty
estimate available" rather than drawing a decorative band.

## Rule 3: pick the display for the reader

| Reader and question | Display |
|---|---|
| Analyst comparing a few estimates | point + interval (error bar), raw points if n is small |
| Time series with forecast | line + band, widening with horizon; fan chart for several levels |
| Non-technical decision maker ("how likely are we to exceed 250 orders?") | quantile dotplot or a stated probability; frequencies ("in 8 of 10 simulated Septembers") |
| Many plausible trajectories | ensemble of thin lines, or hypothetical outcome plots (animated draws) |
| Distribution of a model metric across seeds | dots for each seed, with the summary marked |

Research on lay readers (Kay et al. 2016; Fernandes et al. 2018; Hullman et
al. 2015) found frequency-framed displays such as quantile dotplots and
hypothetical outcome plots support better probability judgements than error
bars alone. Use them where a decision depends on a probability.

## Rule 4: comparisons need the interval of the difference

- Two SE bars that do not overlap do **not** establish a significant
  difference; two 95% CIs that overlap slightly do **not** establish its
  absence. For paired data (same eval items, same weeks) overlap says almost
  nothing.
- If the claim is "B beats A", compute and show the interval of B − A, paired
  where the design is paired.

## Rule 5: respect the bounds of the quantity

A rate cannot leave 0–100%; a count cannot go negative. Symmetric ±1.96·SE
bars on 2 of 10 cancellations give −5% to 45%. Use an interval that respects
the bounds: Wilson 95% for 2/10 is about 5.7% to 51.0%. Report it, and
question whether a rate on n = 10 belongs in the chart at all.

## Rule 6: precision follows uncertainty

Round the estimate to the interval's precision: "conversion 24% (95% CI
20–28%)", not "24.37%". See `numbers-style`.

## ieeVisualizer: what exists and what is planned

- **Intervals (spec 1.0):** a `band` mark (`y_lower`/`y_upper` along `x`), an
  `errorbar` mark (with the point `y` when encoded), and `y_lower`/`y_upper`
  on line (drawn as a band), scatter and vertical bar marks (error bars).
  Every interval needs `interval_kind` (confidence / credible / prediction /
  quantile / min-max / standard-error / standard-deviation) and
  `interval_level` as a fraction (0.95) for the first four, or
  `interval_multiplier` (1 = ±1 SE) for SE/SD bars; a `quantile` level is
  central (0.8 = 10th-90th percentile), `interval_quantiles` [0.05, 0.75]
  states a non-central one; `validate` refuses one
  without (`missing_interval_kind`, `missing_interval_level`), and lower
  above upper (`interval_inverted`) or a bound in another unit
  (`interval_unit_mismatch`). The renderer writes "95 % prediction interval"
  in the legend (or the caption when the legend is hidden) and draws bounds
  as given; a null bound is a gap.
- **Templates:** `timeseries` 2.0.0 takes `intervals` (several levels make a
  fan chart); `fan_chart` draws nested quantile bands from an ensemble's
  paths (empirical quantiles, a level refused when its tail is thinner
  than one path) or from given quantile columns; `estimate_comparison`
  draws estimates with intervals across groups; `distribution` shades
  "central 90% of the distribution (P5–P95)" of a named distribution (a
  discrete one also says what it really covers); `sample_distribution`
  draws a histogram with a KDE whose bandwidth is stated, an ECDF, or a
  quantile dotplot. `timeseries` 1.0.0's `lower_column`/`upper_column`
  still draw two unlabelled dotted lines: state the kind and level in the
  caption there.
- **Simulated ensembles:** `ieeVisualizer.stochastic` (`random_walk`,
  `gbm`) records the seed and marks the data synthetic; `fan_chart` says so
  in the caption. Say how many paths and which model.
- **Still yours to state:** n, the unit of replication and the method
  (Rule 1, items 3-5) have no field; put them in the `caption`.
- **Planned (ROADMAP "Phase 2 onward"):** an ensemble mark for many
  trajectories (thin lines per path).

## Good / bad

Bad: "Model B: 71.3% ± 1.2" (which ±? over what?).
Good: "Model B: 71.3% (mean of 5 seeds; 95% bootstrap CI 70.1–72.4%)".

Bad: forecast line extending three months with no band and a solid style.
Good: dashed forecast with 50% and 80% prediction bands, caption naming the
model and training cut-off.

Bad: grey band on the orders chart labelled "uncertainty".
Good: "Band: 90% range of weekly orders in 2023–2025 for the same week"
(a historical range, labelled as such, not a confidence interval).

## Checklist

- [ ] Every interval names kind, level, n (unit of replication), method, and target.
- [ ] Intervals come from the analysis; nothing widened or invented in plotting.
- [ ] Display matches the reader (frequency framing for lay decisions).
- [ ] Comparative claims use the interval of the difference (paired if paired).
- [ ] Bounded quantities use bounded intervals.
- [ ] Reported precision matches the interval width.
- [ ] If no estimate of uncertainty exists, the figure says so.

Adapted in part from ieeVisualizer's own docs (MIT), K-Dense
`scientific-visualization` and `uncertainty-and-units` (MIT) and Hullman et
al. 2015 (CC BY 4.0); changed: rewritten and condensed, examples replaced.
Sources and licences: `SOURCES.md`.
