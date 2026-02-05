---
name: xai-cons
description: Perform observational constraint (Emergent Constraint, EC) analysis for climate research. Use historical observations to constrain future climate projections from CMIP6 multi-model ensembles, reducing prediction uncertainty. Includes inter-model regression analysis, EC relationship establishment, physical mechanism diagnostics (residual analysis, teleconnection pathways, Walker circulation, lead-lag correlation, SVD), uncertainty quantification (variance reduction, confidence intervals), and reliability assessment (binning analysis, random EC comparison). Use when conducting observational constraint analysis, CMIP multi-model evaluation, reducing prediction uncertainty, validating inter-model relationships, or climate teleconnection research. Applicable to any climate variable pairs (e.g., SST-TAS, precipitation-circulation).
---

# XAI-Cons: Observational Constraint Analysis

## Overview

This skill specializes in **Observational Constraint (Emergent Constraint, EC)** analysis - a powerful method that leverages inter-model differences and historical observations to reduce uncertainty in future climate projections.

**Core Principle:**
If a significant statistical relationship exists between a historical variable (x_hist) and a future prediction variable (y_future) across multiple climate models, then observations of x_hist can "constrain" predictions of y_future, thereby narrowing the uncertainty range.

**Mathematical Expression:**
```
y_future = β × x_historical + ε
```

Where:
- `x_historical`: Historical simulation variable (e.g., 1980-2014 South Atlantic SST)
- `y_future`: Future prediction target (e.g., 2041-2060 East Asia temperature)
- `β`: Regression slope (EC sensitivity)
- `ε`: Residual

**Three Core Steps:**
1. **Establish Emergent Relationship** - Significant inter-model correlation (p<0.05)
2. **Physical Mechanism Validation** - Verify physical linkage through diagnostics
3. **Constraint Quality Assessment** - Evaluate using RRV, RMSE, CRPS, etc.

**For detailed methodology** → See `references/methods.md`

---

## When to Use This Skill

### Automatic Trigger Keywords:

**Method-related:**
- "observational constraint", "emergent constraint", "EC analysis"
- "inter-model regression", "reduce uncertainty", "constrain prediction"
- "CMIP6 evaluation", "multi-model analysis"

**Research content:**
- "South Atlantic", "East Asia", "teleconnection"
- "SST-TAS relationship", "sea surface temperature"
- "Walker circulation", "atmospheric wave train"
- "residual analysis", "remove global signal"

**Analysis tasks:**
- "evaluate EC reliability", "calculate variance reduction"
- "lead-lag correlation", "SVD covariance analysis", "binning analysis"

---

## Core Functionality

### 1. EC Relationship Establishment

**Tasks:**
- Load CMIP6 multi-model historical and future data
- Calculate regional averages (e.g., South Atlantic SST, East Asia TAS)
- Perform inter-model linear regression
- Statistical tests (R², correlation r, p-value)
- Plot scatter + regression line + observational constraint point

**Key Outputs:**
- Regression coefficient β (EC sensitivity)
- R² (explained variance)
- Correlation coefficient r and p-value
- Constrained prediction value and uncertainty range

---

### 2. Reliability Assessment ⭐

**Tasks:**
- Use **binning analysis** to evaluate EC significance
- Compare with random EC to exclude spurious correlations
- Calculate credibility for different correlation strengths
- Generate prior/posterior distribution comparison

**Why Important:**
Not all statistically significant correlations are reliable ECs! Need to assess:
1. Is correlation coefficient strong enough (typically r>0.3)?
2. Better than random correlations?
3. Does constraint actually reduce uncertainty (positive variance reduction)?

**Reference Code:**
- `scripts/examples/src/binning_inference.py` ⭐ Core method
- `scripts/examples/src/plot_random_EC.py` - Random EC comparison
- `scripts/examples/src/plot_PDF_ECS.py` - Probability distributions

**Key Outputs:**
- 66% and 90% confidence intervals
- Prior/posterior distributions
- Variance reduction percentage
- Comparison with random ECs

