---
name: cv-vqa-yes-no-logit-scoring
description: >
  Extracts calibrated yes/no probabilities from a VQA model by masking all logits except yes/no token variants and renormalizing via softmax.
---
# VQA Yes/No Logit Scoring

## Overview

Visual Question Answering models can score image-text alignment by asking "Does this image match [description]? Answer yes or no." But taking `argmax` gives a binary answer, not a confidence score. This technique masks all vocabulary logits except the yes/no tokens (including space-prefixed variants like ` yes`), applies softmax over just those 4 tokens, then sums the yes-variants to get a calibrated probability. This converts any VQA model into a continuous image-text scorer without fine-tuning.

## Quick Start

```python
import torch

class VQAScorer:
    def __init__(self, model, processor):
        self.model = model
        self.processor = processor
        tok = processor.tokenizer
        self.yes_ids = [tok.convert_tokens_to_ids(t) for t in ['yes', ' yes']]
        self.no_ids = [tok.convert_tokens_to_ids(t) for t in ['no', ' no']]

    @torch.no_grad()
    def score(self, image, question):
        inputs = self.processor(images=image, text=question, return_tensors='pt').to('cuda')
        logits = self.model(**inputs).logits[:, -1, :]

        mask = torch.full_like(logits, float('-inf'))
        for tid in self.yes_ids + self.no_ids:
            mask[:, tid] = logits[:, tid]

        probs = torch.softmax(mask, dim=-1)
        p_yes = sum(probs[0, tid].item() for tid in self.yes_ids)
        p_no = sum(probs[0, tid].item() for tid in self.no_ids)
        return p_yes / (p_yes + p_no)

scorer = VQAScorer(model, processor)
score = scorer.score(image, f'Does this image show "{desc}"? Answer yes or no.')
```

## Workflow

1. Feed image + yes/no question to VQA model
2. Extract logits from the last generated token position
3. Mask all logits to -inf except yes/no token IDs (including space variants)
4. Softmax over masked logits
5. Sum yes-variant probabilities and normalize

## Key Decisions

- **Token variants**: Include both `yes` and ` yes` (space-prefixed) — tokenizers handle them differently
- **Last token**: Use logits at position -1 (the next-token prediction position)
- **Question phrasing**: "Answer yes or no" constrains the model to the target tokens
- **Multi-criteria**: Ask multiple questions (fidelity, text presence, style) and combine scores

## References

- [SD Boost via Default SVG](https://www.kaggle.com/code/taikimori/old-metric-lb-0-694-sd-boost-via-my-default-svg)
