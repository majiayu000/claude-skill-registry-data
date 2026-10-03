---
name: nemotron-3-nano
title: "Nemotron 3 Nano: MoE Hybrid Mamba-Transformer for Agentic Reasoning"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.20848
keywords: [mixture-of-experts, mamba-transformer, efficient, agentic, moe]
description: "Efficient agentic reasoning via sparse MoE activating 50% parameters per token. Combines Mamba-Transformer hybrid with 6-of-128 expert routing, three-stage post-training (SFT, verifiable RL, RLHF), and Group Relative Length Control—achieving 3.3× inference throughput of competitors while maintaining 1M token context support and superior reasoning."
---

## Overview

Nemotron 3 Nano achieves efficiency through sparse mixture-of-experts combined with hybrid Mamba-Transformer architecture, backed by sophisticated post-training methodology.

## Core Technique

**Sparse MoE with Hybrid Architecture:**
31.6B total parameters, 3.2B active per token (20% activation).

```python
class NemotronNanoMoE:
    def __init__(self):
        # 6-of-128 expert selection
        self.num_experts = 128
        self.top_k = 6  # Activate only 6 experts per token
        self.router = nn.Linear(hidden_dim, 128)
        self.experts = nn.ModuleList([MambaTransformerBlock() for _ in range(128)])

    def forward(self, x):
        # Router selects top-6 experts
        router_logits = self.router(x)
        expert_indices = torch.topk(router_logits, k=6, dim=-1).indices

        # Activate selected experts only
        output = 0
        for idx in range(6):
            expert = self.experts[expert_indices[:, idx]]
            output = output + expert(x)

        return output / 6
```

**Three-Stage Post-Training:**

```python
def nemotron_nano_training(base_model):
    # Stage 1: Supervised Fine-Tuning
    model = sft_training(base_model, reasoning_data)

    # Stage 2: Verifiable Reinforcement Learning
    model = rlvr_training(model)

    # Stage 3: RLHF with Length Control
    model = rlhf_with_length_control(model)

    return model
```

**Group Relative Length Control:**
Prevent excessive reasoning token generation while maintaining quality.

```python
def group_relative_length_reward(trajectory, length_penalty=0.1):
    """
    Length-normalized reward adjustment prevents models from
    inflating reasoning token counts.
    """
    accuracy_reward = 1.0 if trajectory.correct else 0.0
    length_normalized = accuracy_reward / (1.0 + length_penalty * trajectory.num_tokens)
    return length_normalized
```

## When to Use This Technique

Use when: Deploying efficient models at scale, inference throughput critical, agentic reasoning needed, long-context (1M) support required.

## When NOT to Use This Technique

Avoid if: Max accuracy required, specialized domain needs full parameter activation.

## Implementation Notes

Requires: 128 expert modules, router network, RLVR training, length-controlled reward, 1M token support.

## Key Performance

- 3.3× higher throughput than competitors
- 31.6B parameters, 3.2B active
- Competitive reasoning despite sparsity
- 1M token context support

## References

- Sparse MoE with 6-of-128 expert selection
- Hybrid Mamba-Transformer blocks as experts
- Three-stage post-training methodology
- Group Relative Length Control for RL
