---
name: auroc
description: Compute the AUROC metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute AUROC, or asks how to score with AUROC.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.AUROC
  source: library_introspection
---

# auroc

> Metric `AUROC` from `torchmetrics` (torchmetrics.AUROC)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with AUROC, or
mentions `torchmetrics.AUROC` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import AUROC

# AUROC(task: Literal['binary', 'multiclass', 'multilabel'], thresholds: Union[int, list[float], torch.Tensor, NoneType] = None, num_classes: Optional[int] = None, num_labels: Optional[int] = None, average: Optional[Literal['macro', 'weighted', 'none']] = 'macro', max_fpr: Optional[float] = None, ignore_index: Optional[int] = None, validate_args: bool = True, **kwargs: Any) -> torchmetrics.metric.Metric
```

## Library docstring

```
Compute Area Under the Receiver Operating Characteristic Curve (`ROC AUC`_).

The AUROC score summarizes the ROC curve into an single number that describes the performance of a model for
multiple thresholds at the same time. Notably, an AUROC score of 1 is a perfect score and an AUROC score of 0.5
corresponds to random guessing.

This module is a simple wrapper to get the task specific versions of this metric, which is done by setting the
``task`` argument to either ``'binary'``, ``'multiclass'`` or ``'multilabel'``. See the documentation of
:class:`~torchmetrics.classification.BinaryAUROC`, :class:`~torchmetrics.classification.MulticlassAUROC` and
:class:`~torchmetrics.classification.MultilabelAUROC` for the specific details of each argument influence and
examples.

Legacy Example:
    >>> from torch import tensor
    >>> preds = tensor([0.13, 0.26, 0.08, 0.19, 0.34])
    >>> target = tensor([0, 0, 1, 1, 1])
    >>> auroc = AUROC(task="binary")
    >>> auroc(preds, target)
    tensor(0.5000)

    >>> preds = tensor([[0.90, 0.05, 0.05],
    ...                       [0.05, 0.90, 0.05],
    ...                       [0.05, 0.05, 0.90],
    ...                       [0.85, 0.05, 0.10],
    ...                       [0.10, 0.10, 0.80]])
    >>> target = tensor([0, 1, 1, 2, 2])
    >>> auroc = AUROC(task="multiclass", num_classes=3)
    >>> auroc(preds, target)
    tensor(0.7778)
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.AUROC(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
