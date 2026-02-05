---
name: married-put-strategy
description: Analyzes and implements married-put options strategies for portfolio protection. Calculates breakeven points, profit/loss scenarios, and compares strike prices (ITM, ATM, OTM) across multiple expiration cycles. Use when protecting stock positions, analyzing downside insurance costs, or evaluating protective put options for small to mid-cap holdings.
---

# Married-Put Strategy

A married-put strategy provides downside protection for stock holdings by purchasing put options as insurance against price declines while maintaining unlimited upside potential.

## Strategy Overview

**Definition**: Buy (or own) 100 shares of stock + Buy 1 put option contract

**Key Characteristics**:
- **Maximum Loss**: Limited to stock purchase price minus put strike price, plus net premium paid
- **Maximum Gain**: Unlimited (stock can rise indefinitely)
- **Breakeven**: Stock price at purchase + net premium paid
- **Best Use**: Protecting newly acquired positions or holdings during uncertain periods

**Cost Components**:
- Stock purchase: Number of shares × stock price
- Put premium: Option price × 100 shares
- Transaction cost: $0.65 per option contract

## Quick Start

Calculate married-put metrics for a position:

```python
from scripts.married_put_calculator import MarriedPut

# Create position: 100 shares at $45, put strike $43, premium $2.10
position = MarriedPut(
    stock_price=45.00,
    shares=100,
    put_strike=43.00,
    put_premium=2.10,
    transaction_cost=0.65
)

# Calculate key metrics
print(f"Breakeven: ${position.breakeven_price:.2f}")
print(f"Max Loss: ${position.max_loss:.2f}")
print(f"Total Cost: ${position.total_cost:.2f}")
print(f"Protection Level: {position.protection_percentage:.1f}%")
```

## Strike Price Comparison

Compare ITM, ATM, and OTM puts to optimize cost vs. protection:

```python
from scripts.strike_comparison import compare_strike_prices

# Compare different strike prices for AAPL position
results = compare_strike_prices(
    stock_price=175.50,
    shares=100,
    strike_prices=[165, 170, 175, 180],  # OTM to ITM
    premiums=[2.30, 3.85, 6.10, 9.45],
    days_to_expiration=45
)

# View comparison table
print(results.to_dataframe())
```

**Strike Selection Guidelines**:
- **OTM Puts** (strike < stock price): Lower cost, reduced protection
  - Best for: High-conviction positions, cost-conscious protection
  - Typical protection: 5-10% below current price

- **ATM Puts** (strike ≈ stock price): Balanced cost and protection
  - Best for: Standard hedging, moderate risk tolerance
  - Typical protection: Current price level

- **ITM Puts** (strike > stock price): Higher cost, maximum protection
  - Best for: Maximum downside protection, risk-averse strategies
  - Typical protection: Locks in guaranteed minimum exit price

## Expiration Cycle Analysis

Evaluate 30-day, 60-day, and 90-day options:

```python
from scripts.expiration_analysis import compare_expirations

# Compare different expiration cycles
analysis = compare_expirations(
    stock_price=52.75,
    shares=100,
    put_strike=50.00,
    premiums_30d=1.85,
    premiums_60d=2.95,
    premiums_90d=3.85
)

print(f"30-day: ${analysis['monthly_cost_30d']:.2f}/month")
print(f"60-day: ${analysis['monthly_cost_60d']:.2f}/month")
print(f"90-day: ${analysis['monthly_cost_90d']:.2f}/month")
```

**Expiration Selection Criteria**:
- **30-day**: Lowest total premium, highest monthly cost, frequent rolling required
- **60-day**: Balanced cost/maintenance, moderate time decay
- **90-day**: Highest total premium, lowest monthly cost, reduced transaction frequency

## Position Sizing

For positions $5,000 to $50,000:

```python
from scripts.position_sizer import calculate_position_size

# Determine optimal position size with protection
position_params = calculate_position_size(
    capital_available=25000,
    stock_price=48.25,
    put_premium=2.15,
    max_position_pct=0.40  # Maximum 40% of capital
)

print(f"Recommended shares: {position_params['shares']}")
print(f"Put contracts: {position_params['contracts']}")
print(f"Total investment: ${position_params['total_cost']:.2f}")
print(f"Remaining capital: ${position_params['remaining']:.2f}")
```

