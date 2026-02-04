---
name: long-strangle
description: Analyzes long strangle volatility plays with OTM call and put at different strikes. Requires numpy>=1.24.0, pandas>=2.0.0, matplotlib>=3.7.0, scipy>=1.10.0. Use when expecting very large price movement, want lower-cost alternative to straddle, analyzing high-volatility events, or evaluating wide-range breakout opportunities on stocks with elevated IV.
---

# Long Strangle Strategy

**Version**: 1.0
**Last Updated**: 2025-12-12

## Overview

A long strangle is a neutral volatility strategy similar to a straddle but with lower cost and wider breakevens. By purchasing an OTM call and OTM put at different strikes, the trader profits from very large moves in either direction while paying less premium than a straddle, though requiring larger moves to achieve profitability.

**Quick Summary**: Buy OTM call + Buy OTM put (different strikes) = Lower cost, needs bigger move

## Strategy Characteristics

**Position Structure**:
- Buy 1 call out-of-the-money (OTM)
- Buy 1 put out-of-the-money (OTM)
- Different strike prices (call higher, put lower)
- Same expiration date

**Risk Profile**:
- **Maximum Loss**: Total premium paid (call + put)
- **Maximum Profit**: Unlimited (stock can move infinitely)
- **Breakeven Points**:
  - Upside: Call strike + Total premium
  - Downside: Put strike - Total premium
- **Best Use**: Expect very large move, want lower cost than straddle

**Cost Components**:
- Call premium (debit)
- Put premium (debit)
- Total premium = Call + Put (lower than straddle)
- Transaction costs: ~$0.65 per contract × 2 legs = $1.30

## Quick Start

Calculate long strangle metrics:

```python
from scripts.long_strangle_calculator import LongStrangle

# Example: TSLA at $250, expecting large move
position = LongStrangle(
    underlying_price=250.00,
    call_strike=265.00,   # 6% OTM call
    put_strike=235.00,    # 6% OTM put
    call_premium=8.50,
    put_premium=7.75,
    contracts=1
)

# Key metrics
print(f"Total Cost: ${position.total_cost:.2f}")
print(f"Upper Breakeven: ${position.upper_breakeven:.2f}")
print(f"Lower Breakeven: ${position.lower_breakeven:.2f}")
print(f"Required Move: {position.required_move_percent:.1f}%")
print(f"Cost Savings vs Straddle: {position.vs_straddle_savings:.1f}%")
```

## Core Workflow

### 1. Identify High-Volatility Opportunity

Look for events likely to cause extreme moves:

**Ideal Catalysts**:
- **Biotech**: Binary FDA approvals (pass/fail)
- **Tech Earnings**: High-growth companies with uncertain guidance
- **Legal Outcomes**: Major lawsuit verdicts
- **M&A Speculation**: Takeover rumors or announcements
- **Product Launches**: Make-or-break products

**Market Conditions**:
- Stock with history of large post-event moves (>15%)
- High implied volatility (IV rank >60)
- Uncertain outcome (50/50 scenarios)
- Sufficient liquidity in options

See [references/catalyst-identification.md](references/catalyst-identification.md).

### 2. Strike Selection Framework

**Strike Width Configurations**:

**Narrow Strangle** (2-5% OTM each side):
- Call: 2-5% above current price (delta ~0.35-0.45)
- Put: 2-5% below current price (delta ~-0.35 to -0.45)
- Higher cost, lower breakevens
- Example: Stock $100 → Call $105, Put $95

**Standard Strangle** (5-10% OTM each side):
- Call: 5-10% above current price (delta ~0.20-0.35)
- Put: 5-10% below current price (delta ~-0.20 to -0.35)
- Balanced cost and breakevens
- Example: Stock $100 → Call $110, Put $90

**Wide Strangle** (10-20% OTM each side):
- Call: 10-20% above current price (delta ~0.10-0.20)
- Put: 10-20% below current price (delta ~-0.10 to -0.20)
- Lower cost, very wide breakevens
- Example: Stock $100 → Call $120, Put $80

**Selection Criteria**:
- Match strike width to expected move magnitude
- Balance premium cost vs. probability of profit
- Consider historical post-event moves

