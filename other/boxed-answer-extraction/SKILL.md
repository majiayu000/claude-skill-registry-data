---
name: llm-boxed-answer-extraction
description: Extract final numeric answers from LaTeX \boxed{} notation in LLM math reasoning output, scanning matches in reverse for robustness
---

# Boxed Answer Extraction

## Overview

Math-reasoning LLMs typically wrap their final answer in `\boxed{}`. However, chain-of-thought outputs may contain multiple `\boxed{}` occurrences (intermediate results, corrections). Scan all matches in reverse order and take the last non-empty one — this corresponds to the model's final answer after any self-corrections.

## Quick Start

```python
import re

def extract_boxed_answer(text):
    pattern = r'\\boxed\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
    matches = re.findall(pattern, text)
    if not matches:
        return None
    for match in reversed(matches):
        match = match.strip()
        if match:
            nums = re.findall(r'-?\d+', match)
            if nums:
                return int(nums[-1])
    return None

answers = [extract_boxed_answer(resp) for resp in responses]
valid = [a for a in answers if a is not None]
```

## Workflow

1. Generate reasoning chain from math LLM (DeepSeek-R1, QwQ, etc.)
2. Find all `\boxed{...}` matches via regex
3. Iterate matches in reverse (last = final answer)
4. Parse numeric content, handling nested braces and formatting
5. Apply domain constraints (e.g., modulo 1000 for competition)

## Key Decisions

- **Reverse scan**: models self-correct — intermediate \boxed{} may be wrong, last is final
- **Nested braces**: use non-greedy matching with brace balancing for `\boxed{\frac{1}{2}}`
- **Fallback**: if no \boxed{} found, try extracting last number from the response
- **Normalization**: strip LaTeX commands (`\frac`, `\text`) before numeric parsing

## References

- [Deepseek-r1-distill-qwen-7b](https://www.kaggle.com/code/itahiro/deepseek-r1-distill-qwen-7b)
- [[LB 20] QWQ-32B-preview Optimized inference](https://www.kaggle.com/code/mbmmurad/lb-20-qwq-32b-preview-optimized-inference)
