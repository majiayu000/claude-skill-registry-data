---
name: statistical-claims
description: "Use when a sentence, caption or headline makes an inferential claim: a difference is 'significant', a change was 'caused' or 'driven' by something, an A/B test 'won', a correlation is reported, or a null result is read as 'no effect'. Enforces effect sizes with intervals, honest p-value wording, multiplicity accounting, stopping rules, power for null results, and a causal-language ladder matched to the study design."
license: CC-BY-4.0
---

# Statistical claims

The words in a claim must not be stronger than the design and the data. This
skill checks wording against evidence; `uncertainty-display` checks how the
interval is drawn.

## Rule 1: lead with the effect and its interval

Report the size of the effect in the reader's units, with an interval, before
any test statistic.

Good: "The new checkout page raised checkout conversion by 3.1 percentage
points (95% CI 0.4 to 5.8; 4,000 checkout sessions, randomised)."

(Illustrative; figures invented but consistent: 2,000 sessions per arm, 24.0%
vs 27.1%. SE = √(0.240·0.760/2,000 + 0.271·0.729/2,000) ≈ 1.38 pp, and
3.1 ± 1.96 × 1.38 = 0.4 to 5.8 pp, normal approximation. With only 920
sessions per arm the same rates give ±4.0 pp, an interval of −0.9 to 7.1.)

Bad: "The new checkout page had a significant effect (p = 0.03)."

## Rule 2: say what a p-value is, and nothing more

- It is the probability of data at least this extreme *if* the null model
  were true. It is not the probability that the null is true, nor the size or
  importance of the effect.
- Do not let p = 0.049 and p = 0.051 lead to opposite conclusions. Report the
  exact value and the interval.
- Avoid "significant" in reader-facing text; it is read as "important". If
  used, write "statistically significant at the 5% level" once and define it.

## Rule 3: count the comparisons

- State how many segments, metrics, time windows or variants were examined,
  not only the one that moved. Ten segments at the 5% level give a good chance
  of at least one false alarm (about 40% if independent).
- Either correct (Bonferroni or Holm for a family-wise level,
  Benjamini–Hochberg for the false discovery rate; say which) or label the result
  **exploratory**, to be confirmed on new data.
- Pre-specified primary metric beats post-hoc winner.

## Rule 4: respect the stopping rule

Checking an A/B test daily and stopping at the first p < 0.05 inflates false
positives. Fix the sample size in advance or use a sequential method designed
for repeated looks; report which.

## Rule 5: a null result needs power

"No significant difference" is not "no difference". Report the interval: if it
spans effects that would matter (−4 to +6 pp), the test was inconclusive.
State the minimum detectable effect the design could find.

## Rule 6: causal language ladder

| Design | Allowed verbs | Forbidden without more evidence |
|---|---|---|
| Randomised experiment, pre-specified | caused, raised, reduced, the effect of | — |
| Credible quasi-experiment (diff-in-diff, regression discontinuity) with assumptions stated | estimated effect, likely caused, consistent with | proved |
| Before/after with no control | rose after, coincided with | caused, drove, because of |
| Cross-sectional or observational correlation | associated with, higher among, predicts | drives, leads to, results in |
| Single anomaly | was unusual, departed from | anything causal |

Business example (illustrative; figures invented): conversion rose from 22%
to 26% the week the new pricing page launched, but August→September is also seasonal and a campaign changed
the traffic mix. Write "Conversion rose after the pricing page launch; the
season and a change in traffic mix may account for part of it. A holdout
would separate them."

## Rule 7: name confounders and the comparison group

For any observational claim, list the two or three most plausible alternative
explanations (season, mix, tracking change, selection) and whether the
analysis addressed them. Unknowns stay visible.

## Rule 8: correlation reports carry n and shape

r = 0.62 on 9 cities is not r = 0.62 on 900 customers. Report n, show the
scatter, and check that one outlier is not producing the coefficient.

## ieeVisualizer note

The library draws; it computes no tests, intervals or effects (statistics
belong to the analysis layer, e.g. ieeLabTools). Any claim in a `title` or
`caption` is unchecked text: this skill is the guard.

## Checklist

- [ ] Effect size in reader units with interval comes first.
- [ ] p-values (if any) exact, not used as a size or a probability of truth.
- [ ] Number of comparisons stated; corrected or labelled exploratory.
- [ ] Stopping rule stated for experiments.
- [ ] Null results report the interval and minimum detectable effect.
- [ ] Verbs match the design's rung on the causal ladder.
- [ ] Plausible confounders named for observational claims.
- [ ] Correlations report n and are shown as a scatter.

Adapted in part from K-Dense `statistical-analysis` (MIT); changed: condensed
to claim-wording rules, examples replaced. Sources and licences: `SOURCES.md`.
