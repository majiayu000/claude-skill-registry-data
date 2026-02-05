---
name: financial-time-series
description: Use when working with price data, trading signals, or implementing momentum strategies. Covers returns calculation, volatility targeting, momentum factors, MACD indicators, time-series momentum (TSMOM), portfolio construction, futures contracts, and risk-adjusted returns for trend-following strategies.
---

# Financial Time-Series Processing

## Purpose

Comprehensive guide for processing financial time-series data and implementing trend-following strategies, based on the X-Trend model and Deep Momentum Networks framework.

## When to Use

Activate this skill when:
- Processing price data or returns
- Calculating momentum factors or MACD indicators
- Implementing volatility targeting
- Building trend-following strategies
- Constructing trading portfolios
- Working with futures contracts
- Calculating risk-adjusted returns (Sharpe ratio)

## Core Concepts

### 1. Returns Calculation

Returns linearly de-trend the price series:

```python
def calculate_returns(prices, lookback=1):
    """
    Calculate returns over specified lookback period.

    Args:
        prices: Array of daily close prices p[t]
        lookback: Number of days (t') for return calculation

    Returns:
        returns: r[t-t', t] = (p[t] - p[t-t']) / p[t-t']
    """
    return (prices - prices.shift(lookback)) / prices.shift(lookback)
```

**Key Points:**
- Use daily close prices
- Standard lookbacks: 1-day, 21-day (1-month), 63-day (3-month), 126-day (6-month), 252-day (1-year)
- Returns remove price trends for stationarity

### 2. Volatility Targeting

Normalize positions by ex-ante volatility to ensure equal risk contribution:

```python
def volatility_targeting(position, realized_vol, target_vol=0.15):
    """
    Scale position by volatility targeting leverage factor.

    Args:
        position: Raw trading signal z[t] in [-1, 1]
        realized_vol: Ex-ante volatility σ[t] (60-day EWMA)
        target_vol: Annual target volatility σ_tgt (typically 15%)

    Returns:
        scaled_position: Volatility-adjusted position
    """
    leverage = target_vol / realized_vol
    return position * leverage
```

**Implementation:**
- Calculate σ[t] using exponentially weighted moving standard deviation over 60 days
- Typical annual target: σ_tgt = 0.15 (15%)
- Ensures each asset contributes approximately equal risk

### 3. Momentum Factors

#### Time-Series Momentum (TSMOM)

Classic momentum signal based on historical returns:

```python
def tsmom_signal(returns_252):
    """
    Simple 1-year momentum signal.

    Args:
        returns_252: 252-day (1-year) returns

    Returns:
        signal: +1 (long) or -1 (short)
    """
    return np.sign(returns_252)
```

#### Multi-Scale Momentum

Combine signals at different timescales:

```python
def multi_scale_momentum(prices):
    """
    Weighted combination of momentum at multiple timescales.

    Timescales:
        - 21 days (1-month)
        - 63 days (3-month)
        - 126 days (6-month)
        - 252 days (12-month)
    """
    timescales = [21, 63, 126, 252]
    weights = [0.25, 0.25, 0.25, 0.25]  # Equal weighting

    signals = []
    for t in timescales:
        ret = calculate_returns(prices, lookback=t)
        signals.append(np.sign(ret))

    return np.average(signals, weights=weights)
```

#### MACD (Moving Average Convergence Divergence)

Compare exponentially weighted signals at two timescales:

```python
def macd_factor(prices, short=8, long=24, lookback_std=252):
    """
    Calculate MACD momentum indicator.

    MACD = (EWMA_short - EWMA_long) / std(prices_60)
    Normalized by std of past year returns

    Common timescale pairs: (8,24), (16,28), (32,96)

    Returns:
        macd: Normalized MACD signal
              > 0 indicates buy, < 0 indicates sell
              Magnitude indicates conviction
    """
    ewma_short = prices.ewm(span=short).mean()
    ewma_long = prices.ewm(span=long).mean()
    price_std = prices.ewm(span=60).std()

    m = (ewma_short - ewma_long) / price_std
    m_std = m.rolling(lookback_std).std()

    return m / m_std
```

**MACD to Position Conversion:**
```python
def macd_to_position(macd_signal):
    """Convert MACD signal to position using response function."""
    return macd_signal * np.exp(-macd_signal**2 / 4) / 0.89
```

### 4. Deep Learning Momentum Factors

Normalized returns at multiple timescales for neural network inputs:

```python
def normalized_returns(prices, volatility, timescales=[1, 21, 63, 126, 252]):
    """
    Calculate volatility-normalized returns for deep learning models.

    r_hat[t-t', t] = r[t-t', t] / (σ[t] * sqrt(t'))

    This normalization ensures returns are comparable across timescales.
    """
    factors = []
    for t in timescales:
        ret = calculate_returns(prices, lookback=t)
        r_normalized = ret / (volatility * np.sqrt(t))
        factors.append(r_normalized)

    return np.column_stack(factors)
```

