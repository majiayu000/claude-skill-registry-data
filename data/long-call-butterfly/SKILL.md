---
name: long-call-butterfly
description: Analyzes long call butterfly spreads with 3 strikes and 4 legs for neutral outlook. Requires numpy>=1.24.0, pandas>=2.0.0, matplotlib>=3.7.0, scipy>=1.10.0. Use when expecting minimal price movement, want low-cost defined-risk strategy, analyzing pinning opportunities, or evaluating tight-range neutral positions on stocks near technical levels.
---

# Long Call Butterfly Strategy

**Version**: 1.0
**Last Updated**: 2025-12-12

## Overview

A long call butterfly is a sophisticated neutral strategy that profits from minimal price movement. Using three strike prices with four option contracts (1 ITM call + 2 ATM calls + 1 OTM call), the strategy offers limited risk and limited reward with maximum profit achieved when the stock closes exactly at the middle strike at expiration.

**Quick Summary**: Buy lower call + Sell 2 middle calls + Buy upper call = Profit from no movement

## Strategy Characteristics

**Position Structure**:
- Buy 1 call at lower strike (ITM or ATM)
- Sell 2 calls at middle strike (ATM)
- Buy 1 call at upper strike (OTM)
- All same expiration, equal spacing between strikes

**Risk Profile**:
- **Maximum Loss**: Net debit paid (limited)
- **Maximum Profit**: Middle strike - Lower strike - Net debit
- **Breakeven Points**:
  - Lower: Lower strike + Net debit
  - Upper: Upper strike - Net debit
- **Best Use**: Expect stock to pin near middle strike with low volatility

**Cost Components**:
- Lower call premium: Paid (debit, expensive)
- Middle calls premium: Received (credit × 2, offset cost)
- Upper call premium: Paid (debit, cheap)
- Net debit = Lower + Upper - (2 × Middle)
- Transaction costs: ~$0.65 per contract × 4 legs = $2.60

## Quick Start

Calculate butterfly metrics:

```python
from scripts.butterfly_calculator import LongCallButterfly

# Example: SPY at $450, expect minimal movement
position = LongCallButterfly(
    underlying_price=450.00,
    lower_strike=445.00,    # $5 ITM
    middle_strike=450.00,   # ATM (body)
    upper_strike=455.00,    # $5 OTM
    lower_premium=8.50,
    middle_premium=5.00,    # Sold 2×
    upper_premium=2.50,
    contracts=1
)

# Key metrics
print(f"Net Debit: ${position.net_debit:.2f}")
print(f"Max Profit: ${position.max_profit:.2f}")
print(f"Max Loss: ${position.max_loss:.2f}")
print(f"Breakevens: ${position.lower_breakeven:.2f} - ${position.upper_breakeven:.2f}")
print(f"Profit Zone: {position.profit_zone_width:.2f} points")
```

## Core Workflow

### 1. Identify Low-Volatility Opportunity

Look for stocks likely to trade in tight range:

**Ideal Scenarios**:
- **Post-Earnings Calm**: Stock settles after volatile earnings
- **Consolidation**: Trading in well-defined range
- **Technical Levels**: Near strong support/resistance
- **Pre-Event Lull**: Quiet period before catalyst
- **Low IV Environment**: IV rank <40, low expected move

**Stock Characteristics**:
- Low beta (< 1.0)
- Tight historical trading ranges
- Low implied volatility
- Recent volatility compression
- Clear technical pivot level

See [references/opportunity-identification.md](references/opportunity-identification.md).

### 2. Strike Selection Framework

**Standard Butterfly** (Equal Wing Spacing):
- Lower: $5 below current price
- Middle: At current price (ATM)
- Upper: $5 above current price
- Wing width: $5 both sides
- Example: Stock $100 → $95/$100/$105

**Narrow Butterfly** ($2.50-$5 wings):
- Tighter profit zone
- Higher probability of profit
- Lower max profit potential
- Example: Stock $450 → $447.50/$450/$452.50

**Wide Butterfly** ($10-$20 wings):
- Wider profit zone
- Lower probability of max profit
- Higher max profit potential
- Example: Stock $100 → $90/$100/$110

