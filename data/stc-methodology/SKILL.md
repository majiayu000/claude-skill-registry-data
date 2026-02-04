---
name: stc-methodology
description: Deep methodology knowledge for STC including outcome regression approach, effect modifier selection, covariate centering, and comparison with MAIC. Use when conducting or reviewing STC analyses.
---

# STC Methodology

Comprehensive methodological guidance for conducting rigorous Simulated Treatment Comparisons following NICE DSU TSD 18.

## When to Use This Skill

- Deciding between STC and MAIC
- Selecting effect modifiers for STC model
- Understanding the covariate centering approach
- Implementing Bayesian STC
- Reviewing STC code or results

## Fundamental Concept

### Outcome Regression vs Propensity Weighting

**STC Approach**:
- Fit outcome regression model in IPD
- Include treatment and treatment-covariate interactions
- Predict treatment effect at external population covariate values
- Model-based adjustment for population differences

**MAIC Approach**:
- Reweight IPD to match external population
- Analyze weighted data as if from external population
- Design-based adjustment

### Key Equation (Binary Outcome)

```
logit(P(Y=1)) = β₀ + β_trt × Treatment + β_X × X + β_trt:X × Treatment × X

Where:
- β_trt: Treatment effect when X = 0
- β_X: Effect of covariate X on outcome
- β_trt:X: Treatment-covariate interaction (effect modification)

For anchored STC:
1. Center X on external population mean: X_centered = X - X_external
2. Fit model with centered X
3. β_trt now represents treatment effect at external population values
```

## Assumptions

### Conditional Constancy of Relative Effects

Same as MAIC:
- Relative treatment effect is constant across populations after adjusting for effect modifiers
- Requires all effect modifiers included in model

### Model Specification

**Additional assumption vs MAIC**:
- Outcome model must be correctly specified
- Includes functional form of covariate effects
- Includes correct interactions

```
Trade-off:
├── If model correct → STC more efficient than MAIC
├── If model wrong → STC may be biased
└── MAIC doesn't require outcome model specification
```

## Effect Modifier Selection

### What is an Effect Modifier?

A covariate that interacts with treatment effect:
- Treatment effect differs at different covariate values
- Shows significant treatment × covariate interaction
- Has biological plausibility for interaction

### Selection Strategy

```
Effect Modifier Identification:
├── 1. Clinical/Biological Rationale
│   - Published literature on effect modification
│   - Mechanism of action considerations
│   - Expert clinical input
│
├── 2. Statistical Evidence (from IPD)
│   - Interaction terms in regression
│   - Subgroup analyses
│   - Use α = 0.10 (underpowered for interactions)
│
├── 3. Availability in AgD
│   - Must have summary statistics
│   - Means for continuous, proportions for binary
│
└── 4. Imbalance Between Populations
    - Focus on covariates that differ
    - Balanced covariates less important
```

### Using identify_effect_modifiers()

```r
em_result <- identify_effect_modifiers(
  data = ipd_data,
  outcome_var = "response",
  treatment_var = "treatment",
  candidate_covariates = c("age", "sex", "biomarker", "stage"),
  alpha = 0.10
)

# Returns:
# - Interaction p-values
# - Interaction coefficients
# - Recommended effect modifiers
```

## Covariate Centering

### Why Center Covariates?

```
Without centering (X = raw values):
- β_trt = treatment effect when ALL covariates = 0
- This may be meaningless (e.g., age = 0)

With centering (X_centered = X - X_external):
- β_trt = treatment effect when X = X_external
- This is the effect in external trial population
- Exactly what we need for ITC
```

### Centering Process

```r
# For continuous covariate
age_centered <- age - agd_mean_age

# For binary covariate
male_centered <- male - agd_prop_male

# Result: mean of centered covariate = (IPD mean - AgD mean)
# When evaluated at X_centered = 0, we get AgD population
```

### Including vs Excluding Main Effects

**With interactions**:
```r
# Model: Y ~ treatment + X_centered + treatment:X_centered
# β_trt: effect at X = X_external
# β_trt:X: how effect changes with X
```

**Main effects typically included** even if not "significant":
- Required for proper interpretation of interactions
- Follows statistical best practice
- Model hierarchically well-formulated

## Anchored vs Unanchored STC

### Anchored STC

```
Setup:
- IPD trial: A vs Common (C)
- AgD trial: B vs Common (C)

Steps:
1. Center covariates on AgD population
2. Fit: logit(Y) ~ Treatment + X_centered + Treatment:X_centered
3. Extract β_A (A vs C at AgD population)
4. Calculate d_BC from AgD (B vs C)
5. Indirect: d_AB = β_A - d_BC
```

### Unanchored STC