---

### 3. Physical Mechanism Diagnostics

#### 3a. Residual Analysis
**Purpose:** Answer "Why this region?"

**Tasks:**
- Remove linear influence of global warming signal
- Calculate residual: `residual = SA_SST - (β·Global_SST + intercept)`
- Verify residual uncorrelated with global SST (r≈0)
- Analyze spatial correlation between residual and global temperature field
- Identify unique teleconnection patterns and wave train pathways

**Key Outputs:**
- Spatial correlation maps
- Wave train pathway identification
- Percentage of significantly correlated regions

---

#### 3b. Mediation Analysis
**Example:** Walker circulation

**Tasks:**
- Calculate mediator variable (e.g., Walker circulation index)
- Analyze mediation effects:
  - Path a: predictor → mediator
  - Path b: mediator → response
  - Path c': partial correlation controlling for mediator
- Calculate mediation percentage

---

#### 3c. Spatiotemporal Diagnostics

**Lead-lag Correlation:**
- Calculate correlation at different time lags (±5 years)
- Determine causal temporal relationship

**SVD Covariance Analysis:**
- Identify coupled spatial modes
- Confirm large-scale patterns, not point-to-point artifacts

**Spatial Regression:**
- Regression at each global grid point
- Spatial distribution of regression coefficients
- Significance testing

**Composite Analysis:**
- High SST vs Low SST groups (top/bottom 1/3 of models)
- Temperature difference fields
- t-test significance

---

### 4. Uncertainty Quantification

**Tasks:**
- Calculate prior (unconstrained) uncertainty
- Calculate posterior (constrained) uncertainty
- Variance reduction: `VR = 1 - (σ_posterior / σ_prior)²`
- Confidence interval calculation

**Key Metrics:**
- Variance reduction percentage (should be positive)
- 66% confidence interval width
- 90% confidence interval width
- Reliability rating

---

## Quick Start Examples

### Example 1: Basic EC Analysis

**User says:**
```
"Perform observational constraint analysis for South Atlantic SST
and East Asia temperature using CMIP6 data,
historical period 1980-2014, future period 2041-2060"
```

**Skill executes:**
1. Reference code in `scripts/examples/`
2. Generate scripts adapted to your data
3. Perform inter-model regression
4. Calculate statistics
5. Plot EC scatter diagram
6. Apply observational constraint

---

### Example 2: Reliability Assessment

**User says:**
```
"My EC relationship is r=0.39, R²=0.15, p=0.006.
Use binning method to evaluate if this EC is reliable"
```

**Skill executes:**
1. Apply logic from `binning_inference.py`
2. Generate binning analysis code for your data
3. Calculate credibility at different correlation strengths
4. Compare your r=0.39 with distribution
5. Provide reliability assessment

---

### Example 3: Physical Mechanism Diagnostics

**User says:**
```
"Analyze South Atlantic SST's unique teleconnection.
After removing global warming signal,
check if still correlated with East Asia"
```

**Skill executes:**
1. Calculate South Atlantic SST residual (remove global SST influence)
2. Verify residual uncorrelated with global SST
3. Calculate spatial correlation between residual and global temperature
4. Identify significantly correlated regions
5. Search for wave train pathways
6. Generate comprehensive analysis figure

---

## Available Resources

### Core Tools (`scripts/examples/src/`)

**`binning_inference.py`** ⭐⭐⭐
- Gold standard for EC reliability assessment
- Applicable to any EC relationship
- Directly usable (adjust data paths)

**`tools.py`**
- Statistical analysis utilities
- Plotting tools
- Histograms, modal analysis, etc.

**`plot_PDF_ECS.py`**
- Probability density function visualization
- Prior/posterior distribution comparison

**`plot_random_EC.py`**
- Random EC generation and comparison
- Significance assessment

### Literature Examples

**Bonan et al. (2025) Nature Geoscience**
- EC analysis of ocean overturning circulation
- Physical constraint methodology

