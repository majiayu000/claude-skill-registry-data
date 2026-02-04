---
name: dashboard-parallel-lists
description: "Dashboard symbol_signals uses parallel lists (symbols[], signal_values[], gate_statuses[]) not dict keyed by symbol. Trigger when: (1) 'list' object has no attribute 'get', (2) .items() on symbol_signals fails."
author: Claude Code
date: 2024-12-26
---

# Dashboard Parallel Lists Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-26 |
| **Goal** | Fix dashboard error when processing symbol signals |
| **Environment** | scripts/monitor_dashboard.py, scripts/live_trader.py |
| **Status** | Success |

## Context

The dashboard crashed with:
```
[ERROR] __main__: Dashboard error: 'list' object has no attribute 'get'
```

**Root Cause**: Code assumed `symbol_signals` was a dict keyed by symbol:
```python
# WRONG assumption
for symbol, data in symbol_signals.items():
    signal = data.get('signal', 0)
    gate_status = data.get('gate_status', {})
```

**Actual Structure**: `get_symbol_signals()` returns parallel lists:
```python
{
    'symbols': ['AAPL', 'MSFT', 'GOOGL'],
    'signal_values': [1, -1, 0],
    'confidences': [0.72, 0.65, 0.45],
    'gate_statuses': [
        {'final_status': 'READY', ...},
        {'final_status': 'BLOCKED', 'blocking_gate': 'crypto_short'},
        {'final_status': 'HOLD', ...}
    ]
}
```

## Verified Workflow

### Correct Pattern: Iterate by Index

```python
def get_model_metrics(symbol_signals: Dict) -> dict:
    """Process symbol signals using parallel list structure."""
    metrics = {
        'total_symbols': 0,
        'ready_count': 0,
        'blocked_count': 0,
        'hold_count': 0,
        'avg_confidence': 0.0,
        'signals': {'buy': 0, 'sell': 0, 'hold': 0}
    }

    if not symbol_signals:
        return metrics

    # Extract parallel lists
    symbols = symbol_signals.get('symbols', [])
    signal_values = symbol_signals.get('signal_values', [])
    confidences = symbol_signals.get('confidences', [])
    gate_statuses = symbol_signals.get('gate_statuses', [])

    if not symbols:
        return metrics

    metrics['total_symbols'] = len(symbols)
    valid_confidences = []

    # Iterate by index across parallel lists
    for i, sym in enumerate(symbols):
        # Safe access with bounds checking
        gate_status = gate_statuses[i] if i < len(gate_statuses) else {}
        signal = signal_values[i] if i < len(signal_values) else 0
        conf = confidences[i] if i < len(confidences) else 0

        status = gate_status.get('final_status', 'HOLD')

        if status == 'READY':
            metrics['ready_count'] += 1
        elif status == 'BLOCKED':
            metrics['blocked_count'] += 1
        else:
            metrics['hold_count'] += 1

        if signal > 0:
            metrics['signals']['buy'] += 1
        elif signal < 0:
            metrics['signals']['sell'] += 1
        else:
            metrics['signals']['hold'] += 1

        if conf > 0:
            valid_confidences.append(conf)

    if valid_confidences:
        metrics['avg_confidence'] = sum(valid_confidences) / len(valid_confidences)

    return metrics
```

### Why Parallel Lists?

The `get_symbol_signals()` function returns parallel lists because:

1. **Performance**: Lists are faster to append during signal generation loop
2. **Order preservation**: Maintains processing order for display
3. **Flexible lengths**: Different lists can have different lengths if some data missing
4. **JSON serialization**: Easy to serialize for dashboard communication

### Accessing Individual Symbol Data

```python
# Get data for a specific symbol by finding its index
def get_symbol_data(symbol_signals: Dict, target_symbol: str) -> dict:
    symbols = symbol_signals.get('symbols', [])
    try:
        idx = symbols.index(target_symbol)
        return {
            'symbol': target_symbol,
            'signal': symbol_signals.get('signal_values', [])[idx],
            'confidence': symbol_signals.get('confidences', [])[idx],
            'gate_status': symbol_signals.get('gate_statuses', [])[idx],
        }
    except (ValueError, IndexError):
        return None
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| `for sym, data in symbol_signals.items()` | symbol_signals is not keyed by symbol | Use parallel list iteration |
| `symbol_signals[symbol]['signal']` | Lists don't support dict-style access | Find index first, then access |
| Assuming all lists same length | Some fields may be missing | Always use bounds checking |
| Converting to dict-by-symbol | Expensive for large symbol counts | Keep parallel structure |

## Key Insights

### Signal Structure from get_symbol_signals()

```python
# In live_trader.py get_symbol_signals() returns:
{
    'symbols': List[str],           # Symbol names
    'signal_values': List[int],     # -1 (sell), 0 (hold), 1 (buy)
    'confidences': List[float],     # Model confidence [0, 1]
    'gate_statuses': List[Dict],    # Gate check results
    'prices': List[float],          # Current prices
    'regime_contexts': List[Dict],  # Markov regime info
}
```

### Gate Status Structure

```python
# Each gate_status dict contains:
{
    'final_status': 'READY' | 'BLOCKED' | 'HOLD',
    'blocking_gate': str | None,    # Which gate blocked (if any)
    'confidence_gate': bool,
    'crypto_short_gate': bool,
    'portfolio_limit_gate': bool,
    'capital_manager_gate': bool,
    'portfolio_risk_gate': bool,
}
```

### Common Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `'list' object has no attribute 'get'` | Called `.get()` on a list | Use index access |
| `'list' object has no attribute 'items'` | Called `.items()` on symbol_signals | Iterate by index |
| `KeyError: 'AAPL'` | Tried `symbol_signals['AAPL']` | Find index in symbols list |
| `IndexError: list index out of range` | Lists have different lengths | Add bounds checking |

## Files Modified

```
scripts/monitor_dashboard.py:
  - Lines 536-577: get_model_metrics() rewritten for parallel lists
  - Pattern: Extract lists first, iterate by index with bounds checking
```

## References
- `scripts/live_trader.py`: `get_symbol_signals()` function (lines ~800-900)
- `scripts/monitor_dashboard.py`: `get_model_metrics()` function (lines ~536-577)
- `alpaca_trading/visualization/dashboard.py`: Dashboard display logic
