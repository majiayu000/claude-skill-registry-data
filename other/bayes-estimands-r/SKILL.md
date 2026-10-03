---
name: bayes-estimands-r
description: >-
  Define and estimate the quantity a Bayesian analysis is actually about, rather than reading
  it off a coefficient table. Covers stating the estimand before the model, the difference
  between sample and population average treatment effects,
  poststratifying posterior draws to a target population, computing causal contrasts by
  simulating each counterfactual assignment, direct and indirect effects through a mediator,
  and checking whether a model expansion has inflated the uncertainty of the estimand while
  coefficients still look stable. Use when a Bayesian model is fitted or planned and the
  question concerns a treatment or exposure effect; when results must generalise beyond the
  sample; when posterior estimates from a survey sample must represent a target population
  whose composition differs from the sample; when a mediator sits between exposure and
  outcome; or when asked what a brms coefficient means on the response scale. For fitting
  and checking the model itself, use bayes-workflow-r.
license: MIT
compatibility: Requires R with brms, marginaleffects and a working Stan toolchain (cmdstanr recommended).
metadata:
  author: Chris Moreh
  version: "0.1.0"
  repository: https://github.com/CGMoreh/bayes-workflow-r
---

# Estimands, generalisation and causal contrasts

A causal effect is not a coefficient. It is a comparison between what would happen under one
assignment and what would happen under another, averaged over some population you have to
name. Two generalisations are involved, and confusing them is the most common failure in
applied work: from the sample you have to the population you care about, and from the control
condition to the treatment condition.

Once that is stated properly, the estimation strategy follows. You do not need a closed-form
expression for the effect. You simulate the outcome under each assignment from every posterior
draw, take the difference, and average it over whichever population the claim is about. That
works for any model brms can fit, linear or not, with or without interactions and mediators.

## Say what the estimand is before fitting anything

Four questions, answered in writing:

1. **What contrast?** Treated against untreated, a one-unit change, a change from the 25th to
   the 75th percentile, presence against absence.
2. **Over what population?** The sample as observed, a target population with a different
   composition, or a subgroup.
3. **On what scale?** A probability difference, a risk ratio, an expected count, a latent-scale
   coefficient. The last of these is almost never what a reader wants.
4. **Total or direct?** If a mediator sits in the middle, which path is the claim about?

Write the answers into the workflow log. Most disagreements in review about a causal claim turn
out to be disagreements about one of these four, and they are much cheaper to settle before the
model is fitted.

## The sample is not the population

The distinction matters whenever the effect varies with a covariate whose distribution differs
between sample and target. With an interaction present, the average effect over the sample and
the average effect over the population are different numbers, and neither is wrong – they answer
different questions.

```r
library(brms)
library(marginaleffects)
library(dplyr)

fit <- brm(y ~ x * z, data = d, family = gaussian(),
           prior = priors, seed = 20260826, backend = "cmdstanr",
           file = "model-data/m_effect", file_refit = "on_change")

# the average effect over the sample as observed
avg_comparisons(fit, variables = "z")

# the average effect over a target population with a different composition
pop <- tibble(x = rnorm(5000, mean = 6, sd = 2), z = 0)
avg_comparisons(fit, variables = "z", newdata = pop)
```

How much this matters is best seen on real data. `MatchIt::lalonde` holds 185 participants in
the National Supported Work demonstration pooled with 429 comparison cases drawn from the Panel
Study of Income Dynamics – not a randomised trial, and the dataset economists reach for
precisely to show how fragile adjustment against a non-experimental comparison group is. The
raw treated-minus-control difference in 1978 earnings is −$635.

The specification, stated in full because this skill's whole argument is that it must be:

```r
d <- lalonde |>
  mutate(re78k = re78 / 1000, re74k = re74 / 1000,
         age_z = as.numeric(scale(age)), educ_z = as.numeric(scale(educ)))

fit <- brm(re78k ~ treat * age_z + educ_z + re74k + race + married,
           data = d, family = gaussian(), seed = 1, backend = "cmdstanr")
```

The outcome is in thousands of dollars. On that fit:

| Estimand | Effect | 95% interval |
|---|---:|---|
| Sample average, as observed | $1,730 | [232, 3,220] |
| Population one SD younger | $681 | [−1,280, 2,620] |
| Population one SD older | $2,800 | [373, 5,070] |

One fitted model, three answers. For the sample the estimated effect is credibly positive; for a
younger target population it cannot be distinguished from nothing; for an older one it is about
four times the younger estimate. Nothing about the model changed – only the population the
question is about.

**Read those as estimands, not as findings about the programme.** Whether any of them identifies
a causal effect depends on whether the covariates above close every backdoor path between a
training programme and a PSID comparison sample, which is exactly the claim this dataset is used
to cast doubt on. The sample-against-population point does not depend on the causal reading and
survives without it.

