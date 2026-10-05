---
name: nlp-length-sorted-batching
description: Sort texts by length before batching with dynamic padding to minimize wasted padding tokens and speed up transformer inference
---

# Length-Sorted Batching

## Overview

When using dynamic padding (`padding='longest'`), batch padding length equals the longest sequence in the batch. If a 512-token text lands in a batch of 20-token texts, every sample pads to 512. Sorting by length first ensures each batch contains similarly-sized texts, drastically reducing total padding tokens. Typical speedup: 1.5–3x on inference.

## Quick Start

```python
from transformers import DataCollatorWithPadding

df['length'] = df['text'].apply(len)
df = df.sort_values('length').reset_index(drop=True)

dataset = Dataset.from_pandas(df)
tokenized = dataset.map(lambda x: tokenizer(x['text'], truncation=True),
                        batched=True)

loader = DataLoader(
    tokenized, batch_size=32, shuffle=False,
    collate_fn=DataCollatorWithPadding(tokenizer, padding='longest')
)
```

## Workflow

1. Compute text length (character or token count) for each sample
2. Sort DataFrame by length ascending
3. Save original index to restore order after inference
4. Create DataLoader with `shuffle=False` and `padding='longest'`
5. Run inference, then reorder predictions to original order

## Key Decisions

- **Character vs token length**: character length is faster to compute and correlates well enough
- **Inference only**: for training, use bucket sampling instead (preserves randomness within length ranges)
- **Restore order**: always save the original index — predictions must align with input rows
- **Batch size**: larger batches amplify the benefit; small batches (4-8) see less improvement

## References

- [all-minilm-l6-v2 tuning_model_add](https://www.kaggle.com/code/yuiwai/all-minilm-l6-v2-tuning-model-add)
- [LECR Inference P](https://www.kaggle.com/code/ragnar123/lecr-inference-p)
