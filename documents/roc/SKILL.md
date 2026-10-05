---
name: roc
description: Compute the ROC metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute ROC, or asks how to score with ROC.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.ROC
  source: library_introspection
---

# roc

> Metric `ROC` from `torchmetrics` (torchmetrics.ROC)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with ROC, or
mentions `torchmetrics.ROC` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import ROC

# ROC(task: Literal['binary', 'multiclass', 'multilabel'], thresholds: Union[int, list[float], torch.Tensor, NoneType] = None, num_classes: Optional[int] = None, num_labels: Optional[int] = None, ignore_index: Optional[int] = None, validate_args: bool = True, **kwargs: Any) -> torchmetrics.metric.Metric
```

## Library docstring

```
Compute the Receiver Operating Characteristic (ROC).

The curve consist of multiple pairs of true positive rate (TPR) and false positive rate (FPR) values evaluated at
different thresholds, such that the tradeoff between the two values can be seen.

This function is a simple wrapper to get the task specific versions of this metric, which is done by setting the
``task`` argument to either ``'binary'``, ``'multiclass'`` or ``'multilabel'``. See the documentation of
:class:`~torchmetrics.classification.BinaryROC`,
:class:`~torchmetrics.classification.MulticlassROC` and
:class:`~torchmetrics.classification.MultilabelROC` for the specific details of each argument
influence and examples.

Legacy Example:
    >>> from torch import tensor
    >>> pred = tensor([0.0, 1.0, 2.0, 3.0])
    >>> target = tensor([0, 1, 1, 1])
    >>> roc = ROC(task="binary")
    >>> fpr, tpr, thresholds = roc(pred, target)
    >>> fpr
    tensor([0., 0., 0., 0., 1.])
    >>> tpr
    tensor([0.0000, 0.3333, 0.6667, 1.0000, 1.0000])
    >>> thresholds
    tensor([1.0000, 0.9526, 0.8808, 0.7311, 0.5000])

    >>> pred = tensor([[0.75, 0.05, 0.05, 0.05],
    ...                [0.05, 0.75, 0.05, 0.05],
    ...                [0.05, 0.05, 0.75, 0.05],
    ...                [0.05, 0.05, 0.05, 0.75]])
    >>> target = tensor([0, 1, 3, 2])
    >>> roc = ROC(task="multiclass", num_classes=4)
    >>> fpr, tpr, thresholds = roc(pred, target)
    >>> fpr
    [tensor([0., 0., 1.]), tensor([0., 0., 1.]), tensor([0.0000, 0.3333, 1.0000]), tensor([0.0000, 0.3333, 1.0000])]
    >>> tpr
    [tensor([0., 1., 1.]), tensor([0., 1., 1.]), tensor([0., 0., 1.]), tensor([0., 0., 1.])]
    >>> thresholds  # doctest: +NORMALIZE_WHITESPACE
    [tensor([1.0000, 0.7500, 0.0500]),
     tensor([1.0000, 0.7500, 0.0500]),
     tensor([1.0000, 0.7500, 0.0500]),
     tensor([1.0000, 0.7500, 0.0500])]

    >>> pred = tensor([[0.8191, 0.3680, 0.1138],
    ...                [0.3584, 0.7576, 0.1183],
    ...                [0.2286, 0.3468, 0.1338],
    ...                [0.8603, 0.0745, 0.1837]])
    >>> target = tensor([[1, 1, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1]])
    >>> roc = ROC(task='multilabel', num_labels=3)
    >>> fpr, t
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.ROC(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
