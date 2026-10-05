---
name: quant-experiments
description: >
  Design and execute quantitative experiments in Jupyter notebooks with rich markdown narrative
  and visualizations. Use this skill whenever the user wants to: run statistical tests or
  hypothesis testing, build Monte Carlo simulations, design A/B tests or causal inference
  analyses, run numerical optimization experiments, build time series & forecasting models,
  run machine learning experiments, or structure any rigorous quantitative analysis in a
  notebook. Trigger even for partial requests like "test if X is significant", "simulate
  this process", "forecast this series", "optimize this function", "compare model performance",
  or "set up an experiment for Y". Always use this skill when the user provides data and asks
  for quantitative analysis — don't attempt quant experiments without it.
---

# Quantitative Experiments in Jupyter — Skill Guide

## Overview

This skill produces **end-to-end Jupyter notebooks** for quantitative experiments. The output
style is **markdown-narrative-first with rich visualizations**: every analysis section is
preceded by a markdown cell explaining the *why*, every result is followed by a markdown cell
interpreting the *so what*, and every key finding is illustrated with a well-labeled, annotated plot.

---

## Notebook Structure (Always Follow This)

```
1. # Experiment Title
   [markdown] Objective, hypothesis, scope, expected outcome

2. ## 🔧 Setup & Imports
   [code] All imports, seeds, config constants
   [markdown] Brief note on key libraries and why they're used

3. ## 📊 Data / Data Generation
   [markdown] Describe the data source or generative process
   [code] Load or simulate data
   [code] Descriptive statistics + distribution plot
   [markdown] Key observations from the data

4. ## 📐 Methodology
   [markdown] Explain the chosen method with LaTeX formula
   [markdown] State assumptions and how they'll be verified
   [code] Assumption checks with diagnostic plots

5. ## 🧪 Experiment / Analysis
   [markdown] Walk through each analysis step in plain language
   [code] Core analysis (clean, well-commented)
   [code] Intermediate visualizations after each major step
   [markdown] Narrative of what intermediate results suggest

6. ## 📈 Results
   [code] Results table (pandas Styler)
   [code] Primary results visualization (always required)
   [markdown] Narrative interpretation of what the chart shows

7. ## ✅ Conclusion
   [markdown] APA-style statistical summary line
   [markdown] Plain-language decision and takeaway
   [markdown] Limitations and suggested next steps

8. ## 🔍 Appendix (optional)
   Sensitivity analysis, robustness checks, extra plots
```

### Markdown Cell Rules
- **Before every code block**: 1–3 sentence explanation of what the code does and why
- **After every visualization**: 2–4 sentence interpretation ("The distribution is right-skewed, suggesting…")
- Use `>` blockquotes for key findings: `> **Finding:** The treatment group shows a 12% lift (p < .001)`
- Use emoji section headers to improve scannability

---

## Visualization Standards

### Global Figure Setup (always in Setup cell)
```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep", font="DejaVu Sans")
mpl.rcParams.update({
    'figure.dpi': 150,
    'figure.figsize': (10, 6),
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
})
PALETTE = sns.color_palette("deep")
```

### Required Plots by Experiment Type

| Experiment | Required plots |
|------------|----------------|
| Hypothesis test | Distribution KDE comparison + effect size forest plot |
| Monte Carlo | Outcome histogram with percentile bands + convergence trace |
| A/B test | Conversion rate bars with CI + power curve |
| Time series | Decomposition (4-panel) + forecast with CI band |
| Optimization | Objective landscape + convergence curve |
| ML experiment | CV score violin plot + mean±CI bar + feature importance |

### Plot Template (use for every figure)
```python
fig, ax = plt.subplots(figsize=(10, 6))

# --- your plot code ---

ax.set_title('Descriptive Title', pad=15)
ax.set_xlabel('X Label (units)')
ax.set_ylabel('Y Label (units)')
ax.legend(framealpha=0.9)

# Annotate key finding directly on chart
ax.annotate('Key insight here',
            xy=(x_pos, y_pos), xytext=(x_pos + dx, y_pos + dy),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=10, color='#333333')

plt.tight_layout()
plt.show()
```

### Multi-panel Layout (preferred for results sections)
```python
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Experiment Results Overview', fontsize=16, fontweight='bold')
# panel 1: raw data / distributions
# panel 2: main test result / finding
# panel 3: effect size / confidence intervals
plt.tight_layout()
```

---

## Experiment Types

### 1. Hypothesis Testing

**Markdown narrative pattern:**
> "We test whether [X differs from Y] using [test] because [normality check result / n].
> H₀: μ₁ = μ₂  |  H₁: μ₁ ≠ μ₂ (two-tailed, α = 0.05)"

