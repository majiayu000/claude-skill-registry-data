---
name: pairwise-ma-methodology
description: Deep methodology knowledge for pairwise meta-analysis including fixed vs random effects, heterogeneity assessment, publication bias, and sensitivity analysis. Use when conducting or reviewing pairwise MA.
---

# Pairwise Meta-Analysis Methodology

Comprehensive methodological guidance for conducting rigorous pairwise meta-analysis following Cochrane and PRISMA guidelines.

## When to Use This Skill

- Planning a pairwise meta-analysis
- Choosing between fixed and random effects models
- Interpreting heterogeneity statistics
- Assessing publication bias
- Designing sensitivity analyses
- Reviewing pairwise MA code or results

## Fixed vs Random Effects

### Decision Framework

```
Are studies functionally identical?
├── Yes → Fixed-effect model appropriate
│   - Same population, intervention, comparator, outcome
│   - Estimating single "true" effect
│
└── No (usually the case) → Random-effects model
    - Studies differ in ways that affect true effect
    - Estimating mean of distribution of effects
    - More generalizable inference
```

### When to Use Fixed-Effect

- Studies are very similar (rare in practice)
- Want to estimate effect in "identical" studies
- Very few studies (< 5) - random effects unreliable
- Sensitivity analysis alongside random effects

### When to Use Random-Effects

- Studies differ in populations, settings, methods
- Want inference applicable beyond included studies
- Default choice for most meta-analyses
- Use with appropriate adjustments (Knapp-Hartung)

### Key Differences

| Aspect | Fixed-Effect | Random-Effects |
|--------|-------------|----------------|
| Assumption | Common true effect | Distribution of true effects |
| Weights | Based on precision only | Includes between-study variance |
| Small study | More weight | Less weight |
| Large study | Less relative weight | More weight |
| CI width | Narrower (if heterogeneity exists) | Wider (appropriately) |
| Inference | To identical studies | To broader population |

## Heterogeneity Assessment

### Statistics Overview

#### Q Statistic (Cochran's Q)
- Tests null hypothesis of homogeneity
- Follows chi-square distribution under null
- Low power with few studies
- Overpowered with many studies

```r
# Interpretation
Q_pvalue < 0.10  # Suggests heterogeneity (use 0.10, not 0.05)
```

#### I² (Inconsistency Index)
- Percentage of variability due to heterogeneity (vs sampling error)
- Independent of number of studies
- Has wide confidence interval with few studies

| I² Value | Interpretation |
|----------|---------------|
| 0-25% | Low heterogeneity |
| 25-50% | Moderate heterogeneity |
| 50-75% | Substantial heterogeneity |
| >75% | Considerable heterogeneity |

**Caution**: These thresholds are rules of thumb, not strict cutoffs.

#### τ² (Tau-squared)
- Absolute between-study variance
- On scale of effect measure
- Used for prediction intervals
- Compare to typical effect sizes for context

#### H²
- Relative excess heterogeneity
- H² = Q/(k-1) where k = number of studies
- H² = 1 means no heterogeneity

### Prediction Intervals

**Critical**: Always report prediction intervals alongside confidence intervals.

- CI: Uncertainty in mean effect estimate
- PI: Range where 95% of true study effects would lie

```r
# In meta package
metabin(..., prediction = TRUE)
```

If PI includes null but CI doesn't:
- Mean effect is statistically significant
- But future studies might show no effect or opposite effect
- Heterogeneity is clinically important

## Investigation of Heterogeneity

### Subgroup Analysis
```r
# Categorical moderator
update(ma_result, subgroup = risk_of_bias)

# Requirements:
# - Pre-specified in protocol
# - Limited number of subgroups
# - Biological/clinical rationale
# - Report within and between subgroup heterogeneity
```

### Meta-Regression
```r
# Continuous moderator
rma(yi, vi, mods = ~ year + sample_size, data = es_data)

# Requirements:
# - Minimum 10 studies per moderator
# - Pre-specified moderators
# - Avoid overfitting
# - Use Knapp-Hartung adjustment
# - Permutation test for multiple moderators
```

### Rule of Thumb for Investigation
- Need ≥10 studies for meaningful subgroup analysis
- Meta-regression requires even more studies
- Pre-specify investigations in protocol
- Report all investigated moderators (avoid selective reporting)

## Publication Bias Assessment

