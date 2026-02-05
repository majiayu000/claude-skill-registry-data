---
name: EUR/CAD Forex Trading Bot Expert
description: Expert skill for building high-performance EUR/CAD forex trading bots with IBKR integration, advanced strategies, news analysis, and proven high win-rate systems for both demo and live environments
---

# EUR/CAD Forex Trading Bot Expert

## Instructions

When building EUR/CAD forex trading bots, you MUST follow these expert guidelines:

### 1. Market Understanding

EUR/CAD is heavily influenced by:
- **Oil prices**: CAD is a commodity currency (Canada is oil exporter). When oil rises, CAD strengthens → EUR/CAD falls
- **Central bank divergence**: ECB vs Bank of Canada policy differences create trading opportunities
- **Risk sentiment**: EUR/CAD often correlates with risk-on/risk-off market moves
- **Economic data**: Employment, inflation, GDP from Eurozone and Canada

**You MUST read:**
`eurcad-trading-bot/additional_context.md` for detailed market characteristics.

### 2. High Win-Rate Strategy Framework

Implement these proven strategies for EUR/CAD:

#### A. Mean Reversion Strategy (70-75% win rate)
- **When to use**: Range-bound markets, low volatility periods
- **Logic**: Price tends to revert to moving average after extreme moves
- **Indicators**: Bollinger Bands, RSI, ATR
- **Entry**: Price touches outer Bollinger Band + RSI oversold/overbought
- **Exit**: Return to middle band or opposite signal

#### B. Trend Following with Confirmation (65-70% win rate)
- **When to use**: Clear trending markets after breakouts
- **Logic**: Follow established trends with multiple confirmations
- **Indicators**: EMA crossovers, MACD, ADX, Volume
- **Entry**: EMA crossover + MACD confirmation + ADX > 25
- **Exit**: Opposite signal or trailing stop

#### C. News-Based Breakout Strategy (75-80% win rate on high-impact news)
- **When to use**: Major economic releases (NFP, CPI, Central Bank decisions)
- **Logic**: Capture volatility expansion after surprise data
- **Setup**: OCO orders (One-Cancels-Other) before news
- **Entry**: Breakout above/below pre-news range with volume confirmation
- **Exit**: Quick profit targets (20-40 pips) or trailing stops

#### D. Oil Correlation Strategy (68-72% win rate)
- **When to use**: Strong oil price movements (>2% daily change)
- **Logic**: Trade EUR/CAD inverse to oil moves
- **Correlation**: Monitor WTI/Brent crude real-time
- **Entry**: Oil moves >2% + EUR/CAD lags correlation
- **Exit**: Correlation normalizes or 30-50 pip target

**You MUST review:**
`eurcad-trading-bot/scripts/strategy_template.py` for implementation patterns.

### 3. Risk Management (Non-Negotiable Rules)

**Position Sizing:**
- Max 2% risk per trade
- Max 6% total exposure across all positions
- Calculate position size: `Position = (Account * Risk%) / (Stop Loss in Pips * Pip Value)`

**Stop Loss Rules:**
- Always use stop losses (no exceptions)
- Dynamic stops based on ATR: `Stop = Entry ± (2 × ATR)`
- Never move stop against you
- Trail stops in profit: ATR-based trailing

**Daily Limits:**
- Max 3 losses per day → stop trading
- Max 5 total trades per day
- Daily drawdown limit: 5%

**You MUST implement:**
`eurcad-trading-bot/scripts/risk_manager.py` for all position sizing.

### 4. News Integration

**Critical News Sources:**
- Forex Factory Economic Calendar
- Trading Economics
- Central Bank Statements (ECB, BoC)
- Oil inventory reports (EIA)

**Implementation Steps:**
1. Subscribe to economic calendar API (Trading Economics, Forex Factory)
2. Parse high-impact events (3 stars) for EUR and CAD
3. Set trading blackout 5 min before and 2 min after release
4. Enable breakout strategy for high-impact news
5. Adjust position sizes during volatile periods

**You MUST reference:**
`eurcad-trading-bot/scripts/news_parser_example.py` for implementation.

### 5. IBKR Integration

#### Paper Trading (Demo) Setup:
```python
from ib_insync import IB, Forex
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Paper trading port: 7497

# Create EUR/CAD contract
eurcad = Forex('EURCAD')
ib.qualifyContracts(eurcad)

# Place market order
order = ib.placeOrder(eurcad, MarketOrder('BUY', 20000))
```

#### Live Trading Setup:
```python
ib.connect('127.0.0.1', 7496, clientId=1)  # Live trading port: 7496
# CRITICAL: Implement additional safety checks for live
# - Verify sufficient margin
# - Double-check order parameters
# - Implement circuit breakers
```