**Key elements:**
- State H₀ / H₁ in LaTeX in a markdown cell
- Normality: `scipy.stats.shapiro` (n<50) or `scipy.stats.normaltest`
- Variance: `scipy.stats.levene`; plot violin/box side-by-side
- Report: test statistic, p-value, Cohen's d, 95% CI
- APA string: `f"t({df}) = {t:.3f}, p = {p:.3f}, d = {d:.3f}, 95% CI [{lo:.3f}, {hi:.3f}]"`

**Required plots:** Overlapping KDE + rug plot with group means marked; effect size with CI bar

---

### 2. Monte Carlo Simulations

**Markdown narrative pattern:**
> "We simulate [process] N=100,000 times to estimate [quantity]. The generative model is:
> $$X_t = \mu + \sigma \epsilon_t, \quad \epsilon_t \sim \mathcal{N}(0,1)$$
> Vectorized NumPy is used for performance (~50× faster than loops)."

**Key elements:**
- LaTeX process equation in markdown before code
- Vectorized NumPy (`np.random.default_rng`)
- Report: mean, std, 5th / 25th / 75th / 95th percentiles
- Convergence plot to verify N is sufficient

**Required plots:**
```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Left: outcome distribution with shaded percentile bands
ax1.hist(results, bins=80, color=PALETTE[0], alpha=0.7, density=True)
for pct, ls in [(5,'--'), (25,':'), (75,':'), (95,'--')]:
    ax1.axvline(np.percentile(results, pct), color='red', ls=ls, lw=1.2,
                label=f'{pct}th %ile')
ax1.set_title('Simulation Outcome Distribution')

# Right: convergence trace
running_mean = np.cumsum(results) / np.arange(1, len(results)+1)
ax2.plot(running_mean, color=PALETTE[1], lw=1.2)
ax2.axhline(results.mean(), color='red', ls='--', label='Converged mean')
ax2.set_title('Convergence of Running Mean')
ax2.set_xlabel('Simulation #'); ax2.set_ylabel('Running Mean')
```

---

### 3. A/B Testing & Causal Inference

**Markdown narrative pattern:**
> "Required sample size (MDE=[X]%, power=80%, α=5%) is N=[n] per group.
> We have N=[actual]; the test is [adequately/under] powered."

**Sub-types and libraries:**

| Goal | Method | Library |
|------|---------|---------|
| Proportion test | Z-test | `statsmodels.stats.proportion` |
| Continuous metric | Welch's t-test | `scipy.stats` |
| Bayesian A/B | Beta-binomial | analytical |
| Uplift / CATE | Meta-learners | `causalml` |
| Observational | Propensity score matching | `causalinference` |
| Panel data | Difference-in-Differences | `linearmodels` |

