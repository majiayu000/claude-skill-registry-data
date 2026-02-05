---
name: position-sizing-action-space
description: "7-action space with position sizing (25/50/75%) + small account simulation. Trigger when: (1) model needs sizing decisions, (2) training for <$25K accounts, (3) upgrading obs_dim 5600->5900."
author: Claude Code
date: 2024-12-29
---

# Position Sizing Action Space (v2.7.0)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-29 |
| **Goal** | Make RL model learn WHEN to trade AND HOW MUCH to allocate |
| **Environment** | vectorized_env.py, ppo_trainer_native.py, live_trader.py, inference_obs_builder.py |
| **Status** | Success |

## Context

Prior to v2.7.0, the RL model only decided direction:
- 3 actions: HOLD (0), BUY (1), SELL (2)
- Position sizing was external (GARCH-adjusted, fixed 15% base)
- Model trained with 100% allocation per trade

**Problem**: The model learned timing but not sizing. Live trader applied external sizing rules the model never learned. Small accounts ($1,000-$25,000) need conservative sizing.

**Solution**: 7-action space with integrated position sizing + account simulation.

## Action Space Design

| Action | Direction | Size | Meaning |
|--------|-----------|------|---------|
| 0 | HOLD | 0% | No position change |
| 1 | BUY | 25% | Conservative long entry |
| 2 | BUY | 50% | Standard long entry |
| 3 | BUY | 75% | Aggressive long entry |
| 4 | SELL | 25% | Conservative short/exit |
| 5 | SELL | 50% | Standard short/exit |
| 6 | SELL | 75% | Aggressive short/exit |

**Note:** 100% achieved via consecutive same-direction signals (scale in).

## Verified Workflow

### 1. Config Parameters (GPUEnvConfig)

```python
# In vectorized_env.py GPUEnvConfig dataclass (~line 400)
# Account simulation (v2.7.0)
initial_account_value: float = 1000.0  # $1,000 small account
base_alloc: float = 0.15  # 15% base allocation
safety_buffer_pct: float = 0.30  # 30% never risked
max_position_pct: float = 0.20  # 20% max per position

# Position sizing action space (v2.7.0)
use_position_sizing: bool = True  # Enable 7-action space
n_actions: int = 7  # HOLD + 3 BUY sizes + 3 SELL sizes
size_buckets: tuple = (0.25, 0.50, 0.75)  # Size multipliers
```

### 2. Action Constants and Decoder

```python
# Action mapping (v2.7.0)
ACTION_HOLD = 0
ACTION_BUY_25 = 1
ACTION_BUY_50 = 2
ACTION_BUY_75 = 3
ACTION_SELL_25 = 4
ACTION_SELL_50 = 5
ACTION_SELL_75 = 6

def decode_action(action: int) -> tuple[int, float]:
    """Decode action into direction and size multiplier."""
    if action == 0:
        return 0, 0.0  # HOLD
    elif action <= 3:
        return 1, [0.25, 0.50, 0.75][action - 1]  # BUY
    else:
        return -1, [0.25, 0.50, 0.75][action - 4]  # SELL
```

### 3. Account State Tensors

```python
# In _init_state_tensors() after equity tracking
# Account simulation (v2.7.0)
self.account_value = torch.full(
    (self.n_envs,), self.config.initial_account_value,
    dtype=self.dtype, device=self.device
)
self.cash = torch.full(
    (self.n_envs,), self.config.initial_account_value * (1 - self.config.safety_buffer_pct),
    dtype=self.dtype, device=self.device
)  # 70% available ($700 of $1000)
self.position_value = torch.zeros(self.n_envs, dtype=self.dtype, device=self.device)
self.position_size_pct = torch.zeros(self.n_envs, dtype=self.dtype, device=self.device)
```

### 4. Position Sizing Logic

