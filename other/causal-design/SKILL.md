---
name: causal-design
description: Triage a causal question to the identification strategy the data can support, then hand off to the owning method skill. Owns the selection-on-observables branch (overlap, doubly robust estimation, double ML, causal forests, policy learning, sensitivity analysis), plain panel fixed effects, and the inference rules shared across designs (clustering, multiplicity, interference routing). TRIGGER on "identification strategy", "which causal method", "research design", "endogeneity", "quasi-experiment", "natural experiment", "selection on observables", "unconfoundedness", "propensity score", "doubly robust", "double machine learning", "causal forest", "policy learning", "sensitivity analysis", "Oster bounds", "overlap", "panel fixed effects", "strict exogeneity", "surrogate index", "mediation", or "how do I estimate the effect of X on Y" with no design chosen yet. Once a design is named, its method skill owns it.
---

# Causal design triage

The router of the family, grounded in a read canon of four sources
(references/canon.md, current as of 2026-08-05): Imbens (2024) supplies the assumption axis
(what licenses identification), Li, Luo, and Pattabhiramaiah (2024, hereafter AMA) the
marketing data-shape axis (how many treated units, how many pre-periods, how rich the
covariates), Feder et al. (2022) the text-role axis (which role unstructured data plays
in the graph), and Abadie, Athey, Imbens, and Wooldridge (2023) the clustering rules the
family shares. The deliverable is a design
recommendation carrying four things: the assumption that licenses it, the estimand it
actually identifies WITH its subpopulation named, the handoff to the owning skill, and, for
the one branch no method skill owns (selection on observables), estimation code and a methods
paragraph. Marketing's framing throughout: randomization is the gold standard, and
quasi-experimental work substitutes statistical rigor for design rigor (AMA); a design that
fails its gate is a verdict, not an obstacle.

Refresh path: run litreview on quasi-experimental methods in marketing since the canon date,
then propose additions to references/canon.md as flagged addenda.

## The triage: four questions in order

1. Was assignment randomized, or as good as (lottery, randomized rollout)? Yes:
   field-experiment. Two cautions at this gate: naive sample means from adaptive/bandit
   experiments are biased (the arm that looked worse early is truncated; Imbens), and
   suspected interference changes the DESIGN, not just the analysis (routing below). One
   sub-route: profile experiments randomizing multiple attributes within alternatives
   (conjoint, fully randomized factorial vignettes) go to conjoint, which owns the
   per-component estimand family and its correction layers.
2. If observational: is unconfoundedness defensible with PRETREATMENT covariates only? The
   conditioning set may contain only non-descendants of treatment and outcome, normally
   justified by temporal precedence. Verbatim, because it is the highest-frequency error
   (Imbens 2024): "In practice, using variables causally affected by the treatment or
   outcome is the most common mistake in choosing variables to condition on in estimating
   average treatment effects using unconfoundedness approaches." The marketing case where
   yes is credible: the targeting rule is known and observable (a campaign targeted on
   demographics or behavior selects on observables by construction; AMA). Tiebreak: a
   known DETERMINISTIC rule (treatment jumps at a cutoff on an observed score) is the rdd
   case, question 3, not this branch; the observables branch needs probabilistic
   assignment, since a deterministic rule makes every propensity 0 or 1 and leaves no
   overlap to estimate on. Yes: the selection-on-observables branch below, owned by this
   skill.