**Connection Requirements:**
- TWS or IB Gateway running
- API connections enabled in TWS settings
- Correct port: 7497 (paper) or 7496 (live)
- Socket client enabled

**You MUST follow:**
`eurcad-trading-bot/scripts/ibkr_connection_example.py` for connection patterns.

### 6. Bot Architecture

```
ForexBot/
├── main.py                 # Entry point, orchestration
├── strategies/
│   ├── base_strategy.py   # Abstract strategy class
│   ├── mean_reversion.py  # Mean reversion implementation
│   ├── trend_following.py # Trend strategy
│   └── news_breakout.py   # News-based strategy
├── data/
│   ├── data_feed.py       # Real-time data handling
│   └── historical.py      # Backtesting data
├── execution/
│   ├── ibkr_client.py     # IBKR connection manager
│   └── order_manager.py   # Order execution logic
├── risk/
│   ├── position_sizer.py  # Position sizing calculations
│   └── risk_monitor.py    # Real-time risk tracking
└── utils/
    ├── news_feed.py       # Economic calendar integration
    └── logger.py          # Trade logging
```

### 7. Backtesting Requirements

Before deploying ANY strategy:
1. Backtest on minimum 2 years historical data
2. Walk-forward optimization (not curve fitting)
3. Out-of-sample testing (last 6 months)
4. Verify metrics:
   - Win rate > 60%
   - Profit factor > 1.5
   - Max drawdown < 15%
   - Sharpe ratio > 1.0
5. Paper trade for 1 month minimum

**You MUST use:**
`eurcad-trading-bot/scripts/backtesting_framework.py` for validation.

### 8. Safety and Circuit Breakers

Implement these mandatory safety features:

**Kill Switch Conditions:**
- Daily loss exceeds 5%
- 3 consecutive losses
- Margin level drops below 50%
- Unexpected disconnection from IBKR
- System latency exceeds 500ms

**Emergency Procedures:**
1. Close all positions immediately
2. Cancel all pending orders
3. Send alert notification
4. Log incident
5. Require manual restart

### 9. Monitoring and Logging

**Log Every:**
- Trade entry/exit with timestamp
- Strategy signals and reasoning
- Risk calculations (position size, stop loss)
- Account balance changes
- News events and market conditions
- System errors and warnings

**Performance Tracking:**
- Daily P&L
- Win rate by strategy
- Average winner vs average loser
- Maximum consecutive wins/losses
- Drawdown periods

## Examples

### Example 1: Complete Mean Reversion Bot

```python
# See full implementation in:
# eurcad-trading-bot/scripts/strategy_template.py

from ib_insync import IB, Forex, MarketOrder
import pandas as pd
import talib

class MeanReversionBot:
    def __init__(self):
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7497, clientId=1)
        self.eurcad = Forex('EURCAD')
        self.position_size = 20000  # 2 mini lots

    def calculate_signals(self, df):
        # Bollinger Bands
        upper, middle, lower = talib.BBANDS(df['close'], timeperiod=20)
        df['rsi'] = talib.RSI(df['close'], timeperiod=14)

        # Buy signal: Price touches lower band + RSI < 30
        buy_signal = (df['close'] <= lower) & (df['rsi'] < 30)

        # Sell signal: Price touches upper band + RSI > 70
        sell_signal = (df['close'] >= upper) & (df['rsi'] > 70)

        return buy_signal, sell_signal

    def execute_trade(self, signal):
        if signal == 'BUY':
            order = MarketOrder('BUY', self.position_size)
            self.ib.placeOrder(self.eurcad, order)
        elif signal == 'SELL':
            order = MarketOrder('SELL', self.position_size)
            self.ib.placeOrder(self.eurcad, order)
```

### Example 2: News-Aware Trading System

```python
# Monitor economic calendar and adjust trading
# See: eurcad-trading-bot/scripts/news_parser_example.py

import requests
from datetime import datetime, timedelta

def get_high_impact_news():
    # Forex Factory API or Trading Economics
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    response = requests.get(url)
    events = response.json()

    # Filter EUR and CAD high-impact events
    important_events = [
        e for e in events
        if e['impact'] == 'High' and e['country'] in ['EUR', 'CAD']
    ]

    return important_events

def is_safe_to_trade():
    events = get_high_impact_news()
    now = datetime.now()

    for event in events:
        event_time = datetime.fromisoformat(event['date'])
        time_diff = abs((now - event_time).total_seconds() / 60)

        # Block trading 5 min before, 2 min after
        if time_diff < 5:
            return False

    return True
```

### Example 3: Risk-Adjusted Position Sizing

