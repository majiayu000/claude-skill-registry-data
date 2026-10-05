---
name: bleurt
description: Evaluates the correlation between automatic text generation scores and human quality ratings. Probes a model's ability to accurately rank or score generated translations and data-to-text outputs against human judgments, including robustness to domain/quality drift and few-shot adaptation. Use when the user has predictions and gold and needs to compute Kendall's Tau ($\tau$).
metadata:
  skill_kind: metric
  source_arxiv: 2004.04696
  bibtex_key: sellam2020bleurt
  confidence: high
---

# bleurt

> BLEURT: Learning Robust Metrics for Text Generation — Sellam et al. (2020) (arXiv:2004.04696, 2020)

## What this evaluates

Evaluates the correlation between automatic text generation scores and human quality ratings. Probes a model's ability to accurately rank or score generated translations and data-to-text outputs against human judgments, including robustness to domain/quality drift and few-shot adaptation.

## Datasets

- **WMT Metrics Shared Task (2017-2019)** — total ?; splits: train (-1), test (-1)
- **WebNLG 2017** — total 4677; splits: train (-1), test (-1)

## Metrics

- `Kendall's Tau ($\tau$)` **(primary)** — range: [-1, 1]
  - Measures the ordinal association between predicted scores and human ratings. Computed as the number of concordant pairs minus discordant pairs, divided by total pairs.
- `Pearson correlation ($r$) / Direct Assessment (DA)` — range: [-1, 1]
  - Linear correlation coefficient between predicted and human scores. DA is a scaled version of human assessment scores used as the official WMT metric.

## Input / output format

**Input**: Source sentence and generated target sentence (or multiple reference sentences), paired with human quality ratings.

**Output**: A scalar quality score for the generated text.

## Scoring recipe

```python
def compute_agreement(predictions, human_ratings):
    # predictions and human_ratings are lists of floats of equal length
    tau = kendalltau(predictions, human_ratings).correlation
    pearson = pearsonr(predictions, human_ratings).correlation
    return tau, pearson
```

## Common pitfalls

- When multiple references are available, compute the metric for each reference and report the maximum score.
- Training and test splits vary by year; for WMT, the test set from the previous year is used for training/validation.
- Quality drift experiments use a skew factor α that heavily biases training data toward low ratings and test data toward high ratings.

## Evidence (verbatim from paper)

> We evaluate the agreement between the automatic metrics and the human ratings. For each year, we report two metrics: Kendall's Tau $\tau$ (for consistency across experiments), and the official WMT metric for that year (for completeness). The official WMT metric is either Pearson's correlation or a robust variant of Kendall's Tau called DARR, described in the Appendix.

## Citation

```bibtex
@misc{sellam2020bleurt,
  title={BLEURT: Learning Robust Metrics for Text Generation},
  author={Sellam et al. (2020)},
  year={2020},
  note={arXiv:2004.04696}
}
```

- arXiv: 2004.04696
