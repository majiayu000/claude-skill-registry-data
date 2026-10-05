---
name: f1score
description: Compute the F1Score metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute F1Score, or asks how to score with F1Score.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.F1Score
  source: library_introspection
---

# f1score

> Metric `F1Score` from `torchmetrics` (torchmetrics.F1Score)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with F1Score, or
mentions `torchmetrics.F1Score` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import F1Score

# F1Score(task: Literal['binary', 'multiclass', 'multilabel'], threshold: float = 0.5, num_classes: Optional[int] = None, num_labels: Optional[int] = None, average: Optional[Literal['micro', 'macro', 'weighted', 'none']] = 'micro', multidim_average: Optional[Literal['global', 'samplewise']] = 'global', top_k: Optional[int] = 1, ignore_index: Optional[int] = None, validate_args: bool = True, zero_division: float = 0, **kwargs: Any) -> torchmetrics.metric.Metric
```

## Library docstring

```
Compute F-1 score.

.. math::
    F_{1} = 2\frac{\text{precision} * \text{recall}}{(\text{precision}) + \text{recall}}

The metric is only proper defined when :math:`\text{TP} + \text{FP} \neq 0 \wedge \text{TP} + \text{FN} \neq 0`
where :math:`\text{TP}`, :math:`\text{FP}` and :math:`\text{FN}` represent the number of true positives, false
positives and false negatives respectively. If this case is encountered for any class/label, the metric for that
class/label will be set to `zero_division` (0 or 1, default is 0) and the overall metric may therefore be
affected in turn.

This function is a simple wrapper to get the task specific versions of this metric, which is done by setting the
``task`` argument to either ``'binary'``, ``'multiclass'`` or ``'multilabel'``. See the documentation of
:class:`~torchmetrics.classification.BinaryF1Score`, :class:`~torchmetrics.classification.MulticlassF1Score` and
:class:`~torchmetrics.classification.MultilabelF1Score` for the specific details of each argument influence and
examples.

Legacy Example:
    >>> from torch import tensor
    >>> target = tensor([0, 1, 2, 0, 1, 2])
    >>> preds = tensor([0, 2, 1, 0, 0, 1])
    >>> f1 = F1Score(task="multiclass", num_classes=3)
    >>> f1(preds, target)
    tensor(0.3333)
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.F1Score(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