3. If unconfoundedness is not plausible, look for structure in assignment:
   - An incentive or cost shifter moves treatment with no direct path to the outcome: iv.
     It identifies the LATE for compliers only; the ATE needs substantially stronger
     assumptions, and the complier population is the focus because it is the only one
     identifiable (Imbens).
   - Cases are routed to decision-makers who differ in strictness (judges, patent examiners,
     assessors, loan officers, reviewers) and the routing is as good as random within a
     stratum: iv, which owns the leniency design. The decision-maker identity is the
     instrument, 2SLS on it is biased, and the estimator is UJIVE.
   - Treatment switches at a threshold on a running variable: rdd (fuzzy RD is IV at the
     cutoff).
   - Treatment switches on over time for some units with untreated comparisons: the panel
     branch below, routed by data shape between did and synthetic-control.
   - Treatment switches on and off within unit, with no untreated comparisons and no
     adoption date: plain panel fixed effects, the section below.
   - No structure at all: bounds and sensitivity analysis (the ladder below), or advise
     against the causal claim. Estimate under the best defensible conditioning anyway and
     report how much calibrated confounding overturns it, or report Manski bounds alone;
     the sensitivity report, not the point estimate, is the deliverable.
   - Marketing's regression-based endogeneity corrections (control functions, Gaussian
     copulas; the third leaf of the AMA figure) sit outside this family's coverage: the iv
     skill's exclusion and relevance discipline is the nearest relative, and copula
     identification rests on distributional assumptions that need their own defense.
4. Does unstructured data (text, image, audio, video) appear anywhere in the graph, and in
   which role: confounder, outcome, treatment, or machine-coded measurement?
   The role warnings below apply, and the measurement it rests on is settled before the
   estimate, not after. Discovering an unknown concept, or measuring one from a model's
   internals, is a measurement problem with its own validity argument. Intervening on a
   model's internals to build stimuli or model-respondents is instrument practice, and the
   design around it still routes through the questions above.

## The panel branch: routing by data shape

The AMA heuristic: DiD/SC-family methods match on outcomes (pretreatment paths),
propensity-family methods match on covariates; pick the branch by which matching the data
supports. Within outcomes-matching, crossed with the Arkhangelsky-Imbens (2024) three-axis
taxonomy (data type, frame shape, assignment mechanism; did skill):

- Many treated units, parallel trends plausible (only its pretreatment shadow is testable;
  did owns the statement of which variant is imposed): did. Same-time adoption: TWFE is
  fine; staggered: Callaway-Sant'Anna, Sun-Abraham, or stacked regression (whose implicit
  weights carry a caveat in did), and justify the clean controls (AMA).
- One or few treated aggregate units, long pre-period: synthetic-control (few treated
  CLUSTERS of micro units with plausible parallel trends stay in did on its few-clusters
  map). The AMA gate, both parts: plot treated vs fitted counterfactual and verify
  pretreatment fit, AND run a backdating exercise; "only using the methods that satisfy
  both best practices." Both parts are necessary, never sufficient: backdating assumes
  strict exogeneity and backfires under selection on recent shocks, and
  synthetic-control's fuller feasibility gate (pre-fit quality, T0 length, overfitting
  screens) controls the final verdict.
- The routing result between them: under selection on lagged outcomes with autocorrelated
  errors, DiD is inconsistent while SC is consistent (Arkhangelsky-Hirshberg, via the
  panel survey, Arkhangelsky and Imbens 2024). The DiD-to-SC-to-SDID decision path lives
  in did and synthetic-control.
- Data-shape fan-out when neither default fits (estimator details in synthetic-control's
  extensions map): treated outcome outside the donor convex hull: augmented DiD (Li and
  Van den Bulte 2023); outcome in range but too few pre-periods for SC: forward DiD (Li
  2024); control units far fewer than pre-periods: HCW OLS (Hsiao, Ching, and Wan 2012);
  many treated units or short panels: generalized synthetic control / factor models (Xu
  2017) or matrix completion (Athey et al. 2021), with the warning that the gsynth
  parametric bootstrap yields biased CIs, subsampling or the Li-Sonnier corrections
  instead (Li and Sonnier 2023, via AMA); unit AND time reweighting wanted: synthetic DiD;
  the inference-procedure-by-data-shape rules live in synthetic-control.

## Plain panel fixed effects: no comparison group, no adoption date

