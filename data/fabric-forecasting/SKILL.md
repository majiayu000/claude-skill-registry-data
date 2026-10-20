---
name: "fabric-forecasting"
description: 'Build time-series forecasting pipelines on Microsoft Fabric - data preparation, profiling, clustering, feature engineering, and model training. Use when implementing demand forecasting, training LightGBM/Prophet models, engineering time-series features, or deploying prediction pipelines on Fabric.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-07-13"
 updated: "2025-07-13"
compatibility:
 languages: ["python", "pyspark", "sql"]
 frameworks: ["microsoft-fabric", "apache-spark", "lightgbm", "prophet", "optuna"]
 platforms: ["windows", "linux", "macos"]
prerequisites:
 - "Microsoft Fabric workspace with active capacity"
 - "Fabric MCP Server (ms-fabric-mcp-server)"
 - "Lakehouse with historical time-series data (12+ months recommended)"
 - "Python libraries: lightgbm, prophet, optuna, scikit-learn, plotly"
---

# Fabric Forecasting

> Time-series forecasting pipelines on Fabric - from raw data to trained models with profiling, clustering, and feature engineering.

## When to Use

- Building demand forecasting models (retail, supply chain, finance)
- Forecasting across many series (products, stores, regions)
- Classifying time-series patterns (regular, intermittent, lumpy, erratic)
- Creating feature-engineered datasets for ML models
- Training and tuning LightGBM, Prophet, or ensemble models on Fabric

## Decision Tree

```
Need time-series forecasting on Fabric?
+- Have historical data in Lakehouse?
| +- Yes -> Start at Phase 1 (Intake & Discovery)
| - No -> Use fabric-analytics skill to ingest data first
+- Know the forecasting scenario?
| +- Clear requirements -> Start at Phase 2 (Scenario Interpretation)
| - Need discovery -> Start at Phase 1
+- Have a customization plan?
| - Yes -> Start at Phase 4 (Notebook Generation)
+- Which model?
| +- Many series + external features -> LightGBM [PASS]
| +- Few series + strong seasonality -> Prophet [PASS]
| +- Intermittent demand -> Specialized methods (Croston, SBA)
| - Unsure -> Profile data first (Phase 1-2), then decide
- Not forecasting?
 +- Ad-hoc analytics -> Use fabric-analytics skill
 - Chat-based Q&A -> Use fabric-data-agent skill
```

## Pipeline Overview

The forecasting pipeline follows a **5-phase workflow** organized as a notebook pipeline:

```
Phase 1: Intake --> Phase 2: Interpret --> Phase 3: Plan --> Phase 4: Notebooks --> Phase 5: Finalize
 |
 --------+------------------------
 NB01 NB02 NB03 NB04 NB05
 Prep Profile Cluster Feature Train
```

### Phase 1: Intake & Data Discovery

**Goal**: Understand the data and user's forecasting scenario.

| Step | Action | Output |
|------|--------|--------|
| 1 | Gather inputs (workspace, lakehouse, table) | User requirements |
| 2 | Discover table schema and date range | Data inventory |
| 3 | Identify time column, target, ID columns | Column mapping |
| 4 | Calculate basic statistics (seasonality, trend) | Data profile |

**Checkpoint**: Present data summary, confirm column mapping.

### Phase 2: Scenario Interpretation

**Goal**: Translate business requirements into forecasting parameters.

| Parameter | Examples |
|-----------|---------|
| Forecast horizon | 4 weeks, 12 months, 90 days |
| Time granularity | Daily, weekly, monthly |
| Number of series | 1 (single), 100s (multi-series), 10K+ (hierarchical) |
| Seasonality | Weekly (7), Monthly (30), Yearly (365) |
| External factors | Promotions, holidays, weather, events |

**Checkpoint**: Confirm scenario parameters with user.

### Phase 3: Customization Planning

**Goal**: Determine which notebook customizations are needed based on the scenario.

### Customization Risk Levels

