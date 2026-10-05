---
name: eer
description: Compute the EER metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute EER, or asks how to score with EER.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.classification.EER
  source: library_introspection
---

# eer

> Metric `EER` from `torchmetrics` (torchmetrics.classification.EER)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with EER, or
mentions `torchmetrics.classification.EER` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics.classification import EER

# EER(task: Literal['binary', 'multiclass', 'multilabel'], thresholds: Union[int, list[float], torch.Tensor, NoneType] = None, num_classes: Optional[int] = None, num_labels: Optional[int] = None, average: Optional[Literal['micro', 'macro']] = None, ignore_index: Optional[int] = None, validate_args: bool = True, **kwargs: Any) -> torchmetrics.metric.Metric
```

## Library docstring

```
Compute Equal Error Rate (EER) for multiclass classification task.

.. math::
    \text{EER} = \frac{\text{FAR} + (1 - \text{FRR})}{2}, \text{where} \min_t abs(FAR_t-FRR_t)

The Equal Error Rate (EER) is the point where the False Positive Rate (FPR) and True Positive Rate (TPR) are
equal, or in practise minimized. A lower EER value signifies higher system accuracy.

This module is a simple wrapper to get the task specific versions of this metric, which is done by setting the
``task`` argument to either ``'binary'``, ``'multiclass'`` or ``'multilabel'``. See the documentation of
:class:`~torchmetrics.classification.BinaryEER`, :class:`~torchmetrics.classification.MulticlassEER` and
:class:`~torchmetrics.classification.MultilabelEER` for the specific details of each argument influence and
examples.

Legacy Example:
    >>> from torch import tensor
    >>> preds = tensor([0.13, 0.26, 0.08, 0.19, 0.34])
    >>> target = tensor([0, 0, 1, 1, 1])
    >>> eer = EER(task="binary")
    >>> eer(preds, target)
    tensor(0.5833)

    >>> preds = tensor([[0.90, 0.05, 0.05],
    ...                       [0.05, 0.90, 0.05],
    ...                       [0.05, 0.05, 0.90],
    ...                       [0.85, 0.05, 0.10],
    ...                       [0.10, 0.10, 0.80]])
    >>> target = tensor([0, 1, 1, 2, 2])
    >>> eer = EER(task="multiclass", num_classes=3)
    >>> eer(preds, target)
    tensor([0.0000, 0.4167, 0.4167])
```

## Quick recipe

```python
import torchmetrics.classification as _m
score = _m.EER(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