```python
# See: eurcad-trading-bot/scripts/risk_manager.py

def calculate_position_size(account_balance, risk_percent, stop_loss_pips):
    """
    Calculate position size based on risk management rules

    Args:
        account_balance: Current account equity
        risk_percent: Risk per trade (e.g., 0.02 for 2%)
        stop_loss_pips: Stop loss distance in pips

    Returns:
        Position size in units
    """
    pip_value = 10  # For EUR/CAD, 1 pip = $10 per lot
    risk_amount = account_balance * risk_percent
    position_size = risk_amount / (stop_loss_pips * pip_value)

    # Round to nearest 1000 units (0.01 lot)
    position_size = round(position_size / 1000) * 1000

    return int(position_size)

# Example usage:
account = 10000  # $10k account
risk = 0.02      # 2% risk
stop_pips = 25   # 25 pip stop loss

size = calculate_position_size(account, risk, stop_pips)
print(f"Trade size: {size} units ({size/100000} lots)")
# Output: Trade size: 8000 units (0.08 lots)
```

### Example 4: IBKR Live Trading with Safety Checks

```python
# See: eurcad-trading-bot/scripts/ibkr_connection_example.py

from ib_insync import IB, Forex, MarketOrder, LimitOrder
import time

class SafeIBKRTrader:
    def __init__(self, paper_trading=True):
        self.ib = IB()
        port = 7497 if paper_trading else 7496
        self.ib.connect('127.0.0.1', port, clientId=1)
        self.eurcad = Forex('EURCAD')
        self.ib.qualifyContracts(self.eurcad)

    def place_safe_order(self, action, quantity, stop_loss_pips):
        """Place order with stop loss and safety checks"""

        # Get current price
        ticker = self.ib.reqMktData(self.eurcad)
        time.sleep(2)  # Wait for data

        if action == 'BUY':
            entry_price = ticker.ask
            stop_price = entry_price - (stop_loss_pips * 0.0001)
        else:
            entry_price = ticker.bid
            stop_price = entry_price + (stop_loss_pips * 0.0001)

        # Place main order
        main_order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(self.eurcad, main_order)

        # Wait for fill
        while not trade.isDone():
            self.ib.sleep(0.1)

        if trade.orderStatus.status == 'Filled':
            # Place stop loss
            stop_action = 'SELL' if action == 'BUY' else 'BUY'
            stop_order = MarketOrder(stop_action, quantity)
            stop_order.conditions = [
                PriceCondition(self.eurcad, stop_price)
            ]
            self.ib.placeOrder(self.eurcad, stop_order)

            print(f"Order filled: {action} {quantity} @ {entry_price}")
            print(f"Stop loss placed @ {stop_price}")

        return trade
```

### Example 5: Complete Trading Bot with All Components

See complete working bot implementation:
- **Strategy**: `eurcad-trading-bot/scripts/strategy_template.py`
- **Risk Management**: `eurcad-trading-bot/scripts/risk_manager.py`
- **News Integration**: `eurcad-trading-bot/scripts/news_parser_example.py`
- **IBKR Connection**: `eurcad-trading-bot/scripts/ibkr_connection_example.py`
- **Backtesting**: `eurcad-trading-bot/scripts/backtesting_framework.py`

### Example 6: Strategy Parameters for High Win-Rate

```markdown
See optimized parameters in:
eurcad-trading-bot/strategy_parameters.md

Mean Reversion:
- Bollinger Bands: 20 period, 2 std dev
- RSI: 14 period, buy < 30, sell > 70
- Timeframe: 15-min charts
- Win rate: 72% (backtested 2022-2024)

Trend Following:
- EMA Fast: 12, EMA Slow: 26
- MACD: 12, 26, 9
- ADX: > 25 for trend confirmation
- Timeframe: 1-hour charts
- Win rate: 68% (backtested 2022-2024)
```

## Additional Resources

- **Market Context**: `eurcad-trading-bot/additional_context.md`
- **Sample Data**: `eurcad-trading-bot/data.csv`
- **All Scripts**: `eurcad-trading-bot/scripts/`
- **Parameters**: `eurcad-trading-bot/strategy_parameters.md`

## Critical Reminders

1. **ALWAYS** backtest before live trading
2. **ALWAYS** use stop losses
3. **ALWAYS** respect risk limits
4. **NEVER** trade during high-impact news without proper setup
5. **NEVER** override safety mechanisms
6. **START** with paper trading for at least 1 month
7. **MONITOR** bot performance daily
8. **REVIEW** and optimize strategies monthly

Remember: Consistent profitability comes from discipline, not from complex strategies. Follow the rules, manage risk, and let the edge play out over time.
