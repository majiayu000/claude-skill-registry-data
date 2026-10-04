---
name: rdd
description: Design, estimate, validate, and write up a regression discontinuity analysis, in both the continuity and local-randomization frameworks, with the full falsification battery and a refusal rule for designs that fail validation. TRIGGER on "regression discontinuity", "RDD", "running variable", "cutoff", "rdrobust", "bandwidth", "McCrary test", "density test", "fuzzy RD", "regression kink", or any setting where treatment switches at a known score threshold (loyalty tiers, spend thresholds, ranking cutoffs, algorithmic triggers, eligibility scores, age or tenure rules).
---

# Regression discontinuity

An opinionated RD workflow grounded in a read canon (references/canon.md, current as of
2026-07-28): the Cattaneo-Titiunik Annual Review of Economics survey and its applied companion,
the Cattaneo-Keele-Titiunik guide, which includes a real failed design this skill uses as its
refusal template. Deliverable: the recommendation with its citation, the R estimation and
diagnostics code, and a methods paragraph.

Refresh path: run litreview on the method since the canon date, then propose additions to
references/canon.md as flagged addenda.

## Design shapes and the case that anchors each

Each canonical case is a precedent a methods section can cite; details.md says what each teaches.

| Design shape | Canonical case | Marketing analogue | What kills it |
|---|---|---|---|
| Age or tenure eligibility rule | Card, Dobkin, Maestas 2008 | trial expiry, anniversary status rolloff | something else switches at the same threshold |
| Agency-measured score, sharp | Hansen 2015 | churn-score retention offers | reps or managers override the rule off-cutoff |
| Heaped or rounded score | Almond et al. 2010; Barreca et al. 2011, 2016 | spend thresholds recorded in whole dollars | excess mass at round values that the density test misses |
| Share crossing a fixed bar | Lee, Moretti, Butler 2004 | seller badge above an on-time-delivery rate | predetermined covariates already jump in the smallest window |
| Admission cutoff, fuzzy first stage | Hoekstra 2009 | lead-score outreach with rep discretion | a first stage too weak to carry the ratio |
| Boundary or geographic RD | Black 1999 | DMA advertising borders | the border sorts households, or ads spill across it |

## The design gate: is this an RD at all?

An RD requires a score, a known cutoff, and a treatment rule that existed ex ante and is
verifiable. Before any estimation, write the qualitative account: who computes the score, was
the cutoff public, can agents precisely control their score near it. Precise manipulation is the
most important threat. Lab-measured or third-party-computed scores resist it; self-influenced
scores (customer spend near a tier threshold, follower counts near a monetization bar) invite
exactly the sorting the density test detects, so the falsification battery carries more weight
in marketing settings than in the medical originals.

One more gate question, and the one sharp designs skip: list every rule, benefit, message, and
flag that changes at this exact threshold, and say which of them is the treatment. Medicare
starts at 65 and so does retirement, so Card, Dobkin, and Maestas (2008) went to a third dataset
on the same running variable (the March CPS 1996-2004) and showed employment does not jump. When
the confounder is not in your data, find a dataset on the same score where it is.

Two red flags, the first disqualifying on its own (from the failed Oncotype-DX application in
Cattaneo-Keele-Titiunik 2023):

1. Treatment take-up jumps at score values away from the official cutoff (the rule was soft:
   reps contact leads below the threshold, managers grant status matches early). Plot take-up
   against the score before anything else.
2. Covariate imbalance already in the smallest window around the cutoff: disqualifying when
   the imbalanced covariate plausibly drives the outcome (the balance battery's standard,
   below), otherwise a serious flag that demands an explanation before proceeding.

When a design fails, say so and decline to report an effect; the guide's own verdict on its
failed application ("the evidence does not support an RD analysis") is the template. Route the
question back to causal-design for another identification strategy.

## Triage: two frameworks, and which one leads

Sharp vs fuzzy is a fact of the institution, not a choice: sharp when the rule binds
mechanically (a trial expires, a discount ends at an anniversary), fuzzy whenever anyone can
cross their assignment (overrides, opt-ins). Under fuzziness always report both ITT effects (on
take-up and on the outcome) alongside the fuzzy ratio.

Continuity vs local randomization is decided by the score:

- Continuous score, many observations near the cutoff: continuity framework with local
  polynomials leads; local randomization is the robustness complement.
- Discrete score (rule of thumb: roughly 30 or fewer distinct values) or very few observations
  near the cutoff: local randomization leads. Continuity methods there extrapolate from the
  nearest mass points and their effective sample size is the number of mass points, not the
  number of observations. Discrete running variables (weeks of tenure, order counts, months
  since signup) are the norm in marketing data, which makes this branch more common than the
  econ literature suggests.
- Local randomization needs a strictly stronger assumption (potential outcomes unrelated to the
  score inside the window), which must be argued, not assumed.

When both frameworks apply, run both; agreement is a robustness result, and the local
randomization CIs covering the continuity point estimate counts as consistency. Expect the
window to be far narrower than the bandwidth (in the guide's HIV application, 121 patients vs
2,593), so a local-randomization null alongside a significant continuity estimate can be a power
difference, not a contradiction.