## Profit/Loss Analysis

Calculate P/L at various stock prices:

```python
# Generate P/L table
position = MarriedPut(stock_price=45.00, shares=100,
                      put_strike=43.00, put_premium=2.10)

# Calculate P/L at different price points
price_points = [35, 40, 43, 45, 50, 55, 60]
for price in price_points:
    pl = position.calculate_pl_at_price(price)
    print(f"Stock at ${price}: P/L = ${pl:.2f}")
```

## Visualization

Generate payoff diagram:

```python
from scripts.visualizations import plot_married_put_payoff

# Create payoff diagram
plot_married_put_payoff(
    stock_price=45.00,
    put_strike=43.00,
    put_premium=2.10,
    price_range=(30, 60),
    save_path="married_put_diagram.png"
)
```

## Real-World Examples

Five example positions with varying volatility levels:

**Low Volatility (15-20% IV)**:
- Large-cap, stable companies
- Lower premium costs
- Suitable for conservative protection

**Medium Volatility (25-35% IV)**:
- Mid-cap growth stocks
- Moderate premium costs
- Standard hedging scenarios

**High Volatility (40-60% IV)**:
- Small-cap or volatile stocks
- Higher premium costs
- Aggressive protection needed

See [examples/sample_positions.csv](examples/sample_positions.csv) for detailed scenarios.

## Advanced Analysis

For detailed Greeks calculations, volatility analysis, and advanced scenarios:

See [reference.md](reference.md) for:
- Greeks (Delta, Gamma, Theta, Vega) calculations
- Implied volatility impact
- Rolling strategies
- Tax implications
- Break-even analysis across time

## Usage Workflow

1. **Identify Position**: Determine stock, shares, and capital allocation
2. **Analyze Strikes**: Compare ITM/ATM/OTM protection levels
3. **Select Expiration**: Choose 30/60/90-day based on cost and maintenance
4. **Calculate Metrics**: Compute breakeven, max loss, total cost
5. **Visualize Payoff**: Generate diagram to confirm risk profile
6. **Execute Trade**: Place stock and put orders simultaneously
7. **Monitor Position**: Track P/L and plan for put expiration/rolling

## Risk Considerations

**Advantages**:
- Defined maximum loss
- Unlimited profit potential
- Known upfront cost
- Psychological comfort in volatile markets

**Disadvantages**:
- Reduces overall returns by premium amount
- Time decay erodes put value
- May encourage holding losing positions
- Transaction costs on frequent rolling

**Best For**:
- New positions in uncertain markets
- Protecting unrealized gains
- Risk-averse investors
- Compliance with mandate risk limits

## Required Dependencies

```
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
scipy>=1.10.0
```

See [requirements.txt](requirements.txt) for complete list.

## Quick Reference

| Metric | Calculation |
|--------|-------------|
| Total Cost | (Stock Price × Shares) + (Put Premium × 100) + Transaction Cost |
| Breakeven | Stock Price + (Put Premium + Transaction Cost/100) |
| Max Loss | Stock Price - Put Strike + Put Premium + Transaction Cost/100 |
| Protection % | (Stock Price - Put Strike) / Stock Price × 100 |
| ROI at Expiry | (Final Stock Price - Stock Price - Put Premium) / Total Cost × 100 |

## File Organization

```
married-put-strategy/
├── SKILL.md                    # Main documentation (this file)
├── reference.md                # Advanced Greeks and analysis
├── requirements.txt            # Python dependencies
├── scripts/
│   ├── married_put_calculator.py    # Core calculations
│   ├── strike_comparison.py         # Compare strike prices
│   ├── expiration_analysis.py       # Compare expiration cycles
│   ├── position_sizer.py            # Position sizing logic
│   └── visualizations.py            # Plotting functions
└── examples/
    ├── sample_positions.csv         # 5 example scenarios
    └── README.md                    # Examples documentation
```