**Always include:** MDE calc, power curve plot, segment breakdown table (Simpson's paradox guard)

**MDE formula in markdown:**
$$n = \frac{(z_{\alpha/2} + z_\beta)^2 \cdot 2\sigma^2}{\delta^2}$$

**Required plots:** Conversion rate bars with CI error bars; Bayesian posterior overlay if Bayesian

---

### 4. Numerical Optimization

**Markdown narrative pattern:**
> "We minimize f(x) = [expression] subject to [constraints]. The landscape is visualized
> first to identify the number of local minima before choosing a solver."

**Key elements:**
- Always visualize objective landscape before running optimizer
- Track convergence via callback: log f(x*) per iteration
- Compare methods if relevant (gradient-based vs. evolutionary)
- Report: optimal x*, f(x*), iterations to converge, wall-clock time

**Standard pattern:**
```python
from scipy.optimize import minimize, differential_evolution

# 1. Visualize landscape
x_grid = np.linspace(*bounds, 300)
ax.plot(x_grid, [objective(x) for x in x_grid], lw=2)
ax.set_title('Objective Function Landscape')

# 2. Optimize with convergence tracking
history = []
result = minimize(objective, x0, method='L-BFGS-B',
                  bounds=[bounds],
                  callback=lambda xk: history.append(objective(xk)))

# 3. Convergence plot
ax2.plot(history, marker='o', markersize=3, lw=1.5)
ax2.set_title('Convergence Trace')
ax2.set_xlabel('Iteration'); ax2.set_ylabel('Objective f(x)')
```

**Multi-method comparison table (styled):**
```python
results_df.style\
    .highlight_min(subset=['f(x*)'], color='lightgreen')\
    .highlight_min(subset=['Runtime (s)'], color='lightyellow')\
    .format({'f(x*)': '{:.6f}', 'Runtime (s)': '{:.3f}'})\
    .set_caption('Optimizer Comparison')
```

---

### 5. Time Series & Forecasting

**Markdown narrative pattern:**
> "We decompose the series into trend, seasonal, and residual components, then test for
> stationarity (ADF). Model order is guided by ACF/PACF plots before fitting [ARIMA/ETS/Prophet]."

**Key elements:**
- Decomposition: `statsmodels.tsa.seasonal.seasonal_decompose`
- Stationarity: ADF test (`statsmodels.tsa.stattools.adfuller`)
- ACF/PACF plots to guide model order (`statsmodels.graphics.tsaplots`)
- Always show forecast with **confidence interval band**
- Metrics: MAE, RMSE, MAPE, directional accuracy

**Required plots:**
```python
# 4-panel decomposition
fig, axes = plt.subplots(4, 1, figsize=(12, 14), sharex=True)
fig.suptitle('Time Series Decomposition', fontsize=16, fontweight='bold')
decomp = seasonal_decompose(series, model='additive', period=period)
for ax, data, label in zip(axes,
    [series, decomp.trend, decomp.seasonal, decomp.resid],
    ['Observed', 'Trend', 'Seasonal', 'Residual']):
    ax.plot(data, lw=1.5)
    ax.set_ylabel(label, fontsize=11)

# Forecast with CI band
fig2, ax = plt.subplots(figsize=(12, 5))
ax.plot(train.index, train, label='Train', lw=1.5)
ax.plot(test.index, test, label='Actual', lw=1.5)
ax.plot(forecast.index, forecast['mean'], label='Forecast', ls='--', lw=2)
ax.fill_between(forecast.index,
                forecast['mean_ci_lower'], forecast['mean_ci_upper'],
                alpha=0.2, label='95% CI')
ax.set_title('Forecast vs. Actuals')
ax.legend()
```

---

### 6. Machine Learning Experiments

**Markdown narrative pattern:**
> "We compare [N] models using [K]-fold stratified CV on [metric]. Statistical significance
> of pairwise differences is assessed with Wilcoxon signed-rank test on the per-fold scores."

**Key elements:**
- Stratified K-fold; report mean ± std per model
- Wilcoxon / Friedman test across folds — never compare point estimates alone
- Learning curves for best model
- Feature importance or SHAP values

**Required plots:**
```python
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('ML Experiment Results', fontsize=16, fontweight='bold')

# Panel 1: CV score violin + strip (shows full distribution)
sns.violinplot(data=cv_scores_df, ax=axes[0], palette='deep', inner='box')
sns.stripplot(data=cv_scores_df, ax=axes[0], color='black', alpha=0.4, size=3)
axes[0].set_title('CV Score Distributions')

# Panel 2: Mean ± 95% CI horizontal bar
axes[1].barh(model_names, means, xerr=1.96*stds/np.sqrt(K),
             color=PALETTE[:len(model_names)], capsize=5, alpha=0.85)
axes[1].set_title('Mean CV Score ± 95% CI')

# Panel 3: Feature importances (top 15)
feat_imp.sort_values().tail(15).plot(kind='barh', ax=axes[2], color=PALETTE[0], alpha=0.85)
axes[2].set_title('Top 15 Feature Importances')

plt.tight_layout()
```

---

## Standard Imports Cell

```python
# === Core ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from scipy import stats

# === Stats & Experiments ===
import statsmodels.api as sm
from statsmodels.stats.power import TTestIndPower

# === Display ===
from IPython.display import display, Markdown, Latex
from tabulate import tabulate

# === Visualization Theme ===
sns.set_theme(style="whitegrid", palette="deep")
mpl.rcParams.update({
    'figure.dpi': 150, 'figure.figsize': (10, 6),
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.titlesize': 14, 'axes.titleweight': 'bold', 'axes.labelsize': 12,
})
PALETTE = sns.color_palette("deep")

# === Reproducibility ===
SEED = 42
np.random.seed(SEED)
print(f"NumPy {np.__version__} | Pandas {pd.__version__} | Seaborn {sns.__version__}")
```

---

## Reporting Checklist

Before finalizing any notebook:

- [ ] Every code section has a markdown cell before (explaining *what* and *why*)
- [ ] Every visualization has a markdown cell after (interpreting *what it shows*)
- [ ] Key findings called out with `> **Finding:** ...` blockquotes
- [ ] Random seed set and documented
- [ ] All assumptions explicitly tested with plots
- [ ] Effect size alongside p-value; confidence intervals on all estimates
- [ ] All figures: axis labels, title, legend, annotations
- [ ] Results table styled with pandas Styler
- [ ] Conclusion in plain language with limitations

---

## Reference Files

- `references/statistical_tests_guide.md` — Test selection decision tree + assumptions
- `references/effect_sizes.md` — Effect size formulas, code, and interpretation benchmarks
- `references/causal_inference_patterns.md` — RCT, DiD, PSM, Bayesian A/B patterns
- `references/timeseries_optimization.md` — Time series model selection + optimization algorithms

Read the relevant reference when deeper guidance on test selection, causal design, model order,
or optimization algorithm choice is needed.
