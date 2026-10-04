---
name: vera-ai-image-reviewing
description: >-
  Runs data quality diagnostics and baseline image classification. Produces
  class distribution tables, sample image grids, image size and channel
  statistics, a baseline CNN or pre-trained feature extractor with Logistic
  Regression, weighted F1 and macro AUC (bootstrapped 95% CIs), confusion
  matrix, and ROC curves. Ends with a recommendation block listing additional
  models available in the analysis workflow. Outputs Python scripts with 2
  publication-quality plots. Triggered when user has image data and says
  "image classification," "computer vision," "CNN," "object recognition,"
  "medical imaging," "image detection," "visual recognition," "photo
  classification," "X-ray classification," or describes a task involving
  classifying images into categories. Does not handle free-text NLP or
  tabular-only data.
argument-hint: [dataset-path-or-description]
allowed-tools: Read, Bash, Write, Edit
---

# Image Classification --- Data Diagnostics & Baseline Modeling

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
- The task is supervised image classification with labeled folders or label metadata.
- A reproducible baseline is needed before transfer learning, ViT, or ensembles.

Do not use this skill when:
- The task is detection, segmentation, captioning, retrieval, video understanding, or generation.
- The dataset is so small that any result should be treated only as a smoke test, not a benchmark.
- The main signal is tabular metadata rather than image pixels.

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
   └── Imbalanced (minority < 10%) → weighted loss, data augmentation note

2. IMAGE SIZE STRATEGY
   ├── Uniform size → use directly
   └── Variable size → resize to common dimension (224x224 default)

3. BASELINE MODEL SELECTION
   ├── N ≥ 1000 → Simple CNN (train from scratch)
   └── N < 1000 → Pre-trained feature extractor (ResNet18) + LogReg
   # N=1000 threshold: below this, from-scratch CNNs typically overfit (too few examples
   # per parameter). ResNet18 is deliberately the smallest modern ResNet — large enough
   # to carry useful ImageNet features, small enough that feature-extraction + LogReg is
   # tractable on CPU. Larger backbones (ResNet50, ViT) are reserved for the analyzing skill.
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Image source** | Directory path, dataset name, or file format |
| **Label source** | Subdirectory names, CSV mapping, or metadata |
| **Image format** | PNG, JPEG, DICOM, etc. |
| **Number of classes** | Binary or multi-class |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Data Diagnostics          → plot_01_data_overview.png
PART 2: Baseline Classification   → plot_02_confusion_roc.png
PART 3: Recommendation Block      → text pointing to analysis workflow
```

## Reporting Standards

1. Metrics: weighted F1 and macro AUC (OVR) — always with 95% bootstrapped CIs
2. **For imbalanced classes (minority < 10%)**: also report **PR-AUC (Average Precision)** — primary discrimination metric under imbalance.
3. Format: "F1 = 0.XXX, 95% CI [0.XXX, 0.XXX]"; "PR-AUC = 0.XXX, 95% CI [..., ...]"
4. AUC: "AUC = 0.XXX, 95% CI [0.XXX, 0.XXX]"
5. Decimal places: 3 for F1/AUC, 1 for percentages, 0 for counts
6. Image dimensions: report as HxWxC
7. Sample size: report final analytic N (train/val/test split sizes)
8. Data augmentation: always report what augmentations were applied
9. Bootstrapped CIs: 1000 iterations, 2.5th/97.5th percentiles

## Models Available

| Status | Models |
|---|---|
| Implemented in this skill | Simple CNN (larger datasets) or ResNet18 feature extractor + Logistic Regression (small datasets) |
| Implemented downstream in `vera-ai-image-generating` | ResNet50, EfficientNet-B0, VGG16 (legacy replication only), DenseNet121, ViT-B/16, soft voting, stacking, GradCAM, attention maps |
| Planned but not yet shipped | ConvNeXt-Tiny is a roadmap item only; there is no open-source `src/` module for it yet |

## Example Dataset

torchvision built-ins: `CIFAR10`, `FashionMNIST`, `MNIST`.
Python: `from torchvision.datasets import CIFAR10`

## Configuration Defaults

Pipeline constants live in `config/default.json`. Read it before generation. Key knobs:

- `alpha`, `ci_level` — inference thresholds
- `plot_dpi`, `plot_width`, `plot_height` — figure dimensions
- `bootstrap_iterations` — bootstrap CIs for metrics
- `split.{test_size, val_size_of_train, random_state}` — data-split reproducibility
- `image.{resize, normalize_mean, normalize_std}` — preprocessing (ImageNet norms by default)
- `baseline.{N_threshold, small_N_model, large_N_model}` — N-dependent baseline choice (ResNet18 feature extractor for small N; simple CNN for large N)
- `augmentation.*` — train-time augmentation pipeline
- `class_balance_threshold` — minority-class rare-event threshold

To override: create `config/local.json`; the runtime merges local over default.

## Why These Defaults

- `baseline.N_threshold = 1000` is a practical overfitting guardrail, not a formal cutoff. Below that scale, frozen transfer features usually behave more predictably than a from-scratch CNN in open-source baseline runs.
- `image.resize = 224x224` and ImageNet normalization are defaults because they align with the shipped torchvision backbones and make the baseline comparable to the downstream transfer-learning models.
- PR-AUC is promoted under class imbalance for the same reason as the NLP and structured skills: ROC-AUC often looks healthier than the positive-class retrieval story when negatives dominate.

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-ai-image-reviewing` on a 2-4 class subset of CIFAR-10 or an equivalent `ImageFolder` dataset. Produce the standard T1 artifacts."
- Suggested fixture: 20-100 images per class for a CPU-only smoke test; use the ResNet18 feature-extractor branch if the sample is small.
- Expected pass condition: the run writes one runnable Python script, `methods.md`, `results.md`, `tables/`, `references.bib`, and the two baseline figures listed below.

## Cross-Skill Interface

```
Output:
├── code_python      → .py script
├── methods_md       → methods.md baseline fragment
├── results_md       → results.md baseline results fragment
├── tables/          → Markdown/CSV tables for dataset stats + metrics
├── figures/         → 2 PNGs (data overview + confusion/ROC)
├── references_bib   → .bib with baseline/evaluation citations
└── recommendations  → text block (what analysis workflow produces)
```

When this skill is used as `T1_baseline` inside `vera-ai-application-pipelining`,
the standardized track artifacts above are REQUIRED, not optional.
