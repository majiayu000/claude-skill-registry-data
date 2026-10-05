---
name: cwi-eval
description: This benchmark evaluates a model's ability to perform binary classification on lexical complexity, determining whether a given word is perceived as complex or non-complex by human readers. Use when the user wants to benchmark on SemEval CWI, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1710.04989
  bibtex_key: zampieri2017complex
  confidence: high
---

# cwi-eval

> Complex Word Identification: Challenges in Data Annotation and System Performance — Zampieri et al. (2017) (arXiv:1710.04989, 2017)

## What this evaluates

This benchmark evaluates a model's ability to perform binary classification on lexical complexity, determining whether a given word is perceived as complex or non-complex by human readers.

## Datasets

- **SemEval CWI** — total ?; splits: train (2237), test (-1)

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall: F1 = 2 * (Precision * Recall) / (Precision + Recall). Reported separately for class 0 (non-complex) and class 1 (complex).

## Input / output format

**Input**: A single lexical item (word).

**Output**: Binary label: 0 for non-complex, 1 for complex.

## Scoring recipe

```python
def compute_f1(predictions, gold):
    tp = sum(1 for p, g in zip(predictions, gold) if p == 1 and g == 1)
    fp = sum(1 for p, g in zip(predictions, gold) if p == 1 and g == 0)
    fn = sum(1 for p, g in zip(predictions, gold) if p == 0 and g == 1)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return f1
```

## Common pitfalls

- High class imbalance: the dataset is heavily skewed towards non-complex words (class 0), which can bias models and inflate accuracy.
- Annotation noise: training labels are assigned if any annotator marks a word as complex, leading to inconsistent ground truth and low predictive power.
- Train/test label mismatch: approximately 50% of the most complex words receive different labels in the training and test sets, undermining generalization evaluation.

## Evidence (verbatim from paper)

> Plurality voting results for class 1 are presented in Table 2 in terms of precision, recall, and F1 score. For comparison we also report a threshold-based baseline on word frequencies from Wikipedia (Paetzold and Specia, 2016a) and the performance of the best system in terms of f-score for class 1.

## Citation

```bibtex
@misc{zampieri2017complex,
  title={Complex Word Identification: Challenges in Data Annotation and System Performance},
  author={Zampieri et al. (2017)},
  year={2017},
  note={arXiv:1710.04989}
}
```

- arXiv: 1710.04989
