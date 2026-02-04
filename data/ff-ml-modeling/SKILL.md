---
name: ff-ml-modeling
description: Expert guidance on machine learning and feature engineering for fantasy football player projection models. Use this skill when building predictive models, engineering features from player statistics, selecting appropriate ML algorithms, or addressing sports-specific ML challenges. Covers feature engineering patterns, model selection frameworks, validation strategies, and interpretability techniques for fantasy football analytics.
---

# Machine Learning & Feature Engineering for Fantasy Football

## Overview

Provide expert guidance on building ML-based player projection models using research-backed feature engineering patterns, appropriate model selection, and sports-specific validation strategies. Apply domain expertise to help design features, choose models, avoid common pitfalls, and create interpretable predictions.

## When to Use This Skill

Trigger this skill for queries involving:

- **Feature engineering**: "What features should I include?" "How do I create age curve features?" "What are good opportunity metrics?"
- **Model selection**: "Which ML model should I use?" "Random Forest or XGBoost?" "When to use regularized regression?"
- **Validation strategies**: "How do I validate sports models?" "What's wrong with standard cross-validation?" "How to avoid data leakage?"
- **Sports-specific challenges**: "How to handle small sample sizes?" "How to model position differences?" "Handling regime changes?"
- **Feature selection**: "How to reduce 109 stats to key features?" "Lasso vs Ridge?" "How to handle multicollinearity?"
- **Model interpretability**: "How to explain predictions?" "What features matter most?" "SHAP values for fantasy?"

**Note:** For dynasty strategy questions (player valuation, trade analysis, roster construction), use `ff-dynasty-strategy`. For statistical methods (regression types, simulations, GAMs), use `ff-statistical-methods`.

## Core Capabilities

### 1. Feature Engineering

**Core Principle:** Feature engineering is more important than model selection for sports predictions.

**Key Feature Categories:**

**Age Curves**

- Marcel system: 3-year weighted average + age adjustment + regression to mean
- Position-specific peaks: RB 23-26, WR 26-28, QB 28-33, TE 26-29
- Implementation: `age_factor = 1 - (age - peak_age) * 0.003` for decline phase

**Opportunity Metrics**

- Target share, snap share, weighted opportunities (carries + targets×1.5)
- Points per opportunity (efficiency measure)
- Volume is king: opportunity metrics predict better than TDs

**Efficiency Statistics**

- Yards per route run (YPRR), yards per carry (YPC)
- Yards after contact (YAC), catch rate
- Warning: Noisy with small samples, use rolling averages

**Interaction Terms**

- QB quality × target share (receiver production context)
- Opponent strength adjustments
- Game script (leading = rushing, trailing = passing)
- ~40% of team performance from synergy effects

**Rolling Averages**

- Last 3 games, last 5 games, season-long
- Trend features: recent form vs established baseline
- Lag features: last game, same opponent last season

**Reference:** `references/feature_engineering.md` for formulas, implementation patterns, and common mistakes.

### 2. Model Selection

**Decision Framework:**

```
Primary Goal?
├─ Interpretability → Linear/Ridge/Lasso Regression
└─ Performance
   ├─ Small (<1000) → Ridge/Lasso/Elastic Net
   ├─ Medium (1K-10K) → Random Forest or XGBoost
   └─ Large (>10K) → XGBoost/LightGBM or Ensemble
```

**Model Types:**

**Linear Regression:** Baseline, interpretability, small samples

**Regularized Regression:** High-dimensional data, multicollinearity, automatic feature selection (Lasso)

**Random Forest:** Medium data, robustness, feature importance

**XGBoost/LightGBM:** Best single-model performance, handles missing values

**Ensemble:** Combine Ridge + RF + XGBoost (weighted 1:2:2), often 2-5% improvement

**Position-Specific Modeling:** Train separate models per position (RB features ≠ WR features)

**Reference:** `references/model_selection.md` for detailed comparisons, hyperparameters, and implementation.

