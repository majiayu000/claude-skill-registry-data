---
name: portfolio-optimization
description: Portfolio optimization using PyPortfolioOpt for mean-variance optimization, efficient frontier analysis, risk modeling, and discrete allocation. Use when building investment portfolios, calculating optimal weights, analyzing risk-return tradeoffs, maximizing Sharpe ratio, minimizing volatility, or converting weights to share allocations. Supports HRP, CVaR, semivariance, and custom objectives.
---

# Portfolio Optimization

Portfolio optimization using PyPortfolioOpt library.

## Installation

```bash
pip install pypfopt pandas numpy matplotlib
```

## Quick Start

```python
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

# Calculate expected returns and covariance
mu = expected_returns.mean_historical_return(prices_df)
S = risk_models.sample_cov(prices_df)

# Optimize for max Sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe(risk_free_rate=0.02)
cleaned_weights = ef.clean_weights()
ret, vol, sharpe = ef.portfolio_performance(verbose=True)

# Convert to share allocation
latest_prices = get_latest_prices(prices_df)
da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=100000)
allocation, leftover = da.greedy_portfolio()
```

## Core Workflows

### 1. Expected Returns

```python
from pypfopt.expected_returns import mean_historical_return, ema_historical_return, capm_return

# Mean historical (default)
mu = mean_historical_return(prices_df, frequency=252, compounding=True)

# Exponentially weighted (more weight to recent)
mu = ema_historical_return(prices_df, span=500)

# CAPM-based
mu = capm_return(prices_df, market_prices=benchmark_df, risk_free_rate=0.02)
```

### 2. Risk Models

```python
from pypfopt.risk_models import sample_cov, exp_cov, semicovariance, CovarianceShrinkage

# Sample covariance
S = sample_cov(prices_df)

# Exponentially weighted
S = exp_cov(prices_df, span=180)

# Semicovariance (downside risk only)
S = semicovariance(prices_df, benchmark=0)

# Shrinkage methods (more robust)
cs = CovarianceShrinkage(prices_df)
S = cs.ledoit_wolf()  # or cs.oracle_approximating()
```

### 3. Optimization Objectives

```python
ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

# Max Sharpe ratio
ef.max_sharpe(risk_free_rate=0.02)

# Min volatility
ef.min_volatility()

# Max quadratic utility: max w'μ - (δ/2)w'Σw
ef.max_quadratic_utility(risk_aversion=1.0)

# Target return
ef.efficient_return(target_return=0.15)

# Target risk
ef.efficient_risk(target_volatility=0.20)

# Get results
weights = ef.clean_weights()
ret, vol, sharpe = ef.portfolio_performance()
```

### 4. Constraints

```python
ef = EfficientFrontier(mu, S)

# Sector constraints
ef.add_constraint(lambda w: w[0] >= 0.2)  # Min 20% in asset 0
ef.add_constraint(lambda w: w[2] == 0.15)  # Exactly 15% in asset 2
ef.add_constraint(lambda w: w[3] + w[4] <= 0.10)  # Max 10% combined

# L2 regularization (diversification)
from pypfopt import objective_functions
ef.add_objective(objective_functions.L2_reg, gamma=0.1)
```

### 5. Alternative Methods

```python
# Hierarchical Risk Parity
from pypfopt import HRPOpt
hrp = HRPOpt(returns_df)
weights = hrp.optimize()
ret, vol, sharpe = hrp.portfolio_performance()

# Efficient CVaR (tail risk)
from pypfopt.efficient_frontier import EfficientCVaR
ef_cvar = EfficientCVaR(mu, returns_df, beta=0.95)
ef_cvar.min_cvar()

# Efficient Semivariance
from pypfopt.efficient_frontier import EfficientSemivariance
ef_semi = EfficientSemivariance(mu, returns_df, benchmark=0)
ef_semi.min_semivariance()
```

### 6. Discrete Allocation

```python
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(prices_df)
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=100000)

# Greedy algorithm (faster)
allocation, leftover = da.greedy_portfolio()

# Integer programming (more precise)
allocation, leftover = da.lp_portfolio()
```

## Plotting

```python
from pypfopt import plotting
import matplotlib.pyplot as plt

# Efficient frontier
fig, ax = plt.subplots()
plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)

# With random portfolios overlay
n_samples = 10000
w = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
rets = w.dot(ef.expected_returns)
stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
ax.scatter(stds, rets, marker=".", c=rets/stds, cmap="viridis_r")

# Covariance matrix
plotting.plot_covariance(S)

# Portfolio weights
plotting.plot_weights(weights)

# HRP dendrogram
plotting.plot_dendrogram(hrp)
```

## Reference Files

- **[references/methods.md](references/methods.md)**: Detailed API for all optimization methods
- **[references/risk_models.md](references/risk_models.md)**: Complete risk model parameters
