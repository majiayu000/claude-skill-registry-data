---
name: ff-statistical-methods
description: Expert guidance on statistical analysis methodologies and Monte Carlo simulation for fantasy football. Use this skill when selecting regression approaches, designing simulations, performing variance analysis, or conducting hypothesis tests. Covers regression types (OLS, Ridge, Lasso, GAMs), Monte Carlo frameworks, regression-to-mean analysis, and statistical best practices for player performance modeling.
---

# Statistical Analysis & Simulation for Fantasy Football

## Overview

Provide expert guidance on statistical methodologies and simulation techniques for fantasy football analytics. Apply appropriate regression methods, design Monte Carlo simulations, perform variance analysis, and conduct hypothesis tests using research-backed approaches.

## When to Use This Skill

Trigger this skill for queries involving:

- **Regression selection**: "Should I use OLS or Lasso?" "When to use GAMs?" "Ridge vs Elastic Net?"
- **Monte Carlo simulation**: "How do I simulate rest-of-season?" "Calculate championship probability?" "Quantify trade impact?"
- **Variance analysis**: "Identify regression-to-mean candidates?" "Calculate confidence intervals?" "Prediction intervals?"
- **Statistical testing**: "Hypothesis test for performance trends?" "Is this improvement significant?"
- **Aging curves**: "Model non-linear age effects?" "GAMs for position-specific curves?"
- **Uncertainty quantification**: "Error bars on projections?" "Probability of outcomes?"

**Note:** For ML model selection and feature engineering, use `ff-ml-modeling`. For dynasty strategy domain knowledge, use `ff-dynasty-strategy`.

## Core Capabilities

### 1. Regression Methods

**Decision Framework:**

**Linear Regression (OLS):** Baseline, interpretability, small samples

**Ridge (L2):** Multicollinearity, keep all features, shrink coefficients

**Lasso (L1):** High-dimensional data, automatic feature selection, sparse models

**Elastic Net:** Best default for fantasy (combines Ridge + Lasso)

**GAMs:** Non-linear relationships (aging curves), interpretable smooth functions

**Reference:** `references/regression_methods.md` for detailed comparisons and Python code.

### 2. Monte Carlo Simulation

**Applications:**

- Rest-of-season projections with uncertainty
- Championship probability estimation
- Trade scenario impact analysis
- Lineup optimization under uncertainty

**Core Approach:**

```python
# Simulate player week: Normal(projection, std_dev)
simulated_points = np.random.normal(projection, std_dev, n_sims=10000)
simulated_points = np.maximum(simulated_points, 0)  # Floor at zero
```

**Key Considerations:**

- **Iterations:** 10,000 default (SE ≈ 0.5%), 100,000 for critical decisions
- **Error correlation:** QB and WRs are correlated, model synergies
- **Path dependence:** Update team ratings within simulations (FiveThirtyEight approach)
- **Flaw of averages:** Analyze full distribution, not just mean

**Reference:** `references/simulation_design.md` for frameworks, templates, and best practices.

**Asset:** `assets/monte_carlo_template.py` - Python templates for common simulations.

### 3. Regression to the Mean

**Concept:** Extreme values tend toward average in subsequent measurements

**Fantasy Application:**

- +TDOE (Touchdowns Over Expected): Declines 86% next year
- -TDOE: Improves 93% next year
- High TD rates regress downward, low TD rates improve

**Position-Specific Sample Sizes (50% regression):**

- QB: 21 games
- RB: 29-30 games
- WR: 13-14 games
- TE: ~20 games

**Implementation:**

```python
regression_factor = sample_size / (sample_size + n_50[position])
regressed_estimate = (regression_factor * current_stat) + ((1 - regression_factor) * position_mean)
```

**Reference:** `references/regression_methods.md` section on regression to the mean.

### 4. Confidence vs Prediction Intervals

**Confidence Interval:** Uncertainty in estimated mean (narrow)

**Prediction Interval:** Uncertainty for new observation (wider - use this for player projections!)

**Why it matters:** Individual player performance has more variability than average performance

```python
# Prediction interval accounts for both parameter uncertainty AND individual variance
margin = t_score * residual_standard_error
lower, upper = prediction - margin, prediction + margin
```

### 5. Generalized Additive Models (GAMs)

**When to use:** Non-linear relationships like aging curves

**How it works:** Fit smooth spline for each feature: `y = β₀ + f₁(age) + f₂(experience) + ...`

**Fantasy use cases:**

- Aging curves (inverted-U shapes for position-specific performance)
- Experience effects on production
- Visualize smooth trends

**Research finding:** GAMs reveal QB peaks at 28-33, RB declines post-27

**Python:**

```python
from pygam import LinearGAM, s, f

# s() = smooth (non-linear), f() = factor (categorical)
gam = LinearGAM(s(0) + s(1) + f(2))  # age, experience, position
gam.fit(X_train, y_train)

# Visualize smooth curves
gam.partial_dependence(term=0)  # Age curve
```

