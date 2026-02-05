---
name: symbol-selection-statistical
description: "Statistical analysis for selecting trading symbols compatible with mean-reversion/momentum strategies, GARCH risk models, and Markov regime detection"
author: Claude Code
date: 2025-12-12
---

# Symbol Selection Statistical Analysis - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-12 |
| **Goal** | Create sophisticated symbol selection using Hurst exponent, half-life, GARCH quality, and regime persistence to find assets compatible with predator-prey Markov trading systems |
| **Environment** | Python 3.10+, numpy, pandas, scipy, arch, hmmlearn (optional) |
| **Status** | Success |

## Context
Simple Sharpe/momentum/volatility screening is insufficient for selecting symbols compatible with advanced trading systems that use:
- Predator-prey Markov regime detection (needs clear regime separation)
- GARCH-based position sizing (needs good volatility model fit)
- Mean-reversion strategies (needs appropriate half-life for trading timeframe)

Literature review identified key statistical metrics that predict trading compatibility better than traditional metrics.

## Verified Workflow

### 1. Hurst Exponent Analysis
Determines mean-reverting (H<0.5) vs trending (H>0.5) behavior.

```python
def calculate_hurst_dfa(prices, max_lag=100):
    """Detrended Fluctuation Analysis for Hurst exponent."""
    returns = prices.pct_change().dropna()
    y = (returns - returns.mean()).cumsum()

    scales = np.unique(np.logspace(1, np.log10(max_lag), 20).astype(int))
    fluctuations = []

    for scale in scales:
        n_segments = len(y) // scale
        f_list = []
        for i in range(n_segments):
            segment = y.iloc[i * scale:(i + 1) * scale].values
            # Detrend with linear fit
            x = np.arange(len(segment))
            coeffs = np.polyfit(x, segment, 1)
            trend = np.polyval(coeffs, x)
            detrended = segment - trend
            f = np.sqrt(np.mean(detrended ** 2))
            f_list.append(f)
        if f_list:
            fluctuations.append((scale, np.mean(f_list)))

    # Linear regression: log(F) = H * log(n) + c
    log_scales = np.log([x[0] for x in fluctuations])
    log_fluct = np.log([x[1] for x in fluctuations])
    hurst = np.polyfit(log_scales, log_fluct, 1)[0]
    return np.clip(hurst, 0, 1)
```

**Key insight**: Use BOTH short-term (window=50) and long-term (window=200) Hurst. Ideal symbols show:
- Short-term H < 0.45 (mean-reverting for VWAP reversion)
- Long-term H > 0.55 (trending for momentum continuation)

### 2. Half-Life of Mean Reversion (Ornstein-Uhlenbeck)

```python
def calculate_half_life(prices):
    """Half-life using OU process: dP = theta(mu - P)dt"""
    price_lag = prices.shift(1).dropna()
    price_diff = prices.diff().dropna()

    # Align and regress: dP = alpha + beta*P(t-1)
    X = np.column_stack([np.ones(len(price_lag)), price_lag.values])
    y = price_diff.values[:len(price_lag)]
    coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
    beta = coeffs[1]

    if beta >= 0:  # Not mean-reverting
        return float('inf')

    # half_life = -ln(2) / ln(1 + beta)
    half_life = -np.log(2) / np.log(1 + beta)
    return half_life
```

**Target half-life for hourly trading**: 4-24 hours
- < 1 hour: Too fast, transaction costs dominate
- > 72 hours: Capital tied up too long

### 3. GARCH Fit Quality Scoring

```python
from arch import arch_model

def score_garch_fit(returns):
    """Score GARCH(1,1) fit quality."""
    model = arch_model(returns * 100, vol='Garch', p=1, q=1, mean='Zero')
    result = model.fit(disp='off')

    alpha = result.params.get('alpha[1]', 0)
    beta = result.params.get('beta[1]', 0)
    persistence = alpha + beta

    # Check stationarity
    is_stationary = persistence < 0.9999

    # Score components
    score = 0.0
    if is_stationary:
        score += 0.20
    if 0.01 < alpha < 0.30 and 0.50 < beta < 0.95:
        score += 0.20
    # Add Ljung-Box and ARCH-LM test scores...

    return score, persistence
```

**Good GARCH fit requires**:
- Persistence (alpha + beta) between 0.90-0.97
- No remaining autocorrelation in residuals (Ljung-Box p > 0.05)
- No remaining ARCH effects (ARCH-LM p > 0.05)

