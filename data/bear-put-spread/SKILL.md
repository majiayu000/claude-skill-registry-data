---
name: bear-put-spread
description: Analyzes bear-put-spread debit spreads for bearish directional plays with defined risk. Requires numpy>=1.24.0, pandas>=2.0.0, matplotlib>=3.7.0, scipy>=1.10.0. Use when expecting moderate price decline, comparing put spread configurations, analyzing debit spread opportunities, or evaluating defined-risk bearish positions on mid to large-cap stocks.
---

# Bear Put Spread Strategy

**Version**: 1.0
**Last Updated**: 2025-12-12

## Overview

A bear-put-spread is a vertical options strategy that profits from moderate downward price movement while limiting both risk and reward. The strategy involves buying a higher-strike put (closer to ATM) and selling a lower-strike put (further OTM), creating a net debit position with defined maximum loss and profit.

**Quick Summary**: Buy higher put + Sell lower put = Defined-risk bearish play

## Strategy Characteristics

**Position Structure**:
- Buy 1 put at higher strike (long put)
- Sell 1 put at lower strike (short put)
- Same expiration date
- Same underlying stock

**Risk Profile**:
- **Maximum Loss**: Net debit paid (long premium - short premium)
- **Maximum Profit**: Spread width - Net debit
- **Breakeven**: Long strike - Net debit
- **Best Use**: Moderately bearish outlook with defined risk parameters

**Cost Components**:
- Long put premium (debit)
- Short put premium (credit)
- Net debit = Long premium - Short premium
- Transaction costs: ~$0.65 per contract × 2 legs = $1.30

## Quick Start

Calculate bear-put-spread metrics:

```python
from scripts.bear_put_calculator import BearPutSpread

# Example: Bearish on SPY at $450
position = BearPutSpread(
    underlying_price=450.00,
    long_put_strike=450.00,   # Buy ATM put
    short_put_strike=445.00,  # Sell $5 OTM put
    long_put_premium=7.50,
    short_put_premium=5.00,
    contracts=1
)

# Key metrics
print(f"Max Profit: ${position.max_profit:.2f}")
print(f"Max Loss: ${position.max_loss:.2f}")
print(f"Breakeven: ${position.breakeven_price:.2f}")
print(f"Risk/Reward: {position.risk_reward_ratio:.2f}")
```

## Core Workflow

### 1. Market Analysis
Identify bearish opportunity with moderate downside target.

**Criteria**:
- Technical breakdown (support break, bearish pattern)
- Negative fundamental catalyst
- Downtrend confirmation
- Target price identified

### 2. Strike Selection

**Long Put (Higher Strike)**:
- Typically ATM or slightly ITM
- Delta: -0.45 to -0.55
- Provides directional exposure

**Short Put (Lower Strike)**:
- OTM below long strike
- Delta: -0.20 to -0.35
- Reduces cost, defines max profit

**Common Spread Widths**:
- Narrow ($2.50-$5): Lower cost, lower profit
- Standard ($5-$10): Balanced risk/reward
- Wide ($10-$20): Higher cost, higher profit potential

See [references/strike-selection-guide.md](references/strike-selection-guide.md) for delta-based framework.

### 3. Spread Width Analysis

Compare spread configurations:

```python
from scripts.spread_analyzer import analyze_spread_widths

# Compare $2.50, $5, $10 spreads
results = analyze_spread_widths(
    underlying_price=450.00,
    long_put_strike=450.00,
    spread_widths=[2.5, 5.0, 10.0],
    volatility=0.22,
    days_to_expiration=45
)

# Analyze return on risk for each width
for width, metrics in results.items():
    print(f"${width} spread: ROR {metrics['return_on_risk']:.1f}%")
```

See [references/spread-width-analysis.md](references/spread-width-analysis.md) for optimization.

### 4. Expiration Cycle Selection

**Standard Cycles**:
- **30-45 days**: Optimal theta decay, standard choice
- **45-60 days**: More time for thesis to play out
- **60-90 days**: Reduced urgency, lower theta

**Considerations**:
- Time for bearish thesis to materialize
- Theta decay acceleration (30-45 DTE sweet spot)
- Upcoming events (earnings, Fed meetings)

See [references/expiration-analysis.md](references/expiration-analysis.md).

### 5. Position Sizing

Calculate appropriate contracts based on portfolio risk:

```python
from scripts.position_sizer import calculate_position_size

contracts = calculate_position_size(
    portfolio_value=100000,
    risk_per_trade=0.02,      # 2% portfolio heat
    max_loss_per_contract=250  # From spread analysis
)
# Returns: 8 contracts (max risk $2,000)
```

See [references/position-sizing.md](references/position-sizing.md).

### 6. Greeks Analysis

Monitor position Greeks:

```python
from scripts.greeks_calculator import calculate_spread_greeks

greeks = calculate_spread_greeks(
    long_put_strike=450.00,
    short_put_strike=445.00,
    underlying_price=450.00,
    volatility=0.22,
    time_to_expiration=45/365
)

print(f"Delta: {greeks['delta']:.3f}")    # Negative (bearish)
print(f"Theta: {greeks['theta']:.3f}")    # Time decay
print(f"Vega: {greeks['vega']:.3f}")      # IV sensitivity
```

See [references/greeks-guide.md](references/greeks-guide.md).

### 7. Entry Execution

**Order Types**:
- **Limit Order**: Specify max net debit willing to pay
- **Market Order**: Immediate fill (wider slippage)
- **Vertical Spread Order**: Single order for both legs