| Risk | Type | Examples |
|------|------|---------|
| **Low** | Parameter substitution | Column names, table names, horizon, date format |
| **Medium** | Structural adaptation | Time aggregation, lag sizes, clustering params, skip sections |
| **High** | Algorithm/generative | Model changes, external regressors, custom metrics, new cells |

**Rule**: Low = auto-apply. Medium = explain and confirm. High = detailed proposal + approval.

**Checkpoint**: Present customization plan, get approval for medium/high risk changes.

### Phase 4: Notebook Generation (NB01-NB05)

Five notebooks form the pipeline, each building on the previous output:

| Notebook | Purpose | Input | Output |
|----------|---------|-------|--------|
| **NB01: Data Preparation** | Clean, fill gaps, handle missing values | Raw Lakehouse table | `{scenario}_prepared` |
| **NB02: Profiling** | Classify series (regular/lumpy/erratic/intermittent) | `_prepared` table | `{scenario}_profiled` |
| **NB03: Clustering** | Group similar series via K-Means | `_profiled` table | `{scenario}_clustered` |
| **NB04: Feature Engineering** | Lags, rolling stats, calendar features | `_clustered` table | `{scenario}_features` |
| **NB05: Train & Tune** | Train LightGBM, tune with Optuna | `_features` table | `{scenario}_forecasts` |

**Checkpoint**: After each notebook, validate output table before proceeding.

### Phase 5: Finalization & Delivery

**Goal**: Package deliverables and deploy to Fabric.

| Step | Action |
|------|--------|
| 1 | Upload notebooks to Fabric workspace |
| 2 | Attach default Lakehouse to each notebook |
| 3 | Execute notebooks in sequence |
| 4 | Validate forecast output quality |
| 5 | Generate completion report |

## Core Concepts

### Time-Series Classification

Profiling classifies each series to guide model selection:

| Type | CV | ADI | Characteristics | Model Approach |
|------|-----|-----|-----------------|----------------|
| **Regular** | Low | Low | Smooth demand, consistent | LightGBM, Prophet |
| **Erratic** | High | Low | Volatile but frequent | LightGBM with more features |
| **Lumpy** | High | High | Sporadic and variable | Croston, SBA |
| **Intermittent** | Low | High | Infrequent but stable | Croston, TSB |

- **CV** = Coefficient of Variation squared (demand variability)
- **ADI** = Average Demand Interval (frequency of non-zero demand)

### Feature Engineering Patterns

| Feature Type | Examples | When to Use |
|-------------|---------|-------------|
| **Lags** | `lag_7`, `lag_14`, `lag_28` | Always - capture autocorrelation |
| **Rolling stats** | `rolling_mean_7`, `rolling_std_14` | Always - smooth noise |
| **Calendar** | `day_of_week`, `month`, `is_weekend` | When weekly/monthly seasonality |
| **Holiday** | `is_holiday`, `days_to_holiday` | Retail, service industries |
| **External** | `temperature`, `promo_flag` | When external data available |
| **Interaction** | `product_category month` | When patterns differ by group |

### Model Selection Guide

| Scenario | Recommended Model | Reason |
|----------|-------------------|--------|
| Many series (100+) | LightGBM | Scales well, handles features |
| Few series (1-10) with strong seasonality | Prophet | Built-in seasonality decomposition |
| Intermittent demand | Croston / SBA | Designed for sparse data |
| Ensemble approach | LightGBM + Prophet blend | Best accuracy, more complexity |
| Need explainability | LightGBM (SHAP) | Feature importance built-in |

## Notebook Conventions

### Cell Organization

```python
# Every notebook follows this pattern:
# 1. Title cell (markdown) with scenario name and timestamp
# 2. Import/setup cell
# 3. Configuration cell (all parameters in one place)
# 4. Processing cells with markdown explanations
# 5. Validation cells with data quality checks
# 6. Summary cell with output statistics
```

### Customization Markers

```python
# CUSTOMIZED: Changed lag window from 7 to 14 based on bi-weekly seasonality
lag_features = create_lag_features(df, lags=[7, 14, 21, 28])

# DEFAULT: Using standard clustering parameters
n_clusters = 5
```

