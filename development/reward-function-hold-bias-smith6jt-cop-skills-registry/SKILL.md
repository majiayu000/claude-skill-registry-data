---
name: reward-function-hold-bias
description: "Fix HOLD bias in RL reward function. Trigger when: (1) model learns to always HOLD, (2) trade rate is too low (<10%), (3) slippage penalty exceeds typical price moves."
author: Claude Code
date: 2024-12-27
---

# Reward Function HOLD Bias Fix (v2.5.0)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-27 |
| **Goal** | Fix reward function that teaches model HOLD is optimal |
| **Environment** | GPU-native PPO training, vectorized_env.py |
| **Status** | Success |

## Context

Training BTCUSD showed the model wasn't finding trading opportunities over a 2-year period. Investigation revealed the reward function had a hidden HOLD bias.

**Root Cause:** Asymmetric payoff structure made HOLD the rational choice:

| Action | Reward If Correct | Reward If Wrong | Expected Value |
|--------|-------------------|-----------------|----------------|
| HOLD | 0 | 0 | 0 (safe) |
| BUY/SELL | +0.35 to +0.90 | -0.52 (painful) | Negative after costs |

**The Math for BTCUSD:**
- Slippage cost: 0.5% (crypto) per trade
- 5-bar horizon (5 hours at 1H timeframe)
- Bitcoin 5-hour volatility: ~0.3-0.5% average
- Expected move < slippage cost = negative EV for trading

## Root Cause Analysis

| Issue | Problem | Impact |
|-------|---------|--------|
| Slippage penalty too aggressive | 0.5% × 10 scaling = huge penalty | Model avoids trading entirely |
| Exploration bonus negligible | 0.01 × uncertainty = ~0.001 | No incentive to try trading |
| HOLD gets zero reward | HOLD = 0, wrong trade = -0.52 | Asymmetric payoff favors HOLD |
| Direction threshold too strict | 0.1% threshold vs 0.5% slippage | Correct predictions still lose money |

## Verified Workflow

### Step 1: Reduce Slippage Cost

```python
# In vectorized_env.py, GPUEnvConfig
slippage_cost_crypto: float = 0.002  # Was 0.005 (0.5% -> 0.2%)
slippage_weight: float = 0.02        # Was 0.05
```

### Step 2: Add Trading Incentive

```python
# In vectorized_env.py, GPUEnvConfig
trading_incentive: float = 0.02  # NEW: Small bonus for non-HOLD actions

# In _calculate_rewards() after drawdown_penalty
trade_executed = (pred_direction != 0).float()
trading_incentive_reward = trade_executed * self.config.trading_incentive

# Add to combined reward
reward = (
    ... existing components ...
    trading_incentive_reward  # v2.5.0 - fix HOLD bias
) * risk_adjustment
```

### Step 3: Increase Exploration Bonus

```python
# In _calculate_rewards(), COMPONENT 5
exploration_bonus = 0.05 * uncertainty  # Was 0.01
```

### Step 4: Increase Direction Threshold

```python
# In _calculate_rewards()
threshold = 0.003  # Was 0.001 (0.3% vs 0.1%)
# Must exceed slippage to be considered profitable
```

### Step 5: Rebalance Reward Weights

```python
# In GPUEnvConfig
direction_weight: float = 0.40       # Was 0.35 - primary signal
magnitude_weight: float = 0.05       # Was 0.10 - noisy component
pnl_weight: float = 0.25             # Keep
stop_tp_weight: float = 0.10         # Was 0.15
exploration_weight: float = 0.15     # Was 0.10
slippage_weight: float = 0.02        # Was 0.05
drawdown_penalty_weight: float = 0.03 # Was 0.05
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Switch to 15-min timeframe | Smaller moves, same costs = worse HOLD bias | Fix reward function first, then consider timeframe |
| Just reduce slippage penalty | Model still biased toward HOLD | Need positive incentive for trading |
| Large trading incentive (0.1) | Caused overtrading | 0.02 is sufficient to break tie |
| Remove slippage penalty entirely | Model overtrades, ignores costs | Need penalty, just not excessive |

## Final Parameters

```python
# vectorized_env.py - GPUEnvConfig (v2.5.0)

# Reward weights (8 components)
direction_weight: float = 0.40
magnitude_weight: float = 0.05
pnl_weight: float = 0.25
stop_tp_weight: float = 0.10
exploration_weight: float = 0.15
slippage_weight: float = 0.02
drawdown_penalty_weight: float = 0.03
trading_incentive: float = 0.02  # NEW

# Transaction costs
slippage_cost_crypto: float = 0.002  # Was 0.005
slippage_cost: float = 0.001         # Equity unchanged

# Direction threshold
threshold = 0.003  # Was 0.001 (in _calculate_rewards)

# Exploration bonus multiplier
exploration_bonus = 0.05 * uncertainty  # Was 0.01
```

## Key Insights

1. **Asymmetric payoffs create bias** - If HOLD=0 and wrong trade=-X, model learns HOLD is safe. Add small positive reward for trading to balance.

2. **Slippage must be < expected move** - If cost to trade > expected profit, rational to never trade. Align slippage with actual broker costs (0.1-0.2%).

3. **Threshold should match slippage** - Direction threshold (0.1%) below slippage (0.5%) means "correct" predictions still lose money. Set threshold >= slippage.

4. **Exploration needs real incentive** - 0.01 multiplier is negligible. Increase to 0.05 for meaningful exploration bonus.

5. **Test with volatile assets first** - BTCUSD has higher volatility, so if model won't trade BTC, it definitely won't trade lower-vol assets.

## Expected Behavior After Fix

With the new reward function, expect:
- Trade rate: 30-60% (was ~5%)
- More balanced signal distribution (BUY/SELL/HOLD)
- Model takes trades when expected move > costs
- Still respects risk management (drawdown penalty)

## References

- `alpaca_trading/gpu/vectorized_env.py`: Lines 388-410 (GPUEnvConfig), 1622-1712 (_calculate_rewards)
- `alpaca_trading/api/routes/signals.py`: Lines 75, 136 (dashboard key fix: 'passed' -> 'pass')
- Literature: [Risk-Aware RL Reward](https://arxiv.org/html/2506.04358v1) - multi-component reward design
- Skill: `reward-scaling-calibration` - related fix for reward_scale
