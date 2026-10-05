---
name: logauc
description: Compute the LogAUC metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute LogAUC, or asks how to score with LogAUC.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.LogAUC
  source: library_introspection
---

# logauc

> Metric `LogAUC` from `torchmetrics` (torchmetrics.LogAUC)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with LogAUC, or
mentions `torchmetrics.LogAUC` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import LogAUC

# LogAUC(task: Literal['binary', 'multiclass', 'multilabel'], thresholds: Union[int, List[float], torch.Tensor, NoneType] = None, fpr_range: Optional[Tuple[float, float]] = (0.001, 0.1), num_classes: Optional[int] = None, num_labels: Optional[int] = None, ignore_index: Optional[int] = None, validate_args: bool = True, **kwargs: Any) -> torchmetrics.metric.Metric
```

## Library docstring

```
Compute the `Log AUC`_ score for multiclass classification tasks.

The score is computed by first computing the ROC curve, which then is interpolated to the specified range of false
positive rates (FPR) and then the log is taken of the FPR before the area under the curve (AUC) is computed. The
score is commonly used in applications where the positive and negative are imbalanced and a low false positive rate
is of high importance.

This module is a simple wrapper to get the task specific versions of this metric, which is done by setting the
``task`` argument to either ``'binary'``, ``'multiclass'`` or ``'multilabel'``. See the documentation of
:class:`~torchmetrics.classification.BinaryLogAUC`, :class:`~torchmetrics.classification.MulticlassLogAUC` and
:class:`~torchmetrics.classification.MultilabelLogAUC` for the specific details of each argument influence and
examples.
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.LogAUC(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