## The consensus recipe (continuity framework)

Local linear regression, triangular kernel, MSE-optimal bandwidth, robust bias-corrected
confidence intervals (Calonico-Cattaneo-Titiunik). Report both the conventional and the robust
interval. The one-line justification: conventional 95 percent intervals at the MSE-optimal
bandwidth cover only about 80 percent, and bias correction with the matching variance adjustment
restores coverage at the same bandwidth. Two things get called robust: the Mixtape (Cunningham,
Causal Inference: The Remix, ch. 6) moves between heteroskedasticity-robust OLS standard errors
and rdrobust's Robust row without flagging the difference, and this skill keeps them apart
because HC-robust errors leave the point estimate alone while rdrobust's Robust row recenters on
the bias-corrected estimate and widens the interval by the variance of the bias estimate.

Hard rules from the review, stated as prohibitions because that is how it states them:

- Bandwidths must be data-driven and criterion-optimal; choosing one by hand "is discouraged."
  MSE-optimal for the point estimate, CE-optimal when the interval is the object. Distinct
  left/right bandwidths are available when curvature differs by side. The Mixtape (ch. 6)
  replicates Hansen 2015 with hand-picked bandwidths and a rectangular kernel, which is how RD
  was done before 2014; this skill refuses that as a primary specification and keeps it only
  for reproducing a paper that predates the criterion-optimal machinery.
- Never cluster standard errors on the running variable. The Mixtape (ch. 6) reports the practice
  as history, recommended by Lee 2008 and Lee and Card 2008 and then discouraged; this skill
  states it as a prohibition because Kolesar and Rothe 2018 show it inflates Type I error. Use
  heteroskedasticity-robust variance, honest intervals for a discrete score, and cluster only on
  a real assignment unit that is not the score. Replicating or refereeing an older RD, expect to
  find this and fix it.
- Global polynomial fits are visualization only, never estimation (Gelman-Imbens): boundary
  behavior, counterintuitive weighting, overfitting.
- Polynomial order: p = 1 default, p = 2 as the robustness check, never high order. Underfitting
  biases in the other direction, and the Mixtape's cubic simulation with a true zero effect makes
  it vivid: -176,368.30 from a linear fit and 61,866.33 from a quadratic against 1.14 from the
  cubic. Curvature is handled by narrowing the window, since the MSE-optimal bandwidth shrinks as
  curvature rises. h_MSE also grows with p, so the p = 2 check runs on a wider window and a
  different effective sample. In the Mixtape's Table 6.8 the left bandwidth goes 0.020, 0.033,
  0.038 and the effective N 13,794, 16,774, 17,545 as the fit goes from no polynomial term to BAC
  to BAC and BAC-squared. When p = 2 moves the estimate, check the window.
- Covariates are for precision only; they cannot restore identification of the canonical RD
  parameter, and adjusting an invalid design changes the parameter rather than rescuing it. The
  point estimate should barely move when covariates enter; a large move signals imbalance.

## The local-randomization recipe

Select the window by nested covariate-balance tests, then difference in means inside it, with
Fisherian randomization inference when the window holds few observations (exact under the sharp
null) and Neyman or super-population inference when it is well populated. Window-selection
mechanics, thresholds, and what a narrow window does to power: references/details.md.

## Fuzzy designs: the IV discipline applies

The fuzzy estimand is a complier average effect at the cutoff under relevance, exclusion, and
monotonicity, so the iv skill's habits transfer:

- Test the first stage inside the bandwidth or window, never on the full sample; the full-sample
  F overstates strength. The guide's contrast is the anchor: F around 698 in the valid design
  against F = 1.51 in the failed one, where the first-stage effect is 0.15 with a Fisherian
  p-value of 0.32. An in-bandwidth first-stage F that is neither the strong nor the hopeless
  extreme goes to the iv skill's ladder: read it against the F targets there and report
  Anderson-Rubin/CLR intervals rather than the 2SLS t.
- Argue exclusion qualitatively and concretely: it fails if crossing the cutoff changes behavior
  through anything other than treatment (a low churn score triggering a retention call AND a
  flag another team acts on).
- Monotonicity: safe when crossing the threshold moves treatment in one direction only; suspect
  when overrides run in both directions (the failed-design pattern above, reps contacting
  below-threshold leads while managers grant early crossings, is exactly the defiers case);
  one-sided noncompliance buys it for free.
- Run fuzzy-ratio balance tests: instrument strength amplifies covariate bias, so imbalance
  invisible to ITT balance can surface in the ratio.
- Use one MSE-optimal bandwidth for the ratio, not separate ones for numerator and denominator.

## Falsification battery

Run them in this order. Each check's bandwidth convention and what its failure means are in
references/details.md.

1. Qualitative manipulation account, written before estimation (who computes the score, who
   knows the cutoff).
2. Density continuity test (rddensity, robust bias-corrected) plus the exact binomial count test
   in small windows. A discontinuous density demands an explanation, and the sorting behind it
   can be administrative rather than strategic.
