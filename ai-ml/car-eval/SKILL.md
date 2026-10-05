---
name: car-eval
description: Evaluates continual semi-supervised learning on activity recognition by measuring how well a model adapts to time-varying unlabeled data streams across sequential sessions without predefined class boundaries. Use when the user wants to benchmark on Continual Activity Recognition (CAR), or asks about evaluating this task. Reports F1-score (class average).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2110.14613
  bibtex_key: shahbaz2021cssl
  confidence: high
---

# car-eval

> International Workshop on Continual Semi-Supervised Learning: Introduction, Benchmarks and Baselines — Shahbaz et al. (2021) (arXiv:2110.14613, 2021)

## What this evaluates

Evaluates continual semi-supervised learning on activity recognition by measuring how well a model adapts to time-varying unlabeled data streams across sequential sessions without predefined class boundaries.

## Datasets

- **Continual Activity Recognition (CAR)** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `F1-score (class average)` **(primary)** — range: [0, 1]
  - Average of per-class F1 scores computed as (F1_class1 + F1_class2 + ... + F1_class9) / 9, ignoring class imbalance.

## Input / output format

**Input**: Sequential video/image data streams divided into sessions, containing unlabeled validation and test folds for incremental model updating.

**Output**: Predicted activity class labels for each instance in the stream.

## Scoring recipe

```python
def compute_f1_class_avg(predictions, gold):
    classes = set(gold)
    f1_scores = []
    for c in classes:
        tp = sum(1 for p, g in zip(predictions, gold) if p == c and g == c)
        fp = sum(1 for p, g in zip(predictions, gold) if p == c and g != c)
        fn = sum(1 for p, g in zip(predictions, gold) if p != c and g == c)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        f1_scores.append(f1)
    return sum(f1_scores) / len(f1_scores)
```

## Common pitfalls

- Confusing class-average F1 with weighted-average F1, which accounts for sample counts per class.
- Assuming validation stream updates generalize directly to test streams without session-wise evaluation.
- Comparing results directly to batch-trained baselines without accounting for the continual learning protocol difference.

## Evidence (verbatim from paper)

> The standard classification evaluation metrics precision, recall, and F1-score were used for evaluation. For each evaluation metric we computed both the class average (obtained by computing the score for each class and taking the average without considering the number of training samples in each class, i.e., F1_class1+F1_class2...F1_class9) and the weighted average (which uses the number of samples W_i in each class i, i.e., F1_class1*W_1+F1_class2*W_2...F1_class9*W_9).

## Citation

```bibtex
@misc{shahbaz2021cssl,
  title={International Workshop on Continual Semi-Supervised Learning: Introduction, Benchmarks and Baselines},
  author={Shahbaz et al. (2021)},
  year={2021},
  note={arXiv:2110.14613}
}
```

- arXiv: 2110.14613