**Full Feature Vector:**
```python
def create_feature_vector(prices):
    """
    Create input features x[t] for deep momentum models.

    Includes:
    - Normalized returns at multiple timescales
    - MACD indicators at multiple (S, L) pairs
    """
    volatility = prices.pct_change().ewm(span=60).std()

    # Normalized returns
    norm_returns = normalized_returns(prices, volatility)

    # MACD features
    macd_features = [
        macd_factor(prices, 8, 24),
        macd_factor(prices, 16, 28),
        macd_factor(prices, 32, 96)
    ]

    return np.concatenate([norm_returns, macd_features])
```

### 5. Portfolio Construction

Calculate portfolio returns with volatility targeting and transaction costs:

```python
def portfolio_returns(positions, returns, volatility, target_vol=0.15,
                     transaction_costs=0.0):
    """
    Calculate portfolio returns with volatility targeting.

    R_portfolio[t+1] = (1/N) * Σ R[i, t+1]

    where for each asset i:
    R[i,t+1] = z[i,t] * (σ_tgt/σ[i,t]) * r[i,t+1]
               - C[i] * σ_tgt * |z[i,t]/σ[i,t] - z[i,t-1]/σ[i,t-1]|

    Args:
        positions: z[i,t] for each asset (N × T)
        returns: r[i,t+1] for each asset
        volatility: σ[i,t] for each asset
        target_vol: Annual target volatility σ_tgt
        transaction_costs: C[i] per asset

    Returns:
        portfolio_returns: R_portfolio[t+1]

    IMPORTANT: Transaction cost calculation uses position_changes which is
    already scaled by (target_vol / volatility), so we DON'T multiply by
    target_vol again. The formula is C * |scaled_pos[t] - scaled_pos[t-1]|,
    where scaled_pos = z * (σ_tgt/σ). This gives C * σ_tgt * |z/σ - z_prev/σ_prev|
    as per the paper's Eq. (2).
    """
    N = len(positions)

    # Scale by volatility targeting: scaled_pos = z * (σ_tgt/σ)
    scaled_positions = positions * (target_vol / volatility)

    # Asset returns
    asset_returns = scaled_positions * returns

    # Transaction costs
    # position_changes is already in units of σ_tgt * |z/σ - z_prev/σ_prev|
    # So we only multiply by transaction_costs C, NOT by target_vol again
    position_changes = np.abs(
        scaled_positions - scaled_positions.shift(1)
    )
    costs = transaction_costs * position_changes

    # Net returns per asset
    net_returns = asset_returns - costs

    # Equal-weighted portfolio
    return net_returns.mean(axis=0)
```

### 6. Risk-Adjusted Returns

#### Sharpe Ratio

Primary metric for strategy evaluation:

```python
def sharpe_ratio(returns, periods_per_year=252):
    """
    Calculate annualized Sharpe ratio.

    Sharpe = sqrt(252) * mean(returns) / std(returns)

    Measures returns per unit volatility.
    """
    return np.sqrt(periods_per_year) * returns.mean() / returns.std()
```

#### Sharpe Loss for Neural Networks

Differentiable loss function for direct Sharpe optimization:

```python
def sharpe_loss(positions, returns, volatility, target_vol=0.15):
    """
    Negative Sharpe ratio loss for gradient descent.

    L_Sharpe = -sqrt(252) * mean_batch(R[t+1]) / std_batch(R[t+1])

    where R[t+1] = (σ_tgt/σ[t]) * r[t+1] * position[t]

    This is the loss function used in Deep Momentum Networks.
    """
    scaled_returns = (target_vol / volatility) * returns * positions

    mean_ret = scaled_returns.mean()
    std_ret = scaled_returns.std()

    return -np.sqrt(252) * mean_ret / std_ret
```

### 7. Futures Contracts Handling

#### Continuous Futures

```python
def create_continuous_contract(contracts, method='ratio_adjusted'):
    """
    Chain futures contracts into continuous series.

    Methods:
    - 'ratio_adjusted' (backwards): Multiply historical prices by ratio
    - 'difference_adjusted': Add price differences

    Ratio-adjusted method:
    - Preserves percentage returns
    - Preferred for momentum strategies
    - Used in Pinnacle Data CLC Database
    """
    if method == 'ratio_adjusted':
        # When rolling from contract C1 to C2:
        # Adjustment_ratio = P_C1(roll_date) / P_C2(roll_date)
        # Apply ratio to all historical prices before roll_date
        pass  # Implementation details

    return continuous_prices
```

