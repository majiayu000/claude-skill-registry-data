---
name: training-resilience
description: "Fix PPO training early-stop issues. Trigger when: (1) impossible drawdown values (>100%), (2) training stops too early, (3) need adaptive recovery instead of hard stop."
author: Claude Code
date: 2025-12-18
---

# Training Resilience - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-18 |
| **Goal** | Fix training stopping with "1017.8% drawdown" and implement adaptive recovery |
| **Environment** | Google Colab A100, PyTorch, NativePPOTrainer |
| **Status** | Success |

## Context
Training was stopping early with impossible drawdown values like "MaxDD: 1017.8% > 15.0%". Investigation revealed two issues:
1. Drawdown was calculated as absolute value, not percentage
2. PPO reward-based drawdown doesn't map to trading equity drawdown

## Root Cause Analysis

### Bug 1: Absolute Value Instead of Percentage
```python
# BROKEN CODE (returned absolute value):
cumsum = np.cumsum(rewards)
running_max = np.maximum.accumulate(cumsum)
drawdowns = running_max - cumsum
max_drawdown = drawdowns.max()  # Could be 1017.8 (absolute!)
```

When rewards sum to 1000 then drop to -17.8, the "drawdown" is 1017.8 (absolute), which was then displayed as "1017.8%" but compared against 0.15 (15%).

### Bug 2: PPO Rewards != Equity Curve
PPO rewards are small signals (-0.5 to +0.5) per step. Their cumulative sum naturally oscillates and will always show large "drawdowns" from peak - this doesn't indicate bad model behavior.

## Verified Workflow

### Fix 1: Percentage-Based Drawdown
```python
# FIXED CODE (returns percentage):
# Simulate equity curve starting at 1.0
equity_curve = 1.0 + np.cumsum(rewards)
running_max = np.maximum.accumulate(equity_curve)

# Calculate percentage drawdown
with np.errstate(divide='ignore', invalid='ignore'):
    drawdown_pct = np.where(
        running_max > 0,
        (running_max - equity_curve) / running_max,
        0.0
    )
max_drawdown = float(np.nanmax(drawdown_pct))

# Clamp to valid range [0, 1]
max_drawdown = max(0.0, min(1.0, max_drawdown))
```

### Fix 2: Disable Drawdown Early-Stop by Default
```python
# In NativePPOConfig:
max_drawdown_threshold: float = 0.50  # Less sensitive (was 0.15)
early_stop_on_drawdown: bool = False  # Disabled by default
drawdown_penalty_weight: float = 0.5  # Reduced penalty
```

### Fix 3: Adaptive Recovery (if enabled)
```python
# Config options:
max_drawdown_retries: int = 3
lr_reduction_on_drawdown: float = 0.5  # Halve LR
entropy_increase_on_drawdown: float = 1.5  # 50% more exploration

# Recovery logic:
if max_drawdown > threshold:
    retry_count += 1
    if retry_count <= max_retries:
        # Adjust hyperparameters
        current_lr *= lr_reduction_factor
        current_entropy_coef *= entropy_increase_factor

        # Update optimizer
        for param_group in optimizer.param_groups:
            param_group['lr'] = current_lr

        # Continue training (don't break)
    else:
        # Max retries exceeded - stop
        should_stop = True
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Absolute drawdown value | Displayed 1017.8 as 1017.8%, compared against 0.15 | Always use percentage (value / peak) |
| 15% threshold for PPO rewards | Random walk rewards always hit 15% drawdown | PPO rewards need higher threshold or disable |
| Multiplicative equity curve | Rewards can be negative, causing NaN | Use additive: 1.0 + cumsum(rewards) |
| Hard early stop | Lost all training progress on false positive | Implement adaptive recovery first |
| Same threshold for training and live | Different contexts need different thresholds | Training: 50%+, Live: 15% |

## Final Parameters
```python
# NativePPOConfig defaults (v2.3.2):
@dataclass
class NativePPOConfig:
    # Drawdown guardrails (training validation)
    max_drawdown_threshold: float = 0.50  # 50% - less sensitive for PPO
    early_stop_on_drawdown: bool = False  # Disabled by default
    drawdown_penalty_weight: float = 0.5  # Reduced penalty

    # Adaptive recovery
    max_drawdown_retries: int = 3
    lr_reduction_on_drawdown: float = 0.5
    entropy_increase_on_drawdown: float = 1.5
```

## Key Insights
- **PPO rewards != trading equity** - Don't apply trading metrics directly to PPO
- **Always use percentages** - Absolute values are meaningless without scale
- **Clamp to valid ranges** - Drawdown must be [0%, 100%]
- **Adaptive recovery > hard stop** - Give training a chance to recover
- **Different thresholds for different contexts** - Training validation vs live trading
- **Primary metrics: Sharpe and win rate** - These map better to PPO than drawdown

## Testing Checklist
```python
# Verify drawdown calculation:
1. [ ] Returns value in [0, 1] range
2. [ ] Never returns > 1.0 (100%)
3. [ ] Handles negative cumsum gracefully
4. [ ] Handles zero/near-zero running_max

# Verify adaptive recovery:
5. [ ] LR reduces on each retry
6. [ ] Entropy increases on each retry
7. [ ] Optimizer LR actually updates
8. [ ] Stops after max_retries exceeded
```

## References
- `alpaca_trading/gpu/ppo_trainer_native.py`: Lines 1042-1055 (drawdown calc)
- `alpaca_trading/gpu/ppo_trainer_native.py`: Lines 957-986 (adaptive recovery)
- CLAUDE.md: Drawdown guardrails documentation
