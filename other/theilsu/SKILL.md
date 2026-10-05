---
name: theilsu
description: Compute the TheilsU metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute TheilsU, or asks how to score with TheilsU.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.TheilsU
  source: library_introspection
---

# theilsu

> Metric `TheilsU` from `torchmetrics` (torchmetrics.TheilsU)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with TheilsU, or
mentions `torchmetrics.TheilsU` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import TheilsU

# TheilsU(num_classes: int, nan_strategy: Literal['replace', 'drop'] = 'replace', nan_replace_value: Optional[float] = 0.0, **kwargs: Any) -> None
```

## Library docstring

```
Compute `Theil's U`_ statistic measuring the association between two categorical (nominal) data series.

.. math::
    U(X|Y) = \frac{H(X) - H(X|Y)}{H(X)}

where :math:`H(X)` is entropy of variable :math:`X` while :math:`H(X|Y)` is the conditional entropy of :math:`X`
given :math:`Y`. It is also know as the Uncertainty Coefficient. Theils's U is an asymmetric coefficient, i.e.
:math:`TheilsU(preds, target) \neq TheilsU(target, preds)`, so the order of the inputs matters. The output values
lies in [0, 1], where a 0 means y has no information about x while value 1 means y has complete information about x.

As input to ``forward`` and ``update`` the metric accepts the following input:

- ``preds`` (:class:`~torch.Tensor`): Either 1D or 2D tensor of categorical (nominal) data from the first data
  series (called X in the above definition) with shape ``(batch_size,)`` or ``(batch_size, num_classes)``,
  respectively.
- ``target`` (:class:`~torch.Tensor`): Either 1D or 2D tensor of categorical (nominal) data from the second data
  series (called Y in the above definition) with shape ``(batch_size,)`` or ``(batch_size, num_classes)``,
  respectively.

As output of ``forward`` and ``compute`` the metric returns the following output:

- ``theils_u`` (:class:`~torch.Tensor`): Scalar tensor containing the Theil's U statistic.

Args:
    num_classes: Integer specifying the number of classes
    nan_strategy: Indication of whether to replace or drop ``NaN`` values
    nan_replace_value: Value to replace ``NaN``s when ``nan_strategy = 'replace'``
    kwargs: Additional keyword arguments, see :ref:`Metric kwargs` for more info.

Example::

    >>> from torch import randint
    >>> from torchmetrics.nominal import TheilsU
    >>> preds = randint(10, (10,))
    >>> target = randint(10, (10,))
    >>> metric = TheilsU(num_classes=10)
    >>> metric(preds, target)
    tensor(0.8530)
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.TheilsU(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