### 8. Performance Metrics

```python
def calculate_metrics(returns):
    """
    Calculate comprehensive performance metrics.

    Returns:
        metrics: Dict with Sharpe, returns, volatility, drawdown
    """
    cumulative_returns = (1 + returns).cumprod()
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max

    return {
        'sharpe': sharpe_ratio(returns),
        'annual_return': returns.mean() * 252,
        'annual_volatility': returns.std() * np.sqrt(252),
        'max_drawdown': drawdown.min(),
        'cumulative_return': cumulative_returns.iloc[-1] - 1
    }
```

## Common Patterns

### Pattern 1: Basic TSMOM Strategy

```python
def tsmom_strategy(prices, target_vol=0.15):
    """Implement basic time-series momentum strategy."""
    # 1. Calculate 1-year returns
    returns_252 = calculate_returns(prices, lookback=252)

    # 2. Generate signal
    signal = np.sign(returns_252)

    # 3. Calculate realized volatility (60-day EWMA)
    realized_vol = prices.pct_change().ewm(span=60).std()

    # 4. Apply volatility targeting
    position = volatility_targeting(signal, realized_vol, target_vol)

    # 5. Calculate returns
    next_day_returns = prices.pct_change().shift(-1)
    strategy_returns = position * next_day_returns * (target_vol / realized_vol)

    return strategy_returns
```

### Pattern 2: Multi-Asset Portfolio

```python
def multi_asset_portfolio(asset_prices_dict, target_vol=0.15):
    """
    Construct equal-risk portfolio across multiple assets.

    Args:
        asset_prices_dict: {'ASSET1': prices1, 'ASSET2': prices2, ...}
    """
    asset_returns = {}

    for asset, prices in asset_prices_dict.items():
        # Generate signal for each asset
        signal = tsmom_signal(calculate_returns(prices, 252))
        volatility = prices.pct_change().ewm(span=60).std()
        position = volatility_targeting(signal, volatility, target_vol)

        # Calculate asset returns
        next_ret = prices.pct_change().shift(-1)
        asset_returns[asset] = position * next_ret * (target_vol / volatility)

    # Equal-weighted portfolio
    portfolio = pd.DataFrame(asset_returns).mean(axis=1)

    return portfolio
```

## Best Practices

### DO:

✅ **Always use volatility targeting** for risk normalization
✅ **Calculate ex-ante volatility** using 60-day EWMA of returns
✅ **Use backward ratio-adjusted** continuous futures for consistent returns
✅ **Test on out-of-sample data** with expanding window approach
✅ **Monitor drawdowns** especially during regime changes
✅ **Use multiple timescales** to balance trend capture vs. responsiveness

### DON'T:

❌ **Don't assume Gaussian returns** - especially in tails
❌ **Don't ignore transaction costs** - they compound over time
❌ **Don't overfit to training period** - financial markets are non-stationary
❌ **Don't use look-ahead data** - ensure causality in backtests
❌ **Don't neglect correlation** in tail events across assets

## Key Formulas Reference

| Concept | Formula | Notes |
|---------|---------|-------|
| Returns | `r[t-t',t] = (p[t] - p[t-t']) / p[t-t']` | Simple returns over t' days |
| Normalized Returns | `r_hat[t-t',t] = r[t-t',t] / (σ[t] * sqrt(t'))` | For neural network inputs |
| Volatility Targeting | `leverage = σ_tgt / σ[t]` | Ex-ante vol σ[t] from 60-day EWMA |
| TSMOM Signal | `z[t] = sign(r[t-252,t])` | +1 for uptrend, -1 for downtrend |
| MACD | `(EWMA_S - EWMA_L) / std(m[-252:])` | Compare short/long EWMAs |
| Portfolio Return | `R_port = (1/N) * Σ R[i,t+1]` | Equal-weighted across N assets |
| Sharpe Ratio | `sqrt(252) * mean(R) / std(R)` | Annualized risk-adjusted returns |

## Related Concepts

- **Regime Change**: Sudden market condition shifts (e.g., COVID-19)
- **Momentum Crashes**: Rapid reversals causing losses
- **Factor Crowding**: Too many strategies trading same signals
- **Mean Reversion**: Price tendency to return to long-term mean
- **Commodity Trading Advisors (CTAs)**: Funds using trend-following

## References

- Time Series Momentum (Moskowitz, Ooi, Pedersen 2012)
- Deep Momentum Networks (Lim, Zohren, Roberts 2019)
- X-Trend: Few-Shot Learning Patterns (Wood, Kessler, Roberts, Zohren 2024)

---

**Last Updated**: Based on X-Trend paper (March 2024)
**Skill Type**: Domain Knowledge
**Line Count**: ~490 (under 500-line rule ✅)
