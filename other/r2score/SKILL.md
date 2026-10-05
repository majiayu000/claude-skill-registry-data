---
name: r2score
description: Compute the R2Score metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute R2Score, or asks how to score with R2Score.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.R2Score
  source: library_introspection
---

# r2score

> Metric `R2Score` from `torchmetrics` (torchmetrics.R2Score)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with R2Score, or
mentions `torchmetrics.R2Score` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import R2Score

# R2Score(adjusted: int = 0, multioutput: str = 'uniform_average', **kwargs: Any) -> None
```

## Library docstring

```
Compute r2 score also known as `R2 Score_Coefficient Determination`_.

.. math:: R^2 = 1 - \frac{SS_{res}}{SS_{tot}}

where :math:`SS_{res}=\sum_i (y_i - f(x_i))^2` is the sum of residual squares, and
:math:`SS_{tot}=\sum_i (y_i - \bar{y})^2` is total sum of squares. Can also calculate
adjusted r2 score given by

.. math:: R^2_{adj} = 1 - \frac{(1-R^2)(n-1)}{n-k-1}

where the parameter :math:`k` (the number of independent regressors) should be provided as the `adjusted` argument.
The score is only proper defined when :math:`SS_{tot}\neq 0`, which can happen for near constant targets. In this
case a score of 0 is returned. By definition the score is bounded between :math:`-inf` and 1.0, with 1.0 indicating
perfect prediction, 0 indicating constant prediction and negative values indicating worse than constant prediction.

As input to ``forward`` and ``update`` the metric accepts the following input:

- ``preds`` (:class:`~torch.Tensor`): Predictions from model in float tensor with shape ``(N,)``
  or ``(N, M)`` (multioutput)
- ``target`` (:class:`~torch.Tensor`): Ground truth values in float tensor with shape ``(N,)``
  or ``(N, M)`` (multioutput)

As output of ``forward`` and ``compute`` the metric returns the following output:

- ``r2score`` (:class:`~torch.Tensor`): A tensor with the r2 score(s)

In the case of multioutput, as default the variances will be uniformly averaged over the additional dimensions.
Please see argument ``multioutput`` for changing this behavior.

Args:
    num_outputs: Number of outputs in multioutput setting
    adjusted: number of independent regressors for calculating adjusted r2 score.
    multioutput: Defines aggregation in the case of multiple output scores. Can be one of the following strings:

        * ``'raw_values'`` returns full set of scores
        * ``'uniform_average'`` scores are uniformly averaged
        * ``'variance_weighted'`` scores are weighted by their individual variances
    kwargs: Additional keyword arguments, see :ref:`Metric kwargs` for more info.

.. warning::
    Argument ``num_outputs`` in ``R2Score`` has been deprecated because it is no longer necessary and will be
    removed in v1.6.0 of TorchMetrics.
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.R2Score(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