```
Setup:
- IPD trial: Treatment A only (or A vs something)
- AgD: Single-arm Treatment B

Caution: Same issues as unanchored MAIC
- Must adjust for ALL prognostic factors
- Assumes absolute effects transportable
- Strong assumptions - use as sensitivity only
```

## STC vs MAIC Comparison

### Theoretical Comparison

| Aspect | STC | MAIC |
|--------|-----|------|
| Method | Outcome regression | Propensity weighting |
| Efficiency | Higher (if model correct) | Lower (ESS reduction) |
| Model dependence | Higher | Lower |
| Continuous covariates | Natural | May need categorization |
| Extrapolation | Possible (with caution) | Limited to overlap |
| Diagnostic | Model fit, residuals | ESS, weight distribution |

### When to Prefer STC

- Model specification confidence is high
- Continuous covariates to adjust for
- Want to leverage regression framework
- MAIC gives very low ESS
- Interested in Bayesian framework

### When to Prefer MAIC

- Uncertain about outcome model
- Want design-based approach
- Good overlap in covariate distributions
- Acceptable ESS achieved

### Best Practice: Both as Sensitivity

```r
# Run both methods
stc_result <- anchored_stc_binary(...)
maic_result <- maic_anchored(...)

# Compare results
# If similar: increased confidence
# If different: investigate why
```

## Bayesian STC

### Advantages

- Natural uncertainty quantification
- Prior information incorporation
- Posterior predictive checks
- Sensitivity to prior specification

### Prior Selection

```r
# Treatment effect prior
prior_normal(0, 10)  # Weakly informative

# Covariate effects
prior_normal(0, 5)

# Interactions (typically smaller)
prior_normal(0, 2)

# Sensitivity analysis with different priors
```

### Implementation

```r
bayes_result <- bayesian_anchored_stc_binary(
  ipd_data = ipd,
  agd_data = agd,
  outcome_var = "response",
  treatment_var = "treatment",
  covariates = c("age", "sex"),
  priors = list(
    treatment = prior_normal(0, 10),
    covariates = prior_normal(0, 5),
    interactions = prior_normal(0, 2)
  ),
  n_iter = 10000,
  n_warmup = 2000,
  seed = 12345
)
```

## Reporting Requirements

### Methods
- [ ] Justification for STC (vs MAIC, vs nothing)
- [ ] Effect modifier selection process
- [ ] Covariates included with rationale
- [ ] Model specification (link function, interactions)
- [ ] Centering approach explained
- [ ] Frequentist vs Bayesian justification
- [ ] Prior specification (if Bayesian)

### Results
- [ ] Model coefficients with CIs
- [ ] Treatment effect at external population
- [ ] Comparison with unadjusted estimate
- [ ] Model diagnostics
- [ ] Sensitivity analyses (including vs MAIC)

## Common Pitfalls

### 1. Forgetting to Center Covariates
- Treatment coefficient won't have correct interpretation
- Will estimate effect at covariate = 0, not external population

### 2. Omitting Interactions
- Defeats purpose of STC
- Must include treatment × covariate interactions

### 3. Including Too Many Covariates
- Model overfitting
- Unstable estimates
- Focus on effect modifiers only

### 4. Ignoring Model Diagnostics
- Check residuals
- Assess model fit
- Validate assumptions (linearity, etc.)

### 5. Not Comparing to MAIC
- Both methods should give similar answers
- Differences indicate model issues
- Always run as sensitivity

## Quick Reference Code

```r
library(stc)

# 1. Identify effect modifiers
em <- identify_effect_modifiers(
  data = ipd,
  outcome_var = "response",
  treatment_var = "treatment",
  candidate_covariates = c("age", "sex", "biomarker"),
  alpha = 0.10
)

# 2. Run anchored STC (frequentist)
result <- anchored_stc_binary(
  ipd_data = ipd,
  agd_data = list(
    n_total_A = 150, n_total_C = 150,
    n_events_A = 45, n_events_C = 60,
    covariates = list(
      age = list(mean = 62),
      sex = list(prop = 0.55)
    )
  ),
  outcome_var = "response",
  treatment_var = "treatment",
  covariates = c("age", "sex"),
  reference_arm = "A",
  include_interactions = TRUE,
  robust_se = TRUE
)

# 3. View results
print(result)
summary(result)

# 4. Access specific effects
result$treatment_effect_BC  # Indirect comparison
result$treatment_effect_AB  # Direct from IPD
result$treatment_effect_AC  # From AgD

# 5. Bayesian sensitivity
bayes_result <- bayesian_anchored_stc_binary(
  ...,
  priors = list(
    treatment = prior_normal(0, 10)
  )
)
```

## Resources

- NICE DSU TSD 18: Population-adjusted indirect comparisons
- Phillippo et al. (2018): Methods for STC
- Ishak et al. (2015): Simulation studies
- stc package documentation