The within estimator on Y_it = delta D_it + u_i + eps_it is licensed by strict exogeneity
conditional on the unit effect, E[eps_it | D_i1, ..., D_iT, u_i] = 0 for every t (Wooldridge
2010 for the unobserved-effects model and the assumption). It buys every time-invariant
confounder, observed or not, and lets D_it be arbitrarily correlated with u_i. It buys
nothing against a time-varying unobservable, feedback from past outcomes to current
treatment, or simultaneity. Feedback is what fires in marketing panels: last period's sales
set this period's promotion, last quarter's churn sets this quarter's retention spend. The
Mixtape's own 5% price premium on unprotected sex holds "under the assumption of strict
exogeneity", and the condom decision is settled inside the session alongside the price, so a
session-level shock moving both is the violation it rests on being absent. Reverse causality
and simultaneity defeat the estimator outright: Cornwell and Trumbull (1994) put crime on
police in North Carolina counties and the within estimate is 0.413 (0.027), the wrong sign
against Becker's (1968) prediction, because Y -> D was there all along. Exits: iv under
feedback or simultaneity, did when an adoption date and clean untreated or not-yet-treated
comparisons exist. The design needs within-unit variation in D and identifies no
time-invariant covariate's effect (the Mixtape's Table 8.3 shows the column of exact zeros
with (.) standard errors).

Do not add controls that are consequences of the treatment, which is what makes columns 3 and 4
of the Mixtape's Table 8.2 inadmissible here (references/details.md for the argument, the
constant-effects scope it assumes, and the estimators that stay out).

```r
library(fixest)                     # panel: one row per unit-period, unit = the panel id
## Within-variation check first: units with no variation in d contribute nothing to the
## within estimate and every FE routine drops them silently (singletons return NA here).
nv <- tapply(panel$d, panel$unit, function(z) var(z, na.rm = TRUE))
c(no_within_variation = sum(is.na(nv) | nv == 0), units = length(nv))
pols   <- feols(y ~ d, data = panel, cluster = ~unit)   # u_i left in the composite error
within <- feols(y ~ d | unit, data = panel, cluster = ~unit)
etable(pols, within)                # side by side: the gap is the unit effects at work, and
                                    # no time-invariant covariate enters the within column.
## Stata FE standard errors instead (argument-name trap in references/details.md):
# estimatr::lm_robust(y ~ d, data = panel, fixed_effects = ~unit, clusters = unit,
#                     se_type = "stata")
```

## Selection on observables (the branch this skill owns)

- Overlap before estimation, always: estimate the propensity score and look at its
  distribution by arm. Violations move the ESTIMAND, not just the estimator: trim with the
  variance-minimizing rule of Crump et al. (2009) (the 0.1/0.9 rule of thumb is its common
  approximation) and report the retained population, or switch to overlap weights
  e(x)(1-e(x)) (Li, Morgan, and Zaslavsky 2018), which target the population that could
  plausibly receive either treatment.
- Estimator default: doubly robust (AIPW; Bang and Robins 2005), "the most attractive" under
  unconfoundedness with many covariates (Imbens): consistent if either the outcome model
  or the propensity model is consistent, tolerates ML-rate nuisance estimation. In
  practice: grf's causal forest with its built-in AIPW average effect, or double ML
  (Chernozhukov et al. 2018) when you want explicit nuisance control. Plain regression or
  matching are acceptable in low dimensions, with two caveats: fixed-number-of-matches
  matching is never fully efficient and its bias does not vanish with many covariates
  (Imbens), and marketing has moved off propensity score matching for its sensitivity to
  parametric assumptions (AMA).
- Weight by the ESTIMATED propensity score even when the true one is known; the true score
  is inefficient (Hirano, Imbens, and Ridder 2003).
- Heterogeneity has two different goals: describing CATEs (causal forest, Wager and Athey
  2018, honest inference without prespecified subgroups) and deciding WHO to treat, which
  is policy learning (Athey and Wager 2021; policytree), where the complexity of the
  policy class is the key choice. Do not answer a targeting question with a CATE
  map.
