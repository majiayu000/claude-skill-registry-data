---
name: codebase-consolidation-pattern
description: "Reorganize scattered modules into subpackages while maintaining backwards compatibility via shims. Trigger when: (1) too many root-level files, (2) need to group related functionality, (3) cleaning up codebase structure."
author: Claude Code
date: 2024-12-31
---

# Codebase Consolidation Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-31 |
| **Goal** | Reorganize root-level modules into logical subpackages without breaking existing imports |
| **Environment** | alpaca_trading/ package with 24 root-level .py files |
| **Status** | Success |

## Context

**Problem**: Codebase grew organically with many root-level modules (24 .py files). Related functionality scattered:
- Trading: broker.py, executor.py, pdt.py, market_hours.py, profit_tracker.py, notify.py
- Training: model_version.py, online_bandit.py, online_learning.py, rl_context_gpu.py
- Risk: risk_monitor.py floating at root instead of in risk/

**Solution**: Move related modules to subpackages, create compatibility shims at original locations.

## Verified Workflow

### 1. Identify Module Groups

Analyze imports and functionality to group related modules:

```python
# Trading execution group
trading/
  - broker.py          # Alpaca API wrapper
  - executor.py        # Order execution
  - pdt.py             # Pattern Day Trader rules
  - market_hours.py    # Market session detection
  - profit_tracker.py  # P&L tracking
  - notify.py          # Notifications

# Training system group
training/
  - model_version.py   # Version protocol
  - online_bandit.py   # Thompson sampling
  - online_learning.py # Real-time updates
  - rl_context_gpu.py  # GPU context building

# Existing packages to extend
risk/
  - risk_monitor.py    # Real-time monitoring (move from root)
```

### 2. Move Files with Git (Preserve History)

```bash
# Create new package directory
mkdir alpaca_trading/trading

# Move files preserving git history
git mv alpaca_trading/broker.py alpaca_trading/trading/
git mv alpaca_trading/executor.py alpaca_trading/trading/
git mv alpaca_trading/pdt.py alpaca_trading/trading/
git mv alpaca_trading/market_hours.py alpaca_trading/trading/
git mv alpaca_trading/profit_tracker.py alpaca_trading/trading/
git mv alpaca_trading/notify.py alpaca_trading/trading/
```

### 3. Update Internal Imports

After moving, update relative imports in moved files:

```python
# BEFORE (in executor.py at root):
from .broker import Broker, BrokerConfig
from .utils import setup_logger
from .pdt import DayTradeGuard

# AFTER (in trading/executor.py):
from .broker import Broker, BrokerConfig  # Same package, no change
from ..utils import setup_logger          # Parent package, add ..
from .pdt import DayTradeGuard            # Same package, no change
```

### 4. Create Package __init__.py

```python
# alpaca_trading/trading/__init__.py
"""Trading execution and broker integration."""
from .broker import Broker, BrokerConfig
from .executor import Executor
from .pdt import DayTradeGuard
from .market_hours import (
    is_trading_hours,
    get_next_trading_window,
    detect_asset_type,
    AssetType,
    MarketSession,
)
from .profit_tracker import ProfitTracker
from .notify import (
    EmailNotifier,
    TelegramNotifier,
    from_env_email,
    from_env_telegram,
)

__all__ = [
    'Broker', 'BrokerConfig', 'Executor', 'DayTradeGuard',
    'is_trading_hours', 'get_next_trading_window', 'detect_asset_type',
    'AssetType', 'MarketSession', 'ProfitTracker',
    'EmailNotifier', 'TelegramNotifier', 'from_env_email', 'from_env_telegram',
]
```

### 5. Create Backwards Compatibility Shims

At original locations, create thin wrapper files:

```python
# alpaca_trading/broker.py (shim)
"""Compatibility shim - broker moved to trading/broker.py"""
from .trading.broker import *  # noqa: F401,F403
```

```python
# alpaca_trading/executor.py (shim)
"""Compatibility shim - executor moved to trading/executor.py"""
from .trading.executor import *  # noqa: F401,F403
```

### 6. Handle Private Functions

`from module import *` doesn't export private functions (starting with `_`). If tests use them:

```python
# alpaca_trading/mdp.py (shim with private function)
"""Compatibility shim - mdp archived to _archive/mdp.py"""
from ._archive.mdp import *  # noqa: F401,F403
from ._archive.mdp import _tanh_clip  # noqa: F401 - private but used in tests
```

