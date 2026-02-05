---
name: trading-gates-pattern-filter
description: "Pattern filter normalization and multi-gate order entry system"
author: Claude Code
date: 2025-12-18
---

# Trading Gates & Pattern Filter - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-18 |
| **Goal** | Fix pattern filter blocking all trades; add dashboard gate visibility |
| **Environment** | Python 3.10, Alpaca API, Live Trading |
| **Status** | Success |

## Problem Statement

The live trader was showing "Pattern filter rejected - no high-win-rate pattern match" for all symbols, even when the dashboard showed valid BUY/SELL signals. Investigation revealed two issues:

1. **Missing predator/prey values**: `_get_predprey_validation()` wasn't returning predator/prey values
2. **Misaligned thresholds**: Pattern filter used absolute thresholds but Lotka-Volterra dynamics decay values to near-zero

## Failed Attempts

| Attempt | Why It Failed |
|---------|---------------|
| Lowering absolute thresholds (e.g., 0.01 instead of 0.4) | Thresholds become meaningless when values vary by orders of magnitude |
| Using raw predator/prey values directly | Values decay to 0.01-0.02, making both patterns fail |
| Bypassing pattern filter | Defeats purpose of high-win-rate filtering |

## Solution: Normalized Dominance Ratios

The key insight is that while raw predator/prey values can be any magnitude, their **ratio** indicates regime dominance:

```python
# In filter_by_patterns() - alpaca_trading/signals/pattern_filter.py

# Extract raw values
raw_prey = regime_context.get('prey_strength', 0.5)
raw_predator = regime_context.get('predator_strength', 0.5)

# Normalize to dominance ratios (0-1 range)
total_strength = raw_predator + raw_prey + 1e-9  # Avoid division by zero
prey_strength = raw_prey / total_strength  # Higher = more mean-reverting
predator_strength = raw_predator / total_strength  # Higher = more trending
```

### Example
- Raw values: predator=0.015, prey=0.17
- Normalized: predator_dominance=8%, prey_dominance=92%
- Interpretation: Strong mean-reverting regime (VWAP reversion pattern applies)

## Trading Gates Architecture

Orders must pass ALL gates before execution:

| Gate | Threshold | Implementation |
|------|-----------|----------------|
| Confidence | Adaptive (0.50-0.65) | `get_adaptive_entry_threshold()` based on GARCH regime |
| Pattern Filter | 65% min win rate | VWAP reversion (68%) OR momentum continuation (71%) |
| Crypto Short | Block shorts | `detect_asset_type() == CRYPTO and signal < 0` |
| Portfolio Limit | <80% exposure | `portfolio_metrics.total_exposure` |
| Capital Manager | 30% safety buffer | `capital_mgr.check_trade_allowed()` |
| Portfolio Risk | VaR <2% | `portfolio_risk_mgr.check_risk()` |

### Pattern Filter Requirements

**VWAP Reversion (68% win rate):**
- `prey_dominance >= 0.4` (mean-reverting regime)
- Price 2+ standard deviations from VWAP
- Signal direction matches expected reversion

**Momentum Continuation (71% win rate):**
- `predator_dominance >= 0.6` (trending regime)
- `trend_prob_up > 0.7` OR `trend_prob_down > 0.7`
- Pullback in trend direction
- Signal aligns with trend

## Dashboard Gate Display

Added gate status indicators to `plot_symbol_signals()`:

```python
# In dashboard.py - alpaca_trading/visualization/dashboard.py

gate_statuses = symbol_signals.get('gate_statuses', [])
for i, sym in enumerate(symbols):
    gate = gate_statuses[i]
    status = gate.get('final_status', 'UNKNOWN')

    if status == 'READY':
        status_color = 'green'
        status_text = 'READY'
    elif status == 'BLOCKED':
        status_color = 'red'
        status_text = gate.get('block_reason', 'blocked')[:12]
    elif status == 'HOLD':
        status_color = 'gray'
        status_text = 'HOLD'
```

## Key Files Modified

| File | Change |
|------|--------|
| `alpaca_trading/prediction/multi_tf_predictor.py` | Added predator/prey to `_get_predprey_validation()` return |
| `alpaca_trading/signals/pattern_filter.py` | Normalized predator/prey to dominance ratios |
| `alpaca_trading/executor.py` | Changed `qty: int` to `qty: float` for fractional shares |
| `scripts/live_trader.py` | Added crypto short block, `--dashboard` flag |
| `scripts/monitor_dashboard.py` | Added `check_trading_gates()` function |
| `alpaca_trading/visualization/dashboard.py` | Added gate status display |

## Verification

After fix:
- AAPL: PASS (vwap_reversion) - prey_dominance=92%
- AMD: PASS (vwap_reversion) - prey_dominance=91.9%
- AVGO: FAIL (no_match) - SELL signal in prey-dominant regime (expects BUY)
- BTCUSD: FAIL (crypto_no_short) - Alpaca doesn't support crypto shorts

## Key Learnings

1. **Lotka-Volterra dynamics decay**: Both predator and prey values decay to near-zero over time; use ratios, not absolutes
2. **Crypto limitations**: Alpaca doesn't support short selling for crypto; must block SELL signals for crypto entries
3. **Fractional shares**: Executor must use `float` qty, not `int`, for proper fractional share support
4. **Dashboard visibility**: Showing gate status helps debug why signals don't result in orders

## Related Skills

- `position-reconciliation`: Broker state sync
- `markov-regime-features`: Debugging constant Markov features
- `drawdown-guardrails-pattern`: Drawdown control across systems
