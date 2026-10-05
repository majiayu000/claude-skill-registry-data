---
name: nlp-domain-wordpiece-tfidf
description: >
  Trains a WordPiece tokenizer on in-domain text, then feeds its subword token IDs into TF-IDF vectorization for domain-adapted sparse features.
---
# Domain WordPiece TF-IDF

## Overview

Standard TF-IDF uses whitespace or regex tokenization, which misses subword patterns important in domain-specific text (misspellings, slang, coded language in toxic text). Training a WordPiece tokenizer on the domain corpus learns meaningful subword units, then feeding these token IDs into TF-IDF creates sparse features that capture domain-specific vocabulary at the subword level. This bridges the gap between neural tokenizers and classical ML — you get BPE-quality tokenization with TF-IDF + Ridge regression speed.

## Quick Start

```python
from tokenizers import Tokenizer, models, normalizers, pre_tokenizers, trainers
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge

# Train WordPiece tokenizer on domain text
tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
tokenizer.normalizer = normalizers.BertNormalizer(lowercase=True)
tokenizer.pre_tokenizer = pre_tokenizers.BertPreTokenizer()
trainer = trainers.WordPieceTrainer(vocab_size=25000)

def corpus_iter():
    for text in df['text']:
        yield text

tokenizer.train_from_iterator(corpus_iter(), trainer=trainer)

# Tokenize all texts
tokenized = [tokenizer.encode(t).ids for t in df['text']]

# Feed into TF-IDF with identity tokenizer (already tokenized)
identity = lambda x: x
vectorizer = TfidfVectorizer(
    analyzer='word', tokenizer=identity,
    preprocessor=identity, token_pattern=None)
X = vectorizer.fit_transform(tokenized)

model = Ridge(alpha=0.8)
model.fit(X, df['score'])
```

## Workflow

1. Train WordPiece tokenizer on all available text (train + test)
2. Tokenize texts to get lists of token IDs
3. Pass token ID lists to TfidfVectorizer with identity tokenizer/preprocessor
4. Train a linear model (Ridge, SVM) on the sparse TF-IDF matrix

## Key Decisions

- **vocab_size**: 20k-30k; larger captures more subwords but increases sparsity
- **vs BPE**: WordPiece and BPE produce similar subwords; WordPiece is simpler to train via HuggingFace tokenizers
- **Why not just transformers**: 100x faster training, no GPU needed, competitive for simple ranking tasks
- **Train on all text**: Include test text in tokenizer training (not labels) for better vocabulary coverage

## References

- [Try better parameters better score](https://www.kaggle.com/code/yanhf16/0-9-try-better-parameters-better-score)
