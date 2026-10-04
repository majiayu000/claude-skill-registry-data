---
name: vera-ai-nlp-reviewing
description: >-
  Runs class balance diagnostics and baseline text classification for NLP
  tasks. Produces class distribution tables, text length statistics,
  vocabulary analysis, TF-IDF feature inspection, a baseline Logistic
  Regression classifier with weighted F1 and macro AUC (bootstrapped 95%
  CIs), confusion matrix, and ROC curves. Ends with a recommendation
  block listing additional models and analyses available in the analysis
  workflow. Outputs Python scripts with 2 publication-quality plots. Triggered when
  user has text data and says "text classification," "NLP," "sentiment
  analysis," "AI detection," "language model detection," "document
  classification," "spam detection," "text mining," "topic classification,"
  or describes a task involving classifying text into categories.
  Does not handle structured/tabular-only data or image data.
argument-hint: [dataset-path-or-description]
allowed-tools: Read, Bash, Write, Edit
---

# NLP Text Classification --- Data Diagnostics & Baseline Modeling

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
- The task is supervised text classification with labeled examples.
- A lightweight, reproducible baseline is the right first checkpoint before deeper models.

Do not use this skill when:
- The task is generation, summarization, retrieval, topic modeling, or sequence labeling.
- Labels are absent, extremely sparse, or only available through prompt-based weak supervision.
- The core signal lives primarily in images, structured covariates, or temporal ordering rather than text.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Baseline | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks + T1 track artifacts |

## Decision Tree

```
1. CHECK CLASS BALANCE
   ├── Balanced (minority ≥ 10%) → standard methods
   └── Imbalanced (minority < 10%) → class weighting, note power limits

2. TEXT FEATURE STRATEGY
   ├── Vocab size < 50k → standard TF-IDF (max_features=10000)
   └── Vocab size ≥ 50k → sublinear TF-IDF with min_df=5
   # 10k features is the baseline default because it keeps sparse linear models
   # CPU-friendly while still covering common unigrams/bigrams in small-to-mid NLP datasets.
   # The 50k vocabulary gate is a heuristic: once the raw vocabulary gets very large,
   # sublinear TF-IDF and min_df filtering usually stabilize the baseline more than
   # throwing additional rare terms at Logistic Regression.

3. EXTRA FEATURES
   ├── Available → text + extra (augmented matrix)
   └── Not available → text-only (TF-IDF)
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Text column** | Column name containing text data |
| **Label column** | Target variable, number of classes |
| **Group column** | For group-aware splitting (optional) |
| **Extra features** | Numeric columns for augmentation (optional) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Data Diagnostics          → plot_01_data_overview.png
PART 2: Baseline Classification   → plot_02_confusion_roc.png
PART 3: Recommendation Block      → text pointing to analysis workflow
```

## Reporting Standards

1. Metrics: weighted F1 and macro AUC (OVR) — always with 95% bootstrapped CIs
2. Format: "F1 = 0.XXX, 95% CI [0.XXX, 0.XXX]"
3. AUC: "AUC = 0.XXX, 95% CI [0.XXX, 0.XXX]"
4. Decimal places: 3 for F1/AUC/p-values, 1 for percentages, 0 for counts
5. Proportions: report as percentages with 1 decimal
6. Sample size: report final analytic N (train/val/test split sizes)
7. Non-significance: "not statistically significant at alpha = .05" — never "no difference"
8. Bootstrapped CIs: 1000 iterations, 2.5th/97.5th percentiles
9. **For imbalanced classes (minority < 10% of total, or per-class < 20%)**: report **Precision–Recall AUC (PR-AUC / Average Precision)** alongside F1 and ROC-AUC. PR-AUC is more informative than ROC-AUC when the positive class is rare because it does not reward true-negative inflation. Use `sklearn.metrics.average_precision_score` with macro averaging for multi-class. Frame in results as "For class imbalance, PR-AUC is the primary discrimination metric; ROC-AUC is reported for comparability with prior work."

## Models Available

| Status | Models |
|---|---|
| Implemented in this skill | Logistic Regression on TF-IDF features, optionally augmented with extra numeric metadata |
| Implemented downstream in `vera-ai-nlp-generating` | SVM, Random Forest, LightGBM, GRU, TextCNN, ALBERT |
| Not shipped in the open-source build | BERT, RoBERTa, DeBERTa, SetFit, prompt-only classifiers, GPT/Claude few-shot pipelines |

## Example Dataset

Any text classification dataset. Default: 20 Newsgroups (sklearn).
Python: `from sklearn.datasets import fetch_20newsgroups`

## Configuration Defaults

Pipeline constants live in `config/default.json`. Read it before generation — values there override anything in this SKILL.md. Key knobs:

- `alpha` (0.05), `ci_level` (0.95) — inference thresholds
- `plot_dpi` (300), `plot_width`, `plot_height` — figure dimensions
- `bootstrap_iterations` (1000) — bootstrap CIs for metrics
- `split.{test_size, val_size_of_train, random_state}` — data-split reproducibility
- `tfidf.{max_features, ngram_range, sublinear_tf, min_df}` — text featurization
- `baseline_model.*` — LogReg baseline hyperparameter grid
- `class_balance_threshold` (0.10) — minority-class threshold for rare-event warning

To override: create `config/local.json`; the runtime merges local over default.

## Why These Defaults

- `class_balance_threshold = 0.10` is a warning heuristic, not a theorem. Below about 10% minority prevalence, weighted F1 and ROC-AUC often look healthier than the actual positive-class retrieval story, so the skill promotes PR-AUC in that regime.
- `bootstrap_iterations = 1000` is the default compromise between stable percentile intervals and a baseline run that still finishes comfortably on CPU.
- `tfidf.max_features = 10000` keeps the baseline sparse-linear model reproducible and fast enough for smoke tests while still covering the dominant unigram/bigram signal in most benchmark-scale corpora.

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-ai-nlp-reviewing` on a 4-class subset of `fetch_20newsgroups`, using the text as input and the target as label. Produce the standard T1 baseline artifacts."
- Suggested fixture: 200-1000 rows total, 50-250 rows per class, no extra features required.
- Expected pass condition: the run writes one runnable Python script, `methods.md`, `results.md`, `tables/`, `references.bib`, and the two baseline figures listed below.

## Cross-Skill Interface

```
Output:
├── code_python      → .py script
├── methods_md       → methods.md baseline fragment
├── results_md       → results.md baseline results fragment
├── tables/          → Markdown/CSV tables for class balance + metrics
├── figures/         → 2 PNGs (class balance + confusion/ROC)
├── references_bib   → .bib with baseline/evaluation citations
└── recommendations  → text block (what analysis workflow produces)
```

When this skill is used as `T1_baseline` inside `vera-ai-application-pipelining`,
the standardized track artifacts above are REQUIRED, not optional.
