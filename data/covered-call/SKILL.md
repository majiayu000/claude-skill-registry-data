---
name: covered-call
description: Implement covered call options strategy for income generation on long stock positions. Use when seeking to enhance returns through option premium collection while maintaining stock ownership. Covers structure, risk management, Greeks analysis, execution mechanics, and regulatory compliance for covered call writing programs.
---

# Covered Call Strategy

## Instructions

### Step 1: Verify Position Eligibility

Check that you own 100 shares (or multiples of 100) of the underlying stock. The covered call requires stock ownership as collateral for the short call.

### Step 2: Select Strike Price

Choose strike based on your outlook:

**Conservative (5-10% OTM)**:
- Select strike 5-10% above current price
- Target delta: 0.15-0.20
- Use when moderately bullish

**Moderate (2-5% OTM)**:
- Select strike 2-5% above current price
- Target delta: 0.25-0.35
- Use when neutral outlook

**Aggressive (ATM)**:
- Select strike at or near current price
- Target delta: 0.40-0.50
- Use when maximizing income

### Step 3: Select Expiration

Standard approach: 30-45 days to expiration for optimal theta decay.

Alternative approaches:
- Weekly (7 days): Maximum theta, requires active management
- Quarterly (60-90 days): Lower annualized cost, less management

### Step 4: Construct Position

```python
from scripts.strategy import CoveredCallStrategy, CoveredCallParameters

# Configure parameters
params = CoveredCallParameters(
    symbol='AAPL',
    stock_quantity=100,  # Must own shares
    strike_percent_otm=0.05,  # 5% OTM
    days_to_expiration=35,
    min_premium_yield=0.015  # 1.5% minimum monthly return
)

# Create strategy and construct position
strategy = CoveredCallStrategy(params)
position = strategy.construct_position(market_data, options_chain)
```

### Step 5: Execute Orders

**Option A - Sell Call Only** (if you already own stock):
```python
call_order = {
    'symbol': position['call_leg']['symbol'],
    'quantity': 1,
    'side': 'sell_to_open',
    'order_type': 'limit',
    'limit_price': position['call_leg']['limit_price']
}
```

**Option B - Buy-Write** (simultaneous stock purchase and call sale):
```python
combo_order = {
    'order_type': 'buy_write',
    'stock_quantity': 100,
    'call_quantity': 1,
    'net_debit': (stock_price - call_premium) * 100
}
```

### Step 6: Manage Position

**Monitor these conditions**:
- Days to expiration <7: Consider rolling
- Stock price >10% above strike: Consider rolling up
- Captured >80% of max profit: Consider rolling

**Rolling example**:
```python
from scripts.manager import CoveredCallManager

manager = CoveredCallManager(strategy)

if manager.should_roll(position, market_data, options_chain):
    roll = manager.execute_roll(
        position,
        market_data,
        options_chain,
        roll_type='up_and_out'  # or 'out', 'down_and_out'
    )
```

### Step 7: Handle Assignment (if applicable)

If stock price ≥ strike at expiration:
1. Stock automatically sold at strike price
2. You keep premium collected
3. Realize capital gain = (strike - purchase price) + premium
4. Decide whether to repurchase and repeat

## Examples

### Example 1: Conservative Monthly Income

**Scenario**: You own 100 shares of AAPL at $180, want conservative income.

**Action**:
```python
params = CoveredCallParameters(
    symbol='AAPL',
    stock_quantity=100,
    strike_percent_otm=0.08,  # 8% OTM = $194.40 strike
    days_to_expiration=35,
    delta_target=0.20  # Low delta = low assignment risk
)

strategy = CoveredCallStrategy(params)
position = strategy.construct_position(market_data, options_chain)
```

**Result**:
- Sell 1 AAPL call at $194.40 strike
- Collect $1.80 premium (1% monthly return)
- If AAPL <$194.40 at expiration: Keep stock, keep premium, repeat
- If AAPL ≥$194.40: Stock called away, profit = $14.40 + $1.80 = $16.20 (9% return)

### Example 2: Aggressive Income Generation

**Scenario**: You own 200 shares of MSFT at $370, prioritize income over upside.

