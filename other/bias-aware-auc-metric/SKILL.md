---
name: nlp-bias-aware-auc-metric
description: Combine subgroup AUC, BPSN AUC, and BNSP AUC across identity groups via power-mean weighting with overall AUC for fairness evaluation
domain: nlp
---

# Bias-Aware AUC Metric

## Overview

Standard AUC can hide poor performance on identity subgroups. Compute three per-subgroup AUCs: (1) Subgroup AUC (within-group ranking), (2) BPSN AUC (background-positive vs subgroup-negative), (3) BNSP AUC (background-negative vs subgroup-positive). Combine all via generalized power mean (p=−5 emphasizes worst-performing groups), then blend with overall AUC.

## Quick Start

```python
import numpy as np
from sklearn.metrics import roc_auc_score

def power_mean(scores, p=-5):
    """Generalized mean that emphasizes lowest scores when p < 0."""
    scores = np.array(scores)
    return np.power(np.mean(np.power(scores, p)), 1 / p)

def subgroup_auc(df, subgroup, label, pred):
    subset = df[df[subgroup] >= 0.5]
    return roc_auc_score(subset[label] >= 0.5, subset[pred])

def bpsn_auc(df, subgroup, label, pred):
    """Background Positive, Subgroup Negative."""
    mask = ((df[subgroup] >= 0.5) & (df[label] < 0.5)) | \
           ((df[subgroup] < 0.5) & (df[label] >= 0.5))
    subset = df[mask]
    return roc_auc_score(subset[label] >= 0.5, subset[pred])

def bnsp_auc(df, subgroup, label, pred):
    """Background Negative, Subgroup Positive."""
    mask = ((df[subgroup] >= 0.5) & (df[label] >= 0.5)) | \
           ((df[subgroup] < 0.5) & (df[label] < 0.5))
    subset = df[mask]
    return roc_auc_score(subset[label] >= 0.5, subset[pred])

def final_metric(df, identity_cols, label, pred, overall_weight=0.25):
    overall = roc_auc_score(df[label] >= 0.5, df[pred])
    sub_aucs = [subgroup_auc(df, c, label, pred) for c in identity_cols]
    bpsn_aucs = [bpsn_auc(df, c, label, pred) for c in identity_cols]
    bnsp_aucs = [bnsp_auc(df, c, label, pred) for c in identity_cols]
    bias = np.mean([power_mean(sub_aucs), power_mean(bpsn_aucs), power_mean(bnsp_aucs)])
    return overall_weight * overall + (1 - overall_weight) * bias
```

## Key Decisions

- **p=−5**: strongly penalizes worst subgroup — increase toward 0 for softer averaging
- **Overall weight 0.25**: 75% fairness, 25% accuracy — adjust per use case
- **Min subgroup size**: skip subgroups with <100 samples to avoid noisy AUC estimates

## References

- Source: [toxic-bert-plain-vanila](https://www.kaggle.com/code/yuval6967/toxic-bert-plain-vanila)
- Competition: Jigsaw Unintended Bias in Toxicity Classification
