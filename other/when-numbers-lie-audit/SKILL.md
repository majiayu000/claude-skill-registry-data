---
name: when-numbers-lie-audit
description: "Use when checking whether a chart, KPI, comparison or analytic claim could mislead even though every number in it is correct: truncated or dual axes, cherry-picked windows, incomplete periods, denominator or definition shifts, average of averages, mix shift and Simpson's paradox, survivorship, base rates, small-n percentages, seasonality, regression to the mean, join explosion, timezone cut-offs, area/volume encodings. Run before any figure or number leaves the workspace."
license: CC-BY-4.0
---

# When do the numbers lie?

Correct numbers mislead through what they are compared with, what they leave
out, and how they are drawn. This skill is a systematic pass over those
three channels. It finds problems; `figure-review-redteam` runs it
adversarially and `company-report-structure` decides what to do with the
answer.

## Workflow

1. **State the claim** the figure or sentence makes, in one sentence with a
   number: "Consultation-to-order conversion fell from 31% to 24% in September."
2. **Comparison audit** (what is it compared with?): run the *Comparison*
   rows below.
3. **Population audit** (who or what is counted?): run *Population*.
4. **Encoding audit** (how is it drawn?): run *Encoding*.
5. **Recompute one number independently** (a second query, a different
   aggregation path, or a hand count of a few rows). If it disagrees, stop.
6. **Verdict** per claim: *holds*, *holds with caveat* (write the caveat),
   or *does not hold* (rewrite or drop). Details and worked examples for
   each pitfall: `references/pitfalls.md`.

## The audit table

| # | Pitfall | Test that detects it |
|---|---|---|
| **Comparison** | | |
| C1 | Incomplete period | Is the last period complete in the source's timezone? Same number of days/business days as the base? |
| C2 | Cherry-picked window | Does the conclusion survive starting the window one period earlier and later? Is the start a peak or trough? |
| C3 | Seasonality | Demand is seasonal (e.g. spring and pre-holiday peaks for a retailer). Is the base the same season (year over year, same weekday mix)? |
| C4 | Regression to the mean | Was the segment chosen *because* it was extreme? Then its "recovery" is expected without any cause. |
| C5 | Definition or denominator shift | Did the metric definition, tracking, attribution window or eligibility rule change inside the window? |
| C6 | Nominal vs real | Euros compared across years without price-level adjustment, or prices compared across a VAT change. |
| C7 | Missing base rate | "40% of damage claims came from flat-pack deliveries" means nothing until you know what share of deliveries are flat-pack. |
| **Population** | | |
| P1 | Survivorship | Who is not in the data: cancelled orders, churned customers, failed training runs, deleted campaigns? |
| P2 | Selection on the outcome | Segments defined by the result ("customers who ordered twice") then credited with it. |
| P3 | Mix shift / Simpson's paradox | Does the aggregate move the opposite way, or much more, than every segment? Decompose into rate and mix. |
| P4 | Average of averages | Is a mean of per-segment rates or means reported without weights? Recompute from rows. |
| P5 | Join explosion | Row count before vs after each join; `COUNT(DISTINCT id)` vs `COUNT(*)`. |
| P6 | Small n | Any percentage on a small base (roughly under 30 units, a prompt to look, not a threshold), or a change driven by a handful of events? Show the counts. |
| P7 | Timezone and cut-off | Are UTC timestamps bucketed into the business's local days/weeks consistently across sources? |
| **Encoding** | | |
| E1 | Truncated bar or area axis | Bars and areas encode length from a baseline; does the value axis include zero? |
| E2 | Dual axes | Two y-scales chosen independently can manufacture any correlation. Use two aligned panels. |
| E3 | Area/volume for one dimension | Bubble radius (not area) scaled to the value; 3D objects. |
| E4 | Inconsistent panel scales | Small multiples with free y-axes compared as if shared. |
| E5 | Aspect ratio | Slope exaggerated or flattened by plot shape; is the change in the title matched by the visual slope? |
| E6 | Unlabelled transform | Log, index (=100), cumulative, per-capita or smoothed series not said so on the axis or caption. |
| E7 | Cumulative hides decline | A cumulative total always rises; is the per-period series falling? |
| E8 | Forecast styled as data | Projections, targets and plans drawn like observations. |

## Rules

- A chart passes only if the title's claim survives C1–C5 and P1–P4.
- Fix by changing the comparison, not by adding a hedge: drop the partial
  week, compare to the same weeks last year, show the segments.
- When a pitfall cannot be ruled out with the data available, say so in the
  caption in one sentence ("Attribution window changed from 7 to 28 days on
  14 Sep; earlier weeks are not comparable.").
- Do not "fix" a real effect away. The audit asks whether a claim is
  supported, not whether it is welcome.

## Where ieeVisualizer helps, and where it does not

Enforced: spec 1.0 has one y axis per figure, so dual-axis charts cannot be
expressed (E2); `role="forecast"` layers are always drawn distinguishably and
a solid forecast style is overridden with `forecast_style_overridden` (E8);
`log_scale_nonpositive` and `scale_dtype_mismatch` catch impossible scales;
`axis_unit_conflict` and the templates' `mixed_units` stop two units sharing
an axis; columns carry `denominator` and `aggregation` fields so the
definition travels with the data.

Not enforced (the skill is the guard): zero baselines for bars (`axes.y.limits`
can exclude zero), complete periods, window choice, segment decomposition,
weighting, and whether a declared `denominator` is the right one.

## Checklist

- [ ] Claim written as one sentence with a number, period and base.
- [ ] Last period complete, or dropped, or labelled partial.
- [ ] Window robustness: conclusion unchanged when the window shifts ±1 period.
- [ ] Same-season base for seasonal metrics.
- [ ] No definition/tracking change inside the window, or it is annotated.
- [ ] Segment decomposition checked for any aggregate rate change.
- [ ] Rates recomputed from rows, not averaged.
- [ ] Counts shown next to every percentage on a small base.
- [ ] Bars/areas include zero; no dual axes; panel scales shared or flagged.
- [ ] One number recomputed by an independent path.

Adapted in part from Anthropic's `validate-data` skill (Apache-2.0) and UK
Analysis Function chart guidance (OGL v3.0); changed: reorganised into a
comparison/population/encoding audit, rewritten, examples replaced. Sources and licences: `SOURCES.md`.
