---
name: world-cache
title: "WorldCache: Accelerating World Models for Free via Heterogeneous Token Caching"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2603.06331"
keywords: [World Models, Inference Optimization, Caching, Diffusion Models, Token Prediction]
description: "Accelerates iterative world model inference by classifying tokens by temporal curvature (predictability) and applying differentiated caching: stable tokens reused, linear tokens extrapolated, chaotic tokens updated. Achieves 3.7x speedup with 98% rollout quality."
---

# WorldCache: Heterogeneous Token Caching for Fast World Model Rollouts

Diffusion-based world models require iterative denoising at each inference step, making them prohibitively slow for real-time simulation. Token heterogeneity in world models—where structural features change nonlinearly while background elements evolve smoothly—makes uniform caching strategies fail. Some tokens can be safely reused, others need linear extrapolation, and critical chaotic tokens demand full updates. WorldCache exploits this heterogeneity through curvature-guided classification, achieving 3.7x speedup.

## Core Concept

Rather than caching all tokens uniformly or recomputing everything, classify tokens into three categories based on temporal curvature (local nonlinearity of token trajectory):

- **Stable tokens** (low curvature): Evolve predictably; directly reuse from cache
- **Linear tokens** (moderate curvature): Evolve smoothly; use first-order extrapolation
- **Chaotic tokens** (high curvature): Exhibit sharp nonlinear changes; apply damped update mixing recent velocities

Monitor only chaotic tokens for drift accumulation, triggering full backbone evaluation only when their drift exceeds threshold. This avoids per-token overhead while maintaining quality on critical features.

## Architecture Overview

- **Curvature Scoring**: Measure temporal nonlinearity of each token's evolution across denoising steps
- **Token Classification**: Partition tokens into stable/linear/chaotic based on curvature threshold
- **Heterogeneous Prediction**: Apply differentiated strategies per class
- **Drift Monitoring**: Accumulate normalized drift signal from chaotic tokens only
- **Adaptive Skipping**: Trigger full backbone evaluation when chaotic-token drift exceeds threshold η

## Implementation Steps

Implement curvature-based token classification and heterogeneous caching strategies within a diffusion world model loop.

**Compute Curvature Score**

Measure token-level temporal nonlinearity using discrete curvature of the token's trajectory:

```python
import torch
import numpy as np

def compute_token_curvatures(token_history, window_size=3):
    """
    Compute curvature (local nonlinearity) for each token position.

    Args:
        token_history: tensor of shape [num_steps, num_tokens, feature_dim]
                       tracking token evolution across denoising steps
        window_size: number of consecutive steps for local curvature (typically 3)

    Returns:
        curvatures: [num_tokens] tensor with scalar curvature per token
    """
    num_steps = token_history.shape[0]
    num_tokens = token_history.shape[1]
    curvatures = torch.zeros(num_tokens, device=token_history.device)

    # Compute curvature using centered differences over recent steps
    if num_steps >= window_size:
        # Use last 'window_size' steps for local curvature
        recent = token_history[-window_size:, :, :]  # [window_size, num_tokens, dim]

        # First derivative (velocity)
        v1 = recent[1] - recent[0]  # [num_tokens, dim]
        v2 = recent[2] - recent[1]  # [num_tokens, dim]

        # Second derivative (acceleration)
        acceleration = v2 - v1  # [num_tokens, dim]

        # Curvature: magnitude of acceleration normalized by velocity magnitude
        vel_magnitude = torch.norm(v1, dim=1, keepdim=True) + 1e-8  # [num_tokens, 1]
        curvatures = torch.norm(acceleration, dim=1) / vel_magnitude.squeeze(1)

    return curvatures


def classify_tokens(curvatures, curvature_thresholds=(0.1, 0.5)):
    """
    Classify tokens into stable/linear/chaotic based on curvature.

    Args:
        curvatures: [num_tokens] curvature scores
        curvature_thresholds: tuple (low, high) defining class boundaries

    Returns:
        token_classes: [num_tokens] with values 0=stable, 1=linear, 2=chaotic
    """
    low_thresh, high_thresh = curvature_thresholds
    token_classes = torch.zeros_like(curvatures, dtype=torch.long)

    token_classes[curvatures >= low_thresh] = 1  # linear
    token_classes[curvatures >= high_thresh] = 2  # chaotic

    return token_classes
```

**Heterogeneous Token Prediction**

Apply differentiated strategies based on token classification:

