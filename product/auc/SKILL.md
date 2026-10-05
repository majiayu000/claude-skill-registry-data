---
name: AUC
description: This evaluation probes the capability of machine learning classifiers to distinguish signal events from background noise in high-energy particle physics simulations. It measures how well different algorithms and feature sets rank positive (signal) instances higher than negative (background) ones across varying data statistics. Use when the user has predictions and gold and needs to compute AUC.
metadata:
  skill_kind: metric
  source_arxiv: 2110.15099
  bibtex_key: cidvidal2021signalbackground
  confidence: high
---

# AUC

> How to use Machine Learning to improve the discrimination between signal and background at particle colliders — Cid Vidal et al. (2021) (arXiv:2110.15099, 2021)

## What this evaluates

This evaluation probes the capability of machine learning classifiers to distinguish signal events from background noise in high-energy particle physics simulations. It measures how well different algorithms and feature sets rank positive (signal) instances higher than negative (background) ones across varying data statistics.

## Datasets

- **LHCb B-meson decay simulation** — total ?; splits: train (-1), test (-1)

## Metrics

- `AUC` **(primary)** — range: [0, 1]
  - Area Under the Receiver Operating Characteristic curve. Computed by integrating the true positive rate against the false positive rate across all classification thresholds.

## Input / output format

**Input**: Numerical feature vectors representing particle decay events, provided at low-level, high-level, or combined feature sets.

**Output**: Continuous probability score or decision function value indicating the likelihood of the event being signal.

## Scoring recipe

```python
def compute_auc(y_true, y_pred_scores):
    fpr, tpr, _ = roc_curve(y_true, y_pred_scores)
    return auc(fpr, tpr)
```

## Common pitfalls

- AUC can mask poor calibration or suboptimal performance at specific operating points relevant to physics analyses.
- Adding more features or statistics does not guarantee higher AUC due to redundancy or statistical fluctuations in simulations.
- Comparisons across libraries must control for hyperparameter tuning, as default settings may not yield optimal discrimination.

## Evidence (verbatim from paper)

> Once we have calculated the ROC curves and obtained the AUC scores for each of the algorithms, we proceed to compare them all for each channel.

## Citation

```bibtex
@misc{cidvidal2021signalbackground,
  title={How to use Machine Learning to improve the discrimination between signal and background at particle colliders},
  author={Cid Vidal et al. (2021)},
  year={2021},
  note={arXiv:2110.15099}
}
```

- arXiv: 2110.15099
