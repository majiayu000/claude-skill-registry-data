---
name: pytorch-common-pitfalls
description: "Fix common PyTorch bugs: percentile calculations, LayerNorm for Conv1d, buffer edge cases. Trigger when writing PyTorch code for RL or neural networks."
author: Claude Code
date: 2025-01-01
---

# PyTorch Common Pitfalls

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-01-01 |
| **Goal** | Document and fix common PyTorch bugs found during code review |
| **Environment** | PyTorch 2.x, CUDA-enabled training |
| **Status** | Success |

## Context

During review of advanced RL components (ensemble PPO, VAE OOD detector, curiosity module, dilated CNN), GitHub Copilot identified several common PyTorch pitfalls. These patterns appear frequently in ML code and can cause subtle bugs.

## Verified Patterns

### 1. Percentile Calculation: Use `torch.quantile`, NOT `kthvalue`

**Problem**: `kthvalue` requires integer index, leading to off-by-one errors and incorrect percentiles.

**Wrong:**
```python
# BUG: kthvalue needs exact index, rounds incorrectly
k = int(self.threshold_percentile / 100.0 * errors.numel())
threshold = errors.view(-1).kthvalue(k).values
```

**Correct:**
```python
# Use quantile for proper interpolation
q = self.threshold_percentile / 100.0
q = max(0.0, min(1.0, q))  # Clamp to valid range
threshold = torch.quantile(errors.view(-1), q)
```

**Why**: `torch.quantile` handles interpolation automatically and accepts float percentiles directly.

### 2. LayerNorm with Conv1d: Create a Wrapper

**Problem**: Conv1d outputs are `(batch, channels, time)` but LayerNorm expects normalization over the last dimension.

**Wrong:**
```python
# BUG: LayerNorm(channels) applied to wrong dimension
self.norm = nn.LayerNorm(num_channels)
x = self.conv(x)  # (batch, channels, time)
x = self.norm(x)  # Normalizes over the last dim (time) for each channel, not across channels as intended
```

**Correct:**
```python
class ChannelLayerNorm1d(nn.Module):
    """LayerNorm wrapper for Conv1d outputs shaped (batch, channels, time)."""

    def __init__(self, num_channels: int):
        super().__init__()
        self.ln = nn.LayerNorm(num_channels)

    def forward(self, x: Tensor) -> Tensor:
        # x: (batch, channels, time) -> transpose -> (batch, time, channels)
        x = x.transpose(1, 2)
        x = self.ln(x)  # Now normalizes over channels
        return x.transpose(1, 2)  # Back to (batch, channels, time)

# Usage
self.norm = ChannelLayerNorm1d(num_channels)
```

### 3. Buffer Edge Cases: Handle Last Transitions

**Problem**: When sampling from replay buffers, `next_obs = obs[indices + 1]` fails for the last transition.

**Wrong:**
```python
# BUG: Index out of bounds when indices contains last index
indices = torch.randint(0, total_steps, (batch_size,))
next_obs = obs_flat[indices + 1]  # Crashes if indices contains (total_steps - 1)
```

**Correct:**
```python
# Handle edge case for last transitions
total_steps = obs_flat.shape[0]
next_indices = indices + 1
has_next = next_indices < total_steps

# Use safe indices (clamp to valid range)
safe_next_indices = next_indices.clone()
safe_next_indices[~has_next] = total_steps - 1

next_obs = obs_flat[safe_next_indices]

# Mark transitions without valid next_obs as terminal
dones = dones_flat[indices].clone()
dones[~has_next] = True  # These are terminal states
```

**Alternative - Filter invalid transitions:**
```python
# Only use transitions with valid next_obs
valid_mask = next_indices < total_steps
valid_indices = indices[valid_mask]
valid_next_indices = next_indices[valid_mask]

obs = obs_flat[valid_indices]
next_obs = obs_flat[valid_next_indices]
actions = actions_flat[valid_indices]
```

### 4. Safe Action Gating with `torch.where`

**Problem**: Boolean masking with multiplication can be unclear and error-prone.

**Wrong:**
```python
# Unclear intent, potential floating-point issues
gated = proposed * (1 - mask.float()) + hold * mask.float()
```

**Correct:**
```python
# Clear, explicit conditional
gated_action = torch.where(
    intervention_mask,  # Boolean tensor
    torch.full_like(proposed_action, self.hold_action),  # If True
    proposed_action,  # If False
)
```

### 5. NaN/Inf Checks in Calibration

**Problem**: Fitting distributions or thresholds on data with NaN/Inf values corrupts the model.

```python
# Always check for invalid values before calibration
errors = self._compute_reconstruction_errors(data)

if torch.isnan(errors).any() or torch.isinf(errors).any():
    raise ValueError(
        f"Invalid values in calibration data: "
        f"NaN={torch.isnan(errors).sum().item()}, "
        f"Inf={torch.isinf(errors).sum().item()}"
    )

# Safe to proceed with calibration
self.threshold = torch.quantile(errors.view(-1), q)
```

### 6. Minimum Sample Size Checks

**Problem**: Computing statistics on too few samples produces unreliable results.

```python
# Ensure sufficient samples before computing diversity metrics
min_samples = 32

if n_samples < min_samples or total_transitions == 0:
    return torch.zeros(self.config.n_learners, device=self.device)

# Safe to compute statistics
diversity_bonus = self._compute_diversity(samples)
```

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using `kthvalue` for percentiles | Off-by-one errors, integer rounding issues | Use `torch.quantile` for floating-point percentiles |
| `LayerNorm(channels)` on Conv1d output | Normalizes wrong dimension (time instead of channels) | Create wrapper that transposes before/after LayerNorm |
| `obs[indices + 1]` without bounds check | Index out of bounds for last transition | Always handle edge case or filter invalid indices |
| Silent failures returning zeros | Bugs hidden, hard to debug | Raise `ValueError` with informative message |
| Using `x: any = ...` without import | Built-in `any` is not the same as `typing.Any`; not a valid type hint | Use `from typing import Any` and annotate as `x: Any = ...` |

## Key Insights

- **`torch.quantile` > `kthvalue`**: Proper interpolation, accepts float directly
- **Transpose for LayerNorm**: Conv1d is `(B,C,T)`, LayerNorm normalizes last dim
- **Bounds checking is mandatory**: Buffer sampling must handle edge cases
- **Fail loudly**: `raise ValueError` > return zeros silently
- **Type hints matter**: `Any` from typing, not Python builtin `any`

## References

- PyTorch quantile docs: https://pytorch.org/docs/stable/generated/torch.quantile.html
- LayerNorm docs: https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html
- GitHub Copilot PR suggestions for PR #35 and #36 in Alpaca_trading repo