```python
def predict_next_tokens(current_tokens, cached_tokens, token_history, token_classes):
    """
    Predict next tokens using heterogeneous strategies.

    Args:
        current_tokens: [num_tokens, dim] current token embeddings
        cached_tokens: [num_tokens, dim] most recent cached state
        token_history: [num_steps, num_tokens, dim] history for derivatives
        token_classes: [num_tokens] class indices (0=stable, 1=linear, 2=chaotic)

    Returns:
        predicted_tokens: [num_tokens, dim] predicted next state
    """
    num_tokens = current_tokens.shape[0]
    predicted = torch.zeros_like(current_tokens)

    # Stable tokens: direct reuse
    stable_mask = (token_classes == 0)
    predicted[stable_mask] = cached_tokens[stable_mask]

    # Linear tokens: first-order extrapolation
    linear_mask = (token_classes == 1)
    if linear_mask.any() and token_history.shape[0] >= 2:
        velocity = token_history[-1, linear_mask] - token_history[-2, linear_mask]
        predicted[linear_mask] = cached_tokens[linear_mask] + 0.5 * velocity

    # Chaotic tokens: damped update blending recent velocities
    chaotic_mask = (token_classes == 2)
    if chaotic_mask.any() and token_history.shape[0] >= 3:
        # Compute two recent velocities
        v1 = token_history[-1, chaotic_mask] - token_history[-2, chaotic_mask]
        v2 = token_history[-2, chaotic_mask] - token_history[-3, chaotic_mask]

        # Blend with damping (cubic Hermite schedule)
        alpha = 0.4  # weight for recent velocity vs older velocity
        blended_velocity = alpha * v1 + (1 - alpha) * v2

        # Damping factor: reduce velocity magnitude for stability
        damping = 0.7
        predicted[chaotic_mask] = cached_tokens[chaotic_mask] + damping * blended_velocity

    return predicted
```

**Adaptive Skipping with Drift Monitoring**

Track drift accumulation and trigger full backbone when threshold exceeded:

```python
class WorldModelWithCaching:
    def __init__(self, backbone_model, curvature_thresholds=(0.1, 0.5), drift_threshold=0.5):
        self.backbone = backbone_model
        self.curvature_thresholds = curvature_thresholds
        self.drift_threshold = drift_threshold
        self.token_history = []
        self.cached_tokens = None
        self.accumulated_drift = None

    def forward_step(self, tokens, step_idx, use_cache=True):
        """
        Single diffusion step with heterogeneous caching.

        Args:
            tokens: [num_tokens, dim] current latent tokens
            step_idx: current denoising step
            use_cache: whether to apply caching strategy

        Returns:
            next_tokens: [num_tokens, dim] tokens after this step
            cache_used: whether backbone was bypassed
        """
        cache_used = False

        if not use_cache or self.cached_tokens is None:
            # First step or caching disabled: compute normally
            next_tokens = self.backbone(tokens)
            self.cached_tokens = next_tokens
            self.token_history.append(next_tokens.detach().clone())
            self.accumulated_drift = torch.zeros(tokens.shape[0], device=tokens.device)
            return next_tokens, False

        # Compute curvature of token history
        history_tensor = torch.stack(self.token_history[-3:]) if len(self.token_history) >= 3 else torch.stack(self.token_history)
        curvatures = compute_token_curvatures(history_tensor)
        token_classes = classify_tokens(curvatures, self.curvature_thresholds)

        # Predict using heterogeneous strategies
        predicted_tokens = predict_next_tokens(
            tokens, self.cached_tokens, history_tensor, token_classes
        )

        # Compute predicted drift (difference from cached)
        predicted_drift = torch.norm(predicted_tokens - self.cached_tokens, dim=1)

        # Accumulate drift with normalization (only from chaotic tokens)
        chaotic_mask = (token_classes == 2)
        if chaotic_mask.any():
            normalized_drift = predicted_drift[chaotic_mask].mean()
            self.accumulated_drift[chaotic_mask] += normalized_drift

            # Check if drift exceeds threshold
            max_drift = self.accumulated_drift[chaotic_mask].max()
            if max_drift > self.drift_threshold:
                # Trigger full backbone evaluation
                next_tokens = self.backbone(tokens)
                self.cached_tokens = next_tokens
                self.accumulated_drift[chaotic_mask] = 0  # Reset chaotic drift
                cache_used = True  # Backbone was actually used
            else:
                # Use predicted tokens
                next_tokens = predicted_tokens
                cache_used = False
        else:
            next_tokens = predicted_tokens
            cache_used = False

        self.token_history.append(next_tokens.detach().clone())
        return next_tokens, cache_used

    def reset_cache(self):
        """Reset caching state for new rollout"""
        self.token_history = []
        self.cached_tokens = None
        self.accumulated_drift = None
```

## Practical Guidance

**Hyperparameters**:
- Curvature thresholds: (0.1, 0.5) works well; adjust based on model's token variance
- Drift threshold η: 0.5-0.7 is typical; higher = more aggressiveness in skipping, lower = more backbone calls
- Damping factor (chaotic): 0.6-0.8 reduces velocity instability
- History window: 3-5 steps for curvature computation

**When to Apply**:
- Iterative world models (diffusion, autoregressive) where multiple inference steps occur
- Real-time robot simulation where latency is critical
- Models where token types (background vs foreground) have different dynamics

**When NOT to Apply**:
- Single-step generators (direct prediction without iteration)
- Models where all tokens have uniform dynamics
- Cases where cache invalidation is difficult (rapidly changing environments)

**Key Pitfalls**:
- Curvature thresholds not calibrated to your model—leads to misclassification
- Drift threshold too aggressive—causes quality collapse; too conservative—no speedup
- Not resetting cache at episode/trajectory boundaries—stale predictions propagate
- History window too short—noisy curvature estimates; too long—outdated derivatives

**Integration Notes**: Works as a drop-in wrapper around any world model; requires storing token history and cached values; compatible with both pixel-space and latent-space world models.

**Evidence**: Achieves 3.7x speedup on physics simulation tasks; maintains 98% rollout quality (trajectory fidelity); largest gains on multi-modal observations (RGB + depth) where backgrounds are stable and objects are chaotic.

Reference: https://arxiv.org/abs/2603.06331
