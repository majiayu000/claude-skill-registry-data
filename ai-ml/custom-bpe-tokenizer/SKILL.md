---
name: nlp-custom-bpe-tokenizer
description: >
  Trains a Byte-Pair Encoding tokenizer on the task corpus to capture domain-specific vocabulary, typos, and subword patterns.
---
# Custom BPE Tokenizer

## Overview

Instead of relying on a pretrained tokenizer's vocabulary, train a BPE tokenizer on your task's text corpus. This captures domain-specific terms, common misspellings, and subword patterns unique to your data. Particularly effective when the test distribution differs from standard pretraining corpora (e.g., student essays, generated text, medical notes).

## Quick Start

```python
from tokenizers import Tokenizer, models, trainers, normalizers, pre_tokenizers

def train_bpe_tokenizer(texts, vocab_size=30000, lowercase=False):
    """Train BPE tokenizer on task corpus."""
    tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))

    norm_list = [normalizers.NFC()]
    if lowercase:
        norm_list.append(normalizers.Lowercase())
    tokenizer.normalizer = normalizers.Sequence(norm_list)
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()

    special_tokens = ["[UNK]", "[PAD]", "[CLS]", "[SEP]", "[MASK]"]
    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=special_tokens,
        min_frequency=2,
    )

    tokenizer.train_from_iterator(texts, trainer=trainer)
    return tokenizer

# Train on both train + test text (unsupervised, no leakage)
all_texts = list(train_df['text']) + list(test_df['text'])
tokenizer = train_bpe_tokenizer(all_texts, vocab_size=30000)

# Use with TF-IDF or as input to models
tokenized = [tokenizer.encode(t).tokens for t in texts]
```

## Workflow

1. Collect all text from train + test (no labels needed — unsupervised)
2. Train BPE tokenizer with task-appropriate vocab size
3. Tokenize all texts with the custom tokenizer
4. Feed tokenized output into TF-IDF vectorizer or downstream model

## Key Decisions

- **Include test text**: Yes — tokenizer training is unsupervised, no label leakage
- **Vocab size**: 30k for general text; larger (100k+) for character-level patterns like typo detection
- **Lowercase**: Keep case for AI-detection tasks (case patterns are signal); lowercase for topic classification
- **vs pretrained**: Custom captures domain drift; pretrained has better general coverage — try both

## References

- LLM - Detect AI Generated Text (Kaggle)
- Source: [train-your-own-tokenizer](https://www.kaggle.com/code/datafan07/train-your-own-tokenizer)
