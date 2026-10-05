---
name: llm-binary-answer-clamping
description: Force-clamp free-form LLM output to binary yes/no with keyword matching and a fallback default for constrained environments
---

# Binary Answer Clamping

## Overview

When an LLM must produce a strictly binary response (yes/no, true/false) but generates free-form text, post-process the output by searching for target keywords and clamping to the expected format. This handles verbose responses ("Yes, I believe so"), hedged answers ("It might be"), and empty outputs. A configurable default handles cases where neither keyword appears.

## Quick Start

```python
def clamp_binary(response, positive="yes", negative="no", default="yes"):
    if response is None or len(response.strip()) == 0:
        return default

    text = response.lower().strip()

    if positive in text and negative not in text:
        return positive
    if negative in text and positive not in text:
        return negative
    if positive in text and negative in text:
        # Both present — check which appears first
        return positive if text.index(positive) < text.index(negative) else negative

    return default

raw = model.generate(prompt, max_new_tokens=20)
answer = clamp_binary(raw)
```

## Workflow

1. Generate LLM response with short max_new_tokens (5-20)
2. Check for positive/negative keywords in lowercased output
3. Handle ambiguous cases (both present → use first occurrence)
4. Return default when neither keyword found or output is empty

## Key Decisions

- **Default value**: choose based on domain — "yes" is safer for entity-matching games
- **max_new_tokens**: keep low (1-20) to reduce ambiguity and speed up inference
- **Keyword priority**: first occurrence wins when both present
- **Extensions**: add confidence extraction by checking for hedging words ("maybe", "probably")

## References

- [llama3-8b- LLM20 Questions [LB 750]](https://www.kaggle.com/code/wouldyoujustfocus/llama3-8b-llm20-questions-lb-750)
- [Starter Code for Llama 8B LLM - [LB 0.750+]](https://www.kaggle.com/code/cdeotte/starter-code-for-llama-8b-llm-lb-0-750)
