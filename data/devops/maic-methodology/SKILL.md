---
name: maic-methodology
description: Deep methodology knowledge for MAIC including assumptions, weight diagnostics, ESS interpretation, and anchored vs unanchored decisions. Use when conducting or reviewing MAIC analyses.
---

# MAIC Methodology

Comprehensive methodological guidance for conducting rigorous Matching-Adjusted Indirect Comparisons following NICE DSU TSD 18.

## When to Use This Skill

- Deciding whether to use MAIC vs other ITC methods
- Selecting covariates for matching
- Interpreting weight diagnostics and ESS
- Choosing between anchored and unanchored MAIC
- Reviewing MAIC code or results

## Fundamental Assumptions

### Key Assumption: Conditional Constancy of Relative Effects

**For Anchored MAIC**:
- The relative treatment effect (vs common comparator) is the same across populations AFTER adjusting for effect modifiers
- This is untestable - relies on clinical judgment
- Requires all effect modifiers to be included in matching

### No Unmeasured Effect Modifiers

```
Critical: MAIC assumes that adjusting for measured covariates
removes all population differences that modify treatment effects.

If there are unmeasured effect modifiers:
├── Anchored MAIC: Biased indirect comparison
└── Unanchored MAIC: Even more biased

There is NO WAY to test this assumption with available data.
```

### Unanchored MAIC: Additional Assumptions

- All prognostic factors (not just effect modifiers) must be adjusted
- Absolute treatment effects are transportable across populations
- Much stronger, often implausible assumptions
- Should be avoided if anchored is possible

## When to Use MAIC

### MAIC is Appropriate When:
1. IPD available for one trial (index trial)
2. Only AgD available for comparator trial
3. Important population differences exist between trials
4. Effect modifiers are known and measured
5. Sufficient overlap in covariate distributions

### MAIC May Not Be Best When:
- Populations are very similar → Standard ITC may suffice
- Little covariate overlap → ESS will be very low
- Effect modifiers unknown → Cannot ensure adjustment
- Connected network exists → Consider NMA first

## Covariate Selection

### Selection Criteria

```
Include covariates that are:
├── Effect modifiers (interact with treatment effect)
│   - Based on clinical evidence
│   - Biological plausibility
│   - Subgroup analyses from trials
├── Available in both trials
│   - IPD: Individual-level data
│   - AgD: Published summary statistics
└── Different between trial populations
    - Check if actually imbalanced
    - No need to match on similar values
```

### What NOT to Include
- Variables balanced between populations (wasteful)
- Pure prognostic factors in anchored MAIC (cancel out)
- Variables not reported in AgD (impossible to match)
- Too many variables (ESS concerns)

### Practical Strategy

1. **Start with clinical knowledge** - Known effect modifiers
2. **Check availability** - What's reported in AgD?
3. **Assess imbalance** - Compare IPD means to AgD targets
4. **Start conservative** - Fewer variables, check ESS
5. **Iterate** - Add variables if ESS remains acceptable

## Effective Sample Size (ESS)

### Definition
```
ESS = (Σ weights)² / Σ(weights²)

Represents the "equivalent" unweighted sample size
that would give same precision as weighted analysis.
```

### Interpretation Guidelines

| ESS (% of original) | Interpretation | Recommendation |
|--------------------|----------------|----------------|
| >70% | Good | Proceed with confidence |
| 50-70% | Acceptable | Proceed with caution |
| 30-50% | Concerning | Reconsider covariates |
| <30% | Poor | Results likely unreliable |

### Causes of Low ESS
- Many covariates included
- Large population differences
- Little overlap in distributions
- Including unnecessary covariates

### Improving ESS
1. Remove covariates balanced between populations
2. Remove covariates unlikely to be effect modifiers
3. Consider whether MAIC is feasible
4. Accept higher uncertainty in exchange for validity

## Weight Diagnostics

### Essential Checks

#### 1. ESS Calculation
```r
check_weights(weights_obj)
# Look at ESS and ESS percentage
```

#### 2. Weight Distribution
```r
# Check for extreme weights
summary(weights_obj$data$weights)
max(weights) / sum(weights)  # Single observation influence
```

#### 3. Covariate Balance
```r
# Before vs After weighting
# Should see AgD targets achieved after weighting
```

### Red Flags
- Single observation has >5% of total weight
- ESS < 30% of original
- Covariates not balanced after weighting
- Convergence issues in weight estimation

## Anchored vs Unanchored

