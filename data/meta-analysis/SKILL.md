---
name: meta-analysis
description: Use when performing meta-analysis, pooling study data, generating forest plots, funnel plots, assessing heterogeneity, or conducting subgroup and sensitivity analyses. Invoke for any statistical synthesis of multiple studies.
---

# Meta-Analysis Skill

This skill guides statistical synthesis of multiple studies using R.

## When to Use

Invoke this skill when the user:
- Asks to pool study results or combine data
- Requests forest plot or funnel plot
- Asks about heterogeneity (I², Q, tau²)
- Wants subgroup or sensitivity analysis
- Mentions "meta-analysis" or "synthesis"
- Needs publication bias assessment

## R Packages Required

```r
library(meta)      # Primary meta-analysis package
library(metafor)   # Advanced methods
library(dmetar)    # Companion functions
```

## Analysis Types

### Binary Outcomes (OR, RR, RD)

Use `metabin()` for dichotomous data:

```r
ma <- metabin(
    event.e = events_intervention,
    n.e = n_intervention,
    event.c = events_control,
    n.c = n_control,
    studlab = study_id,
    data = data,
    sm = "OR",        # "RR" for Risk Ratio, "RD" for Risk Difference
    method = "MH",    # Mantel-Haenszel
    random = TRUE,    # Random-effects model
    prediction = TRUE # Prediction interval
)
summary(ma)
```

### Continuous Outcomes (MD, SMD)

Use `metacont()` for continuous data:

```r
ma <- metacont(
    n.e = n_intervention,
    mean.e = mean_intervention,
    sd.e = sd_intervention,
    n.c = n_control,
    mean.c = mean_control,
    sd.c = sd_control,
    studlab = study_id,
    data = data,
    sm = "SMD",      # "MD" for Mean Difference
    random = TRUE
)
```

### Single-Arm Proportions

Use `metaprop()` for single-arm rates:

```r
ma <- metaprop(
    event = events,
    n = total,
    studlab = study_id,
    data = data,
    sm = "PLOGIT",   # Logit transformation
    random = TRUE
)
```

### Hazard Ratios (Time-to-Event)

Use `metagen()` for pre-calculated HRs:

```r
ma <- metagen(
    TE = log(HR),
    seTE = (log(HR_upper) - log(HR_lower)) / 3.92,
    studlab = study_id,
    data = data,
    sm = "HR",
    random = TRUE
)
```

## Forest Plot

```r
# Save to file (required for non-interactive sessions)
png("forest_plot.png", width=1200, height=800, res=150)

forest(ma,
    sortvar = TE,                    # Sort by effect size
    xlim = c(0.1, 10),              # X-axis limits for OR/RR
    at = c(0.1, 0.25, 0.5, 1, 2, 4, 10),
    leftcols = c("studlab", "n.e", "n.c"),
    leftlabs = c("Study", "n (Int)", "n (Ctrl)"),
    rightcols = c("effect", "ci"),
    rightlabs = c("OR", "95% CI"),
    prediction = TRUE                # Show prediction interval
)

dev.off()
```

## Heterogeneity Interpretation

| I² Value | Interpretation |
|----------|----------------|
| 0-25% | Low heterogeneity |
| 25-50% | Moderate heterogeneity |
| 50-75% | Substantial heterogeneity |
| >75% | Considerable heterogeneity |

Key statistics to report:
- **I²**: Percentage of variability due to heterogeneity
- **τ²**: Between-study variance (tau-squared)
- **Q**: Cochran's Q statistic and p-value
- **Prediction interval**: Range of true effects

## Subgroup Analysis

```r
# By categorical variable
update(ma, subgroup = study_design, tau.common = FALSE)

# Forest plot with subgroups
forest(ma, subgroup = study_design, test.subgroup = TRUE)
```

## Sensitivity Analysis

```r
# Leave-one-out analysis
metainf(ma, pooled = "random")

# Influence diagnostics
influence(ma)

# Exclude high risk of bias studies
ma_low_rob <- update(ma, subset = rob_overall != "High")
```

## Publication Bias

```r
# Funnel plot
png("funnel_plot.png", width=800, height=600, res=150)
funnel(ma, studlab = TRUE)
dev.off()

# Egger's test (recommended for >10 studies)
metabias(ma, method.bias = "Egger")

# Begg's test (rank correlation)
metabias(ma, method.bias = "Begg")

# Trim-and-fill
tf <- trimfill(ma)
summary(tf)
funnel(tf)
```

## Output Requirements

Always report:
1. Number of studies and total participants
2. Pooled effect estimate with 95% CI
3. P-value for overall effect
4. I² with interpretation
5. τ² (for random-effects)
6. Prediction interval (if using random-effects)
7. Publication bias tests (if ≥10 studies)

## Example Complete Analysis

```r
library(meta)

# Load data
data <- read.csv("extraction_data.csv")

# Meta-analysis
ma <- metabin(
    event.e = events_int, n.e = n_int,
    event.c = events_ctrl, n.c = n_ctrl,
    studlab = study_id, data = data,
    sm = "OR", method = "MH", random = TRUE
)

# Results
summary(ma)

# Forest plot
png("forest_plot.png", width=1200, height=800, res=150)
forest(ma, sortvar=TE, prediction=TRUE)
dev.off()

# Funnel plot
png("funnel_plot.png", width=800, height=600, res=150)
funnel(ma)
dev.off()

# Publication bias
metabias(ma, method.bias="Egger")

# Sensitivity
metainf(ma)
```
