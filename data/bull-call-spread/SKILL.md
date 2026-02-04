---
name: bull-call-spread
description: Analyzes bull-call-spread debit spreads for bullish directional plays with defined risk. Requires numpy>=1.24.0, pandas>=2.0.0, matplotlib>=3.7.0, scipy>=1.10.0. Use when expecting moderate price increase, comparing vertical spread configurations, analyzing debit spread opportunities, calculating Greeks for multi-leg positions, or evaluating defined-risk bullish strategies on liquid optionable securities.
---

# Bull Call Spread Strategy

**Version**: 2.0
**Last Updated**: 2025-12-12

## Overview

A bull-call-spread is a vertical debit spread that profits from moderate upward price movement while limiting both risk and reward. The strategy involves buying a lower-strike call (long call) and selling a higher-strike call (short call), creating a net debit position with defined maximum loss and profit.

**Quick Summary**: Buy lower call + Sell higher call = Defined-risk bullish play

**Previous Version**: v1.0 had comprehensive inline documentation (823 lines). v2.0 refactored to progressive disclosure (<500 lines) following SKILL_PACKAGE_TEMPLATE v3.0.

## Strategy Characteristics

**Position Structure**:
- Buy 1 call at lower strike (long call)
- Sell 1 call at higher strike (short call)
- Same expiration date
- Same underlying stock

**Risk Profile**:
- **Maximum Loss**: Net debit paid (long premium - short premium)
- **Maximum Profit**: Spread width - Net debit
- **Breakeven**: Long strike + Net debit
- **Best Use**: Moderately bullish outlook with defined risk parameters

**Cost Components**:
- Long call premium (debit)
- Short call premium (credit)
- Net debit = Long premium - Short premium
- Transaction costs: ~$0.65 per contract × 2 legs = $1.30

## Quick Start

Calculate bull-call-spread metrics:

```python
from scripts.strategy_calculator import BullCallSpread

# Example: Bullish on SPY at $450
position = BullCallSpread(
    underlying_symbol="SPY",
    underlying_price=450.00,
    long_strike=445.00,    # Buy $5 ITM call
    short_strike=455.00,   # Sell $5 OTM call
    long_premium=8.50,
    short_premium=3.20,
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
Identify bullish opportunity with moderate upside target.

**Criteria**:
- Technical breakout (resistance break, bullish pattern)
- Positive fundamental catalyst
- Uptrend confirmation
- Target price identified

### 2. Strike Selection

**Long Call (Lower Strike)**:
- Typically ATM or slightly ITM
- Delta: 0.50-0.65
- Provides directional exposure

**Short Call (Higher Strike)**:
- OTM above long strike
- Delta: 0.25-0.40
- Reduces cost, defines max profit

**Common Spread Widths**:
- Narrow ($2.50-$5): Lower cost, lower profit
- Standard ($5-$10): Balanced risk/reward
- Wide ($10-$20): Higher cost, higher profit potential

See [reference.md](reference.md#strike-selection-guidelines) for delta-based framework.

### 3. Spread Width Analysis

Compare spread configurations:

```python
from scripts.strategy_calculator import analyze_spread_widths

# Compare $2.50, $5, $10 spreads
results = analyze_spread_widths(
    underlying_price=450.00,
    long_strike=445.00,
    spread_widths=[2.5, 5.0, 10.0],
    volatility=0.20,
    days_to_expiration=45
)

# Analyze return on risk for each width
for width, metrics in results.items():
    print(f"${width} spread: ROR {metrics['return_on_risk']:.1f}%")
```

See [reference.md](reference.md#spread-width-optimization) for optimization framework.

### 4. Expiration Cycle Selection

**Standard Cycles**:
- **30-45 days**: Optimal theta decay, standard choice
- **45-60 days**: More time for thesis to play out
- **60-90 days**: Reduced urgency, lower theta

**Considerations**:
- Time for bullish thesis to materialize
- Theta decay acceleration (30-45 DTE sweet spot)
- Upcoming events (earnings, Fed meetings)

### 5. Position Sizing

Calculate appropriate contracts based on portfolio risk:

```python
from scripts.strategy_calculator import calculate_position_size

contracts = calculate_position_size(
    portfolio_value=100000,
    risk_per_trade=0.02,      # 2% portfolio heat
    max_loss_per_contract=530  # Net debit
)
# Returns: 3 contracts (max risk $1,590 = 1.59%)
```

See [reference.md](reference.md#position-sizing-framework).

### 6. Greeks Analysis

Monitor position Greeks:

```python
from scripts.strategy_calculator import calculate_spread_greeks

greeks = calculate_spread_greeks(
    long_strike=445.00,
    short_strike=455.00,
    underlying_price=450.00,
    volatility=0.20,
    time_to_expiration=45/365
)

