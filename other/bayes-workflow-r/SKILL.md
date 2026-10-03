---
name: bayes-workflow-r
description: >-
  Run a Bayesian analysis in R with brms, rstanarm or cmdstanr on Stan, as an iterative
  workflow rather than a single fit. Covers choosing priors and checking what they imply,
  prior predictive simulation, MCMC failure read as a
  modelling problem, posterior predictive checks that name the next model,
  leave-one-out model comparison with pointwise attribution,
  prior and likelihood sensitivity by power-scaling, design calibration by simulation at
  the real sample size, and what weights() in a brm() call does and does not adjust for. Use when fitting, expanding, diagnosing or
  troubleshooting a model in any of those packages; when Stan warns about divergent
  transitions, treedepth, low effective sample size or non-convergence; or when a small
  sample needs a defence against the objection that the priors drove the result and the
  evidence for that defence has to be generated. For causal estimands and target populations
  use bayes-estimands-r; for writing the analysis up use bayes-reporting-r.
license: MIT
compatibility: Requires R with brms and a working Stan toolchain (cmdstanr recommended). The
  optional steps use loo, priorsense, projpred, bayesplot, posterior, tidybayes and marginaleffects.
metadata:
  author: Chris Moreh
  version: "0.1.0"
  repository: https://github.com/CGMoreh/bayes-workflow-r
---

# Bayesian workflow in R

Fitting a model is one step inside a loop. The loop is: pick the simplest defensible model,
set priors and check what they imply, simulate from the prior, fit, diagnose the computation,
check the fit against the data, expand or compare, calibrate the design, and go round again.
A failed check is not an obstacle to be worked around. It is the most informative thing that
happens, because it names the next model.

This file routes. Every reference file below loads on demand, and none of them is needed
until the step it covers is the step you are on.

## Before the first fit

Three questions, answered in writing, before any `brm()` call:

1. **What is the quantity of interest?** A coefficient is rarely it. If the answer is a
   contrast, a predicted probability, an average effect over some population, or a
   difference between groups, say so now – it changes which checks matter and which
   sensitivity analysis is worth running. Use `bayes-estimands-r` if the quantity is causal
   or defined over a target population different from the sample.
2. **What sample size and structure are you working with?** Clustering, repeated measures
   and crossed classifications all change the model and the cross-validation scheme. Small
   samples change which checks are load-bearing.
3. **What would make you abandon this model?** Deciding in advance what a failed check
   means keeps the workflow from collapsing into fitting until something looks good.

## The loop

| Step | What it does | Detail |
|---|---|---|
| 1 | Simplest defensible model, motivated by subject knowledge rather than fit | – |
| 2 | Priors, and the check on what they jointly imply | `reference/priors.md` |
| 3 | Prior predictive simulation, before the data are used | `reference/priors.md` |
| 4 | Fit | `reference/fitting.md` |
| 5 | Diagnose the computation as a statement about the model | `reference/computation.md` |
| 6 | Posterior predictive checks, chosen to be able to fail | `reference/predictive-checks.md` |
| 7 | Prior and likelihood sensitivity by power-scaling | `reference/sensitivity.md` |
| 8 | Expand or compare, judged on the quantity of interest | `reference/comparison.md` |
| 9 | Calibrate the design by simulation at the real sample size | `reference/calibration.md` |
| 10 | Back to step 1 with what you learned | – |

The numbering is a reading order, not a schedule. Steps 5 to 8 send you back to steps 1 to 3
regularly, and that is the workflow working rather than failing.

### Spend the compute where the question is

The steps are not equally load-bearing for every question, and running all of them at full
length is not the goal. Decide from question 1 above which step answers the thing being asked,
and give that step the budget; the rest are checks on the answer and can be run at whatever
resolution is enough to pass or fail them.

This gets inverted easily, because the checks are the memorable part of a workflow and the
answer is the ordinary part. A worked example from validating these skills: an analysis whose
brief asked which predictors matter spent 130 refits on design calibration, a check, and then
ran the variable selection - the answer - at five cross-validation folds on the reasoning that
a fuller search cost more than the question was worth. The size rule came back unusable, the
fold-stability table was too noisy to read, and the analysis dropped a predictor that every
better-resourced run keeps. The diagnostics were the strongest part of that report and its
answer was the weakest, and the two facts have the same cause.

## Gates

Three claims must not be made until the corresponding check has actually been run, and the
skill should say so plainly rather than proceeding:

- **No estimate is reported before the computational diagnostics pass.** R-hat below 1.01,
  bulk and tail effective sample size above 400 per parameter of interest, no divergent
  transitions. Divergences that persist are a statement about the model's geometry, not a
  nuisance to be silenced by raising `adapt_delta` until the warning stops.
- **No prior is called weakly informative before something has checked what it implies.**
  Priors that look weak on individual coefficients can be strong on the quantity of
  interest. See `reference/priors.md`, which is the single most commonly skipped step in
  applied practice.
- **No model comparison is reported from `elpd_diff` alone.** Read it against `se_diff`,
  check the Pareto k diagnostics, and look at which observations drive the difference.
  See `reference/comparison.md`.