See [references/strike-selection-guide.md](references/strike-selection-guide.md).

### 3. Strangle Width Optimization

Compare different strike configurations:

```python
from scripts/strangle_optimizer import optimize_strangle_width

configs = optimize_strangle_width(
    underlying_price=250.00,
    otm_percentages=[5, 10, 15, 20],  # Test various widths
    volatility=0.80,
    days_to_expiration=7,
    historical_avg_move=18.0  # Historical post-earnings move
)

for config in configs:
    print(f"OTM {config['otm_pct']}%:")
    print(f"  Cost: ${config['total_premium']:.2f}")
    print(f"  Breakevens: ${config['lower_be']:.2f} - ${config['upper_be']:.2f}")
    print(f"  Required Move: {config['required_move_pct']:.1f}%")
    print(f"  Prob Profit: {config['prob_profit']:.1f}%")
```

See [references/width-optimization.md](references/width-optimization.md).

### 4. Cost-Benefit vs Straddle

Compare strangle cost and requirements to straddle:

```python
from scripts.strangle_vs_straddle import compare_strategies

comparison = compare_strangle_vs_straddle(
    underlying_price=250.00,
    atm_strike=250.00,
    atm_call_premium=15.00,
    atm_put_premium=14.50,
    otm_call_strike=265.00,
    otm_call_premium=8.50,
    otm_put_strike=235.00,
    otm_put_premium=7.75
)

print("Straddle:")
print(f"  Cost: ${comparison['straddle_cost']:.2f}")
print(f"  Breakevens: ±{comparison['straddle_be_pct']:.1f}%")
print("\nStrangle:")
print(f"  Cost: ${comparison['strangle_cost']:.2f}")
print(f"  Cost Savings: {comparison['cost_savings_pct']:.1f}%")
print(f"  Breakevens: +{comparison['upper_be_pct']:.1f}% / -{comparison['lower_be_pct']:.1f}%")
```

**Decision Guide**:
- **Use Strangle** if: Historical moves >15%, want to reduce cost
- **Use Straddle** if: Moderate moves expected (8-12%), tighter breakevens needed

See [references/strangle-vs-straddle.md](references/strangle-vs-straddle.md).

### 5. IV Rank and Expected Move

Assess volatility environment:

```python
from scripts.iv_analyzer import analyze_iv_environment

analysis = analyze_iv_environment(
    symbol='TSLA',
    current_iv=0.80,
    lookback_period=252
)

print(f"IV Rank: {analysis['iv_rank']:.0f}")
print(f"IV Percentile: {analysis['iv_percentile']:.0f}")
print(f"Expected Move: {analysis['expected_move_pct']:.1f}%")
print(f"Historical Avg Move: {analysis['historical_avg']:.1f}%")
print(f"Strangle Breakevens Reasonable: {analysis['breakevens_achievable']}")
```

**Ideal Environment**:
- IV Rank: 60-90 (high but not extreme)
- Historical moves > Strangle breakevens
- Expected move ≥ Required move

See [references/iv-analysis.md](references/iv-analysis.md).

### 6. Expiration Timing

**Event-Driven Strangles**:
- **1-3 days before event**: Minimize theta while capturing IV
- **Week of event**: Balance time and cost
- **After event**: Capture move but risk IV crush

**Time-Driven Strangles**:
- **30-45 days**: Standard volatility play
- **60-90 days**: Longer-term speculation (expensive)
- **7-14 days**: Short-term binary event

**Timing Strategy**:
- Enter 2-5 days before catalyst
- Avoid entering day-of (IV peak, max cost)
- Exit day after event (before IV crush accelerates)

See [references/timing-strategies.md](references/timing-strategies.md).

### 7. Greeks Monitoring

Track strangle Greeks:

```python
from scripts.greeks_calculator import calculate_strangle_greeks

greeks = calculate_strangle_greeks(
    call_strike=265.00,
    put_strike=235.00,
    underlying_price=250.00,
    volatility=0.80,
    time_to_expiration=7/365
)

print(f"Delta: {greeks['delta']:.3f}")    # ~0 (neutral)
print(f"Gamma: {greeks['gamma']:.3f}")    # Positive (benefits from moves)
print(f"Theta: {greeks['theta']:.3f}")    # Negative (time decay hurts)
print(f"Vega: {greeks['vega']:.3f}")      # Positive (benefits from IV increase)
```

