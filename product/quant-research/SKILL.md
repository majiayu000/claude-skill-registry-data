---
name: quant-research
description: Quantitative Research Engineer — Institutional capability and runbook for quant-research.
---

# SKILL: Quantitative Research Engineer
## Domain: Strategy Development, Backtesting, Signal Generation, Statistical Analysis

**Activation triggers:** trading strategy, backtest, alpha signal, statistical
analysis, risk-adjusted return, Monte Carlo, walk-forward analysis, strategy
optimization, quant model, factor analysis.

---

## Strategy Development Framework

```
1. HYPOTHESIS → form testable market hypothesis
2. SIGNAL DESIGN → define entry/exit logic
3. BACKTEST → test on historical data (in-sample)
4. VALIDATION → out-of-sample test (avoid data leakage)
5. WALK-FORWARD → rolling window optimization
6. MONTE CARLO → simulate worst-case scenarios
7. LIVE PAPER → paper trade before capital commitment
8. RISK SIZING → Kelly criterion or fixed fractional
9. PRODUCTION → deploy with circuit breakers
```

---

## Backtesting Engine Pattern

```python
# integral-imi-backend/app/services/quant/backtester.py
from dataclasses import dataclass, field
from decimal import Decimal
import numpy as np
import pandas as pd

@dataclass
class BacktestConfig:
    symbol: str
    timeframe: str           # "D", "H1", "M15"
    start_date: str
    end_date: str
    initial_capital: Decimal = Decimal("10000")
    commission_pct: float = 0.0002    # 0.02% per trade
    slippage_pips: float = 1.0
    max_risk_per_trade: float = 0.02  # 2% of capital

@dataclass
class BacktestResult:
    total_trades: int
    win_rate: float
    profit_factor: float
    sharpe_ratio: float
    max_drawdown: float
    total_return: float
    calmar_ratio: float      # annual return / max drawdown
    trades: list[dict] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)

class Backtester:
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.capital = float(config.initial_capital)
        self.equity_curve = [self.capital]
        self.trades = []

    def run(self, strategy: callable, data: pd.DataFrame) -> BacktestResult:
        """Run strategy over historical OHLCV data."""
        position = None

        for i in range(len(data)):
            bar = data.iloc[i]
            signal = strategy(data.iloc[:i+1])   # pass only past data (no look-ahead!)

            if signal == "buy" and position is None:
                position = self._open_position(bar, "buy")
            elif signal == "sell" and position is not None and position["direction"] == "buy":
                pnl = self._close_position(position, bar)
                self.trades.append(pnl)
                self.capital += pnl["profit"]
                self.equity_curve.append(self.capital)
                position = None

        return self._compute_metrics()

    def _open_position(self, bar, direction: str) -> dict:
        entry = bar["close"] + (self.config.slippage_pips * 0.0001)
        size = self._position_size(entry)
        return {"direction": direction, "entry": entry, "size": size, "opened_at": bar.name}

    def _close_position(self, position: dict, bar) -> dict:
        exit_price = bar["close"] - (self.config.slippage_pips * 0.0001)
        raw_pnl = (exit_price - position["entry"]) * position["size"] * 100000
        commission = abs(raw_pnl) * self.config.commission_pct
        return {
            "direction": position["direction"],
            "entry": position["entry"],
            "exit": exit_price,
            "size": position["size"],
            "profit": raw_pnl - commission,
            "opened_at": position["opened_at"],
            "closed_at": bar.name,
        }

    def _position_size(self, entry_price: float) -> float:
        risk_amount = self.capital * self.config.max_risk_per_trade
        pip_value = 0.0001 * 100000   # 1 standard lot = $10/pip for EURUSD
        stop_pips = 20   # default 20-pip stop
        return risk_amount / (stop_pips * pip_value)

    def _compute_metrics(self) -> BacktestResult:
        if not self.trades:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)

        profits = [t["profit"] for t in self.trades]
        wins = [p for p in profits if p > 0]
        losses = [p for p in profits if p < 0]

        equity = np.array(self.equity_curve)
        returns = np.diff(equity) / equity[:-1]

        peak = np.maximum.accumulate(equity)
        drawdown = (equity - peak) / peak
        max_drawdown = float(drawdown.min())

        total_return = (equity[-1] - equity[0]) / equity[0]
        annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
        calmar = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0

        return BacktestResult(
            total_trades=len(self.trades),
            win_rate=len(wins) / len(profits) if profits else 0,
            profit_factor=sum(wins) / abs(sum(losses)) if losses else float("inf"),
            sharpe_ratio=float(returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0,
            max_drawdown=max_drawdown,
            total_return=total_return,
            calmar_ratio=calmar,
            trades=self.trades,
            equity_curve=self.equity_curve,
        )
```