```python
def _calculate_position_size(self, action: torch.Tensor, current_price: torch.Tensor) -> torch.Tensor:
    """Calculate position size in dollars based on action."""
    # available = account_value * (1 - safety_buffer) = $700 for $1000 account
    available = self.account_value * (1 - self.config.safety_buffer_pct)

    # base_position = available * base_alloc = $700 * 0.15 = $105
    base_position = available * self.config.base_alloc

    # actual_position = base * size_mult = $105 * 0.50 = $52.50
    position_dollars = base_position * size_mults

    # Cap at max_position_pct
    max_position = self.account_value * self.config.max_position_pct
    position_dollars = torch.minimum(position_dollars, max_position)

    return directions, position_dollars
```

### 5. Reward Scaling by Position Size

```python
# Current: reward = price_return (assumes 100% allocation)
# New: reward = price_return * (position_size / account_value)

def _compute_reward(self, price_return: torch.Tensor) -> torch.Tensor:
    """Compute reward scaled by position size."""
    # Position return = price_return * position_size_pct
    # If 50% position and price moves 1%, account moves 0.5%
    position_return = price_return * self.position_size_pct
    reward = self._apply_reward_components(position_return)
    return reward
```

### 6. Position Sizing Observation Features

```python
# In _get_observations() - 3 new features for 59 total

# Feature 57: Current position size as % of account (0.0 to 0.20)
position_pct_norm = self.position_size_pct / self.config.max_position_pct
obs[:, :, feat_idx] = position_pct_norm.unsqueeze(1).expand(-1, self.config.window)
feat_idx += 1

# Feature 58: Available capital as % of account (0.0 to 0.70)
available_pct = self.cash / self.account_value
obs[:, :, feat_idx] = available_pct.unsqueeze(1).expand(-1, self.config.window)
feat_idx += 1

# Feature 59: Current account value normalized (log scale)
# $1000 -> 0.0, $2000 -> 0.30, $500 -> -0.30
account_norm = torch.log10(self.account_value / self.config.initial_account_value)
obs[:, :, feat_idx] = account_norm.unsqueeze(1).expand(-1, self.config.window)
feat_idx += 1
```

### 7. Actor Network Update

```python
# In ppo_trainer_native.py NativeActorCritic
class NativeActorCritic(nn.Module):
    def __init__(self, obs_dim: int, n_actions: int = 7, ...):
        # n_actions now defaults to 7 instead of 3
        self.actor_head = nn.Linear(hidden_dims[-1], n_actions)
```

### 8. Live Trader Integration

```python
# In live_trader.py
def interpret_model_action(action: int, n_actions: int = 7) -> Tuple[int, float]:
    """Interpret model's action output into direction and size multiplier."""
    if n_actions == 7:
        if action == 0:
            return 0, 0.0  # HOLD
        elif action <= 3:
            size_mult = [0.25, 0.50, 0.75][action - 1]
            return 1, size_mult  # BUY
        else:
            size_mult = [0.25, 0.50, 0.75][action - 4]
            return -1, size_mult  # SELL
    else:
        # Legacy 3-action model - default to 50% sizing
        if action == 1:
            return 1, 0.50
        elif action == 2:
            return -1, 0.50
        else:
            return 0, 0.50

# Apply to allocation
effective_alloc = alloc * model_size_mult
max_qty_from_alloc = portfolio_metrics.cash_available * effective_alloc / price
```

### 9. Inference Observation Builder

```python
# In inference_obs_builder.py get_target_features_from_obs_dim()
if features == 59:
    return 59  # v2.7 with position sizing
elif features == 56:
    return 56  # v2.4-v2.6

# In build_inference_observation() - position sizing features
if target_features >= 59:
    # Position size as % of max (0.0 for no position)
    obs[:, feat_idx] = kwargs.get('position_pct', 0.0)
    feat_idx += 1
    # Available capital % (default 70% = full availability)
    obs[:, feat_idx] = kwargs.get('available_pct', 0.70)
    feat_idx += 1
    # Account change from initial (0.0 = no change)
    obs[:, feat_idx] = kwargs.get('account_change', 0.0)
    feat_idx += 1
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| 12-action space (4 sizes) | Too granular, model couldn't differentiate | 3 sizes (25/50/75%) is sufficient |
| 100% as separate action | Encourages all-in behavior | Achieve 100% via scale-in (consecutive signals) |
| Raw dollar amounts in obs | Scale varies by account size | Use percentages normalized to 0-1 |
| Equal action probabilities init | Model biased toward HOLD | Initialize with slight trading bias |
| Position size in reward directly | Double-counting with P&L | Scale P&L by position size, not add as component |

## Final Parameters

```yaml
# GPUEnvConfig (v2.7.0)
n_features: 59  # Was 56 in v2.4-v2.6
n_actions: 7    # Was 3 in v2.4-v2.6
initial_account_value: 1000.0
base_alloc: 0.15
safety_buffer_pct: 0.30
max_position_pct: 0.20
size_buckets: (0.25, 0.50, 0.75)