### Visual Assessment: Funnel Plot
```r
funnel(ma_result)
# Look for:
# - Asymmetry (small studies with large effects)
# - Missing studies in certain regions
# - Outliers
```

### Statistical Tests

#### Egger's Test (Continuous Outcomes)
```r
metabias(ma_result, method.bias = "linreg")
# P < 0.10 suggests asymmetry
# Low power with < 10 studies
```

#### Peters' Test (Binary Outcomes)
```r
metabias(ma_result, method.bias = "peters")
# Better for OR than Egger's
```

#### Begg's Rank Test
```r
metabias(ma_result, method.bias = "rank")
# Non-parametric alternative
# Lower power than regression tests
```

### Adjustment Methods

#### Trim-and-Fill
```r
trimfill(ma_result)
# Imputes "missing" studies
# Provides adjusted estimate
# Sensitivity analysis, not definitive correction
```

#### Selection Models
```r
# More sophisticated approaches
# Model the selection process
# Available in metafor and weightr packages
```

### Interpretation Cautions
- Asymmetry ≠ publication bias (could be true heterogeneity)
- Tests have low power with few studies
- Don't over-interpret with < 10 studies
- Multiple causes of asymmetry exist

## Sensitivity Analyses

### Essential Sensitivity Analyses

1. **Fixed vs Random Effects**
   - Report both; if results differ, investigate why

2. **Leave-One-Out**
   ```r
   metainf(ma_result)
   # Identifies influential studies
   ```

3. **Risk of Bias**
   - Exclude high risk of bias studies
   - Subgroup by risk of bias

4. **Influence Diagnostics**
   ```r
   influence(ma_result)
   # DFBETAS, Cook's distance
   ```

5. **Different Effect Measures**
   - OR vs RR vs RD for binary
   - May give different conclusions

6. **Estimation Method**
   - DerSimonian-Laird vs REML vs ML

### GOSH Analysis
```r
# Graphical display of study heterogeneity
gosh(ma_result)
# Identifies subsets with different results
```

## Reporting Checklist (PRISMA)

### Methods
- [ ] Effect measure and rationale
- [ ] Model choice (fixed/random) and rationale
- [ ] Heterogeneity measures planned
- [ ] Publication bias assessment planned
- [ ] Sensitivity analyses planned
- [ ] Software and packages used

### Results
- [ ] Number of studies and participants
- [ ] Pooled effect with CI
- [ ] Prediction interval
- [ ] Heterogeneity statistics (Q, I², τ²)
- [ ] Forest plot
- [ ] Funnel plot (if ≥10 studies)
- [ ] Publication bias test results
- [ ] Sensitivity analysis results

## Common Pitfalls

### 1. Using Q p-value to Choose Model
- Wrong: "Q p > 0.05, so use fixed-effect"
- Right: Choose based on study similarity, report both

### 2. Ignoring Prediction Intervals
- CI shows precision of mean estimate
- PI shows variability in true effects
- Both are clinically important

### 3. Over-interpreting I²
- I² has wide CI with few studies
- Context matters (clinical significance)
- Don't use arbitrary thresholds mechanically

### 4. Selective Subgroup Analysis
- Pre-specify in protocol
- Report all, not just significant ones
- Adjust for multiple testing

### 5. Publication Bias Assessment with Few Studies
- Tests unreliable with < 10 studies
- State this limitation, don't perform test

## Quick Reference Code

```r
library(meta)

# Basic random-effects MA (binary)
ma <- metabin(
  event.e, n.e, event.c, n.c,
  studlab = study,
  data = dat,
  sm = "OR",
  method = "MH",
  method.tau = "REML",
  hakn = TRUE,           # Knapp-Hartung adjustment
  prediction = TRUE      # Prediction interval
)

# Forest plot
forest(ma, sortvar = TE, prediction = TRUE)

# Funnel plot and Egger's test
funnel(ma)
metabias(ma, method.bias = "linreg")

# Influence analysis
metainf(ma)

# Subgroup analysis
update(ma, subgroup = risk_of_bias)
```

## Resources

- Cochrane Handbook: https://training.cochrane.org/handbook
- PRISMA Statement: http://www.prisma-statement.org/
- Higgins & Green: Cochrane Handbook for Systematic Reviews
- Borenstein et al.: Introduction to Meta-Analysis
