---
name: ranksums
description: Compute the ranksums metric — provided by scipy.stats. Use when the user has predictions and ground-truth and needs to compute ranksums, or asks how to score with ranksums.
metadata:
  skill_kind: metric
  source_lib: scipy.stats
  import_path: scipy.stats.ranksums
  source: library_introspection
---

# ranksums

> Metric `ranksums` from `scipy.stats` (scipy.stats.ranksums)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with ranksums, or
mentions `scipy.stats.ranksums` directly, or wants the standard scipy.stats implementation.

## Reference signature

```python
from scipy.stats import ranksums

# ranksums(x, y, alternative='two-sided', *, axis=0, nan_policy='propagate', keepdims=False)
```

## Library docstring

```
Compute the Wilcoxon rank-sum statistic for two samples.

The Wilcoxon rank-sum test tests the null hypothesis that two sets
of measurements are drawn from the same distribution.  The alternative
hypothesis is that values in one sample are more likely to be
larger than the values in the other sample.

This test should be used to compare two samples from continuous
distributions.  It does not handle ties between measurements
in x and y.  For tie-handling and an optional continuity correction
see `scipy.stats.mannwhitneyu`.

Parameters
----------
x,y : array_like
    The data from the two samples.
alternative : {'two-sided', 'less', 'greater'}, optional
    Defines the alternative hypothesis. Default is 'two-sided'.
    The following options are available:

    * 'two-sided': one of the distributions (underlying `x` or `y`) is
      stochastically greater than the other.
    * 'less': the distribution underlying `x` is stochastically less
      than the distribution underlying `y`.
    * 'greater': the distribution underlying `x` is stochastically greater
      than the distribution underlying `y`.

    .. versionadded:: 1.7.0
axis : int or None, default: 0
    If an int, the axis of the input along which to compute the statistic.
    The statistic of each axis-slice (e.g. row) of the input will appear in a
    corresponding element of the output.
    If ``None``, the input will be raveled before computing the statistic.
nan_policy : {'propagate', 'omit', 'raise'}
    Defines how to handle input NaNs.

    - ``propagate``: if a NaN is present in the axis slice (e.g. row) along
      which the  statistic is computed, the corresponding entry of the output
      will be NaN.
    - ``omit``: NaNs will be omitted when performing the calculation.
      If insufficient data remains in the axis slice along which the
      statistic is computed, the corresponding entry of the output will be
      NaN.
    - ``raise``: if a NaN is present, a ``ValueError`` will be raised.
keepdims : bool, default: False
    If this is set to True, the axes which are reduced are left
    in the result as dimensions with size one. With this option,
    the result will broadcast correctly agai
```

## Quick recipe

```python
import scipy.stats as _m
score = _m.ranksums(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