# Feature breakdown (59 total)
base_features: 56             # All v2.6 features
position_sizing_features: 3   # position_pct, available_pct, account_change

# obs_dim = n_features * window = 59 * 100 = 5900
```

## Position Math Example

```
Initial State ($1,000 account):
  Account: $1,000
  Safety buffer: $300 (30%)
  Available: $700 (70%)
  Base allocation: $105 (15% of $700)

Model outputs BUY_50%:
  Position size: $105 * 0.50 = $52.50
  Position %: 5.25% of account

Price moves +2%:
  Dollar P&L: $52.50 * 0.02 = $1.05
  Account P&L: $1.05 / $1,000 = 0.105%
  Reward: 0.00105 (scaled by position size)

Model outputs BUY_75% (scale in):
  Additional: $105 * 0.75 = $78.75
  Total position: $52.50 + $78.75 = $131.25
  Position %: 13.125% of account
```

## Sizing Strategy the Model Should Learn

| Market Condition | Expected Sizing | Rationale |
|------------------|-----------------|-----------|
| High volatility | 25% (small) | Limit risk during uncertainty |
| Low confidence | 25% (small) | Uncertain signal |
| Strong trend + low vol | 75% (large) | High conviction opportunity |
| Near PDT limit | 25% (small) | Preserve day trades |
| Drawdown >10% | 25% (small) | Capital preservation |

## Backward Compatibility

```python
# In live_trader.py - support old 3-action models
def map_legacy_action(action: int) -> int:
    """Map legacy 3-action to new 7-action space."""
    if action == -1:  # SELL
        return 5  # SELL_50%
    elif action == 0:  # HOLD
        return 0  # HOLD
    else:  # BUY
        return 2  # BUY_50%

# NativeModelWrapper detects n_actions from checkpoint
n_actions = checkpoint.get('n_actions', 3)  # Default to legacy
```

## Key Insights

- **Breaking Change**: obs_dim 5600 -> 5900 means v2.6 models CANNOT be used with v2.7 environments
- **7 vs 12 Actions**: 12 actions (4 sizes per direction) was too granular; 7 is the sweet spot
- **No 100% Action**: Full allocation is achieved by scale-in (consecutive same-direction)
- **Reward Scaling**: P&L scaled by position_size_pct makes small positions have proportionally small rewards
- **Inference Defaults**: Use neutral defaults (position_pct=0, available_pct=0.70, account_change=0)

## Model Behavior Expected

With position sizing awareness, the model should learn:
1. **Size down in volatility** (sees market conditions)
2. **Size up with confidence** (sees strong signal patterns)
3. **Scale in gradually** (achieves 100% via multiple actions)
4. **Preserve capital in drawdown** (sees account_change feature)
5. **Match live trading behavior** (same sizing logic in training and inference)

## References
- `alpaca_trading/gpu/vectorized_env.py`: Lines 400+ (config), 640-720 (action decoding), 1258+ (obs features)
- `alpaca_trading/gpu/ppo_trainer_native.py`: Lines 642+ (n_actions config)
- `scripts/live_trader.py`: Lines 150+ (interpret_model_action), 1200+ (apply sizing)
- `alpaca_trading/gpu/inference_obs_builder.py`: Lines 61-108 (feature detection), 680+ (position features)
- `alpaca_trading/prediction/multi_tf_predictor.py`: Lines 200+ (size_mult aggregation)