### 7. Update Extended Package __init__.py

When adding to existing package (e.g., risk/):

```python
# alpaca_trading/risk/__init__.py
"""Risk management module."""
from .portfolio_risk import AdvancedRiskManager, RiskLimits, PositionRisk
from .garch import GARCHRiskManager, fit_garch_model
from .capital_manager import CapitalManager, CapitalAllocation
# NEW: Add moved module
from .risk_monitor import (
    RealTimeRiskMonitor,
    RiskAlert,
    CircuitBreakerConfig,
    create_risk_monitoring_system,
)

__all__ = [
    # ... existing exports ...
    # NEW exports
    'RealTimeRiskMonitor', 'RiskAlert', 'CircuitBreakerConfig',
    'create_risk_monitoring_system',
]
```

## Import Patterns Summary

| Original Location | New Location | Import Change |
|-------------------|--------------|---------------|
| `from alpaca_trading.broker import Broker` | `alpaca_trading/trading/broker.py` | **No change** (shim handles it) |
| `from alpaca_trading import broker` | `alpaca_trading/trading/broker.py` | **No change** (shim handles it) |
| Internal: `from .utils import` | Now in subpackage | `from ..utils import` |
| Internal: `from .other_module import` | Now in same subpackage | `from .other_module import` |

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Move without shims | Breaks all existing imports immediately | Always create backwards-compat shims |
| Use deprecation warnings in shims | Noisy for users, not actionable | Only warn in truly deprecated modules |
| `from module import *` for private functions | Private `_func` not exported by `*` | Explicitly import private functions if needed |
| Forget to update __init__.py | New package not importable | Always create/update package __init__.py |
| Update imports before moving | Files don't exist yet | Move first, then update imports |

## Checklist

- [ ] Identify logical module groups
- [ ] Create target package directories
- [ ] Use `git mv` to preserve history
- [ ] Update internal imports (`.` → `..` for parent)
- [ ] Create package `__init__.py` with exports
- [ ] Create compatibility shims at original locations
- [ ] Handle private functions explicitly if needed
- [ ] Run tests to verify nothing broken
- [ ] Commit with descriptive message

## Final Structure

```
alpaca_trading/
├── trading/                    # NEW: Trading execution
│   ├── __init__.py
│   ├── broker.py
│   ├── executor.py
│   ├── pdt.py
│   ├── market_hours.py
│   ├── profit_tracker.py
│   └── notify.py
├── training/                   # EXTENDED: Training system
│   ├── __init__.py
│   ├── archive.py             # existing
│   ├── gating.py              # existing
│   ├── model_version.py       # moved
│   ├── online_bandit.py       # moved
│   ├── online_learning.py     # moved
│   └── rl_context_gpu.py      # moved
├── risk/                       # EXTENDED: Risk management
│   ├── __init__.py
│   ├── portfolio_risk.py      # existing
│   ├── garch.py               # existing
│   └── risk_monitor.py        # moved from root
│
├── broker.py                   # SHIM → trading/broker.py
├── executor.py                 # SHIM → trading/executor.py
├── pdt.py                      # SHIM → trading/pdt.py
├── market_hours.py             # SHIM → trading/market_hours.py
├── profit_tracker.py           # SHIM → trading/profit_tracker.py
├── notify.py                   # SHIM → trading/notify.py
├── model_version.py            # SHIM → training/model_version.py
├── online_bandit.py            # SHIM → training/online_bandit.py
├── online_learning.py          # SHIM → training/online_learning.py
├── rl_context_gpu.py           # SHIM → training/rl_context_gpu.py
└── risk_monitor.py             # SHIM → risk/risk_monitor.py
```

## Key Insights

- **Shims are essential**: Without them, all existing code breaks instantly
- **Git history preserved**: Use `git mv`, not `mv` + `git add`
- **Test after each group**: Move one group, test, commit, then next group
- **Relative imports change**: Moving deeper requires `..` prefix for parent imports
- **Private functions need explicit import**: `*` doesn't export `_prefixed` functions

## References
- Commit `d0f12b5`: Full consolidation implementation
- `alpaca_trading/trading/__init__.py`: Example package exports
- `alpaca_trading/broker.py`: Example shim file