**Selection Rules**:
- Middle strike = Expected pin point (often ATM)
- Equal spacing: Upper-Middle = Middle-Lower
- Match wing width to expected range

See [references/strike-selection-guide.md](references/strike-selection-guide.md).

### 3. Wing Width Optimization

Compare different wing widths:

```python
from scripts.wing_optimizer import analyze_wing_widths

results = analyze_wing_widths(
    underlying_price=450.00,
    wing_widths=[2.5, 5.0, 10.0],
    volatility=0.18,
    days_to_expiration=30
)

for width, metrics in results.items():
    print(f"${width} wings:")
    print(f"  Max Profit: ${metrics['max_profit']:.2f}")
    print(f"  Max Loss: ${metrics['max_loss']:.2f}")
    print(f"  Profit Zone: ${metrics['profit_zone_width']:.2f}")
    print(f"  Prob of Profit: {metrics['prob_profit']:.1f}%")
```

**Trade-off**:
- Narrow wings: Higher prob, lower profit
- Wide wings: Lower prob, higher profit

See [references/wing-width-analysis.md](references/wing-width-analysis.md).

### 4. Probability Analysis

Calculate probability of profit:

```python
from scripts.probability_calculator import calculate_butterfly_probabilities

prob = calculate_butterfly_probabilities(
    underlying_price=450.00,
    lower_strike=445.00,
    middle_strike=450.00,
    upper_strike=455.00,
    volatility=0.18,
    days_to_expiration=30
)

print(f"Prob at Middle Strike: {prob['at_middle']:.1f}%")
print(f"Prob in Profit Zone: {prob['in_profit_zone']:.1f}%")
print(f"Prob of Max Profit: {prob['max_profit']:.1f}%")
print(f"Prob of Max Loss: {prob['max_loss']:.1f}%")
print(f"Expected Value: ${prob['expected_value']:.2f}")
```

**Decision Criteria**:
- Prob in profit zone >60%: Good setup
- Expected value >0: Positive expectancy
- Max profit/Max loss ratio >3:1: Favorable R:R

See [references/probability-analysis.md](references/probability-analysis.md).

### 5. Expiration Cycle Selection

**Short-Term Butterflies** (7-21 days):
- Lower cost (less time premium)
- Faster theta decay benefit
- Less time for stock to move outside range
- Higher gamma risk (rapid changes)
- Best for: Near-term pinning opportunities

**Medium-Term Butterflies** (30-45 days):
- Balanced cost and time
- Standard approach
- Moderate theta benefit
- Reasonable gamma exposure
- Best for: Standard neutral plays

**Long-Term Butterflies** (60-90 days):
- Higher cost (more time premium)
- Slow theta decay
- More time for adjustment
- Lower gamma risk
- Best for: Patient, adjustment-friendly approach

See [references/expiration-timing.md](references/expiration-timing.md).

### 6. Greeks Analysis

Monitor butterfly Greeks:

```python
from scripts.greeks_calculator import calculate_butterfly_greeks

greeks = calculate_butterfly_greeks(
    lower_strike=445.00,
    middle_strike=450.00,
    upper_strike=455.00,
    underlying_price=450.00,
    volatility=0.18,
    time_to_expiration=30/365
)

print(f"Delta: {greeks['delta']:.3f}")    # ~0 at middle
print(f"Gamma: {greeks['gamma']:.3f}")    # Changes rapidly
print(f"Theta: {greeks['theta']:.3f}")    # Positive (earns decay)
print(f"Vega: {greeks['vega']:.3f}")      # Negative (hurts from IV rise)
```

**Key Insights**:
- **Delta**: Near zero at middle strike, changes outside wings
- **Gamma**: Positive in profit zone, negative outside
- **Theta**: Positive (benefits from time decay)
- **Vega**: Negative (benefits from IV decrease)

See [references/greeks-guide.md](references/greeks-guide.md).

### 7. Position Sizing

Calculate appropriate contracts:

