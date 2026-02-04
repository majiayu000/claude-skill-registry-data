---
name: markov-regime-features
description: "Debugging constant Markov regime features in RL observations - when HMM probabilities show uniform values instead of dynamic regime estimates"
author: Claude Code
date: 2025-12-13
---

# markov-regime-features - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-13 |
| **Goal** | Debug why Markov features (indices 19-24) appeared constant in observation heatmaps while other features showed high variability |
| **Environment** | Python 3.10, PyTorch 2.0+, alpaca_trading package |
| **Status** | Success |

## Context
When visualizing RL observation features as a heatmap, the Markov regime features (volatility and trend probabilities) appeared as constant horizontal bands with values ~0.33, while all other features showed expected variability over time. This made the Markov features useless for regime detection.

## Root Cause
The standalone `build_inference_observation()` function defaults to **uniform priors** when `markov_vol_probs` and `markov_trend_probs` are not provided:

```python
# From inference_obs_builder.py:391-401
if include_markov:
    if markov_vol_probs is not None:
        obs[:, feat_idx:feat_idx+3] = markov_vol_probs
    else:
        obs[:, feat_idx:feat_idx+3] = [0.33, 0.34, 0.33]  # Uniform prior
```

The 6 Markov features are:
| Index | Feature | Description |
|-------|---------|-------------|
| 19 | vol_prob_low | P(low volatility regime) |
| 20 | vol_prob_medium | P(medium volatility regime) |
| 21 | vol_prob_high | P(high volatility regime) |
| 22 | trend_prob_down | P(downtrend regime) |
| 23 | trend_prob_neutral | P(neutral regime) |
| 24 | trend_prob_up | P(uptrend regime) |

## Verified Workflow

### Solution: Use InferenceObservationBuilder class
The `InferenceObservationBuilder` class maintains Markov state and updates probabilities based on price history:

```python
from alpaca_trading.gpu.inference_obs_builder import InferenceObservationBuilder

# Create stateful builder with GPU Markov system
obs_builder = InferenceObservationBuilder(window=100, use_gpu_markov=True)

# Build observation - Markov states are updated from price history
obs = obs_builder.build(
    prices=prices,
    high=high,
    low=low,
)

# Access current regime estimates
print(f"Volatility: {obs_builder.vol_probs}")  # e.g., [0.15, 0.60, 0.25]
print(f"Trend: {obs_builder.trend_probs}")      # e.g., [0.20, 0.30, 0.50]
```

### Visualizing Regime Evolution
To see how regimes change over time, build observations at multiple points:

```python
eval_points = list(range(150, n_bars, 10))
vol_history = {'low': [], 'med': [], 'high': []}

for end_idx in eval_points:
    obs_builder.build(prices=prices[:end_idx], high=high[:end_idx], low=low[:end_idx])
    vol_history['low'].append(obs_builder.vol_probs[0])
    vol_history['med'].append(obs_builder.vol_probs[1])
    vol_history['high'].append(obs_builder.vol_probs[2])

plt.plot(eval_points, vol_history['high'], 'r-', label='P(High Vol)')
plt.plot(eval_points, vol_history['low'], 'g-', label='P(Low Vol)')
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using `build_inference_observation()` directly | No Markov state passed, defaults to uniform [0.33, 0.34, 0.33] | Use `InferenceObservationBuilder` class for stateful Markov tracking |
| Setting `include_markov=False` | Removes features entirely, breaks model compatibility | Keep Markov features, just ensure proper initialization |
| Manual Markov probability calculation | Complex HMM implementation needed | Use `GPUMarkovSystem` via `use_gpu_markov=True` |

## Final Parameters

```python
# Correct usage for dynamic Markov features
obs_builder = InferenceObservationBuilder(
    window=100,           # Must match training window
    use_gpu_markov=True   # Enable GPU-accelerated HMM
)

# For live trading - maintain single builder instance across bars
# For backtesting - create new builder per symbol, maintain across timesteps
```

## Key Insights
- The standalone function is for **single-shot inference** where Markov state is passed externally
- The builder class is for **stateful inference** where Markov state evolves with price data
- GPU Markov system uses last 20 returns to estimate regime probabilities
- Uniform priors [0.33, 0.34, 0.33] indicate Markov system not receiving updates
- In heatmaps, constant horizontal bands at indices 19-24 are a red flag for this issue

## References
- `alpaca_trading/gpu/inference_obs_builder.py` - Feature building implementation
- `alpaca_trading/gpu/harmonized_gpu.py` - GPUMarkovSystem class
- `notebooks/develop_branch_testing.ipynb` - Visualization examples