**Key Insights**:
- **Delta**: Near zero (directionally neutral)
- **Gamma**: Lower than straddle (OTM strikes)
- **Theta**: Negative but lower than straddle
- **Vega**: High (very sensitive to IV changes)

See [references/greeks-guide.md](references/greeks-guide.md).

### 8. Position Sizing

Calculate risk-appropriate contracts:

```python
from scripts.position_sizer import calculate_strangle_size

contracts = calculate_strangle_size(
    portfolio_value=100000,
    risk_per_trade=0.03,      # 3% max risk
    strangle_cost=1625         # $16.25 × 100
)
# Returns: 2 contracts (max risk $3,250 = 3.25%)
```

**Sizing Guidelines**:
- Risk 2-5% of portfolio per strangle
- Account for 100% loss potential
- Consider multiple contracts if confident
- Never oversize on single binary event

See [references/position-sizing.md](references/position-sizing.md).

### 9. Entry Execution

**Order Types**:
- **Strangle Order**: Single order for both legs (best execution)
- **Limit Order**: Set maximum total premium
- **Individual Legs**: Separate orders (worse pricing, wider spreads)

**Best Practices**:
- Always enter as strangle order (better fill)
- Set limit at mid-point of bid/ask
- Adjust by $0.05-$0.10 if not filled
- Avoid market orders (significant slippage on OTM options)

**Timing**:
- Enter 2-5 days before event
- Avoid immediate pre-event (IV spike)
- Avoid post-event (IV crush risk)

### 10. Management and Exit

**Profit Targets**:
- **20-30% profit**: Quick exit, lock gains
- **50% profit**: Strong target for event plays
- **Breakeven reached**: Consider partial exit

**Stop Loss**:
- **50-70% loss**: Cut position, avoid max loss
- **Day after event**: Exit if no move (IV crush coming)
- **Time-based**: If event passes with small move

**Post-Event Strategy**:
- **Large move in direction**: Close winning side, let loser expire
- **Moderate move**: May still be unprofitable, exit both sides
- **No move**: Accept loss, exit position
- **IV Crush**: Exit immediately day after event

See [references/exit-strategies.md](references/exit-strategies.md).

## Scripts

### Calculator

```bash
# Calculate long strangle metrics
python scripts/long_strangle_calculator.py \
  --underlying TSLA \
  --price 250 \
  --call-strike 265 \
  --put-strike 235 \
  --call-premium 8.50 \
  --put-premium 7.75 \
  --contracts 1
```

### Width Optimizer

```bash
# Compare different strike widths
python scripts/strangle_optimizer.py \
  --underlying TSLA \
  --price 250 \
  --otm-pcts 5 10 15 20 \
  --dte 7 \
  --volatility 0.80
```

### IV Analyzer

```bash
# Analyze IV environment
python scripts/iv_analyzer.py \
  --symbol TSLA \
  --current-iv 0.80 \
  --lookback 252
```

### Strangle vs Straddle Comparison

```bash
# Compare strangle to straddle
python scripts/strangle_vs_straddle.py \
  --underlying TSLA \
  --price 250 \
  --straddle-strike 250 \
  --call-strike 265 \
  --put-strike 235
```

## References

### Core Guides
- [quickstart-guide.md](references/quickstart-guide.md) - 5-minute overview
- [installation-guide.md](references/installation-guide.md) - Setup instructions
- [developer-guide.md](references/developer-guide.md) - Code standards

### Strategy-Specific
- [catalyst-identification.md](references/catalyst-identification.md) - Finding high-volatility events
- [strike-selection-guide.md](references/strike-selection-guide.md) - OTM strike framework
- [width-optimization.md](references/width-optimization.md) - Optimize strike spacing
- [strangle-vs-straddle.md](references/strangle-vs-straddle.md) - When to use each
- [iv-analysis.md](references/iv-analysis.md) - IV rank, percentile, expected move
- [timing-strategies.md](references/timing-strategies.md) - Optimal entry timing
- [greeks-guide.md](references/greeks-guide.md) - Delta, gamma, theta, vega
- [position-sizing.md](references/position-sizing.md) - Risk management
- [exit-strategies.md](references/exit-strategies.md) - Profit targets, stop loss
- [examples.md](references/examples.md) - Real biotech/earnings plays

