---
name: dirl-diffusion-rl
title: "DiRL: Efficient Post-Training for Diffusion Language Models"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.22234
keywords: [diffusion-language-model, reinforcement-learning, policy-optimization]
description: "Enable effective RL for diffusion language models via DiPO (unbiased GRPO for dLLMs) and framework optimizations. FlexAttention accelerates blockwise training, LMDeploy optimizes inference, achieving training-inference consistency—improving dLLM math performance to rival larger autoregressive models."
---

## Overview

DiRL introduces RL infrastructure tailored for diffusion language models.

## Core Technique

**DiPO Algorithm:**
First unbiased Group Relative Policy Optimization for dLLMs.

```python
def dipo_training(model, dataset):
    # Blockwise attention for efficient computation
    # Unbiased logit computation (fixes prior biases)
    # GRPO with dLLM-specific optimizations
```

## Performance

- State-of-the-art dLLM math performance
- Outperforms larger autoregressive models

## References

- DiPO: unbiased GRPO for dLLMs
- Blockwise training optimization
