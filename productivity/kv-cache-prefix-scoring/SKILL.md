---
name: llm-kv-cache-prefix-scoring
description: >
  Shares KV cache from a common prefix (context+question) across multiple answer suffixes for efficient multi-choice scoring.
---
# KV Cache Prefix Scoring

## Overview

For multiple-choice QA, the context and question are shared across all answer options. Compute the KV cache once for this shared prefix, then score each answer suffix by expanding the cache. This avoids redundant computation — scoring 5 options costs ~1.2x of a single forward pass instead of 5x.

## Quick Start

```python
import torch

def score_options(model, prefix_ids, suffix_ids_list):
    """Score multiple suffixes against a shared prefix."""
    with torch.no_grad():
        # Forward pass on shared prefix — cache the KV states
        prefix_out = model(prefix_ids, use_cache=True)
        kv_cache = prefix_out.past_key_values

        scores = []
        for suffix_ids in suffix_ids_list:
            # Expand cache to match suffix batch
            expanded_kv = [(k.expand_as(k), v.expand_as(v)) for k, v in kv_cache]
            out = model(suffix_ids, past_key_values=expanded_kv)
            # Score = mean log-prob of suffix tokens
            logprobs = torch.log_softmax(out.logits[:, :-1], dim=-1)
            token_scores = logprobs.gather(2, suffix_ids[:, 1:].unsqueeze(-1))
            scores.append(token_scores.mean().item())
    return scores
```

## Workflow

1. Tokenize shared prefix (context + question)
2. Run single forward pass to get KV cache
3. For each answer option, run forward pass with cached KV states
4. Score each option by mean log-probability of suffix tokens
5. Rank options by score

## Key Decisions

- **Memory**: Cache is ~2x model hidden size per layer; fits for models up to 13B on T4
- **Scoring metric**: Mean log-prob normalizes for option length differences
- **Batch suffixes**: If GPU memory allows, batch all suffixes in one pass
- **Applicability**: Any LLM multiple-choice or ranking task

## References

- Kaggle LLM Science Exam (Kaggle)
- Source: [platypus2-70b-with-wikipedia-rag](https://www.kaggle.com/code/simjeg/platypus2-70b-with-wikipedia-rag)
