---
name: infolm
description: Compute the InfoLM metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute InfoLM, or asks how to score with InfoLM.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.text.InfoLM
  source: library_introspection
---

# infolm

> Metric `InfoLM` from `torchmetrics` (torchmetrics.text.InfoLM)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with InfoLM, or
mentions `torchmetrics.text.InfoLM` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics.text import InfoLM

# InfoLM(model_name_or_path: Union[str, os.PathLike] = 'bert-base-uncased', temperature: float = 0.25, information_measure: Literal['kl_divergence', 'alpha_divergence', 'beta_divergence', 'ab_divergence', 'renyi_divergence', 'l1_distance', 'l2_distance', 'l_infinity_distance', 'fisher_rao_distance'] = 'kl_divergence', idf: bool = True, alpha: Optional[float] = None, beta: Optional[float] = None, device: Union[str, torch.device, NoneType] = None, max_length: Optional[int] = None, batch_size: int = 64, num_threads: int = 0, verbose: bool = True, return_sentence_level_score: bool = False, **kwargs: dict[str, typing.Any]) -> None
```

## Library docstring

```
Calculate `InfoLM`_.

InfoLM measures a distance/divergence between predicted and reference sentence discrete distribution using one of
the following information measures:

    - `KL divergence`_
    - `alpha divergence`_
    - `beta divergence`_
    - `AB divergence`_
    - `Rényi divergence`_
    - L1 distance
    - L2 distance
    - L-infinity distance
    - `Fisher-Rao distance`_

`InfoLM`_ is a family of untrained embedding-based metrics which addresses some famous flaws of standard
string-based metrics thanks to the usage of pre-trained masked language models. This family of metrics is mainly
designed for summarization and data-to-text tasks.

The implementation of this metric is fully based HuggingFace ``transformers``' package.

As input to ``forward`` and ``update`` the metric accepts the following input:

- ``preds`` (:class:`~Sequence`): An iterable of hypothesis corpus
- ``target`` (:class:`~Sequence`): An iterable of reference corpus

As output of ``forward`` and ``compute`` the metric returns the following output:

-  ``infolm`` (:class:`~torch.Tensor`): If `return_sentence_level_score=True` return a tuple with a tensor
   with the corpus-level InfoLM score and a list of sentence-level InfoLM scores, else return a corpus-level
   InfoLM score

Args:
    model_name_or_path:
        A name or a model path used to load ``transformers`` pretrained model.
        By default the `"bert-base-uncased"` model is used.
    temperature:
        A temperature for calibrating language modelling. For more information, please reference `InfoLM`_ paper.
    information_measure:
        A name of information measure to be used. Please use one of: ['kl_divergence', 'alpha_divergence',
        'beta_divergence', 'ab_divergence', 'renyi_divergence', 'l1_distance', 'l2_distance', 'l_infinity_distance',
        'fisher_rao_distance']
    idf:
        An indication of whether normalization using inverse document frequencies should be used.
    alpha:
        Alpha parameter of the divergence used for alpha, AB and Rényi divergence measures.
    beta:
        Beta parameter of the divergence used for beta and AB divergence measures.
    device:
        A device to be used
```

## Quick recipe

```python
import torchmetrics.text as _m
score = _m.InfoLM(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