**Best Practices**:
- Enter as single spread order (better pricing)
- Set limit at mid-point of bid/ask spread
- Adjust limit if not filled within 30 seconds
- Avoid wide markets (>10% spread width)

### 8. Management and Exit

**Profit Targets**:
- 50% max profit: Close early, reduce risk
- 75% max profit: Near maximum, theta slowing
- Max profit: Hold to expiration (if confident)

**Stop Loss**:
- 100% of debit: Full loss, thesis invalidated
- 150% of debit: Avoid if spread widens against you

**Adjustments**:
- Roll down: Lower both strikes if further bearish
- Roll out: Extend expiration if need more time
- Close early: Take profits or cut losses

See [references/management-strategies.md](references/management-strategies.md).

## Scripts

### Calculator

```bash
# Calculate bear-put-spread metrics
python scripts/bear_put_calculator.py \
  --underlying SPY \
  --price 450 \
  --long-strike 450 \
  --short-strike 445 \
  --long-premium 7.50 \
  --short-premium 5.00 \
  --contracts 1
```

### Spread Analyzer

```bash
# Compare multiple spread widths
python scripts/spread_analyzer.py \
  --underlying SPY \
  --price 450 \
  --widths 2.5 5.0 10.0 \
  --dte 45
```

### Position Sizer

```bash
# Calculate optimal contracts
python scripts/position_sizer.py \
  --portfolio 100000 \
  --risk-percent 2 \
  --max-loss 250
```

## References

### Core Guides
- [quickstart-guide.md](references/quickstart-guide.md) - 5-minute overview
- [installation-guide.md](references/installation-guide.md) - Setup instructions
- [developer-guide.md](references/developer-guide.md) - Code standards

### Strategy-Specific
- [strike-selection-guide.md](references/strike-selection-guide.md) - Delta-based strike framework
- [spread-width-analysis.md](references/spread-width-analysis.md) - Compare $2.50/$5/$10 spreads
- [expiration-analysis.md](references/expiration-analysis.md) - 30/45/60 day comparison
- [greeks-guide.md](references/greeks-guide.md) - Delta, theta, vega calculations
- [position-sizing.md](references/position-sizing.md) - Portfolio heat calculations
- [management-strategies.md](references/management-strategies.md) - Profit targets, stop loss, adjustments
- [examples.md](references/examples.md) - Real-world scenarios

## Dependencies

**Required Packages**:
```
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
scipy>=1.10.0
```

**Installation**:
```bash
pip install -r requirements.txt
```

**Python Version**: 3.11+

## Risk Warnings

⚠️ **Key Risks**:
- **Limited Profit**: Capped at spread width - net debit
- **Directional Risk**: Requires downward movement to profit
- **Time Decay**: Theta works against long put if stock doesn't move
- **Assignment Risk**: Short put may be assigned if ITM at expiration
- **Early Assignment**: Possible if short put goes deep ITM (rare on index options)

**Risk Mitigation**:
- Define max loss before entry (net debit paid)
- Use stop loss at 100-150% of debit
- Avoid holding through earnings (IV crush risk)
- Monitor short put for early assignment (if deep ITM)
- Size positions appropriately (2-5% portfolio heat)

## When to Use Bear Put Spread

✅ **Ideal Scenarios**:
- Moderately bearish outlook (5-10% downside expected)
- Want defined risk and defined reward
- Prefer lower cost than buying puts outright
- Time horizon: 30-60 days
- Normal to elevated IV environment

❌ **Avoid When**:
- Strongly bearish (>15% move expected) - consider long puts
- Neutral outlook - use different strategy
- Very low IV - debit may be too low for good R:R
- Need unlimited profit potential - use long puts

## Comparison to Other Strategies

**vs. Long Put**:
- ✅ Lower cost (short put reduces debit)
- ❌ Limited profit (capped at spread width)
- ✅ Defined risk with better R:R ratio

**vs. Put Ratio Spread**:
- ✅ Simpler structure (1:1 ratio)
- ✅ No naked short exposure
- ❌ Lower profit potential

**vs. Bear Call Spread**:
- ❌ Requires debit (capital upfront)
- ✅ Profits from downside move (not time decay)
- ✅ Better for strong bearish conviction

## Example Trade

**Scenario**: SPY at $450, expecting decline to $440-445 over 45 days

**Setup**:
- Buy 1 SPY $450 put @ $7.50 (debit)
- Sell 1 SPY $445 put @ $5.00 (credit)
- Net debit: $2.50 × 100 = $250 per spread
- Contracts: 4 (based on 2% portfolio risk on $50k account)

**Risk Profile**:
- Max Loss: $250 × 4 = $1,000 (if SPY > $450 at expiration)
- Max Profit: ($5.00 - $2.50) × 100 × 4 = $1,000 (if SPY ≤ $445)
- Breakeven: $450 - $2.50 = $447.50
- Risk/Reward: 1:1

**Outcomes**:
- SPY drops to $442: Max profit ($1,000)
- SPY at $447: Breakeven
- SPY at $451: Max loss ($1,000)

## Version History

### v1.0 (2025-12-12)
- Initial release using SKILL_PACKAGE_TEMPLATE v3.0
- Anthropic + Claude Code compliant (<500 lines)
- Progressive disclosure with references/
- Complete calculator and analysis scripts
- Delta-based strike selection framework

---

**Compliance**: Anthropic Best Practices ✅ | Claude Code Compatible ✅
**Template**: SKILL_PACKAGE_TEMPLATE v3.0
**Lines**: ~420 (under 500-line limit)