---

## Statistical Significance Testing

```python
import scipy.stats as stats

def test_strategy_significance(backtest_result: BacktestResult, min_trades: int = 30) -> dict:
    """Test if strategy results are statistically significant."""
    profits = [t["profit"] for t in backtest_result.trades]

    if len(profits) < min_trades:
        return {"significant": False, "reason": f"Insufficient trades ({len(profits)} < {min_trades})"}

    # t-test: is mean return significantly different from 0?
    t_stat, p_value = stats.ttest_1samp(profits, 0)

    # Sharpe > 0.5 with p < 0.05 is generally considered tradeable
    significant = p_value < 0.05 and backtest_result.sharpe_ratio > 0.5

    return {
        "significant": significant,
        "t_statistic": round(t_stat, 3),
        "p_value": round(p_value, 4),
        "sharpe_ratio": round(backtest_result.sharpe_ratio, 2),
        "confidence": f"{(1 - p_value) * 100:.1f}%",
    }
```

---

## Monte Carlo Simulation

```python
def monte_carlo_drawdown(
    trades: list[float],
    n_simulations: int = 10_000,
    percentile: float = 0.05,  # 5th percentile worst case
) -> dict:
    """Simulate worst-case drawdown by shuffling trade order."""
    results = []

    for _ in range(n_simulations):
        shuffled = np.random.choice(trades, size=len(trades), replace=True)
        equity = np.cumsum(shuffled) + 10000   # assuming $10k starting capital
        peak = np.maximum.accumulate(equity)
        drawdown = (equity - peak) / peak
        results.append(drawdown.min())

    results = np.array(results)
    return {
        "worst_case_drawdown": float(np.percentile(results, percentile * 100)),
        "median_drawdown": float(np.median(results)),
        "mean_drawdown": float(results.mean()),
        "p5_drawdown": float(np.percentile(results, 5)),
    }
```

---

## Walk-Forward Analysis

```python
def walk_forward_analysis(
    data: pd.DataFrame,
    strategy_fn: callable,
    train_pct: float = 0.7,
    n_windows: int = 5,
) -> list[BacktestResult]:
    """Roll window forward to test out-of-sample robustness."""
    window_size = len(data) // (n_windows + 1)
    results = []

    for i in range(n_windows):
        start = i * window_size
        split = start + int(window_size * train_pct)
        end = start + window_size

        train_data = data.iloc[start:split]
        test_data = data.iloc[split:end]

        # Optimize on train, evaluate on test
        optimized_strategy = optimize_strategy(strategy_fn, train_data)
        result = Backtester(config).run(optimized_strategy, test_data)
        results.append(result)

    return results
```

---

## Anti-Patterns

```
✗ Look-ahead bias: using future data in strategy signal (common bug)
✗ Overfitting: optimizing > 3 parameters on same dataset
✗ Ignoring commissions/slippage (live performance always worse than backtest)
✗ Testing on 1 year of data (need > 3 years, multiple market regimes)
✗ Not testing out-of-sample (in-sample Sharpe 2.0 → live Sharpe 0.3)
✗ Missing survivorship bias in universe selection
✗ No Monte Carlo for drawdown estimation (backtest shows best-case order)
✗ Trading live from backtest without paper trading phase
✗ Position sizing ignoring current drawdown (Kelly requires adjustment)
```