- Sensitivity analysis is mandatory, because unconfoundedness is untestable. The graded
  ladder (details in references/details.md): Manski bounds (assumption-free, honest,
  usually uninformative); calibrated confounder models (Rosenbaum and Rubin 1983, Imbens
  2003, with Oster 2019 and Cinelli-Hazlett 2020 as the modern reporting standards;
  sensemakr implements Cinelli-Hazlett); Rosenbaum design sensitivity (Rosenbaum 2002). An
  estimate that flips under mild confounding indicts the design, not the estimator.

## Rules shared across every design

- Estimand first, with the subpopulation named: complier, ATT, or overlap population.
- Cluster where treatment was assigned or the sample was drawn, and say which of the two.
- Multiplicity staged by cost: FDR to screen, resampling FWER to confirm, gatekeeping by stage.
- Interference routes to field-experiment by structure: clustered, network, or marketplace.
- Surrogate index for long-run outcomes, valid only if every causal path runs through it.
- Text-role warnings at handoff (Feder). Machine-coded variables get PPI first.
- Mediation has no route here. Sequential ignorability is a regime no skill carries.

Full argument: references/shared-rules.md.

## Implementation

scripts/unconfoundedness_template.R is the runnable path for the branch this skill owns
(overlap diagnostics and trimming, grf AIPW, CATE and policy learning, sensemakr
sensitivity reporting), verified against package documentation. Package index with
versions, links, and traps in references/details.md. Every other branch's code lives in
the owning skill's template.

## Methods paragraph template

> Following the taxonomy in Imbens (2024), our setting is [randomized / observational with
> a defensible unconfoundedness argument / observational with assignment structure X /
> combined]. The assignment structure that identifies the effect is [structure], which
> points to [estimator], identifying [estimand] for [subpopulation]. [Observables branch:]
> We condition on [pretreatment covariates], none causally affected by treatment or
> outcome; overlap is [assessed how, trimmed how, moving the estimand to whom]; estimation
> is doubly robust [implementation]; and we report [Cinelli-Hazlett robustness values /
> Oster's delta] against a confounder as strong as [benchmark covariate]. [Panel branch:]
> Given [T treated units, K pre-periods], we use [method] per the data-shape criteria in
> Li, Luo, and Pattabhiramaiah (2024). A limitation I accept: [the identifying assumption
> this design rests on], stated where the choice is made, with its price named.

Every claim traces to references/canon.md; keys live in references/causal.bib.

## Handoffs

- field-experiment: anything randomized, prospective experimental design, interference
  analysis, power.
- conjoint: profile experiments with multiple randomized attributes (AMCEs, marginal
  means, measurement-error and multiple-testing corrections, HB partworths and WTP).
- did: many treated units with timing variation; parallel-trends machinery; it sends
  plain-FE cases with no comparison group back to the plain panel fixed effects section.
- synthetic-control: few treated units, long pre-periods; SDID; factor models and matrix
  completion; the augmented/forward DiD and HCW conditions stated above.
- rdd: thresholds on running variables; the design gate and falsification battery.
- iv: instruments, shift-share, formula instruments, leniency and examiner designs;
  weak-instrument inference.
- Any text, image, audio, or video role in the graph carries a measurement design of its own:
  a prediction-powered correction for machine-coded variables, an internal-state adjustment
  where the confounder is latent, and the split-sample rule throughout.
- Unknown-concept discovery and model-internals measurement are instruments, and their
  validity is argued before they enter a design.
- Activation steering for stimuli and model-respondents (instrument choice, strength
  calibration, damage audits) is instrument practice; the surrounding design stays with the
  owning method skill.
- preregister: pre-analysis plans once the design is chosen (experiment-first skill;
  quasi-experimental and measurement PAPs adapt its structure).