## Where the detail lives

| Reference file | Load it when |
|---|---|
| `reference/priors.md` | Choosing priors; prior predictive simulation; the prior implied on R² and other derived quantities; `brms::R2D2()` |
| `reference/fitting.md` | Model syntax, multilevel and repeated-measures structures, caching fits, reproducible seeds |
| `reference/families.md` | The family casebook: counts and overdispersion, hurdle against zero-inflation, ordinal models and `cs()`, bounded proportions, heavy tails, censoring and truncation, distributional models |
| `reference/computation.md` | Divergences, treedepth, low effective sample size, non-mixing chains, funnels, multimodality: symptom to cause to remedy |
| `reference/predictive-checks.md` | Posterior predictive checking; choosing summaries that can fail; interrogating the joint posterior rather than the marginals |
| `reference/sensitivity.md` | Power-scaling with `priorsense`; sensitivity of the estimand rather than of marginal coefficients; static sensitivity analysis without refitting |
| `reference/comparison.md` | LOO-CV, pointwise attribution, leave-one-group-out for clustered data, the small-sample caveats, `projpred` |
| `reference/calibration.md` | Fake-data recovery at the real sample size; simulation-based calibration |
| `reference/book-map.md` | Where each step is treated in Gelman et al. (2026), and which case study demonstrates it |

## Bundled scripts

Run these from the project root. Each is self-contained, takes a fitted `brmsfit`, and
prints a report rather than modifying anything.

| Script | Purpose |
|---|---|
| `scripts/bw_diagnose.R` | Convergence, divergences, treedepth, E-BFMI, and the triage that follows from each |
| `scripts/bw_prior_check.R` | Prior predictive simulation including the implied prior on R² and, for binary families, the implied event rate |
| `scripts/bw_sensitivity.R` | Power-scaling sensitivity for parameters and for the quantity of interest |
| `scripts/bw_loo_report.R` | `bw_loo_report()` for LOO comparison with pointwise attribution, which refuses to compare models fitted to different rows, reports `p_loo` against the parameter count, and lets the Pareto k qualify the comparison instead of printing both and leaving them unconnected; `bw_kfold_grouped()` for leave-one-group-out, which refits and is priced accordingly |
| `scripts/bw_scheme.R` | `bw_scheme()` writes `WORKFLOW.md` from the workflow log and the files beside it: where the analysis stands in the log's own words, the loop as the log walked it, and an index of entries, models and files by stage. It reads the log and the script banners and nothing else, never styles a stage by state, and quotes what comes next rather than proposing it; the parser is shared with the reporting skill's appendix scaffold |
| `scripts/bw_recovery.R` | Design calibration: can this design at this sample size recover the effect you expect? |

Each is callable from the shell on a cached fit – for example
`Rscript "${CLAUDE_SKILL_DIR}/scripts/bw_diagnose.R" model-data/m3.rds`, and
`bw_loo_report.R` takes two or more `.rds` paths – or `source()` the file and call the
function, which is the only route for `bw_recovery()` (it needs a `simulate_fn` written for
the design) and for derived-quantity sensitivity (it needs `newdata`).

## The workflow log

Keep a running `bayes-workflow-log.md` in the project. One dated entry per pass round the
loop, recording the model fitted, the check run, what it showed, and what changed as a
result. Two reasons, and the second matters more than the first: it stops the same failed
check being rediscovered three weeks later, and it *is* the raw material for the methods
section and the supplementary appendix. `bayes-reporting-r` reads it directly.

An entry is three lines, not three paragraphs:

```markdown
## 2026-08-26 – m3: added varying slopes for time by participant
Posterior predictive check on the group-level SDs failed for m2 (observed spread outside
the predictive interval). m3 fixes it; 4 divergences remain, all in the sd_ parameters.
Next: non-centred parameterisation is already brms default, so try tighter prior on sd.
```

Models named `m1`, `m2` and so on in the log, and saved as `model-data/m<n>_<label>.rds`, are
the ones the record and the appendix can join to their files. After appending an entry,
regenerate `WORKFLOW.md` with `Rscript "${CLAUDE_SKILL_DIR}/scripts/bw_scheme.R"` from the
project root and name its path once in the end-of-turn summary. The scheme indexes the log and
the files beside it; it says nothing the log does not, and it is for the person reading the
project rather than for the analysis.

## R style

Native pipe throughout, `mutate()` rather than `$<-`, `purrr` rather than loops, tidyverse
and easystats before package-specific reporting tools, `tinytable` for tables and `ggplot2`
with `patchwork` for figures. Set a seed for anything stochastic. Install with `pak::pak()`.

## Provenance

Built on the workflow set out in Gelman, Vehtari, McElreath and colleagues, *Bayesian
Workflow* (Chapman and Hall / CRC Press, 2026). The book is cited throughout and linked case
study by case study in `reference/book-map.md`; no text, code or data from the book or its
companion site is reproduced here. The R translations, the prose and the scripts are original
to this plugin, and errors in them are ours rather than the book's.
