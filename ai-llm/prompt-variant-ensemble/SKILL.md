---
name: llm-prompt-variant-ensemble
description: Generate multiple LLM responses using diverse system prompt variants to increase reasoning diversity for self-consistency voting
---

# Prompt Variant Ensemble

## Overview

When using self-consistency (majority voting over multiple LLM outputs), all responses sharing the same prompt tend to follow similar reasoning paths — reducing effective diversity. By rotating through multiple distinct system prompts that differ in tone, instruction style, or emphasis, the model explores more diverse reasoning strategies, improving the quality of majority vote aggregation.

## Quick Start

```python
PROMPT_VARIANTS = [
    "You are a math expert. Solve step by step. Put your answer in \\boxed{}.",
    "Please reflect and verify while reasoning. Put the answer in \\boxed{}.",
    "Solve using concise, clear reasoning. Place the answer in \\boxed{}.",
    "Think carefully and double-check your work. Answer in \\boxed{}.",
    "You are good at reverse thinking to recheck answers. Answer in \\boxed{}.",
]

def create_messages(question, variant_idx):
    return [
        {"role": "system", "content": PROMPT_VARIANTS[variant_idx % len(PROMPT_VARIANTS)]},
        {"role": "user", "content": question},
    ]

# Generate with rotating prompts
all_messages = [create_messages(q, i) for i in range(num_samples)]
responses = llm.generate(all_messages, sampling_params)
```

## Workflow

1. Define 3-7 system prompt variants with different reasoning instructions
2. For each generation, cycle through variants using modulo indexing
3. Generate N responses total (e.g., 16), distributed across variants
4. Extract answers and aggregate via majority voting

## Key Decisions

- **Variant count**: 3-7 variants; too many dilutes each variant's sample count
- **Diversity sources**: tone (expert vs careful), strategy (step-by-step vs verify), emphasis (concise vs thorough)
- **Distribution**: weight variants by expected quality — e.g., 13 of one + 3 of another
- **Combined with temperature**: use temperature > 0 AND prompt variants for maximum diversity

## References

- [Deepseek-r1-distill-qwen-7b](https://www.kaggle.com/code/itahiro/deepseek-r1-distill-qwen-7b)
- [[LB24] Deepseek-R1 with more prompt Engineering](https://www.kaggle.com/code/haoruili/lb24-deepseek-r1-with-more-prompt-engineering)