**Reference:** `references/regression_methods.md` section on GAMs with Python and R code.

## Workflows

### Choosing a Regression Method

**Step 1: Define Goal**

- Interpretation needed? → OLS or GAMs
- Prediction focus? → Consider regularization

**Step 2: Check Data Characteristics**

- Small sample (<100)? → OLS or Ridge
- High-dimensional (many features)? → Lasso or Elastic Net
- Multicollinearity (VIF > 5)? → Ridge or Elastic Net
- Non-linear patterns? → GAMs

**Step 3: Baseline**

- Always start with OLS to establish floor

**Step 4: Regularization**

- If overfitting, try Ridge/Lasso/Elastic Net
- Use cross-validation to select regularization strength

**Step 5: Non-linearity**

- If residuals show patterns, consider GAMs
- Particularly for aging curves

### Designing a Monte Carlo Simulation

**Step 1: Define Scenario**

- What are you simulating? (Rest-of-season, trade impact, championship probability)
- What's the time horizon? (Weeks remaining)

**Step 2: Gather Inputs**

- Player projections (expected values)
- Standard deviations (from historical performance or model residuals)
- Correlations (QB-WR pairs, teammates)

**Step 3: Build Simulation**

- Use `assets/monte_carlo_template.py` as starting point
- Implement correlated errors for teammates
- Consider path dependence if multi-week

**Step 4: Run Simulations**

- 10,000 iterations default
- 100,000 for final decisions

**Step 5: Analyze Distribution**

- Don't just report mean!
- Show percentiles (10th, 50th, 90th)
- Probability of exceeding thresholds
- Visualize histograms and CDFs

### Analyzing Regression to the Mean

**Step 1: Identify Extreme Performers**

- Find players with unusually high/low TD rates
- Calculate TDOE (Touchdowns Over Expected)

**Step 2: Check Sample Size**

- How many games/opportunities?
- Compare to position-specific threshold (QB: 21, RB: 30, WR: 14)

**Step 3: Apply Regression Formula**

- `regression_factor = n / (n + n_50)`
- `regressed = (factor * current) + ((1 - factor) * mean)`

**Step 4: Identify Buy-Low / Sell-High**

- Positive TDOE → Likely to regress down (sell high)
- Negative TDOE → Likely to improve (buy low)
- Volume matters more than TDs!

## Identifying Data Requirements

**For Regression Analysis:**

- Dependent variable (fantasy points, production metrics)
- Independent variables (age, usage, efficiency stats)
- Historical data (3+ years for robust estimates)
- Position labels (for position-specific models)

**For Monte Carlo Simulation:**

- Player projections (weekly expected values)
- Historical variance (to estimate std dev)
- Roster compositions (for team simulations)
- Correlation structures (teammate relationships)

**For Variance Analysis:**

- Historical performance distributions
- Sample sizes (games played, opportunities)
- Position-specific baselines (for regression to mean)

## Integrating with Other Skills

**Complement with `ff-ml-modeling` when:**

- Choosing between regression types and tree-based models
- Feature engineering informs what to include in regression
- Validation strategies apply to statistical models too

**Complement with `ff-dynasty-strategy` when:**

- Identifying TD regression candidates (TDOE analysis)
- Applying aging curves to trade decisions
- Understanding domain context for statistical findings

## Best Practices

**Start Simple** - OLS baseline before complex methods

**Regularize for High Dimensions** - Use Lasso/Elastic Net when features > samples

**Use GAMs for Clear Non-Linearity** - Aging curves, experience effects

**Model Correlations in Simulations** - QB and WRs are correlated (ρ ≈ 0.6)

**Sufficient Iterations** - 10,000 minimum for stable estimates

**Analyze Full Distribution** - Percentiles and probabilities, not just means

**Validate Assumptions** - Plot residuals, check for patterns

**Regression to Mean is Powerful** - TDs regress, volume is king

## Common Pitfalls

**Ignoring non-linearity** - Age curves aren't linear, use GAMs

**Too few simulations** - <1,000 gives unstable estimates

**Independence assumptions** - Teammates are correlated

**Flaw of averages** - Non-linear outcomes make "average" misleading

**Over-interpreting small samples** - NFL has only 17 games/season

**Forgetting regression to mean** - Extreme TDs will regress

## Python Libraries

```python
# Regression
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression
import statsmodels.api as sm  # For statistical inference
from pygam import LinearGAM, s, f  # GAMs

# Simulation
import numpy as np
import scipy.stats

# Analysis
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
```

## References

- `references/regression_methods.md` - OLS, Ridge, Lasso, Elastic Net, GAMs, regression to mean, confidence/prediction intervals
- `references/simulation_design.md` - Monte Carlo frameworks, championship probability, trade impact, path dependence, error correlation

## Assets

- `assets/monte_carlo_template.py` - Python templates for rest-of-season simulation, championship probability, and trade impact analysis
