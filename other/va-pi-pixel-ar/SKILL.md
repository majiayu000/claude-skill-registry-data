---
name: va-pi-pixel-ar
title: "VA-π: Variational Policy Alignment for Pixel-Aware AR Generation"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.19680
keywords: [autoregressive, image-generation, reinforcement-learning, pixel-alignment]
description: "Align autoregressive image models with pixel-space quality via variational optimization. Formulates alignment as ELBO combining reconstruction (pixel supervision) and prior regularization (token distribution), treating model as RL policy with tokenizer reconstruction as reward—achieving 86.6% cost reduction vs standard RL fine-tuning."
---

## Overview

VA-π addresses the token-to-pixel mismatch in autoregressive image generation through principled variational alignment, eliminating expensive standard RL fine-tuning.

## Core Technique

**Variational Alignment Formulation:**

```python
class VariationalAlignment:
    def __init__(self, ar_model, tokenizer):
        self.ar_model = ar_model
        self.tokenizer = tokenizer
        self.optimizer = torch.optim.Adam(ar_model.parameters())

    def elbo_loss(self, images, prompts):
        """
        Evidence Lower Bound combining pixel reconstruction and prior.
        """
        # Sample tokens from AR model
        z_sampled = self.ar_model.sample(prompts)

        # Reconstruction term: pixel-space supervision
        reconstructed = self.tokenizer.decode(z_sampled)
        reconstruction_loss = mse(reconstructed, images)

        # Prior term: preserve token distribution
        z_prior = self.tokenizer.encode(images)  # Ground truth
        prior_loss = cross_entropy(z_sampled, z_prior)

        # ELBO = reconstruction + prior
        elbo = reconstruction_loss + 0.1 * prior_loss

        return elbo
```

**RL Formulation with Intrinsic Reward:**

```python
def pixel_quality_reward(tokens, images, tokenizer):
    """
    Tokenizer reconstruction quality is RL reward signal.
    """
    reconstructed = tokenizer.decode(tokens)
    mse_error = mse(reconstructed, images)
    reward = -mse_error  # Negative MSE as reward
    return reward

def policy_gradient_with_pixel_reward(ar_model, images, prompts):
    """
    Treat AR model as RL policy, pixel quality as reward.
    """
    tokens_sampled = ar_model.sample(prompts)
    reward = pixel_quality_reward(tokens_sampled, images, tokenizer)

    # Policy gradient
    log_prob = ar_model.log_probability(tokens_sampled)
    policy_loss = -reward * log_prob

    return policy_loss
```

**Computational Efficiency:**

```
Standard RL fine-tuning: expensive per-episode rollouts
VA-π: 25 minutes on 1% ImageNet-1K
Cost reduction: 86.6% vs standard RL
```

## When to Use

Use when: AR image generation, pixel quality important, training efficiency critical.

## Performance

- FID: 14.36 → 7.65
- IS: 86.55 → 116.70
- 86.6% cost reduction vs RL fine-tuning

## References

- Variational alignment with ELBO
- Tokenizer reconstruction as reward
- RL policy formulation for AR models