### 3. Validation Strategies

**Critical Rule: NEVER use standard cross-validation with shuffle=True**

❌ **Wrong:** `KFold(n_splits=5, shuffle=True)` → Data leakage!

✅ **Correct:** `TimeSeriesSplit(n_splits=5)` → Train on past, test on future

**Time-Series Split:** Always predict future from past data

**Appropriate Metrics:**

- MAE (Mean Absolute Error): Most interpretable
- RMSE: Penalizes large errors
- R²: Proportion of variance explained

**Nested Cross-Validation:** Outer loop for evaluation, inner loop for hyperparameter tuning

**Reference:** `references/validation_strategies.md` for detailed workflows and common mistakes.

### 4. Sports-Specific Challenges

**Small Sample Sizes:** NFL = 17 games/season → Use regularization (Ridge/Lasso)

**Position-Specific Modeling:** Separate models per position with different feature sets

**Regime Changes:** Weight recent seasons heavier, use sliding window validation

**Data Leakage Prevention:** Only use data available at prediction time, time-series validation

**Reference:** `references/model_selection.md` sections on sports-specific considerations.

## Workflow: Building a Player Projection Model

**Step 1: Feature Engineering**

- Start with raw stats (yards, TDs, targets, snaps)
- Create opportunity metrics (target share, snap %)
- Add efficiency features (YPRR, YPC)
- Generate rolling averages (3-game, 5-game)
- Include age curves and interaction terms
- Use `assets/player_projection_model_template.py` as starting point

**Step 2: Feature Selection**

- Check correlation (remove highly correlated features)
- Use Lasso for automatic selection
- SHAP values for importance
- Domain knowledge: prioritize opportunity > efficiency > TDs

**Step 3: Model Selection**

- Establish baseline (linear regression or Marcel)
- Try regularized model (Elastic Net)
- Test tree-based (Random Forest, then XGBoost)
- Position-specific models
- Ensemble top 2-3 models

**Step 4: Validation**

- Hold out most recent season as final test
- TimeSeriesSplit on training data
- Nested CV for hyperparameter tuning
- Evaluate MAE by position

**Step 5: Interpretability**

- SHAP values for feature importance
- Partial dependence plots for age curves
- Validate on new season

## Identifying Data Requirements

**For Player Projection Models:**

- Historical performance (3+ years for aging curves)
- Opportunity metrics (targets, snaps, routes run, carries)
- Efficiency stats (YPRR, YPC, catch rate)
- Contextual data (opponent strength, QB quality, game script)
- Position and age

**For Feature Engineering:**

- Player-level: Stats, age, position, career year
- Team-level: Total targets, snaps, carries (for share calculations)
- Game-level: Score differential, home/away, opponent defense rank
- Season-level: Rule changes, schedule strength

## Integrating with Other Skills

**Complement with `ff-dynasty-strategy` when:**

- Need domain knowledge for feature selection (aging curves, TD regression)
- Interpreting model outputs (sell-high candidates)
- Understanding position-specific patterns

**Complement with `ff-statistical-methods` when:**

- Choosing regression type (OLS vs Lasso vs GAMs)
- Running Monte Carlo simulations using predictions
- Performing variance analysis

## Best Practices

**Feature Engineering Over Model Complexity** - Well-engineered features make simple models outperform complex ones

**Always Use Time-Series Validation** - Standard CV inflates performance 15-20%

**Position-Specific Models** - RB features ≠ WR features ≠ QB features

**Regularization for Small Samples** - NFL has limited games (17/season)

**Prioritize Interpretability** - SHAP values for explainability, start simple

## References

- `references/feature_engineering.md` - Age curves, opportunity metrics, efficiency stats, interaction terms
- `references/model_selection.md` - Decision framework, model types, hyperparameters
- `references/validation_strategies.md` - Time-series splits, nested CV, metrics

## Assets

- `assets/player_projection_model_template.py` - Python template for building player projection models
