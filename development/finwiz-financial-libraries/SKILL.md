---
name: finwiz-financial-libraries
description: "Guides when to use financial libraries (TA-Lib, Empyrical, Backtrader) vs custom code for calculations, scoring, and business logic in FinWiz. Use when implementing financial calculations, technical indicators, risk metrics, or scoring systems."
allowed-tools: ["Read", "Edit", "Bash"]
---

# FinWiz Financial Libraries Strategy

When implementing financial calculations in FinWiz, follow this clear separation between **standard calculations** (use libraries) and **business logic** (custom code).

## Library vs Custom Code Decision Matrix

| Calculation Type | Use Library | Custom Code | Library Choice |
|------------------|-------------|-------------|----------------|
| **Technical Indicators** | ✅ | ❌ | TA-Lib (C-optimized, 200+ indicators) |
| **Risk Metrics** | ✅ | ❌ | Empyrical-Reloaded (Sharpe, drawdown, etc.) |
| **Backtesting** | ✅ | ❌ | Backtrader (industry standard) |
| **Scoring Thresholds** | ❌ | ✅ | FinWiz business logic |
| **Grading System** | ❌ | ✅ | Custom A+/A/B/C/D/F scale |
| **Fundamental Analysis** | ❌ | ✅ | Custom ROE/debt/growth thresholds |

## Implementation Patterns

### ✅ CORRECT: Library + Custom Scoring

```python
import talib
from empyrical import sharpe_ratio

# Library calculates the standard metric
rsi = talib.RSI(close_prices, timeperiod=14)
sharpe = sharpe_ratio(returns, risk_free=0.02)

# Custom code applies FinWiz business logic
if 40 <= rsi <= 60 and sharpe >= 1.5:
    recommendation = "BUY"  # FinWiz scoring logic
elif rsi > 70 or sharpe < 0.5:
    recommendation = "SELL"  # FinWiz scoring logic
else:
    recommendation = "HOLD"  # FinWiz scoring logic
```

### ❌ WRONG: Reimplementing Standard Calculations

```python
# DON'T DO THIS - TA-Lib already provides RSI
def calculate_rsi(prices, period=14):
    # Complex RSI implementation...
    # Use talib.RSI() instead!
```

## Key Libraries in FinWiz

### TA-Lib (Technical Analysis)

- **Use for**: RSI, MACD, Bollinger Bands, moving averages
- **Import**: `import talib`
- **Benefits**: C-optimized (100x faster), battle-tested

### Empyrical-Reloaded (Risk Metrics)

- **Use for**: Sharpe ratio, max drawdown, volatility, alpha/beta
- **Import**: `from empyrical import sharpe_ratio, max_drawdown`
- **Benefits**: Standard financial formulas, Quantopian-tested

### Backtrader (Backtesting)

- **Use for**: Strategy backtesting, portfolio simulation
- **Import**: `import backtrader as bt`
- **Benefits**: Industry standard, comprehensive framework

## Decision Framework

When implementing new financial calculations:

1. **Is this a standard calculation?**
   - YES → Use library (TA-Lib, Empyrical, Backtrader)
   - NO → Custom code

2. **Is this business logic/scoring?**
   - YES → Custom code (competitive advantage)
   - NO → Check if library exists

3. **Does a library exist?**
   - YES → Use the library
   - NO → Implement with proper documentation

## Current FinWiz Architecture

### What Uses Libraries (Calculations)

- Technical indicators: TA-Lib
- Risk metrics: Empyrical-Reloaded  
- Backtesting: Backtrader

### What Uses Custom Code (Business Logic)

- Scoring thresholds: "RSI 40-60 = score 1.0"
- Grading system: "Score >0.90 = A+"
- Asset-specific rules: ROE/debt thresholds

## Migration Strategy

### Current Custom Implementations to Migrate

Consider migrating these to Empyrical-Reloaded:

- Volatility calculation
- Maximum drawdown calculation
- Beta calculation

```python
# CURRENT (custom)
volatility = np.std(returns) * np.sqrt(252)

# FUTURE (Empyrical for calculation)
from empyrical import annual_volatility
volatility = annual_volatility(returns, period='daily')

# KEEP (custom scoring threshold)
if volatility <= 0.10:
    vol_score = 1.0  # FinWiz business logic
```

## Benefits of This Approach

### Libraries Provide

- **Performance**: C-optimized implementations
- **Correctness**: Battle-tested by thousands of users
- **Maintenance**: Automatic updates and bug fixes
- **Standards**: Industry-accepted formulas

### Custom Code Provides

- **Competitive Advantage**: Unique scoring methodology
- **Flexibility**: Easy threshold adjustments
- **Business Logic**: Domain-specific rules
- **Customization**: Per-asset-class logic

Remember: **Libraries** = Standard calculations, **Custom Code** = Business logic and scoring thresholds.