3. Heaping: plot the raw histogram of the score at its finest granularity before any formal
   test. The density test can pass while heaping biases the estimate, so run the donut whatever
   the density test says (Almond et al. 2010; Barreca et al. 2011, 2016).
4. Covariate and placebo-outcome balance: the full RD machinery with each predetermined
   covariate as the outcome, a fresh MSE-optimal bandwidth per covariate, robust p-values. A
   failure on a covariate that plausibly drives the outcome invalidates the design, and the
   verdict is to walk away rather than to adjust.
5. Placebo cutoffs, one side of the true cutoff at a time so treatment effects do not
   contaminate the placebo.
6. Donut hole: drop the observations at and immediately adjacent to the cutoff, keep the
   original bandwidth, re-estimate. The donut estimate is a different parameter, local to a
   wider neighborhood, and the write-up should describe it as one.
7. Bandwidth and window sensitivity: instability at or below the chosen bandwidth is the warning
   sign, failure far above it is expected by construction.

When a null matters, report minimum detectable effects (rdpower), never ex-post power from the
observed effect.

## The live dispute, carried honestly

Robust bias correction (this canon's school) vs honest uniform-in-bias inference
(Armstrong-Kolesar, Imbens-Wager; R package RDHonest). The honest school bounds the second
derivative by a constant M and gets uniformly valid intervals; the canon's objection is that a
data-driven M destroys the uniformity that motivates the method, and a manual M is equivalent to
choosing the bandwidth by hand. Default here: RBC. When a referee or coauthor asks for honest
intervals, report RDHonest alongside with the M choice justified in text, and cite both sides.

## Extensions, briefly

- Kink designs: same machinery on first derivatives; identification is more delicate.
- Multiple cutoffs or scores (tiered loyalty programs; geographic borders such as DMA
  boundaries): cutoff-specific effects or normalize-and-pool (rdmulti), with the pooled
  estimand's interpretation checked.
- RD in time: hard to justify as standard RD; the local-randomization framework is the
  adaptation when it works at all. Prefer did or synthetic-control for policy-date designs.
- Extrapolation beyond the cutoff LATE needs added assumptions, and the menu is in
  references/details.md. Say which one when claiming anything away from the cutoff. Absent one,
  the methods paragraph says the estimate is local to the cutoff, full stop.

## R implementation

The complete runnable pipeline is scripts/rdd_template.R (estimation in both frameworks, fuzzy
diagnostics, the full falsification battery, power/MDE), with every call verified against the
rdpackages suite. The core:

```r
library(rdrobust); library(rddensity); library(rdlocrand)
rdplot(y, x, c = cutoff)                      # anatomy first
summary(rdrobust(y, x, c = cutoff))           # sharp: local linear, triangular, MSE-h, RBC
summary(rdrobust(d, x, c = cutoff))           # first stage / ITT on take-up
summary(rdrobust(y, x, c = cutoff, fuzzy = d))# fuzzy ratio
summary(rddensity(x, c = cutoff))             # manipulation
w <- rdwinselect(x, Z, c = cutoff)            # local-randomization window
rdrandinf(y, x, cutoff = cutoff, wl = w$w_left, wr = w$w_right)
```

Four figures carry a credible RD: the density of the score, take-up against the score, covariate
balance, and the outcome in bin means. If you cannot see the effect in the bin means you are
underpowered or it is not there. Report the estimate against the mean of the dependent variable,
so a small coefficient on a large base reads as a precise null (0.6 points on an 84.6 percent
base, in the Mixtape's balance table).

Package index with versions and links in references/details.md. Stata and Python mirrors of the
whole suite live at rdpackages.github.io; the guide ships full replication code in all three.

## Methods paragraph template

> Treatment assignment changes discontinuously at [cutoff] in [score], a rule set by
> [institution] before the outcomes we study, and units [cannot / can only imprecisely] control
> their score near it. We estimate the RD effect with local linear regression, a triangular
> kernel, and an MSE-optimal bandwidth, and report robust bias-corrected confidence intervals
> (Calonico, Cattaneo, and Titiunik 2014; Cattaneo and Titiunik 2022). We validate the design
> with the Cattaneo-Jansson-Ma density test and an exact binomial test, covariate balance at the
> cutoff with per-covariate bandwidths, placebo cutoffs, donut-hole estimates, and bandwidth
> sensitivity [and, for the fuzzy design, verify first-stage strength within the estimation
> bandwidth and report intention-to-treat effects alongside the complier estimate]. The estimate
> is local to the cutoff; a limitation of this design is that it does not identify effects for
> [units far from the threshold], and I extrapolate only [not at all / under the stated
> assumption], which costs [generalizability across the score distribution].

Every claim traces to references/canon.md; keys live in ../causal-design/references/causal.bib.

## Handoffs

- causal-design: whether an RD exists at all; where to go when the design gate fails.
- iv: the fuzzy branch's in-bandwidth first stage and exclusion argument live here;
  weak-instrument inference (the F ladder, AR/CLR intervals) lives in iv, along with
  many-instrument and shift-share logic.
- did / synthetic-control: policy-date designs masquerading as RD in time.
- preregister: pre-specifying an RD on an upcoming threshold change.