```python
from scripts/position_sizer import calculate_butterfly_size

contracts = calculate_butterfly_size(
    portfolio_value=100000,
    risk_per_trade=0.01,      # 1% max risk
    max_loss_per_butterfly=150 # Net debit
)
# Returns: 6 contracts (max risk $900 = 0.9%)
```

**Sizing Guidelines**:
- Risk 0.5-2% per butterfly (low risk strategy)
- Max loss = Net debit (clearly defined)
- Consider multiple butterflies at different strikes
- Scale in/out rather than all-in

See [references/position-sizing.md](references/position-sizing.md).

### 8. Entry Execution

**Order Types**:
- **Butterfly Order**: Single order for all 4 legs (best execution)
- **Limit Order**: Set max net debit willing to pay
- **Spread Order**: Enter as vertical spreads (2 separate orders)

**Best Practices**:
- Always enter as butterfly order (1 ticket, 4 legs)
- Set limit at mid-point of butterfly bid/ask
- Adjust by $0.05 if not filled within 60 seconds
- Avoid wide markets (>15% spread)
- Verify equal wing spacing before sending

**Entry Timing**:
- Enter when stock at middle strike (optimal)
- Avoid entering after large move
- Best during low volatility periods
- Consider multiple strikes if uncertain of pin point

### 9. Adjustment Strategies

**Stock Moves Outside Profit Zone**:

**Upside Adjustment** (Stock above upper strike):
- Close entire butterfly, accept loss
- Roll to higher strikes (all 3 strikes up)
- Add short call spread above (convert to condor)

**Downside Adjustment** (Stock below lower strike):
- Close entire butterfly, accept loss
- Roll to lower strikes (all 3 strikes down)
- Add short put spread below (convert to condor)

**Widening Profit Zone**:
- Close current butterfly
- Open wider wing butterfly (increase spacing)
- Accept lower max profit for wider range

See [references/adjustment-techniques.md](references/adjustment-techniques.md).

### 10. Exit Management

**Profit Targets**:
- **50-70% max profit**: Excellent target, reduces risk
- **80% max profit**: Near optimal, theta slowing
- **Expiration**: Hold for max profit if confident

**Stop Loss**:
- **100% of debit**: Full max loss, exit immediately
- **Stock outside wings**: Low recovery probability
- **Volatility spike**: Exit if IV increases significantly

**Early Exit Scenarios**:
- Stock moves >75% toward wing
- IV increases >50% (vega loss)
- Theta benefit exhausted (little time value left)
- Better opportunity elsewhere

See [references/exit-strategies.md](references/exit-strategies.md).

## Scripts

### Calculator

```bash
# Calculate butterfly metrics
python scripts/butterfly_calculator.py \
  --underlying SPY \
  --price 450 \
  --lower-strike 445 \
  --middle-strike 450 \
  --upper-strike 455 \
  --lower-premium 8.50 \
  --middle-premium 5.00 \
  --upper-premium 2.50
```

### Wing Optimizer

```bash
# Compare different wing widths
python scripts/wing_optimizer.py \
  --underlying SPY \
  --price 450 \
  --widths 2.5 5.0 10.0 \
  --dte 30 \
  --volatility 0.18
```

### Probability Calculator

```bash
# Calculate probability of profit
python scripts/probability_calculator.py \
  --price 450 \
  --lower 445 \
  --middle 450 \
  --upper 455 \
  --dte 30 \
  --vol 0.18
```

## References

### Core Guides
- [quickstart-guide.md](references/quickstart-guide.md) - 5-minute overview
- [installation-guide.md](references/installation-guide.md) - Setup instructions
- [developer-guide.md](references/developer-guide.md) - Code standards

