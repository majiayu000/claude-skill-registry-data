---
name: squad
description: Compute the SQuAD metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute SQuAD, or asks how to score with SQuAD.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.SQuAD
  source: library_introspection
---

# squad

> Metric `SQuAD` from `torchmetrics` (torchmetrics.SQuAD)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with SQuAD, or
mentions `torchmetrics.SQuAD` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import SQuAD

# _SQuAD(**kwargs: Any) -> None
```

## Library docstring

```
Wrapper for deprecated import.

>>> preds = [{"prediction_text": "1976", "id": "56e10a3be3433e1400422b22"}]
>>> target = [{"answers": {"answer_start": [97], "text": ["1976"]}, "id": "56e10a3be3433e1400422b22"}]
>>> squad = _SQuAD()
>>> squad(preds, target)
{'exact_match': tensor(100.), 'f1': tensor(100.)}
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.SQuAD(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
