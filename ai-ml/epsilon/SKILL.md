---
name: epsilon
description: Evaluates the correlation between a zero-cost NAS metric (epsilon) and actual training accuracy across different neural architecture search spaces, testing the metric's ability to rank architectures without training. It probes whether output dispersion from constant weight initializations can serve as a reliable, hyperparameter-free proxy for architecture selection. Use when the user has predictions and gold and needs to compute Spearman ρ (global).
metadata:
  skill_kind: metric
  source_arxiv: 2302.04406
  bibtex_key: gracheva2023neural
  confidence: high
---

# epsilon

> Neural Architecture Search: Two Constant Shared Weights Initialisations — Gracheva (2023) (arXiv:2302.04406, 2023)

## What this evaluates

Evaluates the correlation between a zero-cost NAS metric (epsilon) and actual training accuracy across different neural architecture search spaces, testing the metric's ability to rank architectures without training. It probes whether output dispersion from constant weight initializations can serve as a reliable, hyperparameter-free proxy for architecture selection.

## Datasets

- **NAS-Bench-201** — total 15625; splits: all (15625)
- **NAS-Bench-101** — total 423624; splits: all (423624)
- **NAS-Bench-NLP** — total 14322; splits: all (14322)

## Metrics

- `Spearman ρ (global)` **(primary)** — range: [-1, 1]
  - Spearman rank correlation coefficient evaluated on the entire dataset of architectures.
- `Spearman ρ (top-10%)` — range: [-1, 1]
  - Spearman rank correlation coefficient computed only on the top-10% performing architectures.
- `Kendall τ (global)` — range: [-1, 1]
  - Kendall rank correlation coefficient evaluated on the entire dataset.
- `Kendall τ (top-10%)` — range: [-1, 1]
  - Kendall rank correlation coefficient computed only on the top-10% performing architectures.
- `Top-10%/top-10%` — range: [0, 1]
  - Fraction of top-10% performing models (by ground truth accuracy) that appear within the top-10% models ranked by the zero-cost metric.
- `Top-64/top-5%` — range: [0, 64]
  - Number of top-64 models ranked by the zero-cost metric that fall within the top-5% performing models.

## Input / output format

**Input**: Architecture definition from a NAS search space (e.g., NAS-Bench-201, NAS-Bench-101, NAS-Bench-NLP).

**Output**: A scalar score representing the output dispersion normalized by average output magnitude.

## Scoring recipe

```python
def compute_epsilon(arch, input_tensor):
    out1 = forward(arch, init_weights_const1, input_tensor)
    out2 = forward(arch, init_weights_const2, input_tensor)
    dispersion = std(out1 - out2)
    avg_mag = mean(abs(out1))
    return dispersion / avg_mag

def evaluate_correlation(scores, ground_truth):
    spearman_global = spearmanr(scores, ground_truth).correlation
    top_k = int(len(scores) * 0.1)
    spearman_top = spearmanr(scores[:top_k], ground_truth[:top_k]).correlation
    top10_overlap = len(set(top_k_indices(scores)) & set(top_k_indices(ground_truth))) / top_k
    return spearman_global, spearman_top, top10_overlap
```

## Common pitfalls

- For NLP tasks using perplexity, correlation signs must be reversed because perplexity should be minimized, unlike accuracy.
- Discrepancies can arise in calculating Top-64/top-5% if not handled consistently with prior works.
- The metric was developed on NAS-Bench-201, so performance on other spaces may vary.

## Evidence (verbatim from paper)

> Here we evaluate the performance of epsilon and compare it to the results for zero-cost NAS metrics reported in Abdelfattah et al. (2021). We use the following evaluation scores (computed with NaN omitted): Spearman ρ (global): Spearman rank correlation ρ evaluated on the entire dataset. Spearman ρ (top-10%): Spearman rank correlation ρ for the top-10% performing architectures. Kendall τ (global): Kendall rank correlation coefficient τ evaluated on the entire dataset. Kendall τ (top-10%): Kendall rank correlation coefficient τ for the top-10% performing architectures. Top-10%/top-10%: fraction of top-10% performing models within the top-10% models ranked by zero-cost scoring metric (%). Top-64/top-10%: number of top-64 models ranked by zero-cost scoring metric within top-5% performing models.

## Citation

```bibtex
@misc{gracheva2023neural,
  title={Neural Architecture Search: Two Constant Shared Weights Initialisations},
  author={Gracheva (2023)},
  year={2023},
  note={arXiv:2302.04406}
}
```

- arXiv: 2302.04406
