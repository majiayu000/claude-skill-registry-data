---
name: "technical-indicator"
description: "Use this skill ONLY when adding a new technical indicator (e.g., Bollinger Bands, Stochastic, ATR). Do not use for strategies or agents."
---

# Scope Constraint

**CRITICAL:** You are executing from the repository root.

- Technical indicators go in `src/alpacalyzer/analysis/technical_analysis.py`
- Tests go in `tests/test_technical_analysis.py`
- This module uses TA-Lib extensively

# Technical Analysis Overview

The `TechnicalAnalyzer` class calculates various indicators and aggregates them into trading signals. All indicator functions are methods of this class.

# Procedural Steps

## 1. Review Existing Indicators

```bash
# See existing indicator implementations
cat src/alpacalyzer/analysis/technical_analysis.py

# See how indicators are tested
cat tests/test_technical_analysis.py
```

**Key patterns**:

- Indicators use TA-Lib where available
- Functions return both values and interpretation (bullish/bearish/neutral)
- Error handling for insufficient data
- Indicators are called by `analyze_ticker()` method

## 2. Check TA-Lib Availability

Many indicators are already implemented in TA-Lib. Check first:

```python
import talib

# See available functions
print(dir(talib))

# Example: RSI is available
# rsi = talib.RSI(close_prices, timeperiod=14)
```

**If indicator exists in TA-Lib**: Use it directly.
**If not**: Implement from scratch using pandas/numpy.

## 3. Add Indicator Method

**Location**: `src/alpacalyzer/analysis/technical_analysis.py`

**Template for TA-Lib indicator**:

```python
def calculate_<indicator>(self, ticker: str, period: int = 14) -> dict:
    """
    Calculate <Indicator Name> for ticker.

    <Brief description of indicator and what it measures>

    Args:
        ticker: Stock ticker symbol
        period: Lookback period (default: 14)

    Returns:
        Dict with:
            - value: Current indicator value
            - signal: "bullish", "bearish", or "neutral"
            - description: Human-readable interpretation
    """
    try:
        # Fetch price data
        data = self.get_price_data(ticker, days=max(period * 2, 30))

        if data is None or len(data) < period:
            return {
                "value": None,
                "signal": "neutral",
                "description": "Insufficient data"
            }

        # Calculate using TA-Lib
        close_prices = data['Close'].values
        indicator_values = talib.<INDICATOR_FUNCTION>(close_prices, timeperiod=period)
        current_value = indicator_values[-1]

        # Interpret signal
        if <bullish_condition>:
            signal = "bullish"
            description = "<Bullish interpretation>"
        elif <bearish_condition>:
            signal = "bearish"
            description = "<Bearish interpretation>"
        else:
            signal = "neutral"
            description = "<Neutral interpretation>"

        return {
            "value": current_value,
            "signal": signal,
            "description": description
        }

    except Exception as e:
        logger.error(f"Error calculating <indicator> for {ticker}: {e}")
        return {
            "value": None,
            "signal": "neutral",
            "description": f"Error: {str(e)}"
        }
```

**Template for custom indicator**:

```python
def calculate_<indicator>(self, ticker: str, period: int = 20) -> dict:
    """
    Calculate <Indicator Name> for ticker.

    <Mathematical formula or description>

    Args:
        ticker: Stock ticker symbol
        period: Lookback period (default: 20)

    Returns:
        Dict with value, signal, description
    """
    try:
        data = self.get_price_data(ticker, days=max(period * 2, 30))

        if data is None or len(data) < period:
            return {
                "value": None,
                "signal": "neutral",
                "description": "Insufficient data"
            }

        # Custom calculation using pandas/numpy
        # Example: Simple Moving Average
        # sma = data['Close'].rolling(window=period).mean()
        # current_value = sma.iloc[-1]

        # Your calculation here
        current_value = self._calculate_custom_indicator(data, period)

        # Interpret signal
        signal, description = self._interpret_<indicator>(current_value, data)

        return {
            "value": current_value,
            "signal": signal,
            "description": description
        }

    except Exception as e:
        logger.error(f"Error calculating <indicator> for {ticker}: {e}")
        return {
            "value": None,
            "signal": "neutral",
            "description": f"Error: {str(e)}"
        }

    def _calculate_custom_indicator(self, data: pd.DataFrame, period: int) -> float:
        """Helper to calculate indicator value."""
        # Implementation
        pass

    def _interpret_<indicator>(self, value: float, data: pd.DataFrame) -> tuple[str, str]:
        """Helper to interpret indicator signal."""
        # Return (signal, description)
        pass
```

## 4. Integrate with analyze_ticker()

Add your indicator to the main analysis method:

```python
def analyze_ticker(self, ticker: str) -> TradingSignals:
    """Analyze ticker with all indicators."""
    # ... existing code ...

    # Add your indicator
    <indicator>_result = self.calculate_<indicator>(ticker)

    # Include in signals list if applicable
    if <indicator>_result["signal"] == "bullish":
        signals.append(f"<Indicator>: {<indicator>_result['description']}")
    elif <indicator>_result["signal"] == "bearish":
        signals.append(f"<Indicator> Bearish: {<indicator>_result['description']}")

    # Add to overall score calculation if appropriate
    if <indicator>_result["signal"] == "bullish":
        total_score += 1
        positive_signals += 1
    elif <indicator>_result["signal"] == "bearish":
        total_score -= 1

    # ... rest of analysis ...
```

## 5. Write Tests

**Location**: `tests/test_technical_analysis.py`

**Test template**:

```python
def test_calculate_<indicator>_bullish(technical_analyzer):
    """Test <indicator> calculation with bullish signal."""

    # Create mock data with bullish pattern
    dates = pd.date_range(end=pd.Timestamp.now(), periods=50, freq='D')
    # Create price data that should trigger bullish signal
    close_prices = np.linspace(100, 120, 50)  # Uptrend

    mock_data = pd.DataFrame({
        'Close': close_prices,
        'High': close_prices * 1.02,
        'Low': close_prices * 0.98,
        'Open': close_prices * 0.99,
        'Volume': np.random.randint(1000000, 5000000, 50)
    }, index=dates)

    # Mock data fetching
    technical_analyzer.get_price_data = lambda ticker, days: mock_data

    # Calculate indicator
    result = technical_analyzer.calculate_<indicator>("AAPL")

    # Assertions
    assert result is not None
    assert "value" in result
    assert "signal" in result
    assert "description" in result
    assert result["signal"] in ["bullish", "bearish", "neutral"]

    # Value should be calculated
    if result["value"] is not None:
        assert isinstance(result["value"], (int, float))


def test_calculate_<indicator>_bearish(technical_analyzer):
    """Test <indicator> calculation with bearish signal."""

    dates = pd.date_range(end=pd.Timestamp.now(), periods=50, freq='D')
    # Create price data that should trigger bearish signal
    close_prices = np.linspace(120, 100, 50)  # Downtrend

    mock_data = pd.DataFrame({
        'Close': close_prices,
        'High': close_prices * 1.02,
        'Low': close_prices * 0.98,
        'Open': close_prices * 0.99,
        'Volume': np.random.randint(1000000, 5000000, 50)
    }, index=dates)

    technical_analyzer.get_price_data = lambda ticker, days: mock_data

    result = technical_analyzer.calculate_<indicator>("AAPL")

    assert result is not None
    assert result["signal"] in ["bullish", "bearish", "neutral"]


def test_calculate_<indicator>_insufficient_data(technical_analyzer):
    """Test <indicator> handles insufficient data gracefully."""

    # Very short data series
    dates = pd.date_range(end=pd.Timestamp.now(), periods=5, freq='D')
    close_prices = [100, 101, 102, 103, 104]

    mock_data = pd.DataFrame({
        'Close': close_prices,
    }, index=dates)

    technical_analyzer.get_price_data = lambda ticker, days: mock_data

    result = technical_analyzer.calculate_<indicator>("AAPL", period=20)

    # Should return neutral with insufficient data message
    assert result["signal"] == "neutral"
    assert "insufficient" in result["description"].lower()


def test_calculate_<indicator>_handles_errors(technical_analyzer):
    """Test <indicator> handles errors gracefully."""

    # Mock data fetching to return None (simulating API failure)
    technical_analyzer.get_price_data = lambda ticker, days: None

    result = technical_analyzer.calculate_<indicator>("AAPL")

    # Should not raise exception, return neutral
    assert result is not None
    assert result["signal"] == "neutral"


def test_<indicator>_integration_in_analyze_ticker(technical_analyzer):
    """Test <indicator> is included in full ticker analysis."""

    # Mock price data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='D')
    close_prices = np.linspace(100, 120, 100)

    mock_data = pd.DataFrame({
        'Close': close_prices,
        'High': close_prices * 1.02,
        'Low': close_prices * 0.98,
        'Open': close_prices * 0.99,
        'Volume': np.random.randint(1000000, 5000000, 100)
    }, index=dates)

    technical_analyzer.get_price_data = lambda ticker, days: mock_data

    # Run full analysis
    signals = technical_analyzer.analyze_ticker("AAPL")

    # Check indicator is included in signals
    # (Exact assertion depends on your implementation)
    assert signals is not None
    assert "signals" in signals
```

## 6. Run Tests

