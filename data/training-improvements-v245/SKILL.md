---
name: training-improvements-v245
description: "Training improvements: LR warmup, validation intervals, reward weights. Trigger when: (1) training unstable in early epochs, (2) need more validation visibility, (3) model too conservative."
author: Claude Code
date: 2024-12-27
---

# Training Improvements v2.4.5

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-27 |
| **Goal** | Improve training stability and visibility based on 20251226 results analysis |
| **Environment** | GPU-native PPO, A100-40GB, 500M timesteps |
| **Status** | Success |

## Context

Analysis of training results from 20251226 showed:
- Training was working (PF 1.55-2.61, consistency 100%)
- But low reward magnitude (0.05-0.10) suggested conservative behavior
- Negative skew (-0.2 to -0.5) indicated more negative outliers
- Only 5 validation points for 477 updates (limited visibility)

These improvements stabilize early training and provide better monitoring.

## Verified Workflow

### 1. LR Warmup (Stabilizes Early Training)

First 5% of training uses linear warmup from lr/10 to full lr. This prevents large updates before the network settles.

```python
# In ppo_trainer_native.py, NativePPOConfig
warmup_fraction: float = 0.05  # First 5% of training
min_lr_fraction: float = 0.01  # Don't decay to 0 - maintain 1% of initial LR

# Scheduler setup with warmup
warmup_steps = max(1, int(n_updates * self.config.warmup_fraction))
main_steps = max(1, n_updates - warmup_steps)

# Warmup scheduler: lr/10 -> lr
warmup_scheduler = torch.optim.lr_scheduler.LinearLR(
    self.optimizer,
    start_factor=0.1,  # Start at lr/10
    end_factor=1.0,    # Warmup to full lr
    total_iters=warmup_steps,
)

# Main scheduler: lr -> lr*min_lr_fraction
main_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    self.optimizer,
    T_max=main_steps,
    eta_min=self.config.learning_rate * self.config.min_lr_fraction,
)

# Chain them
self.lr_scheduler = torch.optim.lr_scheduler.SequentialLR(
    self.optimizer,
    schedulers=[warmup_scheduler, main_scheduler],
    milestones=[warmup_steps],
)
```

### 2. Validation Interval (More Visibility)

Increased validation frequency to ~10 validations per training run:

```python
# In ppo_trainer_native.py, mode_configs
mode_configs = {
    'quick_test': {'validation_interval': 5},   # ~8 validations for ~40 updates
    'standard':   {'validation_interval': 20},  # ~10 validations for ~200 updates
    'production': {'validation_interval': 40},  # ~10 validations for ~400 updates
    'extended':   {'validation_interval': 100}, # ~10 validations for ~1000 updates
    'auto':       {'validation_interval': 40},  # Match production
}
```

### 3. Reward Weights (Less Conservative)

With account-aware training (v2.4), drawdown is already in observations. Reduce penalty weights to avoid making model too conservative:

```python
# In vectorized_env.py, GPUEnvConfig

# Reward weights (v2.4.5 - reduced magnitude and drawdown penalty)
# NOTE: With account-aware training, drawdown is in observations - less penalty needed in reward
direction_weight: float = 0.35      # Keep - primary signal
magnitude_weight: float = 0.10     # Reduced from 0.15 - noisy component
pnl_weight: float = 0.25           # Keep - P&L matters
stop_tp_weight: float = 0.15       # Keep - risk management
exploration_weight: float = 0.10   # Keep - exploration

# Account-aware training (v2.4)
drawdown_penalty_threshold: float = 0.15  # Penalize when drawdown exceeds 15%
drawdown_penalty_weight: float = 0.05     # Reduced from 0.10 - DD already in observations
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Warmup 10% of training | Too long warmup, wasted training time | 5% is sufficient for stabilization |
| Decay to lr=0 | Training stalled at end | Maintain 1% of initial LR |
| Validation every 10 updates | Too frequent, slowed training | ~10 validations total is enough |
| Keep high drawdown penalty | Model became too conservative (only 0.05 rewards) | Reduce penalty when DD is in observations |

## Final Parameters

```python
# ppo_trainer_native.py - NativePPOConfig
warmup_fraction = 0.05        # First 5% of training
min_lr_fraction = 0.01        # Don't decay to 0
max_drawdown_threshold = 0.15  # Reduced from 0.30
drawdown_penalty_weight = 0.2  # Reduced from 0.3

# Validation intervals (per mode)
# quick_test: 5, standard: 20, production: 40, extended: 100

# vectorized_env.py - GPUEnvConfig reward weights
magnitude_weight = 0.10        # Reduced from 0.15
drawdown_penalty_weight = 0.05  # Reduced from 0.10
```

## Key Insights

1. **Warmup prevents early instability** - Large LR in early training can cause divergence. Starting at lr/10 lets the network find a stable region first.

2. **Don't decay to zero** - Training at lr=0 is just noise. Maintaining 1% of initial LR allows continued learning at end of training.

3. **More validations = better visibility** - With only 5 validations, you can't see training dynamics. 10 validations show the learning curve clearly.

4. **Avoid double-penalizing** - Account-aware training already shows the model its drawdown. Heavy reward penalty on top makes it too conservative.

5. **Magnitude is noisy** - The magnitude component (how much price moved) is noisy and less predictive than direction. Reducing its weight helps.

## References

- `alpaca_trading/gpu/ppo_trainer_native.py`: Lines 100-102 (warmup config), 526-572 (scheduler setup), 1708-1747 (mode configs)
- `alpaca_trading/gpu/vectorized_env.py`: Lines 388-409 (reward weights)
- Training analysis: 20251226 results showing low reward magnitude and negative skew
- Commit: `14d07c3` (training improvements)
