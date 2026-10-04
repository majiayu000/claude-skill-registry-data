---
name: vera-ai-structured-generating
description: >-
  Server-side extension that completes the full analysis pipeline for
  structured/tabular data after vera-ai-structured-reviewing has run. Adds SVM,
  Random Forest, XGBoost, LightGBM, CatBoost classifiers/regressors with
  missing value imputation, encoding, and scaling, subgroup analysis by
  metadata variables, deep learning models (MLP, TabNet with optional
  hyperparameter search), stacking ensemble with meta-learner, cross-method
  comparison with unified feature importance on a 0-100 scale, and
  manuscript-ready methods.md and results.md. Supports BOTH classification
  (F1/AUC) AND regression (RMSE/R2/MAE). Applies output variation and
  code style diversity for natural, non-repetitive output. Open-source
  skill. Triggered after vera-ai-structured-reviewing completes and its PART 0–2 artifacts are present
  (see ../../CROSS-SKILL-INTERFACE.md). If invoked directly without those artifacts, halts and
  prompts the user to run testing first or supply equivalent PART 0–2 code.
argument-hint: [testing-output-dir-or-dataset]
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Structured/Tabular Data --- Full Analysis & Manuscript Generation

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Workflow](#workflow)
- [Additional Inputs](#additional-inputs)
- [Output Structure](#output-structure)
- [Key References (read before generation)](#key-references-read-before-generation)
- [Reporting Standards](#reporting-standards)
- [Method Status](#method-status)
- [Leakage Guards (MANDATORY — must appear verbatim in generated code)](#leakage-guards-mandatory-—-must-appear-verbatim-in-generated-code)
- [Task-Type Branching (Classification vs Regression)](#task-type-branching-classification-vs-regression)
- [Configuration Defaults](#configuration-defaults)
- [Why These Defaults](#why-these-defaults)
- [Minimal Smoke Test](#minimal-smoke-test)
- [Cross-Skill Interface](#cross-skill-interface)


Open-source skill. Read `reference/specs/output-variation-protocol.md`
before every generation --- apply all variation layers for natural, diverse output.

## Scope Boundary

Use this skill when:
- `vera-ai-structured-reviewing` has already established the target type and baseline.
- The goal is supervised tabular prediction with a richer model battery and cross-method comparison.

Do not use this skill when:
- The task is survival analysis, time series, repeated measures, causal estimation, or multimodal modeling where text/images dominate.
- The dataset cannot support anything beyond exploratory modeling.
- A method is desired that is not explicitly listed in the status table below.

## Workflow

Continues from where vera-ai-structured-reviewing stopped (PART 0-2 done).

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Additional ML models | Run Additional Models | Main Agent | `workflow/step04-run-additional-models.md` | Prior step output | PART 3 code + prose |
| Subgroup | Analyze Subgroups | Main Agent | `workflow/step05-analyze-subgroups.md` | Prior step output | PART 4 code + prose |
| Deep learning | Fit Advanced Models | Main Agent | `workflow/step06-fit-advanced-models.md` | Prior step output | PART 5 code + prose |
| Comparison | Compare Models | Main Agent | `workflow/step07-compare-models.md` | Prior step output | PART 6 code + prose |
| Manuscript | Generate Manuscript | Main Agent | `workflow/step08-generate-manuscript.md` | Prior step output | methods.md + results.md |

## Additional Inputs

Collect if not already provided:
- Target discipline (for reporting conventions)
- Target journal or style (JMLR, NeurIPS, ICML, domain journal, etc.)
- Research question / hypothesis
- Task type: classification or regression
- Subgroup variable for stratification

## Output Structure

```
output/
├── methods.md
├── results.md
├── tables/             <- Markdown + CSV per table
├── figures/            <- PNGs, 300 DPI
├── references.bib
└── code.py             <- Style-varied
```

## Key References (read before generation)

| File | Purpose |
|---|---|
| `reference/specs/output-variation-protocol.md` | Output quality variation layers |
| `reference/specs/code-style-variation.md` | Seven-dimension code style diversity |
| `reference/patterns/sentence-bank.md` | 4-6 phrasings per result type |
| `reference/rules/reporting-standards.md` | Hard rules for ML/DL reporting |

## Reporting Standards

Same as vera-ai-structured-reviewing, plus:
- Classification: report F1 (weighted) and AUC (macro) with bootstrapped 95% CIs
- Regression: report RMSE, R2, and MAE with bootstrapped 95% CIs
- Deep learning: report training epochs, best epoch, learning rate, batch size
- TabNet: report n_steps, n_a, n_d, relaxation factor, sparsity coefficient
- Feature importance: unified 0-100 scale across ML and DL models
  - LogReg: |coefficients| rescaled
  - SVM: permutation importance
  - RF: Gini importance
  - XGBoost/LightGBM/CatBoost: gain-based importance
  - MLP: permutation importance
  - TabNet: built-in attention masks
- Model comparison: frame as convergent findings, not horse race
- Stacking ensemble: report base learners, meta-learner, CV strategy
- Tree-based with small N: frame as "exploratory"; never claim generalizability

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Logistic Regression / Ridge, SVM / SVR, Random Forest, XGBoost, LightGBM, CatBoost, MLP, TabNet, stacking, weighted voting |
| Implemented task branches | Classification and regression, as routed by `task_type` |
| Not implied beyond this list | Treat any unlisted tabular model family as out of scope until a matching `src/` module exists |

## Leakage Guards (MANDATORY — must appear verbatim in generated code)

Two leakage paths are common in tabular pipelines and MUST be blocked explicitly. Generated code MUST use `sklearn.pipeline.Pipeline` (or `ColumnTransformer` + `Pipeline`) so that any `fit` is confined to the training fold:

1. **Target encoding leakage.** High-cardinality categorical features encoded by target mean MUST be fit on train only, never on the full dataset. Inside cross-validation, target encoding is fit **inside each fold**, not once globally. Use `category_encoders.TargetEncoder` inside a `Pipeline`, or K-fold out-of-fold target encoding (`sklearn.preprocessing.TargetEncoder` with `cv` argument). NEVER compute `df['target_enc'] = df.groupby('cat')['y'].transform('mean')` before splitting — that leaks the test target into train features.

2. **Stacking meta-learner leakage.** The meta-learner MUST be trained on **out-of-fold (OOF) predictions** from the base learners, never on in-fold predictions. Use `sklearn.ensemble.StackingClassifier` / `StackingRegressor` with `cv=5` (default generates OOF) — this is correct by construction. When writing stacking manually: (a) split train into K folds, (b) for each fold, fit base learners on K−1 folds and predict on the held-out fold, (c) concatenate the K held-out prediction vectors into the OOF matrix used as meta-learner features, (d) refit base learners on full train for inference. NEVER train the meta-learner on predictions from models that saw those same rows during fitting.

Also standard: fit imputer, scaler, and encoder on train-fold only (all via `Pipeline`); never refit on test or on combined train+test.

## Task-Type Branching (Classification vs Regression)

This skill supports both classification and regression. The `task_type` key in `config/default.json` (or detected from the testing-skill output) determines which branch of the workflow runs:

| Step | Classification branch | Regression branch |
|---|---|---|
| 04 — Additional tests | Class-balanced metrics, per-class F1/AUC, confusion matrix | Residual normality, heteroscedasticity, QQ plots |
| 05 — Subgroups | Stratified F1/AUC, interaction via logistic | Stratified RMSE/R², interaction via OLS |
| 06 — Models | LogReg, SVC, RF, XGBoost, CatBoost, LightGBM, MLP, TabNet, Stacking | Ridge/Lasso, SVR, RandomForestRegressor, XGBoostReg, CatBoostReg, LightGBMReg, MLPRegressor, TabNetRegressor, Stacking |
| 07 — Comparison | F1 (weighted) + AUC (macro) with bootstrap CIs, calibration | RMSE, R², MAE with bootstrap CIs, predicted-vs-actual plot |
| 08 — Manuscript | "Classification metrics" phrasing; ROC, PR, confusion-matrix figures | "Regression metrics" phrasing; residual, QQ, predicted-vs-actual figures |

Classifier-specific reporting (calibration, threshold selection, confusion matrix) is skipped for regression; regression-specific reporting (residual diagnostics, heteroscedasticity) is skipped for classification. Each workflow file (04–08) MUST check `task_type` before emitting code.

## Configuration Defaults

Pipeline constants live in `config/default.json`. Read it before generation. Key knobs in addition to the testing-skill config:

- `task_type` — "classification" or "regression" (see section above)
- `ml_models.classification.*`, `ml_models.regression.*` — per-task hyperparameter grids
- `deep_models.{MLP, TabNet}.*` — DL hyperparameters
- `stacking.{base_learners, meta_learner, cv_folds}` — ensemble recipe
- `feature_importance.scale` (0, 100) — unified scale across model families

To override: create `config/local.json`.

## Why These Defaults

- `cv=5` for stacking is the default because it is the smallest fold count that usually gives stable out-of-fold meta-features without turning baseline runs into a compute sink.
- CatBoost is kept as a first-class method because native categorical handling removes a large amount of brittle feature engineering from the open-source path.
- Ridge is the default linear regression baseline because it is numerically better behaved than unconstrained OLS once the feature set gets moderately wide after encoding.

## Minimal Smoke Test

- Smoke-test prompt: "Continue from `vera-ai-structured-reviewing` on `load_breast_cancer()` or `load_diabetes()`. Fit the full additional tabular model battery, produce the unified artifacts, and keep all preprocessing inside train-fold-only pipelines."
- Expected pass condition: at least one linear model, one tree ensemble, one neural model, and one ensemble method complete without violating the leakage guards.
- Expected artifacts: `methods.md`, `results.md`, `tables/`, `figures/`, `references.bib`, and one consolidated `code.py`.

## Cross-Skill Interface

```
Method Unit Contract:
├── code_python      -> .py script (style-varied)
├── methods_md       -> methods.md (varied structure)
├── results_md       -> results.md (varied phrasing)
├── tables/          -> Markdown + CSV
├── figures/         -> PNGs 300 DPI (varied layout)
├── references_bib   -> .bib with cited references
└── comparison       -> cross-method narrative (in results.md)
```
