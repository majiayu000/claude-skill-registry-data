---
name: reward-scaling-calibration
description: "Fix phantom MaxDD values in training by calibrating reward_scale. Trigger when: (1) validation MaxDD shows 35-80% values, (2) MaxDD doesn't correlate with training quality, (3) gating thresholds seem too lenient/strict."
author: Claude Code
date: 2024-12-27
---

# Reward Scaling Calibration (v2.4.5)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-27 |
| **Goal** | Fix unrealistic MaxDD values (35-80%) appearing during training validation |
| **Environment** | GPU-native PPO training, A100-40GB |
| **Status** | Success |

## Context

Training runs showed MaxDD values of 35-80% at validation intervals, but the models were actually learning well (profit factor > 1.5, consistency 100%). The MaxDD was a "proxy metric" calculated from simulated equity during validation, not real equity.

**Root Cause:** `reward_scale = 0.1` in `ppo_trainer_native.py` was 100x too aggressive.

With reward_scale=0.1:
- A reward of +10 → 10 * 0.1 = +1.0 = 100% equity gain in one step
- A reward of -5 → -0.5 = 50% drawdown in one step
- Normal reward variance created phantom 35-80% drawdowns

With reward_scale=0.001:
- A reward of +10 → 0.01 = 1% equity change
- MaxDD now reflects realistic reward volatility (5-15%)

## Verified Workflow

### Step 1: Identify the Issue
Look for these symptoms:
- Validation MaxDD consistently 35-80%
- MaxDD doesn't correlate with training quality
- Models with high PF and consistency still show high MaxDD

### Step 2: Fix Reward Scaling

```python
# In ppo_trainer_native.py, line ~1103
# Change reward_scale from 0.1 to 0.001
reward_scale = 0.001  # Was 0.1 (100x too high)

# Also update per-step clamping
# Change from [0.01, 2.0] to [0.95, 1.05]
equity_multiplier = torch.clamp(
    1.0 + reward_scale * reward,
    0.95,  # Was 0.01
    1.05   # Was 2.0
)
```

### Step 3: Recalibrate Gating Thresholds

With new scaling, MaxDD values are 5-15% instead of 35-80%. Update thresholds:

```python
# In gating.py, ModelGatingConfig
@dataclass
class ModelGatingConfig:
    # APPROVED thresholds
    approved_min_fitness: float = 0.70     # Was 0.85
    approved_min_pf: float = 1.8           # Was 2.0
    approved_min_consistency: float = 0.85 # Was 0.90
    approved_max_drawdown: float = 0.08    # Was 0.20 (8% proxy MaxDD)

    # REVIEW thresholds
    review_min_fitness: float = 0.50       # Was 0.70
    review_min_pf: float = 1.3             # Was 1.5
    review_min_consistency: float = 0.65   # Was 0.70
    review_max_drawdown: float = 0.15      # Was 0.30 (15% proxy MaxDD)
```

### Step 4: Adjust Reward Weights (Optional)

Since account-aware training (v2.4) added drawdown to observations, reduce the drawdown penalty weight in rewards to avoid double-penalizing:

```python
# In vectorized_env.py, GPUEnvConfig
magnitude_weight: float = 0.10      # Was 0.15 - noisy component
drawdown_penalty_weight: float = 0.05  # Was 0.10 - DD in observations
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Ignore MaxDD, only use PF/consistency | Missed genuine training collapse cases | MaxDD still useful as reward stability indicator |
| Set reward_scale=0.01 | Still produced 20-30% MaxDD values | Need 0.001 for realistic <15% values |
| Keep old thresholds with new scaling | All models classified as APPROVED (thresholds too lenient) | Must recalibrate thresholds with scaling |
| Remove MaxDD from fitness calculation | Lost valuable signal about reward volatility | Keep but with appropriate weight |

## Final Parameters

```python
# ppo_trainer_native.py - Validation equity tracking
reward_scale = 0.001  # 100x reduction from 0.1
equity_clamp_min = 0.95
equity_clamp_max = 1.05

# gating.py - Threshold recalibration
ModelGatingConfig(
    approved_min_fitness=0.70,
    approved_min_pf=1.8,
    approved_min_consistency=0.85,
    approved_max_drawdown=0.08,
    review_min_fitness=0.50,
    review_min_pf=1.3,
    review_min_consistency=0.65,
    review_max_drawdown=0.15,
)

# vectorized_env.py - Reward weights
magnitude_weight = 0.10      # Reduced from 0.15
drawdown_penalty_weight = 0.05  # Reduced from 0.10

# ppo_trainer_native.py - Training improvements
max_drawdown_threshold = 0.15  # Reduced from 0.30
drawdown_penalty_weight = 0.2  # Reduced from 0.3
```

## Key Insights

1. **MaxDD is a PROXY metric** - It reflects reward volatility, not actual trading drawdown. The simulated equity is for monitoring training stability, not backtesting.

2. **Scaling affects interpretation** - With reward_scale=0.001:
   - 8% proxy MaxDD = rewards staying mostly positive
   - 15% proxy MaxDD = occasional negative reward streaks

3. **Fitness calculation uses MaxDD** - Lower MaxDD with new scaling means the MaxDD component contributes less to fitness. That's why fitness thresholds were also lowered (0.70 vs 0.85).

4. **Per-step clamp prevents extreme moves** - The [0.95, 1.05] clamp ensures no single step moves equity more than 5%. This is more realistic than [0.01, 2.0].

5. **Don't double-penalize drawdown** - With drawdown in observations (v2.4), the model already sees its performance. Adding heavy drawdown penalty in rewards makes training too conservative.

## References

- `alpaca_trading/gpu/ppo_trainer_native.py`: Lines 1103-1110 (reward scaling)
- `alpaca_trading/training/gating.py`: Lines 22-45 (ModelGatingConfig)
- `alpaca_trading/gpu/vectorized_env.py`: Lines 388-409 (reward weights)
- Training results: `Alpaca_trading_trained_20251226_211819.zip` (before fix)
- Commit: `9c10ca1` (reward_scale fix)
- Commit: `14d07c3` (gating thresholds + training improvements)