### Validation After Each Notebook

```python
# Standard validation pattern
output_df = spark.read.table(f"{scenario}_prepared")
row_count = output_df.count()
null_count = output_df.filter(F.col(target_col).isNull()).count()
date_range = output_df.agg(F.min(date_col), F.max(date_col)).collect()[0]

print(f"[PASS] Output table: {scenario}_prepared")
print(f" Rows: {row_count:,}")
print(f" Nulls in target: {null_count}")
print(f" Date range: {date_range[0]} to {date_range[1]}")
```

## Livy Session Management

Same rules as `fabric-analytics` and `fabric-data-agent`:

```
1. Check for existing sessions FIRST (reuse idle sessions)
2. Create only if none exist (cold start: 3-6+ minutes)
3. Never close sessions unless explicitly requested
4. Use naming: forecasting-{scenario}-{timestamp}
5. Validate all code via Livy before including in final notebooks
```

## Error Handling

### Retry Protocol

```
Attempt 1 -> Execute via Livy
 (down) (on failure)
Attempt 2 -> Diagnose error, apply fix, retry
 (down) (on failure)
Attempt 3 -> Try alternative approach
 (down) (on failure)
Escalate to user with error details + options:
 A) Suggested fix
 B) Skip this cell and continue
 C) User provides guidance
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|---------|
| Not enough data | < 2 full seasons of history | Reduce forecast horizon or aggregate to coarser grain |
| Too many nulls | Missing dates in time series | Fill gaps in NB01 (forward fill or interpolation) |
| Memory error | Too many series features | Reduce feature set or process in batches |
| Optuna timeout | Hyperparameter search too long | Reduce `n_trials` or use early stopping |
| Cluster imbalance | One cluster gets 90% of series | Adjust `n_clusters` or try different algorithm |

## Output Artifacts

```
run/{scenario_name}_{YYYYMMDD}/
+-- Fabric 01 DataPreparation.ipynb
+-- Fabric 02 ProfilingIntermittent.ipynb
+-- Fabric 03 Clustering.ipynb
+-- Fabric 04 FeatureEngineering.ipynb
+-- Fabric 05 TrainTestSelectTune.ipynb
+-- completion_report.md
-- requirements.txt (if new dependencies)
```

## Anti-Patterns

- **Skip profiling**: Treating all series identically -> wrong model for intermittent data
- **Too many lags**: 100+ lag features -> overfitting, slow training
- **No train/test split**: Evaluating on training data -> inflated accuracy
- **Ignore data quality**: Missing dates, duplicates -> biased forecasts
- **Fixed parameters**: Using defaults without tuning -> suboptimal accuracy
- **No validation checkpoints**: Running all notebooks blindly -> catching errors too late

## Boundaries

### Always Do

- Gather inputs (workspace, lakehouse, table, scenario) before starting
- Profile data before choosing models
- Validate output after each notebook
- Get user approval for medium/high risk customizations
- Generate all code as reproducible notebooks
- Use timestamped output folders
- Document all customization decisions in completion report

### Ask First

- Structural changes (adding/removing notebooks, changing flow)
- Algorithm changes (swapping LightGBM for another model)
- New dependencies not in original requirements
- Skipping entire notebooks or major sections
- High-risk generative customizations

### Never Do

- Proceed without required inputs
- Save notebook code that hasn't been validated via Livy
- Overwrite original template notebooks
- Hardcode credentials or connection strings
- Assume column names without schema verification
- Skip user approval for medium/high risk changes

## Reference Index

| Document | Description |
|----------|-------------|
| [references/model-selection-guide.md](references/model-selection-guide.md) | Detailed model comparison and hyperparameter tuning |
| [references/feature-engineering-catalog.md](references/feature-engineering-catalog.md) | Complete feature engineering patterns and formulas |

## Asset Templates

| File | Description |
|------|-------------|
| [assets/completion-report-template.md](assets/completion-report-template.md) | Cross-phase handover document template |
| [assets/notebook-config-template.py](assets/notebook-config-template.py) | Standard configuration cell for all notebooks |
