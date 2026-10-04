---
name: vera-ai-image-generating
description: >-
  Server-side extension that completes the full analysis pipeline for image
  classification after vera-ai-image-reviewing has run. Adds ResNet50,
  EfficientNet-B0, VGG16, DenseNet121 CNN classifiers with transfer learning
  (feature extraction and full fine-tuning), subgroup analysis by metadata
  or image properties, advanced models (ViT transformer with optional
  tabular fusion and hyperparameter search), ensemble methods,
  cross-method comparison with unified feature attribution (GradCAM,
  attention maps) on a 0-100 scale, and manuscript-ready methods.md and
  results.md. Applies output variation and code style diversity for
  natural, non-repetitive output. Open-source skill. Triggered after vera-ai-image-reviewing completes
  and its PART 0–2 artifacts are present (see ../../CROSS-SKILL-INTERFACE.md). If invoked directly
  without those artifacts, halts and prompts the user to run testing first or supply equivalent PART 0–2
  code.
argument-hint: [testing-output-dir-or-dataset]
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Image Classification --- Full Analysis & Manuscript Generation

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
- `vera-ai-image-reviewing` has already produced the baseline artifacts.
- The task is supervised image classification and the user wants transfer learning, ViT, ensembles, and interpretability.

Do not use this skill when:
- The task is detection, segmentation, captioning, retrieval, generation, or video.
- The user expects every contemporary vision backbone; this open-source build only guarantees the methods listed below.
- Hardware limits make anything beyond feature-extraction smoke tests unrealistic.

## Workflow

Continues from where vera-ai-image-reviewing stopped (PART 0-2 done).

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Additional CNN models | Run Additional Models | Main Agent | `workflow/step04-run-additional-models.md` | Prior step output | PART 3 code + prose |
| Subgroup | Analyze Subgroups | Main Agent | `workflow/step05-analyze-subgroups.md` | Prior step output | PART 4 code + prose |
| Advanced models | Fit Advanced Models | Main Agent | `workflow/step06-fit-advanced-models.md` | Prior step output | PART 5 code + prose |
| Comparison | Compare Models | Main Agent | `workflow/step07-compare-models.md` | Prior step output | PART 6 code + prose |
| Manuscript | Generate Manuscript | Main Agent | `workflow/step08-generate-manuscript.md` | Prior step output | methods.md + results.md |

## Additional Inputs

Collect if not already provided:
- Target discipline (for reporting conventions)
- Target journal or style (CVPR, ECCV, MICCAI, NeurIPS, etc.)
- Research question / hypothesis
- Subgroup variable or image property for stratification
- Image dimensions (HxWxC) and any DICOM metadata if medical imaging

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
| `reference/rules/reporting-standards.md` | Hard rules for CNN/ViT reporting |

## Reporting Standards

Same as vera-ai-image-reviewing, plus:
- All models: report F1 (weighted) and AUC (macro) with bootstrapped 95% CIs
- Transfer learning: report backbone name, pre-trained weights, frozen vs fine-tuned layers
- Training: report epochs, best epoch, learning rate, batch size, data augmentation pipeline
- ViT: report pre-trained model name, patch size, whether backbone was frozen
- Image input: report HxWxC dimensions, normalization (mean/std), parameter counts, FLOPs
- Feature attribution: unified 0-100 scale via GradCAM (CNNs) and attention maps (ViT)
- Model comparison: frame as convergent findings, not horse race
- Small dataset CNN: frame as "exploratory"; never claim generalizability
- Medical imaging: report DICOM preprocessing, windowing, DenseNet rationale

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | ResNet50, EfficientNet-B0, VGG16, DenseNet121, ViT-B/16, soft voting, stacking, GradCAM, ViT attention maps |
| Legacy-only support | VGG16 is kept for replication and sanity-check comparisons, not as a recommended modern default |
| Planned but not yet shipped | ConvNeXt-Tiny is not part of the open-source engine yet |

## Configuration Defaults

Pipeline constants live in `config/default.json`. Read it before generation. Key knobs in addition to the testing-skill config:

- `transfer.{backbones, frozen_below_N, fine_tune_above_N}` — N-dependent feature-extraction vs fine-tuning decision
- `backbones.*` — ResNet50, EfficientNet-B0, VGG16, DenseNet121, ViT hyperparameters
- `training.{epochs, batch_size, learning_rate, optimizer, scheduler}` — defaults per backbone
- `augmentation.{train_pipeline, test_pipeline}` — augmentation recipe
- `gpu.{required, fallback_to_cpu}` — CPU fallback behavior (see GPU Availability below)
- `interpretability.{gradcam_layer, vit_attention}` — explanation method per model class

To override: create `config/local.json`.

## Why These Defaults

- The transfer-learning split between feature extraction and full fine-tuning exists to keep small-data runs from overclaiming what the labels can support.
- ViT is intentionally narrowed to ViT-B/16 because that is the variant implemented in `src/dl_vit.py`; the skill should not imply broader transformer coverage than the code actually ships.
- Small-dataset CNN results stay marked "exploratory" because backbone capacity can easily outrun the evidence available in limited image collections.

## GPU Availability

Check at workflow step 06 (advanced models) start. Implementation pattern:

```python
import torch
GPU_AVAILABLE = torch.cuda.is_available()
if not GPU_AVAILABLE:
    print("WARNING: CUDA not available. Fine-tuning large backbones on CPU is impractical.")
    print("Falling back to ResNet18/ResNet50 feature-extraction mode only (frozen backbones + LogReg head).")
    TRAINING_MODE = "feature_extraction_only"
else:
    TRAINING_MODE = "full"
```

Always log the decision to `RESEARCH_LOG.md` so the manuscript methods section can note training environment.

## Minimal Smoke Test

- Smoke-test prompt: "Continue from `vera-ai-image-reviewing` on a 2-4 class CIFAR-10 or `ImageFolder` subset. Produce the transfer-learning, advanced-model, and manuscript-ready artifacts."
- CPU pass condition: the skill logs that large-model fine-tuning is impractical and falls back to feature-extraction mode. GPU-heavy steps may be reduced, but the artifact contract must still be satisfied.
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
