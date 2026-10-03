---
name: nemotron-3
title: "NVIDIA Nemotron 3: Efficient and Open Intelligence"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.20856
keywords: [language-model, mixture-of-experts, mamba-transformer, moe, efficient]
description: "Build efficient open-source LLMs via hybrid Mamba-Transformer MoE architecture with LatentMoE expert design, multi-token prediction training, FP4 precision, and multi-environment RL post-training—achieving 3.3× higher throughput than equivalently-sized models while maintaining state-of-the-art reasoning, coding, and tool-use capabilities."
---

## Overview

Nemotron 3 combines five efficiency innovations to create high-performance open models. The core architectural change—hybrid Mamba-Transformer with MoE—reduces KV cache overhead while maintaining accuracy through careful expert design and multi-environment training.

## Core Technique

**Hybrid Mamba-Transformer MoE Architecture:**
Replace expensive self-attention with cheaper Mamba layers, retaining attention where needed.

```python
class HybridMambaTransformerMoE:
    def __init__(self, num_layers=32, num_experts=128, top_k=6):
        self.layers = nn.ModuleList()
        for i in range(num_layers):
            if i % 2 == 0:
                # Even layers: Mamba (cheaper)
                layer = MambaLayer()
            else:
                # Odd layers: MoE (routed)
                layer = MixtureOfExpertsLayer(num_experts, top_k)
            self.layers.append(layer)

    def forward(self, x):
        """Alternate between Mamba and MoE."""
        for layer in self.layers:
            x = layer(x)
        return x
```

**LatentMoE (Hardware-Aware Expert Design):**
Project tokens to latent space before routing to reduce routed parameters.

```python
class LatentMoE(nn.Module):
    def __init__(self, input_dim=4096, latent_dim=1024, num_experts=128):
        self.projection_in = nn.Linear(input_dim, latent_dim)
        self.experts = nn.ModuleList([
            nn.Linear(latent_dim, latent_dim) for _ in range(num_experts)
        ])
        self.router = Router(latent_dim, num_experts)
        self.projection_out = nn.Linear(latent_dim, input_dim)

    def forward(self, x):
        """Project to latent, route, return to original dimension."""
        # Project down: d/ℓ reduction (e.g., 4× reduction)
        latent = self.projection_in(x)

        # Route in latent space (reduced parameters and traffic)
        expert_idx = self.router(latent)
        expert_out = self.experts[expert_idx](latent)

        # Project back to original dimension
        output = self.projection_out(expert_out)

        return output
```

**Multi-Token Prediction (MTP):**
Train models to predict multiple future tokens simultaneously for richer signals.

```python
def multi_token_prediction_loss(model, input_ids, target_ids, num_predict=5):
    """
    Predict next 5 tokens in parallel, providing richer supervision.
    """
    logits = model(input_ids)

    # Standard loss for next token
    next_token_loss = cross_entropy(logits[:, -1, :], target_ids[:, 0])

    # Bonus losses for future tokens
    mtp_loss = 0
    for i in range(1, num_predict):
        if i < target_ids.shape[1]:
            future_logits = logits[:, -(num_predict - i), :]
            future_loss = cross_entropy(future_logits, target_ids[:, i])
            mtp_loss += 0.1 * future_loss

    total_loss = next_token_loss + mtp_loss
    return total_loss
```

**NVFP4 Training (4-bit Floating Point):**
Use FP4 for weights, activations, and gradients on compatible hardware.

```python
def nvfp4_quantization(model):
    """
    Convert to 4-bit floating point for 3× speedup on GB300.
    """
    for name, param in model.named_parameters():
        if 'weight' in name or 'activation' in name:
            # Quantize to FP4
            param.data = quantize_to_fp4(param.data)

    # Gradient computation also in FP4
    # Maintains comparable accuracy to BF16 with 3× throughput
    return model
```

**Multi-Environment RL Post-Training:**
Train on diverse environments simultaneously for broad capability coverage.

```python
def multi_environment_rl_training(model, num_envs=4):
    """
    Post-train on multiple RL environments concurrently:
    - Reasoning (math, logic)
    - Coding (code generation, debugging)
    - Tool use (API calling, function orchestration)
    - Long-context (extended document understanding)
    """
    environments = [
        ReasoningEnvironment(),
        CodingEnvironment(),
        ToolUseEnvironment(),
        LongContextEnvironment()
    ]

    for env in environments:
        # Collect rollouts
        rollouts = env.collect_rollouts(model, num_episodes=1000)

        # RL training (GRPO)
        model = train_with_grpo(model, rollouts, reward_fn=env.reward)

    return model
```

## When to Use This Technique

Use Nemotron 3 when:
- Building efficient open-source models
- Throughput is critical
- Multi-capability agents needed
- Extended context support required (1M tokens)

## When NOT to Use This Technique

Avoid if:
- Max accuracy needed (MoE not perfectly optimal)
- Inference hardware not compatible with Mamba
- FP4 support unavailable

## Implementation Notes

Requires: Mamba implementation, MoE routing, LatentMoE projection, multi-token prediction, FP4 support, multi-environment RL.

## Key Performance

- 3.3× higher throughput than similarly-sized models
- State-of-the-art reasoning, coding, tool-use
- 1M token context support
- Open-source availability

## References

- Hybrid Mamba-Transformer MoE architecture
- LatentMoE for hardware-aware expert design
- Multi-token prediction for training signals
- NVFP4 precision training
- Multi-environment RL post-training
