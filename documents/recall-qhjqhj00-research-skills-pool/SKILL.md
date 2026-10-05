---
name: recall
description: Compute the Recall metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute Recall, or asks how to score with Recall.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.Recall
  source: library_introspection
---

# recall

> Metric `Recall` from `torchmetrics` (torchmetrics.Recall)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with Recall, or
mentions `torchmetrics.Recall` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import Recall

# Recall(task: Literal['binary', 'multiclass', 'multilabel'], threshold: float = 0.5, num_classes: Optional[int] = None, num_labels: Optional[int] = None, average: Optional[Literal['micro', 'macro', 'weighted', 'none']] = 'micro', multidim_average: Optional[Literal['global', 'samplewise']] = 'global', top_k: Optional[int] = 1, ignore_index: Optional[int] = None, validate_args: bool = True, **kwargs: Any) -> torchmetrics.metric.Metric
```

## Library docstring

```
Compute `Recall`_.

.. math:: \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}

Where :math:`\text{TP}` and :math:`\text{FN}` represent the number of true positives and
false negatives respectively. The metric is only proper defined when :math:`\text{TP} + \text{FN} \neq 0`. If this
case is encountered for any class/label, the metric for that class/label will be set to 0 and the overall metric may
therefore be affected in turn.

This function is a simple wrapper to get the task specific versions of this metric, which is done by setting the
``task`` argument to either ``'binary'``, ``'multiclass'`` or ``'multilabel'``. See the documentation of
:class:`~torchmetrics.classification.BinaryRecall`,
:class:`~torchmetrics.classification.MulticlassRecall` and :class:`~torchmetrics.classification.MultilabelRecall`
for the specific details of each argument influence and examples.

Legacy Example:
    >>> from torch import tensor
    >>> preds  = tensor([2, 0, 2, 1])
    >>> target = tensor([1, 1, 2, 0])
    >>> recall = Recall(task="multiclass", average='macro', num_classes=3)
    >>> recall(preds, target)
    tensor(0.3333)
    >>> recall = Recall(task="multiclass", average='micro', num_classes=3)
    >>> recall(preds, target)
    tensor(0.2500)
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.Recall(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
