---
name: vera-ai-structured-reviewing
description: >-
  Runs data quality diagnostics and baseline classification/regression for
  structured (tabular) data. Produces missing value analysis, feature
  distributions, correlation matrix, class balance check, outlier detection,
  a baseline LightGBM classifier with weighted F1 and macro AUC (bootstrapped
  95% CIs), feature importance, confusion matrix, and ROC curves. Ends with
  a recommendation block listing additional models available in the analysis
  workflow. Outputs Python scripts with 2 publication-quality plots. Triggered when user
  has tabular/structured data and says "tabular data," "structured data,"
  "classification," "regression," "feature engineering," "predict from columns,"
  "CSV classification," "spreadsheet," "predict outcome," or describes a task
  involving predicting from numeric/categorical columns. Does not handle
  free-text NLP or image data.
argument-hint: [dataset-path-or-description]
allowed-tools: Read, Bash, Write, Edit
---

# Structured Data --- Data Quality Diagnostics & Baseline Modeling

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Workflow](#workflow)
- [Decision Tree](#decision-tree)
- [Required Inputs](#required-inputs)
- [Code Structure](#code-structure)
- [Reporting Standards](#reporting-standards)
- [Models Available](#models-available)
- [Example Dataset](#example-dataset)
- [Configuration Defaults](#configuration-defaults)
- [Why These Defaults](#why-these-defaults)
- [Minimal Smoke Test](#minimal-smoke-test)
- [Cross-Skill Interface](#cross-skill-interface)


Open-source skill.

## Scope Boundary

Use this skill when:
- The task is supervised prediction from row-column data with a single target.
- A strong tabular baseline is needed before trying a larger model battery.

Do not use this skill when:
- The main problem is causal inference, survival analysis, time series, panel data, or repeated measures.
- The feature space is mostly free text or images rather than tabular columns.
- The dataset is so small or leakage-prone that a simple baseline can only be interpreted as exploratory.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Baseline | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks + T1 track artifacts |

## Decision Tree

```
1. TASK TYPE
   ├── Classification (target is categorical) → F1 + AUC metrics
   └── Regression (target is continuous) → RMSE + R² metrics

2. CHECK CLASS BALANCE (classification only)
   ├── Balanced (minority ≥ 10%) → standard methods
   └── Imbalanced (minority < 10%) → class weighting, note power limits
   # 10% threshold: widely used heuristic for "mild" vs "severe" imbalance in tabular ML
   # (matches sklearn's `class_weight='balanced'` becoming materially different below this mark).
   # Not a strict rule — rare events < 1% may warrant additional treatments (SMOTE, Firth).

3. FEATURE TYPES
   ├── All numeric → standard scaling
   ├── Mixed (numeric + categorical) → encoding + scaling
   └── High cardinality categorical → target encoding or frequency encoding
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Target column** | Column name, type (classification/regression) |
| **Feature columns** | List or "all except target" |
| **Task type** | Classification or regression |
| **ID column** | To exclude from features (optional) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Data Quality Diagnostics   → plot_01_data_overview.png
PART 2: Baseline Classification    → plot_02_confusion_roc.png
PART 3: Recommendation Block       → text pointing to analysis workflow
```

## Reporting Standards

1. Classification: weighted F1 and macro AUC (OVR) --- always with 95% bootstrapped CIs
2. **For imbalanced classes (minority < 10%)**: also report **PR-AUC (Average Precision)** alongside F1 and ROC-AUC. PR-AUC is the primary discrimination metric under severe class imbalance because it is not inflated by true negatives.
3. Regression: RMSE and R² with 95% bootstrapped CIs; also report MAE (equally primary — more robust to outliers than RMSE when the loss is symmetric in absolute error).
4. Format: "F1 = 0.XXX, 95% CI [0.XXX, 0.XXX]"
5. Feature importance: top 20 features by gain, normalized 0-100
6. Decimal places: 3 for metrics, 1 for percentages, 0 for counts
7. Sample size: report final analytic N (train/val/test split sizes)
8. Non-significance: "not statistically significant at alpha = .05" --- never "no difference"

## Models Available

| Status | Models |
|---|---|
| Implemented in this skill | LightGBM baseline for classification or regression |
| Implemented downstream in `vera-ai-structured-generating` | Logistic Regression / Ridge, SVM / SVR, Random Forest, XGBoost, LightGBM, CatBoost, MLP, TabNet, stacking, weighted voting |
| Not implied by this open-source build | Any method not named above should be treated as out of scope until a corresponding module exists in `src/` |

## Example Dataset

sklearn built-ins: `load_breast_cancer()` (binary), `load_iris()` (multi-class), `load_wine()` (multi-class).
Python: `from sklearn.datasets import load_breast_cancer`

## Configuration Defaults

Pipeline constants live in `config/default.json`. Read it before generation. Key knobs:

- `alpha`, `ci_level` — inference thresholds
- `plot_dpi`, `plot_width`, `plot_height` — figure dimensions
- `bootstrap_iterations` — bootstrap CIs for metrics
- `split.{test_size, val_size_of_train, random_state}` — data-split reproducibility
- `baseline_model.*` — LightGBM baseline hyperparameter grid
- `imputation.{numeric, categorical}` — default imputation strategy (median/mode)
- `class_balance_threshold` — minority-class rare-event threshold
- `task_type` — "classification" or "regression" (affects metrics and models)

To override: create `config/local.json`; the runtime merges local over default.

## Why These Defaults

- LightGBM is the baseline because it handles mixed tabular features well, gives a credible first-pass nonlinear model, and stays much cheaper than a full model battery for open-source smoke tests.
- Median/mode imputation is the default because it is transparent, deterministic, and easy to keep inside a train-fold-only preprocessing pipeline.
- PR-AUC is promoted under class imbalance because ROC-AUC can remain deceptively high when the negative class dominates.

## Minimal Smoke Test

- Classification smoke test: "Run `vera-ai-structured-reviewing` on `load_breast_cancer()` with the target as label and all other columns as features. Produce the standard T1 artifacts."
- Regression smoke test: "Run `vera-ai-structured-reviewing` on `load_diabetes()` with the target as outcome and all other columns as features. Produce the regression T1 artifacts."
- Expected pass condition: the run writes one runnable Python script, `methods.md`, `results.md`, `tables/`, `references.bib`, and either the classification or regression baseline plot set.

## Cross-Skill Interface

```
Output:
├── code_python      → .py script
├── methods_md       → methods.md baseline fragment
├── results_md       → results.md baseline results fragment
├── tables/          → Markdown/CSV tables for diagnostics + metrics
├── figures/         → 2 PNGs (data overview + confusion/ROC)
├── references_bib   → .bib with baseline/evaluation citations
└── recommendations  → text block (what analysis workflow produces)
```

When this skill is used as `T1_baseline` inside `vera-ai-application-pipelining`,
the standardized track artifacts above are REQUIRED, not optional.
