---
name: geco
description: Evaluates geometric consistency in text-to-video generation by measuring structural and motion coherence across camera trajectories, detecting deformation and occlusion artifacts in static scenes. Use when the user has predictions and gold and needs to compute Fused.
metadata:
  skill_kind: metric
  source_arxiv: 2512.22274
  bibtex_key: gu2025geco
  confidence: high
---

# geco

> GeCo: A Differentiable Geometric Consistency Metric for Video Generation — Gu et al. (2025) (arXiv:2512.22274, 2025)

## What this evaluates

Evaluates geometric consistency in text-to-video generation by measuring structural and motion coherence across camera trajectories, detecting deformation and occlusion artifacts in static scenes.

## Datasets

- **GeCo-Eval** — total 80; splits: test (80)

## Metrics

- `Structure` — range: [0, 1]
  - Measures structural inconsistency (e.g., deformation, occlusion) averaged over pixels with valid depth and covisibility within evaluation windows. Lower is better.
- `Motion` — range: [0, 1]
  - Measures motion inconsistency (e.g., non-rigid drift) averaged over valid pixels. Lower is better.
- `Fused` **(primary)** — range: [0, 1]
  - Combines structure and motion inconsistency scores into a single geometric consistency metric. Lower is better.

## Input / output format

**Input**: Text prompt and generated video frames (resampled to ≤8 FPS), with depth maps and covisibility masks computed for evaluation.

**Output**: Scalar geometric consistency score per clip (Structure, Motion, or Fused), computed as a frame-weighted average over overlapping 3-second windows.

## Scoring recipe

```python
def compute_geco_score(video, fps=8):
    windows = extract_overlapping_3s_windows(video, fps)
    clip_scores = []
    for w in windows:
        mask = get_valid_depth_and_covisibility(w)
        struct_err = compute_structure_inconsistency(w, mask)
        motion_err = compute_motion_inconsistency(w, mask)
        fused_err = fuse(struct_err, motion_err)
        clip_scores.append(fused_err)
    return frame_weighted_average(clip_scores)
```

## Common pitfalls

- High consistency scores can be artificially inflated by videos with very low motion; the protocol requires reporting normalized motion statistics (Total Motion, Mean Motion) to disambiguate.
- Evaluation must be restricted to overlapping ~3-second windows resampled to ≤8 FPS to ensure fair comparison across models with different native generation settings.
- All GeCo metrics are lower-is-better (inconsistency/error), which is the opposite of standard accuracy metrics.

## Evidence (verbatim from paper)

> Within each window, we compute motion, structure, and fused scores averaged over pixels with valid depth and covisibility. Final clip-level scores are derived from the frame-weighted average of these windows, and we report the mean across all 320 clips (80 prompts × 4 seeds) per model.

## Citation

```bibtex
@misc{gu2025geco,
  title={GeCo: A Differentiable Geometric Consistency Metric for Video Generation},
  author={Gu et al. (2025)},
  year={2025},
  note={arXiv:2512.22274}
}
```

- arXiv: 2512.22274