### Anchored MAIC (Preferred)

**Scenario**:
- Index trial: Treatment A vs Common comparator (C)
- External trial: Treatment B vs Common comparator (C)
- Target: A vs B

**Methodology**:
1. Weight IPD to match external population
2. Estimate A vs C in weighted IPD
3. Extract B vs C from external AgD
4. Bucher method: (A vs C) - (B vs C) = A vs B

**Advantages**:
- Only need to adjust for effect modifiers
- Prognostic factors cancel out (appear in both arms)
- More robust to unmeasured confounding

### Unanchored MAIC (Use with Caution)

**Scenario**:
- No common comparator
- Single-arm external study
- Target: Direct comparison A vs B

**Methodology**:
1. Weight IPD to match external population
2. Estimate absolute outcome in weighted IPD (treatment A)
3. Compare directly to external outcome (treatment B)

**Critical Limitations**:
- Must adjust for ALL prognostic factors
- Assumes absolute effects transportable
- Highly susceptible to unmeasured confounding
- Should be sensitivity analysis only

### Decision Framework

```
Is there a common comparator in both trials?
├── Yes → ANCHORED MAIC (strongly preferred)
│   - Adjust for effect modifiers
│   - Bucher method for indirect comparison
│
└── No → Consider alternatives first
    ├── Can NMA with other studies provide estimate?
    ├── Can we use ML-NMR with partial network?
    └── Last resort: UNANCHORED MAIC
        - Adjust for ALL prognostic factors
        - Report with strong caveats
        - Sensitivity analysis
```

## MAIC vs STC

### When to Prefer MAIC
- Concerned about outcome model misspecification
- Covariate-outcome relationship uncertain
- Want method-of-moments balancing

### When to Prefer STC
- Outcome model well-understood
- Continuous covariates (natural handling)
- Want to use regression framework
- Higher precision if model correct

### Recommendation
- Run both as sensitivity analysis
- If results agree, more confidence
- If results differ, investigate why

## Reporting Requirements

### Methods
- [ ] Justification for MAIC over other methods
- [ ] Covariate selection rationale
- [ ] Effect modifier justification
- [ ] Anchored vs unanchored justification
- [ ] Weight estimation method
- [ ] Confidence interval method (bootstrap type)

### Results
- [ ] ESS and percentage of original
- [ ] Weight distribution summary
- [ ] Covariate balance table (before/after)
- [ ] Treatment effect with 95% CI
- [ ] Comparison to unadjusted estimate
- [ ] Sensitivity analyses

## Common Pitfalls

### 1. Including Too Many Covariates
- Reduces ESS unnecessarily
- May include non-effect modifiers
- Start minimal, justify additions

### 2. Ignoring Low ESS
- Proceeding when ESS < 30%
- Not reporting ESS prominently
- Results may be unreliable

### 3. Using Unanchored When Anchored Possible
- Much stronger assumptions
- Higher bias risk
- Always prefer anchored

### 4. Not Checking Covariate Balance
- Weights may not achieve balance
- Must verify targets achieved

### 5. Missing Sensitivity Analyses
- Different covariate sets
- Comparison with STC
- Robustness to assumptions

## Quick Reference Code

```r
library(maicplus)

# 1. Prepare targets from AgD
agd_targets <- c(
  AGE = 62.5,
  MALE = 0.55,
  ECOG1 = 0.35
)

# 2. Center IPD
ipd_centered <- center_ipd(ipd, agd_targets)

# 3. Estimate weights
weights <- estimate_weights(
  data = ipd_centered,
  centered_colnames = c("AGE_centered", "MALE_centered", "ECOG1_centered"),
  n_boot_iteration = 1000,
  set_seed_boot = 12345
)

# 4. Check weights (CRITICAL)
check_weights(weights)
# - ESS should be >50% of original
# - No extreme weights
# - Balance achieved

# 5. Run anchored MAIC
result <- maic_anchored(
  weights_object = weights,
  ipd = ipd,
  pseudo_ipd = pseudo_ipd,
  trt_ipd = "TreatmentA",
  trt_agd = "TreatmentB",
  trt_common = "Placebo",
  endpoint_type = "binary",
  eff_measure = "OR",
  boot_ci_type = "perc"
)

# 6. Report
result$inferential$summary
```

## Resources

- NICE DSU TSD 18: Population-adjusted indirect comparisons
- Signorovitch et al. (2010): Original MAIC methodology
- Phillippo et al. (2016): Methods review
- maicplus package documentation
