---
name: risk-metrics-calculation
description: Calculate portfolio risk metrics including VaR, CVaR, Sharpe, Sortino, and drawdown analysis. Use when measuring portfolio risk, implementing risk limits, or building risk monitoring systems.
---
# Risk Metrics Calculation

Comprehensive risk measurement toolkit for portfolio management, including Value at Risk, Expected Shortfall, drawdown analysis, portfolio risk, rolling windows, and stress testing.

## When to Use This Skill

- Measuring portfolio risk
- Implementing risk limits
- Building risk dashboards
- Calculating risk-adjusted returns
- Setting position sizes
- Regulatory reporting

## Core Concepts

| Category | Metrics | Use Case |
|---|---|---|
| Volatility | standard deviation, beta | general risk |
| Tail Risk | VaR, CVaR / Expected Shortfall | extreme losses |
| Drawdown | max drawdown, Calmar | capital preservation |
| Risk-Adjusted | Sharpe, Sortino, Omega, information ratio | performance quality |
| Portfolio | contribution to risk, diversification, tracking error | allocation and limits |
| Stress | historical, hypothetical, Monte Carlo | scenario resilience |

Time horizons: intraday for active trading, daily for standard reporting, weekly for rebalancing, monthly for attribution, and annual for strategic allocation.

## Operating Pattern

1. Confirm return periodicity, benchmark, risk-free rate, and annualization factor.
2. Clean and align return series before computing metrics.
3. Use multiple metrics; VaR alone is not enough.
4. Inspect distribution shape and tail behavior before assuming normality.
5. Add rolling windows when risk can change over time.
6. Stress test historical and hypothetical scenarios before setting limits.
7. Document assumptions: lookback, confidence level, horizon, benchmark, and costs.

## Implementation References

Read `references/risk-metrics-patterns.md` for full Python implementations of:

- `RiskMetrics` for volatility, VaR, CVaR, drawdowns, Sharpe, Sortino, Calmar, Omega, information ratio, and summary output.
- `PortfolioRisk` for portfolio return/volatility, marginal and component risk, risk parity weights, diversification ratio, tracking error, and conditional correlation.
- `RollingRiskMetrics` for rolling volatility, Sharpe, VaR, max drawdown, beta, and volatility regime classification.
- `StressTester` for historical scenarios, hypothetical shocks, and Monte Carlo stress.

## Quick Reference

```python
metrics = RiskMetrics(returns)
summary = metrics.summary()
var_95 = metrics.var_historical(0.95)
cvar_95 = metrics.cvar(0.95)
max_dd = metrics.max_drawdown()
sharpe = metrics.sharpe_ratio()
```

## Best Practices

### Do

- Use multiple metrics; no single number captures all risk.
- Consider tail risk with CVaR/Expected Shortfall.
- Use rolling analysis because risk regimes change.
- Stress test historical and hypothetical events.
- Document assumptions, lookbacks, distributions, and annualization choices.

### Don't

- Do not rely on VaR alone; it underestimates tail loss severity.
- Do not assume normality without checking skew/kurtosis.
- Do not ignore correlation changes during stress.
- Do not use short lookbacks that miss regime changes.
- Do not forget transaction costs when measuring realized risk.