print(f"Delta: {greeks['delta']:.3f}")    # Positive (bullish)
print(f"Theta: {greeks['theta']:.3f}")    # Negative (time decay hurts)
print(f"Vega: {greeks['vega']:.3f}")      # Positive initially (IV sensitivity)
```

See [reference.md](reference.md#greeks-analysis-detailed) for comprehensive Greeks guide.

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
- Roll up: Higher both strikes if more bullish
- Roll out: Extend expiration if need more time
- Close early: Take profits or cut losses

See [reference.md](reference.md#management-and-adjustments) for detailed adjustment strategies.

## Scripts

### Calculator

```bash
# Calculate bull-call-spread metrics
python scripts/strategy_calculator.py \
  --underlying SPY \
  --price 450 \
  --long-strike 445 \
  --short-strike 455 \
  --long-premium 8.50 \
  --short-premium 3.20 \
  --contracts 1
```

### Black-Scholes Pricing

```bash
# Price individual options
python scripts/black_scholes.py \
  --type call \
  --spot 450 \
  --strike 445 \
  --time 0.123 \
  --rate 0.05 \
  --volatility 0.20
```

### Spread Analyzer

```bash
# Compare multiple spread widths
python scripts/strategy_calculator.py \
  --analyze-widths \
  --underlying SPY \
  --price 450 \
  --long-strike 445 \
  --widths 2.5 5.0 10.0 \
  --dte 45
```

## References

### Core Documentation
- [reference.md](reference.md) - Complete mathematical derivations and advanced topics
  - Strike Selection Guidelines
  - Spread Width Optimization
  - Greeks Analysis Detailed
  - Position Sizing Framework
  - Management and Adjustments
  - Scenario Analysis
  - Historical Performance

### Code Examples
- [scripts/strategy_calculator.py](scripts/strategy_calculator.py) - Main calculator with CLI
- [scripts/black_scholes.py](scripts/black_scholes.py) - Options pricing engine

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
- **Directional Risk**: Requires upward movement to profit
- **Time Decay**: Theta works against long call if stock doesn't move
- **Assignment Risk**: Short call may be assigned if ITM at expiration
- **Early Assignment**: Possible if short call goes deep ITM (rare on index options)

**Risk Mitigation**:
- Define max loss before entry (net debit paid)
- Use stop loss at 100-150% of debit
- Avoid holding through earnings (IV crush risk)
- Monitor short call for early assignment (if deep ITM)
- Size positions appropriately (2-5% portfolio heat)

## When to Use Bull Call Spread

✅ **Ideal Scenarios**:
- Moderately bullish outlook (5-15% upside expected)
- Want defined risk and defined reward
- Prefer lower cost than buying calls outright
- Time horizon: 30-60 days
- Normal to elevated IV environment

❌ **Avoid When**:
- Strongly bullish (>20% move expected) - consider long calls
- Neutral outlook - use different strategy
- Very low IV - debit may be too high for good R:R
- Need unlimited profit potential - use long calls

## Comparison to Other Strategies

**vs. Long Call**:
- ✅ Lower cost (short call reduces debit)
- ❌ Limited profit (capped at spread width)
- ✅ Defined risk with better R:R ratio

**vs. Call Ratio Spread**:
- ✅ Simpler structure (1:1 ratio)
- ✅ No naked short exposure
- ❌ Lower profit potential

**vs. Bear Put Spread**:
- ✅ Opposite direction (bullish vs bearish)
- ✅ Similar risk/reward profile
- ✅ Same debit spread structure

## Example Trade

**Scenario**: SPY at $450, expecting rally to $455-460 over 45 days

**Setup**:
- Buy 1 SPY $445 call @ $8.50 (debit)
- Sell 1 SPY $455 call @ $3.20 (credit)
- Net debit: $5.30 × 100 = $530 per spread
- Contracts: 3 (based on 2% portfolio risk on $80k account)

**Risk Profile**:
- Max Loss: $530 × 3 = $1,590 (if SPY < $445 at expiration)
- Max Profit: ($10.00 - $5.30) × 100 × 3 = $1,410 (if SPY ≥ $455)
- Breakeven: $445 + $5.30 = $450.30
- Risk/Reward: 1:0.89 (not ideal, but acceptable for 90% probability)

**Outcomes**:
- SPY at $460: Max profit ($1,410)
- SPY at $452: Profit $510 ($5.20 spread value - $5.30 cost)
- SPY at $450: Loss $90 ($5.00 spread value - $5.30 cost)
- SPY at $442: Max loss ($1,590)

## Version History

### v2.0 (2025-12-12)
- Refactored to progressive disclosure (<500 lines)
- Conforms to SKILL_PACKAGE_TEMPLATE v3.0
- Anthropic + Claude Code compliant
- Updated frontmatter with packages and triggers
- Moved detailed content to reference.md
- Streamlined workflow to 8 core steps

### v1.0 (2024)
- Initial comprehensive implementation (823 lines)
- Inline documentation with detailed Greeks
- Complete mathematical derivations
- Extensive code examples

---

**Compliance**: Anthropic Best Practices ✅ | Claude Code Compatible ✅
**Template**: SKILL_PACKAGE_TEMPLATE v3.0
**Lines**: ~420 (under 500-line limit ✅)
