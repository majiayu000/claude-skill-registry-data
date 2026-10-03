---
name: shape-of-thought
title: "Shape of Thought: When Distribution Matters More Than Correctness"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.22255
keywords: [training-data, reasoning, distribution-alignment, synthetic-data]
description: "Demonstrate that synthetic CoT traces with incorrect final answers outperform human-written correct solutions for supervised fine-tuning. Distribution proximity between training data and student model's natural output matters more than correctness—validating human traces with model-like distributions improves performance, providing practical guidance for dataset curation."
---

## Overview

Challenges conventional wisdom that training data quality depends primarily on correctness.

## Core Technique

**Distribution Proximity Hypothesis:**

```python
# Human traces (H): correct but distribution-mismatched
# Model traces correct (G): correct and distribution-matched
# Model traces incorrect (W): incorrect but distribution-matched

# W outperforms H despite incorrectness
# because distribution proximity enables faster learning
```

## When to Use

Use when: Curating reasoning datasets, SFT training, synthetic data selection.

## References

- Distribution alignment vs correctness
- Partial correctness in synthetic data
- Dataset curation guidance