### Strategy-Specific
- [opportunity-identification.md](references/opportunity-identification.md) - Finding low-vol setups
- [strike-selection-guide.md](references/strike-selection-guide.md) - Equal wing spacing framework
- [wing-width-analysis.md](references/wing-width-analysis.md) - Optimize wing spacing
- [probability-analysis.md](references/probability-analysis.md) - Calculate profit probabilities
- [expiration-timing.md](references/expiration-timing.md) - 7/30/60 day comparison
- [greeks-guide.md](references/greeks-guide.md) - Delta, gamma, theta, vega
- [position-sizing.md](references/position-sizing.md) - Risk management
- [adjustment-techniques.md](references/adjustment-techniques.md) - Managing outside wings
- [exit-strategies.md](references/exit-strategies.md) - Profit targets, stop loss
- [examples.md](references/examples.md) - Real consolidation plays

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
- **Limited Profit**: Capped at wing width - net debit
- **Narrow Profit Zone**: Small range for profitability
- **Gamma Risk**: Rapid position changes outside wings
- **Assignment Risk**: Short middle calls can be assigned early
- **Pin Risk**: Stock settling exactly at strike (complex assignment scenarios)
- **Complexity**: 4 legs = higher commissions, wider spreads
- **Adjustment Cost**: Expensive to roll or adjust position

**Risk Mitigation**:
- Only use in low volatility environments
- Set stop loss at max loss (net debit)
- Exit early if stock approaches wings (don't wait)
- Monitor middle strike for early assignment risk
- Use stocks with liquid options (tight spreads)
- Verify equal wing spacing to avoid undefined risk

## When to Use Long Call Butterfly

✅ **Ideal Scenarios**:
- Expect minimal price movement (neutral outlook)
- Stock consolidating in tight range
- Post-earnings quiet period
- Low IV environment (IV rank <40)
- Near strong technical support/resistance
- Want defined risk with low capital requirement
- Comfortable with limited profit potential

❌ **Avoid When**:
- Expecting large moves (use straddle/strangle)
- High volatility environment (IV crush hurts)
- Unclear where stock will settle
- Wide bid/ask spreads (execution cost too high)
- Trending market (directional bias)
- Upcoming catalyst (volatility spike risk)

## Comparison to Other Strategies

**vs. Iron Butterfly**:
- ✅ All long options (no naked short risk)
- ❌ Pay debit vs. collect credit
- ✅ Easier approval (no margin requirement)

**vs. Straddle/Strangle**:
- ✅ Lower cost (credit from short middle calls)
- ❌ Limited profit (capped vs. unlimited)
- ✅ Profits from no movement (vs. needing big move)

**vs. Condor**:
- ❌ Narrower profit zone
- ✅ Higher max profit potential
- ✅ Lower cost (fewer legs)

## Example Trade

**Scenario**: SPY consolidating at $450, expect to stay $445-$455 over 30 days

**Setup**:
- Buy 1 SPY $445 call @ $8.50
- Sell 2 SPY $450 calls @ $5.00 (receive $10.00)
- Buy 1 SPY $455 call @ $2.50
- Net debit: $8.50 + $2.50 - $10.00 = $1.00 × 100 = $100
- Contracts: 10 butterflies
- Expiration: 30 days

**Risk Profile**:
- Max Loss: $100 × 10 = $1,000 (if SPY ≤$445 or ≥$455)
- Max Profit: ($5.00 - $1.00) × 100 × 10 = $4,000 (if SPY exactly $450)
- Lower Breakeven: $445 + $1 = $446
- Upper Breakeven: $455 - $1 = $454
- Profit Zone: $446-$454 (8-point range, ±1.8%)
- Risk/Reward: 1:4 (excellent)

**Outcomes at Expiration**:
- SPY at $450: Max profit $4,000
- SPY at $452: Profit ~$2,000 (in profit zone)
- SPY at $446: Near breakeven
- SPY at $443: Max loss $1,000
- SPY at $457: Max loss $1,000

## Version History

### v1.0 (2025-12-12)
- Initial release using SKILL_PACKAGE_TEMPLATE v3.0
- Anthropic + Claude Code compliant (<500 lines)
- Progressive disclosure with references/
- Complete wing width optimizer and probability calculator
- Adjustment techniques and exit strategies
- Equal spacing framework for strike selection

---

**Compliance**: Anthropic Best Practices ✅ | Claude Code Compatible ✅
**Template**: SKILL_PACKAGE_TEMPLATE v3.0
**Lines**: ~480 (under 500-line limit)