## Dependencies

**Required Packages**:
```
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
scipy>=1.10.0
yfinance>=0.2.0  # For historical IV and price data
```

**Installation**:
```bash
pip install -r requirements.txt
```

**Python Version**: 3.11+

## Risk Warnings

⚠️ **Key Risks**:
- **Wider Breakevens**: Requires larger move than straddle (10-20%+)
- **Lower Probability**: OTM strikes = lower chance of profit
- **IV Crush**: Severe vega loss after event (60-90% drop possible)
- **Time Decay**: Theta eats premium if stock doesn't move
- **Both Sides Expire Worthless**: Very possible with moderate moves
- **Gap Risk**: Large overnight gaps may not fully capture value

**Risk Mitigation**:
- Only use on historically volatile stocks (>15% moves)
- Exit day after event (before IV crush accelerates)
- Set stop loss at 50-70% of premium
- Size conservatively (2-3% portfolio risk)
- Verify historical moves justify breakevens
- Have exit plan before entry

## When to Use Long Strangle

✅ **Ideal Scenarios**:
- Binary events (FDA approvals, major earnings)
- Stocks with history of 15%+ post-event moves
- High IV environment (IV rank 60-90)
- Want lower cost than straddle (30-50% savings)
- Willing to accept wider breakevens
- Clear catalyst with uncertain outcome

❌ **Avoid When**:
- Expected move <10% (insufficient for breakevens)
- Low volatility environment (IV rank <40)
- After event (IV already crushed)
- Moderate moves expected (use straddle instead)
- Can't accept very low probability of profit
- Extreme IV (>95) - massive crush risk

## Comparison to Other Strategies

**vs. Long Straddle**:
- ✅ Lower cost (30-50% cheaper)
- ❌ Wider breakevens (needs bigger move)
- ❌ Lower gamma (less responsive)
- ✅ Lower theta decay

**vs. Iron Condor**:
- ❌ Pay premium vs. collect
- ✅ Unlimited profit vs. capped
- ❌ Want volatility vs. want calm
- ✅ Benefit from IV increase

**vs. Directional Play**:
- ✅ No directional bias
- ❌ More expensive (two legs)
- ✅ Profit from move either way

## Example Trade

**Scenario**: Biotech FDA decision, stock at $42, IV rank 85

**Setup**:
- Buy 1 call $48 strike @ $2.10 (14% OTM)
- Buy 1 put $36 strike @ $1.85 (14% OTM)
- Total cost: $3.95 × 100 = $395 per strangle
- Contracts: 3 (based on 3% portfolio risk on $40k)
- Expiration: 7 days (2 days after FDA decision date)

**Risk Profile**:
- Max Loss: $395 × 3 = $1,185 (if stock $36-$48 at expiration)
- Max Profit: Unlimited
- Upper Breakeven: $48 + $3.95 = $51.95 (+23.7%)
- Lower Breakeven: $36 - $3.95 = $32.05 (-23.7%)
- Required Move: 23.7% (either direction)

**Outcomes**:
- **FDA Approval** → Stock $58: Profit $2,415 ($10 ITM - $3.95 cost × 3)
- **FDA Rejection** → Stock $28: Profit $1,215 ($8 ITM - $3.95 cost × 3)
- **Delayed Decision** → Stock $42: Loss $1,185 (max loss, both expire worthless)
- **Partial Approval** → Stock $46: Loss $585 (insufficient move)

## Version History

### v1.0 (2025-12-12)
- Initial release using SKILL_PACKAGE_TEMPLATE v3.0
- Anthropic + Claude Code compliant (<500 lines)
- Progressive disclosure with references/
- Complete strangle optimizer and IV analyzer
- Strangle vs straddle comparison framework
- Width optimization and catalyst identification

---

**Compliance**: Anthropic Best Practices ✅ | Claude Code Compatible ✅
**Template**: SKILL_PACKAGE_TEMPLATE v3.0
**Lines**: ~485 (under 500-line limit)
