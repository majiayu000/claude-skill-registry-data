---
name: hft-quant-expert
description: Quantitative trading expertise for DeFi and crypto derivatives. Use when building trading strategies, signals, risk management. Triggers on signal, backtest, alpha, sharpe, volatility, correlation, position size, risk.
---

# HFT Quant Expert

## Quick Formulas
```python
# Z-score
zscore = (value - rolling_mean) / rolling_std

# Sharpe (annualized)
sharpe = np.sqrt(252) * returns.mean() / returns.std()

# Kelly fraction (use 0.25x)
kelly = (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio

# Half-life of mean reversion
half_life = -np.log(2) / lambda_coef
```

## Common Pitfalls

- **Lookahead bias** - Using future data
- **Survivorship bias** - Only existing assets
- **Overfitting** - Too many parameters
- **Ignoring costs** - Gas + slippage
- **Wrong annualization** - 252 daily, 365*24 hourly