### 4. Regime Persistence (HMM)

```python
from hmmlearn import hmm

def calculate_regime_persistence(returns, n_regimes=2):
    """Measure regime duration using Hidden Markov Model."""
    model = hmm.GaussianHMM(n_components=n_regimes, covariance_type="full")
    model.fit(returns.values.reshape(-1, 1))

    states = model.predict(returns.values.reshape(-1, 1))
    transmat = model.transmat_

    # Calculate average regime duration
    durations = []
    current_duration = 1
    for i in range(1, len(states)):
        if states[i] == states[i-1]:
            current_duration += 1
        else:
            durations.append(current_duration)
            current_duration = 1

    return np.mean(durations), transmat
```

**Target regime duration**: 5-20 bars (hours)
- Enough time to identify and trade the regime
- Self-transition probability 0.85-0.95 (sticky but not too persistent)

### 5. Weighted Composite Scoring

```python
weights = {
    'hurst_short': 0.20,   # Mean reversion at short timeframes
    'hurst_long': 0.15,    # Trending at long timeframes
    'half_life': 0.15,     # Appropriate reversion speed
    'garch': 0.15,         # Volatility modelability
    'regime': 0.10,        # Regime persistence
    'autocorr': 0.10,      # Return predictability
    'sharpe': 0.10,        # Risk-adjusted returns
    'drawdown': 0.05,      # Drawdown risk
}  # Sum = 1.0
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using only Sharpe ratio | High-Sharpe assets often had poor GARCH fit, unpredictable volatility | Traditional metrics don't predict model compatibility |
| Single-scale Hurst | Missed dual-behavior assets (MR short-term + trending long-term) | Always calculate multi-scale Hurst |
| `max_lag` parameter for Hurst | Function signature used `window` not `max_lag` | Check function signatures carefully |
| Entropy calculation with 1 off-diagonal | `log(1) = 0` caused division by zero, yielding negative scores | Handle edge case: single transition = deterministic = score 1.0 |
| Requiring hmmlearn | Package not always available | Implement fallback using simple volatility-based regime detection |
| Half-life on returns | Should use prices for OU regression | Use price series, not returns |
| Ignoring correlation in portfolio | Selected highly correlated assets | Always filter by max correlation (0.6-0.7 threshold) |

## Final Parameters

```yaml
# Selection Configuration
hurst_short_target: [0.30, 0.50]  # Mean-reverting
hurst_long_target: [0.50, 0.70]   # Trending
half_life_target_hours: [4.0, 24.0]
min_garch_score: 0.5
regime_duration_target: [5, 20]  # bars
max_correlation: 0.60
min_data_points: 500
min_price: 5.0
min_avg_volume: 500000

# Scoring Weights (must sum to 1.0)
hurst_short_weight: 0.20
hurst_long_weight: 0.15
half_life_weight: 0.15
garch_weight: 0.15
regime_weight: 0.10
autocorr_weight: 0.10
sharpe_weight: 0.10
drawdown_weight: 0.05
```

## Key Insights

- **Dual-behavior is key**: The best trading symbols show mean-reversion at short timeframes AND momentum at longer timeframes. This supports both VWAP reversion and trend-following.

- **Half-life must match trading frequency**: For hourly trading, 4-24 hour half-life is ideal. Too fast = noise, too slow = capital inefficiency.

- **GARCH fit predicts position sizing accuracy**: Poor GARCH fit means unreliable volatility forecasts, leading to incorrect position sizes.

- **Regime persistence matters for Markov models**: Regimes should last 5-20 bars - long enough to identify but short enough to see transitions.

- **DFA > R/S for Hurst**: Detrended Fluctuation Analysis is more robust to non-stationarity than Rescaled Range method.

- **Fallback implementations are essential**: Not all environments have hmmlearn/arch packages. Implement EWMA-based fallbacks.

- **Correlation filtering prevents over-concentration**: Even high-scoring symbols should be filtered to maintain diversification.

## References

- Hurst, H.E. (1951). "Long-term storage capacity of reservoirs"
- Peng, C.K. et al. (1994). "Mosaic organization of DNA nucleotides" - DFA method
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity" - GARCH
- Rabiner, L.R. (1989). "A tutorial on hidden Markov models" - HMM regime detection
- Avellaneda & Lee (2010). "Statistical Arbitrage in the US Equities Market" - Half-life trading