```bash
# Run specific indicator tests
uv run pytest tests/test_technical_analysis.py::test_calculate_<indicator>_bullish -v

# Run all technical analysis tests
uv run pytest tests/test_technical_analysis.py -v

# Check coverage
uv run pytest tests/test_technical_analysis.py --cov=src/alpacalyzer/analysis/technical_analysis
```

## 7. Document Indicator

Add documentation in the indicator method docstring:

```python
def calculate_<indicator>(self, ticker: str, period: int = 14) -> dict:
    """
    Calculate <Indicator Name> for ticker.

    <Detailed description>

    Interpretation:
        - Bullish: <when considered bullish>
        - Bearish: <when considered bearish>
        - Neutral: <when considered neutral>

    Formula:
        <Mathematical formula if applicable>

    Args:
        ticker: Stock ticker symbol
        period: Lookback period (default: 14)

    Returns:
        Dict with:
            - value: Current indicator value (float or None)
            - signal: "bullish", "bearish", or "neutral"
            - description: Human-readable interpretation

    Example:
        >>> ta = TechnicalAnalyzer()
        >>> result = ta.calculate_<indicator>("AAPL")
        >>> print(result['signal'])
        'bullish'
    """
```

# Reference: Existing Indicators

The following indicators are already implemented:

| Indicator       | Method                        | TA-Lib Function          |
| --------------- | ----------------------------- | ------------------------ |
| RSI             | `calculate_rsi()`             | `talib.RSI`              |
| MACD            | `calculate_macd()`            | `talib.MACD`             |
| Moving Averages | `calculate_moving_averages()` | `talib.SMA`, `talib.EMA` |
| Bollinger Bands | `calculate_bollinger_bands()` | `talib.BBANDS`           |
| ADX             | `calculate_adx()`             | `talib.ADX`              |
| Stochastic      | `calculate_stochastic()`      | `talib.STOCH`            |

See `src/alpacalyzer/analysis/technical_analysis.py` for implementations.

# Special Considerations

1. **TA-Lib Requirement**: TA-Lib requires system library installation. CI workflows handle this.

2. **Data Requirements**: Indicators need sufficient historical data. Use `max(period * 2, 30)` days minimum.

3. **Error Handling**: Always handle insufficient data and API failures gracefully. Return neutral signal on errors.

4. **Signal Interpretation**: Be conservative with bullish/bearish signals. When in doubt, return neutral.

5. **Performance**: Indicator calculations can be expensive. Consider caching results if used frequently.

6. **Integration**: Not all indicators need to be included in `analyze_ticker()`. Some may be reference-only.

## Example: Bollinger Bands

```python
def calculate_bollinger_bands(self, ticker: str, period: int = 20) -> dict:
    """
    Calculate Bollinger Bands for ticker.

    Bollinger Bands consist of:
    - Middle band: 20-period SMA
    - Upper band: Middle + (2 * standard deviation)
    - Lower band: Middle - (2 * standard deviation)

    Interpretation:
        - Bullish: Price near lower band (oversold)
        - Bearish: Price near upper band (overbought)
        - Neutral: Price near middle band
    """
    try:
        data = self.get_price_data(ticker, days=max(period * 2, 30))

        if data is None or len(data) < period:
            return {"value": None, "signal": "neutral", "description": "Insufficient data"}

        close_prices = data['Close'].values

        # Calculate Bollinger Bands using TA-Lib
        upper, middle, lower = talib.BBANDS(
            close_prices,
            timeperiod=period,
            nbdevup=2,
            nbdevdn=2,
            matype=0  # Simple moving average
        )

        current_price = close_prices[-1]
        current_upper = upper[-1]
        current_lower = lower[-1]
        current_middle = middle[-1]

        # Calculate position within bands (0 = lower, 1 = upper)
        band_width = current_upper - current_lower
        position = (current_price - current_lower) / band_width if band_width > 0 else 0.5

        # Interpret
        if position < 0.2:
            signal = "bullish"
            description = f"Price near lower band (oversold): ${current_price:.2f} vs ${current_lower:.2f}"
        elif position > 0.8:
            signal = "bearish"
            description = f"Price near upper band (overbought): ${current_price:.2f} vs ${current_upper:.2f}"
        else:
            signal = "neutral"
            description = f"Price within bands: ${current_lower:.2f} < ${current_price:.2f} < ${current_upper:.2f}"

        return {
            "value": {
                "upper": current_upper,
                "middle": current_middle,
                "lower": current_lower,
                "position": position
            },
            "signal": signal,
            "description": description
        }

    except Exception as e:
        logger.error(f"Error calculating Bollinger Bands for {ticker}: {e}")
        return {"value": None, "signal": "neutral", "description": f"Error: {str(e)}"}
```
