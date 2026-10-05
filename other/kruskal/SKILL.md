---
name: kruskal
description: Compute the kruskal metric — provided by scipy.stats. Use when the user has predictions and ground-truth and needs to compute kruskal, or asks how to score with kruskal.
metadata:
  skill_kind: metric
  source_lib: scipy.stats
  import_path: scipy.stats.kruskal
  source: library_introspection
---

# kruskal

> Metric `kruskal` from `scipy.stats` (scipy.stats.kruskal)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with kruskal, or
mentions `scipy.stats.kruskal` directly, or wants the standard scipy.stats implementation.

## Reference signature

```python
from scipy.stats import kruskal

# kruskal(*samples, nan_policy='propagate', axis=0, keepdims=False)
```

## Library docstring

```
Compute the Kruskal-Wallis H-test for independent samples.

The Kruskal-Wallis H-test tests the null hypothesis that the population
median of all of the groups are equal.  It is a non-parametric version of
ANOVA.  The test works on 2 or more independent samples, which may have
different sizes.  Note that rejecting the null hypothesis does not
indicate which of the groups differs.  Post hoc comparisons between
groups are required to determine which groups are different.

Parameters
----------
sample1, sample2, ... : array_like
    Two or more arrays with the sample measurements can be given as
    arguments. Samples must be one-dimensional.
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
axis : int or None, default: 0
    If an int, the axis of the input along which to compute the statistic.
    The statistic of each axis-slice (e.g. row) of the input will appear in a
    corresponding element of the output.
    If ``None``, the input will be raveled before computing the statistic.
keepdims : bool, default: False
    If this is set to True, the axes which are reduced are left
    in the result as dimensions with size one. With this option,
    the result will broadcast correctly against the input array.

Returns
-------
statistic : float
    The Kruskal-Wallis H statistic, corrected for ties.
pvalue : float
    The p-value for the test using the assumption that H has a chi
    square distribution. The p-value returned is the survival function of
    the chi square distribution evaluated at H.

See Also
--------

:func:`f_oneway`
    1-way ANOVA.
:func:`mannwhitneyu`
    Mann-Whitney rank test on two samples.
:func:`friedmanchisquare`
    Friedman test for repeated meas
```

## Quick recipe

```python
import scipy.stats as _m
score = _m.kruskal(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