**Kornhuber et al. (2024) PNAS**
- Complete EC analysis case study
- Full workflow from data to figures

**Pakistan Case Study**
- Multi-level diagnostic analysis
- EOF, MCA, composite analysis
- Publication-ready figure standards

**Documentation:**
- `scripts/examples/README.md` - Detailed example code documentation
- `references/methods.md` - Comprehensive methodology and theory
- `references/workflow.md` - Step-by-step analysis workflow (if available)
- `references/best_practices.md` - Best practices and FAQ (if available)

---

## Key Statistical Thresholds

### EC Reliability Assessment Standards:

| Metric | Excellent | Good | Acceptable | Weak |
|--------|-----------|------|------------|------|
| **Correlation r** | >0.6 | 0.4-0.6 | 0.3-0.4 | <0.3 |
| **R²** | >0.36 | 0.16-0.36 | 0.09-0.16 | <0.09 |
| **p-value** | <0.01 | 0.01-0.03 | 0.03-0.05 | >0.05 |
| **Variance Reduction** | >50% | 30-50% | 10-30% | <10% or negative |

**Note:**
- These are empirical thresholds, not absolute standards
- Must combine with binning analysis for comprehensive judgment
- Physical mechanism support is crucial

---

## Best Practices

### ✅ Recommended:

1. **Always assess reliability**
   - Don't rely solely on p-values
   - Must perform binning analysis
   - Check if variance reduction is positive

2. **Seek physical mechanisms**
   - EC relationship must have physical explanation
   - Pure statistical correlation insufficient for publication
   - Use multiple diagnostic methods for cross-validation

3. **Sensitivity testing**
   - Different time periods
   - Different region definitions
   - Different observational datasets

### ❌ Avoid These Pitfalls:

1. **Cherry-picking** - Testing many variable pairs and only reporting significant ones
2. **Ignoring uncertainty** - Constrained range may still be large
3. **Over-interpreting weak correlations** - r<0.3 rarely reliable
4. **Ignoring model dependence** - Outlier models may drive correlation

---

## Technical Stack

**Required Python Packages:**
- `numpy` - Numerical computation
- `scipy` - Statistical analysis
- `matplotlib` - Plotting
- `xarray` - Multi-dimensional data (NetCDF)
- `netCDF4` - NetCDF file I/O

**Recommended Packages:**
- `pandas` - Tabular data
- `cartopy` - Map plotting
- `seaborn` - Advanced visualization
- `statsmodels` - Advanced statistics

---

## Output Deliverables

### Figures:
**Main Figures:**
1. EC scatter plot (regression line + observational constraint)
2. Spatial regression pattern map
3. Physical mechanism composite figure (4-6 panels)

**Supplementary Figures:**
1. Binning analysis plot
2. Residual teleconnection map
3. Lead-lag correlation curve
4. SVD covariance pattern
5. Walker circulation mediation effects
6. Composite analysis

### Data:
- Regression statistics (β, R², r, p)
- Pre/post constraint predictions and uncertainties
- Variance reduction percentage
- Binning analysis statistics
- Physical diagnostic metrics

### Text:
- Methods section draft
- Results section draft
- Supplementary materials description
- Reviewer response templates

---

## Related Resources

**Internal:**
- `scripts/examples/README.md` - Example code documentation
- `scripts/examples/src/` - Core utility functions
- `scripts/examples/*.ipynb` - Literature implementation examples
- `scripts/examples/Pakistan/` - Complete case study

**External References:**
- Hall et al. (2019). "Progressing emergent constraints on future climate change". *Nature Climate Change*.
- Brient, F. (2020). "Evaluating the robustness of emergent constraints".
- Cox et al. (2018). "Emergent constraint on ECS from global temperature variability". *Nature*.

---

**Last Updated:** 2025-10-27
**Version:** 1.0
**Maintainer:** Climate-AI Research Team
**Based On:** South Atlantic - East Asia Teleconnection Research
