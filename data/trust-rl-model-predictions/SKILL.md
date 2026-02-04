---
name: trust-rl-model-predictions
description: "Remove pattern filters that second-guess RL model predictions. Trigger when: (1) signals show past threshold but status is HOLD, (2) pattern filter blocks model signals, (3) external gates contradict trained model, (4) dashboard shows disconnect between signal strength and action."
author: Claude Code
date: 2024-12-26
---

# Trust RL Model Predictions

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-26 |
| **Goal** | Remove pattern filter that was second-guessing RL model predictions |
| **Environment** | scripts/live_trader.py, scripts/monitor_dashboard.py, alpaca_trading/visualization/dashboard.py |
| **Status** | Success |

## Context

The trading system had a **pattern filter** that blocked model signals even when:
1. The RL model predicted a direction with good confidence
2. The signal visually crossed the buy/sell threshold on the dashboard
3. All other gates (capital, risk, etc.) would have passed

**Root Problem**: The pattern filter used historical win rates (68-71%) to block trades that didn't match predefined geometric patterns (VWAP reversion, momentum continuation). But the RL model was trained on a DIFFERENT objective (P&L, direction accuracy, stop/TP outcomes) and never learned these patterns.

**User symptom**: "Dashboard shows sell signals past threshold but 'HOLD' under the percentages"

## Analysis: What the RL Model Actually Learns

The model is trained with a **6-component reward function**:

| Component | What Model Learns |
|-----------|-------------------|
| Direction accuracy | Predict correct sign of price change |
| Magnitude accuracy | Predict size of move |
| P&L reward | Maximize trading profit |
| Stop/TP reward | Hit take-profits, avoid stops |
| Exploration bonus | Try uncertain actions |
| Slippage penalty | Don't overtrade |

**Observation space (56 features in v2.4)**: The model sees price action, regime probabilities (12 Markov features), technical indicators (14), calendar effects, multi-window metrics, and account state (P&L %, win rate, drawdown %).

**What the model does NOT learn**:
- Historical pattern win rates (VWAP reversion 68%, momentum 71%)
- Specific geometric pattern requirements
- External human-defined pattern matching rules

## The Conflict

```
RL Model trained on:     P&L + direction accuracy + stop/TP outcomes
Pattern Filter enforced: Historical pattern win rates (68-71%)

These objectives are DIFFERENT and can CONFLICT.
```

When they conflict, the pattern filter blocked valid model signals, causing the disconnect between visual signal strength and action status.

## Solution: Trust the Model

### Remove Pattern Filter

```python
# BEFORE: Pattern filter second-guessed model
should_trade, adjusted_confidence, pattern_name = filter_by_patterns(
    df=df,
    signal_direction=signal,
    confidence=confidence,
    regime_context=regime_context,
    min_pattern_win_rate=0.65
)
if not should_trade:
    return state, {"pattern_rejected": True}

# AFTER: Trust model predictions directly
# Pattern filter REMOVED - RL model predictions are trusted directly
# The model was trained on 53 features including regime, technicals, and calendar.
# Its predictions already incorporate pattern recognition implicitly.
```

### Keep Essential Gates

These gates remain because they check things the model CANNOT learn:

| Gate | Why Keep |
|------|----------|
| Confidence threshold | Prevents weak signals (adaptive 0.50-0.65) |
| Crypto short | Broker limitation (Alpaca doesn't support) |
| Portfolio limit | Model trained on single symbols, can't see portfolio |
| Capital manager | Model has no account balance awareness |
| Portfolio risk | VaR/correlation outside model scope |
| Win rate cooldown | Execution feedback not in training |
| Loss streak | Trade history not in observations |

## Dashboard Updates

### Replaced "Pattern Win Rates" Panel

The useless pattern win rates panel was replaced with **RL Model Status**:

```
RL Model Status
---------------
Symbols: 5

✓ READY     2
✗ BLOCKED   1
— HOLD      2

BUY: 1  SELL: 1  HOLD: 3

Avg Confidence: 58.5%
```

### Compacted Account Performance

Reduced height ratio from 0.8 to 0.5, giving more space to the Symbol Signals panel which shows actionable information.

## Files Modified

```
scripts/live_trader.py:
  - Line 51: Removed filter_by_patterns import
  - Lines 146-147: Removed pattern_gate from GateStatus dataclass
  - Line 183: Removed pattern from gates dict
  - Lines 246-253: Removed pattern rejection check
  - Lines 1294-1297: Removed pattern filter logic (was lines 1302-1326)

scripts/monitor_dashboard.py:
  - Line 45: Removed filter_by_patterns import
  - Lines 129-197: Simplified check_gates (removed pattern filter)
  - Lines 536-577: Replaced get_pattern_performance with get_model_metrics
  - Line 988: Changed pattern_stats to model_metrics

alpaca_trading/visualization/dashboard.py:
  - Lines 53-54: Changed height_ratios to [0.5, 1, 1.4] (was [0.8, 1, 1.2])
  - Line 62: Changed ax_patterns to ax_model
  - Lines 99-105: Changed to use plot_model_status
  - Lines 287-342: Replaced plot_pattern_performance with plot_model_status
  - Lines 583-584: Updated clear_all to use ax_model
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Pattern filter with 65%+ win rate | Blocked good model signals | Model learned different patterns |
| VWAP reversion (68% historical) | Required prey_dominance > 40% + price 2σ from VWAP | Model never learned these specific conditions |
| Momentum continuation (71% historical) | Required predator_dominance > 60% + trend > 70% + pullback | Contradicted model's learned profitability |
| Adding pattern features to obs | Would require retraining all models | Better to just trust existing model |

## Key Insights

### When to Trust vs When to Gate

| Trust Model | Gate Externally |
|-------------|-----------------|
| Direction prediction | Broker limitations (crypto short) |
| Confidence estimation | Portfolio-level constraints |
| Pattern recognition (implicit) | Capital availability |
| Regime-based decisions | Account-level risk |
| Timing decisions | Trade history discipline |

### The Model Already Incorporates Patterns

The model sees:
- **12 Markov regime features** (volatility, trend, momentum, macro)
- **14 technical indicators** (MACD, RSI, Bollinger, etc.)
- **Multi-window price action** (20, 50, 100 bar returns/volatility)

Pattern recognition is IMPLICIT in these features. The model learns which combinations predict profitable trades - we don't need to hard-code geometric patterns on top.

### Dashboard Should Show Model State, Not Override It

The new "RL Model Status" panel shows:
- How many symbols are READY vs BLOCKED vs HOLD
- Signal distribution (BUY/SELL/HOLD counts)
- Average confidence across symbols

This helps users understand what the model is doing, rather than a misleading pattern win rate that the model wasn't trained on.

## References
- `scripts/live_trader.py`: Signal processing at lines 1288-1350
- `alpaca_trading/gpu/vectorized_env.py`: Reward function at lines 650-750
- `alpaca_trading/gpu/inference_obs_builder.py`: 56-feature observation space (v2.4)