Note also that the treatment coefficient on this fit is 1.740, matching the sample average
almost exactly. That is not a general fact: it holds because age was centred before being
interacted, so the coefficient is the effect at the mean age. Shift the covariate or add a
second interaction and the coefficient stops being any of the three quantities above.

Both quantities carry full posterior uncertainty, because the averaging happens inside each
draw rather than after summarising. That is what makes this preferable to computing an effect
from posterior means.

```markdown
| Estimand                    | Effect | 95% interval      |
|-----------------------------|-------:|-------------------|
| Sample average, as observed | $1,730 | [232, 3,220]      |
| Population one SD younger   |   $681 | [−1,280, 2,620]   |
| Population one SD older     | $2,800 | [373, 5,070]      |

: Estimated effect of training on 1978 earnings by target population. MatchIt::lalonde,
185 NSW participants pooled with 429 PSID comparison cases; outcome in thousands of dollars;
model re78k ~ treat * age_z + educ_z + re74k + race + married, seed 1.
```

## Poststratification when the population is a table

Survey work usually has a target population described by cell counts rather than by a
distribution: age by education by sex, with a known population size in each cell. Build the
poststratification frame, predict into it, and average the draws weighted by cell size.

See `reference/poststratification.md` for the full procedure, including how to get uncertainty
right and what to do when some cells are empty in the sample.

## Effects that are not a single contrast

`avg_comparisons()` covers most cases, and its `variables` argument takes the contrast
specification directly. `reference/contrasts.md` is the full cookbook – differences against
ratios, subgroup effects and the contrast-of-contrasts that tests whether they differ, the
`re_formula` decision, and getting draws out for plotting; the short version:

```r
avg_comparisons(fit, variables = list(x = c(25, 75)))        # between two values
avg_comparisons(fit, variables = list(x = "sd"))             # a one-SD change
avg_comparisons(fit, variables = "z", by = "region")         # effect within subgroups
avg_comparisons(fit, variables = "z", type = "response")     # on the probability scale
```

For anything more structured – a mediator, an intervention that changes several variables at
once, an effect unfolding over time – build the counterfactual predictions yourself and
difference them. See `reference/mediation.md`.

## Expansion is judged on the estimand, not the coefficients

Adding a flexible term often leaves the coefficient table looking fine while the estimand's
posterior spreads out, because the new coefficient is correlated with the estimand. This is not
a pathology to be avoided; it is the model correctly reporting that the data cannot pin the
effect down once the functional form is allowed to vary. But it has to be noticed.

```r
library(tidybayes)
library(ggplot2)

est_draws <- avg_comparisons(fit_expanded, variables = "z") |> get_draws()

fit_expanded |>
  spread_draws(`b_x2:z`) |>
  bind_cols(estimand = est_draws$draw) |>
  ggplot(aes(x = `b_x2:z`, y = estimand)) +
  geom_point(alpha = 0.1) +
  labs(x = "Quadratic interaction coefficient", y = "Average treatment effect")
```

A tight relationship says the uncertainty in the number you are reporting now lives in a term
you added for flexibility rather than for substance, and it is a good argument for putting an
informative prior on that term instead of leaving it free.

## Causal structure, briefly

This skill takes the estimand as given and estimates it. Deciding *which* variables to condition
on is a separate problem, solved by reasoning about the causal structure with a graph, and there
are good tools for it: `dagitty` and `ggdag` in R, and several skills that cover them. If you
have one, use it first and come back here with the adjustment set decided.

Three points that bear directly on estimation, though:

- **Conditioning on a post-treatment variable destroys the total effect.** If the goal is the
  total effect, the mediator does not go in the model. If it does go in, what comes out is a
  direct effect, and it must be reported as one.
- **Adjustment identifies a contrast; it does not create one.** Once the adjustment set is in
  the model, the effect still has to be computed as a contrast over a named population. The
  coefficient on the exposure is that contrast only in a linear model with no interactions.
- **Simulation handles structure that formulas cannot.** Spillovers, interference between units,
  treatments applied to several variables at once, and effects that accumulate over time all
  break the simple contrast. They do not break the simulate-and-difference approach, which just
  needs the simulation to respect the structure.

## Reference files

| File | Load it when |
|---|---|
| `reference/contrasts.md` | Turning draws into reportable quantities with marginaleffects: differences, ratios, subgroup contrasts and their differences, scales, weights, draws for plotting |
| `reference/poststratification.md` | The target population is a table of cells with known sizes; survey weighting; multilevel regression and poststratification |
| `reference/mediation.md` | A mediator sits between exposure and outcome; direct and indirect effects; interventions on several variables |

---

Source: Gelman, Vehtari, McElreath et al., *Bayesian Workflow* (CRC Press, 2026), chapter 7,
which frames causal inference as generalisation and works the sample-against-population
distinction through in Stan. The brms and marginaleffects translations here are original; no
text, code or data from the book is reproduced. See `skills/bayes-workflow-r/reference/book-map.md`
in this plugin for chapter and case-study pointers.