**Action**:
```python
params = CoveredCallParameters(
    symbol='MSFT',
    stock_quantity=200,
    strike_percent_otm=0.02,  # 2% OTM = $377 strike
    days_to_expiration=30,
    delta_target=0.40  # Higher delta = more premium
)

strategy = CoveredCallStrategy(params)
position = strategy.construct_position(market_data, options_chain)
```

**Result**:
- Sell 2 MSFT calls at $377 strike
- Collect $11.00 premium (3% monthly return)
- Higher assignment probability but better income

### Example 3: Rolling Strategy

**Scenario**: Your AAPL $190 call is expiring in 5 days, stock at $188.

**Action**:
```python
from scripts.manager import CoveredCallManager

manager = CoveredCallManager(strategy)

# Check if should roll (5 days remaining triggers roll)
if manager.should_roll(position, market_data, options_chain):
    # Roll to next month, same strike
    roll = manager.execute_roll(
        position,
        market_data,
        options_chain,
        roll_type='out'  # Same strike, later expiration
    )

    # Result: Close current call, open new 35-day call at $190
    # Collect additional premium to continue strategy
```

### Example 4: Position Sizing

**Scenario**: $100,000 account, want diversified covered call portfolio.

**Action**:
```python
# Position sizing
account_value = 100_000
max_per_stock = 0.10  # 10% max per position
position_size = account_value * max_per_stock  # $10,000 per stock

# Can hold 10 positions of $10,000 each
# Example: 55 shares of AAPL at $180 = $9,900
# Write calls on multiples of 100, so either 0 or 100 shares

num_positions = 10
shares_per_position = 100  # Must be multiple of 100
stock_price = 100  # Target stocks around $100

# Result: 10 stocks × 100 shares each = $100,000 deployed
# Write 1 call per position = 10 covered calls total
```

### Example 5: Tax-Efficient Implementation

**Scenario**: You've held AAPL for 13 months, want to preserve long-term gains.

**Action**:
```python
# Ensure qualified covered call
params = CoveredCallParameters(
    symbol='AAPL',
    stock_quantity=100,
    strike_percent_otm=0.05,  # Not too deep ITM
    days_to_expiration=35,  # >30 days required
)

# Check qualification
holding_period_days = 390  # >365 days
expiration_days = 35  # >30 days
strike_appropriate = True  # Strike ≥95% of stock price

if all([holding_period_days > 365, expiration_days > 30, strike_appropriate]):
    # Qualified covered call - preserves long-term capital gains
    strategy = CoveredCallStrategy(params)
    position = strategy.construct_position(market_data, options_chain)
```

## When to Use This Strategy

**Use covered calls when**:
- You own stock and want to generate additional income
- Market outlook is neutral to moderately bullish
- Volatility is low to moderate (VIX 12-25)
- You're willing to sell stock if price reaches strike
- You want to reduce cost basis on existing holdings

**Avoid covered calls when**:
- Strong bullish breakout expected (capped upside hurts)
- Before major catalysts like earnings (unless capturing IV crush)
- You're unwilling to part with the stock at strike price
- High volatility with large moves expected

## Risk Management

**Key risks**:
1. **Capped upside**: Miss gains above strike price
2. **Full downside**: Premium only provides 2-5% cushion
3. **Assignment risk**: Early assignment possible before ex-dividend

**Mitigation strategies**:
1. Use stop-loss on stock (10-15% below entry)
2. Roll calls up if stock rallies significantly
3. Monitor ex-dividend dates, close ITM calls before
4. Diversify across 10+ positions
5. Size positions appropriately (max 10% per stock)

## Additional Resources

**For detailed formulas and analysis**:
- See [reference.md](reference.md) for complete Greeks analysis, P&L formulas, tax rules, and performance benchmarking

**For implementation code**:
- See [scripts/strategy.py](scripts/strategy.py) for position construction
- See [scripts/manager.py](scripts/manager.py) for rolling logic
- See [scripts/risk_monitor.py](scripts/risk_monitor.py) for risk assessment

## References

1. CBOE Options Institute - Covered Call Strategies
2. Hull, J. (2022). Options, Futures, and Other Derivatives
3. Natenberg, S. (1994). Option Volatility and Pricing
