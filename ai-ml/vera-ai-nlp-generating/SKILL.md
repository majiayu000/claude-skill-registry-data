---
name: vera-ai-nlp-generating
description: >-
  Server-side extension that completes the full analysis pipeline for NLP
  text classification after vera-ai-nlp-reviewing has run. Adds SVM, Random
  Forest, LightGBM classifiers with TF-IDF and optional extra features,
  subgroup analysis by metadata or text properties, deep learning models
  (GRU, TextCNN, ALBERT with optional tabular fusion and hyperparameter
  search), cross-method comparison with unified feature importance on a 0-100
  scale, and manuscript-ready methods.md and results.md. Applies output
  variation and code style diversity for natural, non-repetitive output.
  Open-source skill. Triggered after vera-ai-nlp-reviewing completes and its PART 0–2 artifacts are
  present (see ../../CROSS-SKILL-INTERFACE.md). If invoked directly without those artifacts,
  halts and prompts the user to run testing first or supply equivalent PART 0–2 code.
argument-hint: [testing-output-dir-or-dataset]
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# NLP Text Classification --- Full Analysis & Manuscript Generation

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Workflow](#workflow)
- [Additional Inputs](#additional-inputs)
- [Output Structure](#output-structure)
- [Key References (read before generation)](#key-references-read-before-generation)
- [Reporting Standards](#reporting-standards)
- [Method Status](#method-status)
- [Configuration Defaults](#configuration-defaults)
- [Why These Defaults](#why-these-defaults)
- [GPU Availability](#gpu-availability)
- [Minimal Smoke Test](#minimal-smoke-test)
- [Cross-Skill Interface](#cross-skill-interface)


Open-source skill. Read `reference/specs/output-variation-protocol.md`
before every generation --- apply all variation layers for natural, diverse output.

## Scope Boundary

Use this skill when:
- `vera-ai-nlp-reviewing` has already established a credible baseline and the user wants a fuller model battery.
- The task is supervised text classification, optionally with a small set of numeric side features.

Do not use this skill when:
- The task is generation, retrieval, summarization, sequence labeling, or prompt-only classification.
- The desired method is not in the shipped model list below.
- The available hardware cannot support anything beyond CPU smoke testing and the user expects transformer-scale benchmarking.

## Workflow

Continues from where vera-ai-nlp-reviewing stopped (PART 0-2 done).

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
- Target journal or style (ACL, EMNLP, NeurIPS, etc.)
- Research question / hypothesis
- Subgroup variable or text property for stratification

## Output Structure

```
output/
├── methods.md
├── results.md
├── tables/             ← Markdown + CSV per table
├── figures/            ← PNGs, 300 DPI
├── references.bib
└── code.py             ← Style-varied
```

## Key References (read before generation)

| File | Purpose |
|---|---|
| `reference/specs/output-variation-protocol.md` | Output quality variation layers |
| `reference/specs/code-style-variation.md` | Seven-dimension code style diversity |
| `reference/patterns/sentence-bank.md` | 4-6 phrasings per result type |
| `reference/rules/reporting-standards.md` | Hard rules for ML/DL reporting |

## Reporting Standards

Same as vera-ai-nlp-reviewing, plus:
- All models: report F1 (weighted) and AUC (macro) with bootstrapped 95% CIs
- Deep learning: report training epochs, best epoch, learning rate, batch size
- ALBERT: report pre-trained model name, whether base was frozen
- Feature importance: unified 0-100 scale across ML and DL models
- Model comparison: frame as convergent findings, not horse race
- Tree-based with small N: frame as "exploratory"; never claim generalizability

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | SVM, Random Forest, LightGBM, GRU, TextCNN, ALBERT |
| Implemented optional variants | Text + extra-feature fusion where the corresponding `*_extra.py` module exists |
| Not shipped in the open-source build | BERT, RoBERTa, DeBERTa, SetFit, prompt-only classifiers, few-shot API-based methods |

## Configuration Defaults

Pipeline constants live in `config/default.json`. Read it before generation. Adds to the testing-skill config:

- `ml_models.*` — SVM/RF/LightGBM hyperparameter grids
- `deep_models.*` — GRU/TextCNN/ALBERT hyperparameter grids, epochs, batch size, learning rate
- `gpu.{required_for, fallback_models}` — e.g., ALBERT requires GPU; falls back to GRU+TextCNN if unavailable (see GPU Availability section below)
- `feature_importance.scale` (0, 100) — unified scale across model families
- `subgroup.{min_size, interaction_alpha}` — subgroup-analysis gating

To override: create `config/local.json`.

## Why These Defaults

- ALBERT is the shipped transformer because it is materially lighter than full BERT-style baselines while still exercising a modern contextual encoder path.
- GRU + TextCNN are the CPU fallback because they preserve two complementary inductive biases, sequential recurrence and local n-gram filters, without pretending a transformer run happened.
- Tree-based models on sparse text remain marked "exploratory" at small N because they are useful robustness checks, not generally the most defensible primary NLP model.

## GPU Availability

Check at workflow step 06 (advanced models) start. Implementation pattern:

```python
import torch
GPU_AVAILABLE = torch.cuda.is_available()
MODELS_TO_FIT = ["GRU", "TextCNN"] + (["ALBERT"] if GPU_AVAILABLE else [])
if not GPU_AVAILABLE:
    print("NOTE: CUDA not available; falling back to GRU + TextCNN. ALBERT skipped.")
```

Do NOT silently proceed without a model — the fallback must always include at least GRU + TextCNN on CPU.

## Minimal Smoke Test

- Smoke-test prompt: "Continue from `vera-ai-nlp-reviewing` on a 4-class 20 Newsgroups subset. Fit the additional ML models and the CPU-safe deep models, then produce the manuscript-ready artifacts."
- CPU pass condition: SVM, Random Forest, LightGBM, GRU, and TextCNN run; ALBERT may be skipped if CUDA is unavailable, but the fallback decision must be logged.
- Expected artifacts: `methods.md`, `results.md`, `tables/`, `figures/`, `references.bib`, and one consolidated `code.py`.

## Cross-Skill Interface

```
Method Unit Contract:
├── code_python      → .py script (style-varied)
├── methods_md       → methods.md (varied structure)
├── results_md       → results.md (varied phrasing)
├── tables/          → Markdown + CSV
├── figures/         → PNGs 300 DPI (varied layout)
├── references_bib   → .bib with cited references
└── comparison       → cross-method narrative (in results.md)
```
