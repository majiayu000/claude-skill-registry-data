---
name: dashboard-symbol-discovery
description: "Auto-discover dashboard symbols from loaded RL models. Trigger when: (1) dashboard shows old/wrong symbols, (2) symbols mismatch between live trader and dashboard, (3) adding new models to system, (4) dashboard shows NO_MODEL for all symbols."
author: Claude Code
date: 2024-12-24
---

# Dashboard Symbol Auto-Discovery

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-24 |
| **Goal** | Fix dashboard showing stale symbols that don't match trained models |
| **Environment** | scripts/monitor_dashboard.py, scripts/live_trader.py |
| **Status** | Success |

## Context

The dashboard was showing hardcoded symbols (SPY, QQQ, AAPL, MSFT, NVDA, GOOGL, TSLA, BTCUSD, ETHUSD) even when:
1. **No models existed** for those symbols
2. **Different models were trained** (e.g., TMO, PANW, AMZN, etc.)
3. **Live trader selected different symbols** via universe selection

Root cause: `DashboardConfig.symbols` had hardcoded defaults, and the live trader didn't pass `--symbols` to the dashboard subprocess.

## Verified Workflow

### Problem Pattern

```python
# WRONG: Hardcoded defaults in DashboardConfig
@dataclass
class DashboardConfig:
    symbols: List[str] = field(default_factory=lambda: [
        "SPY", "QQQ", "AAPL", "MSFT", "NVDA", "GOOGL", "TSLA", "BTCUSD", "ETHUSD"
    ])
```

### Solution: Auto-Discovery

```python
# CORRECT: Empty default, auto-discover from models
@dataclass
class DashboardConfig:
    # Symbols to monitor - auto-discovered from models if not specified
    symbols: List[str] = field(default_factory=list)

# In run_dashboard(), after loading predictors:
if not cfg.symbols:
    if predictors:
        cfg.symbols = list(predictors.keys())
        logger.info(f"Auto-discovered {len(cfg.symbols)} symbols from models: {cfg.symbols}")
    else:
        # Fallback if no models found
        cfg.symbols = ["SPY", "QQQ"]
        logger.warning("No models found - using fallback: SPY, QQQ")
```

### Solution: Pass Symbols from Live Trader

```python
# In live_trader.py, when launching dashboard subprocess:
dashboard_cmd = [
    sys.executable, "-m", "scripts.monitor_dashboard",
    "--paper", str(args.paper),
    "--interval", str(args.dashboard_interval),
    "--keys-file", args.keys_file,
    "--symbols", ",".join(symbols),  # Pass active symbols
    "--show"
]
logger.info(f"Dashboard symbols: {symbols}")
```

### Priority Order

1. **CLI `--symbols` argument** (highest priority) - Explicitly passed symbols
2. **Auto-discovery from models** - If no CLI symbols, use loaded predictors
3. **Fallback** (lowest priority) - SPY, QQQ if nothing else available

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Hardcoded symbol defaults | Symbols became stale when models changed | Use empty default + auto-discovery |
| Dashboard subprocess without --symbols | Live trader and dashboard had different symbol lists | Always pass symbols to subprocess |
| Only auto-discovery | Would ignore explicit user preferences | Support CLI override as highest priority |
| No fallback | Crashes when no models exist | Always have a minimal fallback |

## Key Insights

### Architecture: Two Separate Symbol Flows

The live trader and dashboard have independent symbol selection:

```
live_trader.py:
  1. Discovers models from disk (*.pt files)
  2. Runs universe selection (constrained to symbols WITH models)
  3. Launches dashboard subprocess

monitor_dashboard.py (OLD - BROKEN):
  1. Uses hardcoded defaults
  2. Ignores loaded predictors for symbol list
  3. Shows NO_MODEL for symbols without models

monitor_dashboard.py (NEW - FIXED):
  1. If --symbols passed, use those
  2. Else auto-discover from loaded predictors
  3. Else use minimal fallback
```

### Model Discovery Pattern

Both live_trader and dashboard discover models the same way:

```python
model_dir = Path("models/rl_symbols")
model_files = list(model_dir.glob("*.pt"))
for model_file in model_files:
    # Parse SYMBOL_TIMEFRAME.pt
    stem = model_file.stem  # e.g., "AAPL_1Hour"
    parts = stem.rsplit("_", 1)
    symbol, timeframe = parts[0], parts[1]
```

### Dashboard --symbols Argument

Already existed but wasn't being used:

```python
parser.add_argument('--symbols', type=str, default=None,
                   help='Comma-separated symbols to monitor')

# Parsing:
if args.symbols:
    cfg.symbols = [s.strip() for s in args.symbols.split(',') if s.strip()]
```

### Files Modified

```
scripts/monitor_dashboard.py:
  - Line 297-299: Changed default symbols to empty list
  - Line 961-969: Added auto-discovery logic

scripts/live_trader.py:
  - Line 2033: Added --symbols argument to dashboard command
  - Line 2037: Added logging for dashboard symbols
```

## References
- `scripts/monitor_dashboard.py`: Lines 297-299 (config), 961-969 (auto-discovery)
- `scripts/live_trader.py`: Lines 2028-2037 (subprocess launch)
- `models/rl_symbols/*.pt`: Model files for discovery
