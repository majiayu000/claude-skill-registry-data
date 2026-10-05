---
name: cv-pack-padded-sequence-loss
description: >
  Uses pack_padded_sequence to exclude padding tokens from cross-entropy loss in variable-length sequence generation.
---
# Pack Padded Sequence Loss

## Overview

In image captioning and seq2seq tasks, target sequences have different lengths and are padded. Computing cross-entropy on padding tokens wastes compute and leaks gradient noise. `pack_padded_sequence` strips out padding positions before loss computation, giving a clean loss signal from real tokens only.

## Quick Start

```python
from torch.nn.utils.rnn import pack_padded_sequence

# Sort batch by decreasing sequence length (required by pack_padded_sequence)
caption_lengths, sort_ind = caption_lengths.squeeze(1).sort(dim=0, descending=True)
predictions = predictions[sort_ind]
targets = targets[sort_ind]
decode_lengths = (caption_lengths - 1).tolist()  # exclude <sos>

# Pack to strip padding, then compute loss on real tokens only
packed_preds = pack_padded_sequence(predictions, decode_lengths, batch_first=True).data
packed_targets = pack_padded_sequence(targets, decode_lengths, batch_first=True).data

loss = nn.CrossEntropyLoss()(packed_preds, packed_targets)
```

## Workflow

1. Sort batch by sequence length (descending)
2. Compute `decode_lengths` = actual length of each target sequence
3. Pack both predictions and targets with `pack_padded_sequence`
4. Compute cross-entropy on `.data` attribute (flattened real tokens)
5. Backpropagate — gradients only flow through non-padding positions

## Key Decisions

- **Sort requirement**: `pack_padded_sequence` requires descending sort; re-sort encoder outputs too
- **Alternative**: Use `ignore_index` in CrossEntropyLoss for padding token ID — simpler but slightly less efficient
- **Combine with**: Teacher forcing during training, greedy/beam search during inference
- **Metrics**: Compute Levenshtein distance or BLEU on unpacked decoded sequences

## References

- [InChI / Resnet + LSTM with attention / starter](https://www.kaggle.com/code/yasufuminakama/inchi-resnet-lstm-with-attention-starter)
