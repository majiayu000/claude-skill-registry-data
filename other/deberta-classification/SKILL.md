---
name: nlp-deberta-classification
description: Fine-tunes DeBERTa-v3 for text classification tasks. Use when building text classifiers, sentiment analysis, or multi-label classification on domain-specific data.
---

# DeBERTa Classification

## Overview

DeBERTa-v3 (Decoding-enhanced BERT with disentangled attention) is a strong baseline for text classification. It outperforms BERT/RoBERTa on most NLU benchmarks while maintaining similar inference cost.

## Quick Start

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

model_name = "microsoft/deberta-v3-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
```

## Workflow

1. Prepare dataset in HuggingFace Dataset format (text + label columns)
2. Tokenize with `max_length=512`, dynamic padding
3. Fine-tune with `TrainingArguments(lr=2e-5, epochs=3, warmup_ratio=0.1)`
4. Evaluate with accuracy, F1, and confusion matrix
5. Export model with `model.save_pretrained()`

## Key Decisions

- **Base vs Large**: Use `deberta-v3-base` (86M params) first. Only upgrade to `large` (304M) if base plateaus.
- **Max length**: 512 covers most tasks. Truncate long docs or use sliding window.
- **Learning rate**: 2e-5 is a safe default. Search [1e-5, 3e-5] if needed.

## References

- [DeBERTa-v3 paper](https://arxiv.org/abs/2111.09543)
- [HuggingFace model card](https://huggingface.co/microsoft/deberta-v3-base)
