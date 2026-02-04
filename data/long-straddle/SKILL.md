---
name: long-straddle
description: Analyzes long straddle volatility plays with ATM call and put at same strike. Requires numpy>=1.24.0, pandas>=2.0.0, matplotlib>=3.7.0, scipy>=1.10.0. Use when expecting large price movement in either direction, analyzing earnings plays, evaluating volatility opportunities, or assessing binary event outcomes on high IV stocks.
---

# Long Straddle Strategy

**Version**: 1.0
**Last Updated**: 2025-12-12

## Overview

A long straddle is a neutral volatility strategy that profits from large price movements in either direction. By purchasing both an ATM call and ATM put with the same strike and expiration, the trader benefits from significant moves regardless of direction while accepting high upfront cost and time decay.

**Quick Summary**: Buy ATM call + Buy ATM put (same strike) = Profit from large moves either way

## Strategy Characteristics

**Position Structure**:
- Buy 1 call at-the-money (ATM)
- Buy 1 put at-the-money (ATM)
- Same strike price (typically ATM)
- Same expiration date

**Risk Profile**:
- **Maximum Loss**: Total premium paid (call + put)
- **Maximum Profit**: Unlimited (stock can move infinitely)
- **Breakeven Points**:
  - Upside: Strike + Total premium
  - Downside: Strike - Total premium
- **Best Use**: Expect large move but uncertain of direction

**Cost Components**:
- Call premium (debit)
- Put premium (debit)
- Total premium = Call + Put (significant cost)
- Transaction costs: ~$0.65 per contract × 2 legs = $1.30

## Quick Start

Calculate long straddle metrics:

```python
from scripts.long_straddle_calculator import LongStraddle

# Example: Earnings play on NVDA at $475
position = LongStraddle(
    underlying_price=475.00,
    strike=475.00,        # ATM strike
    call_premium=22.50,
    put_premium=21.00,
    contracts=1
)

# Key metrics
print(f"Total Cost: ${position.total_cost:.2f}")
print(f"Upper Breakeven: ${position.upper_breakeven:.2f}")
print(f"Lower Breakeven: ${position.lower_breakeven:.2f}")
print(f"Required Move: {position.required_move_percent:.1f}%")
```

## Core Workflow

### 1. Identify Volatility Opportunity

Look for catalysts that create uncertainty:

**Binary Events**:
- Earnings announcements (quarterly reports)
- FDA drug approval decisions
- Merger/acquisition outcomes
- Legal rulings or regulatory decisions
- Major product launches

**Market Conditions**:
- Fed meetings with unclear direction
- Geopolitical uncertainty
- Technical breakout/breakdown setups
- Historical volatility compression

**Criteria**:
- High implied volatility (IV rank >50)
- Clear catalyst date
- Expected move >10% (sufficient to overcome cost)
- Liquid options (tight bid/ask spreads)

See [references/volatility-analysis.md](references/volatility-analysis.md).

### 2. IV Rank and Percentile Analysis

Assess current volatility levels:

```python
from scripts.iv_analyzer import analyze_iv_metrics

metrics = analyze_iv_metrics(
    symbol='NVDA',
    current_iv=0.65,
    lookback_period=252  # 1 year
)

print(f"IV Rank: {metrics['iv_rank']:.0f}")          # 75 (high)
print(f"IV Percentile: {metrics['iv_percentile']:.0f}")  # 82
print(f"Expected Move: {metrics['expected_move']:.1f}%")  # 8.5%
```

**Ideal IV Environment**:
- IV Rank: 50-90 (elevated but not extreme)
- IV Percentile: 60-90
- Historical vol < Implied vol (vol expansion expected)

⚠️ **Avoid** when IV rank >90 (extreme - risk of IV crush)

See [references/iv-metrics-guide.md](references/iv-metrics-guide.md).

### 3. Expected Move Calculation

Calculate market's implied move:

```python
from scripts.expected_move_calculator import calculate_expected_move

expected = calculate_expected_move(
    underlying_price=475.00,
    total_premium=43.50,  # Straddle cost
    days_to_expiration=3   # Earnings in 3 days
)

print(f"Expected Move: ${expected['dollar_move']:.2f}")  # $40.25
print(f"Expected Move %: {expected['percent_move']:.1f}%")  # 8.5%
print(f"Implied Move Range: ${expected['lower_bound']:.2f} - ${expected['upper_bound']:.2f}")
```

**Rule of Thumb**: Straddle cost ≈ 85% of expected move (1 standard deviation)

See [references/expected-move-calculation.md](references/expected-move-calculation.md).

### 4. Strike Selection

**ATM Strike** (Standard):
- Strike nearest to current stock price
- Maximum gamma (sensitivity to moves)
- Highest theta decay (most expensive)
- Example: Stock $475 → Strike $475

**Slightly OTM Strikes** (Alternative):
- Lower cost but wider breakevens
- Reduced gamma
- Better for extreme volatility
- Example: Stock $475 → Call $480 + Put $470 (actually a strangle)

For pure straddle, always use ATM strike.

See [references/strike-selection-guide.md](references/strike-selection-guide.md).

### 5. Expiration Timing

**Event-Based**:
- **Before event**: 1-7 days (earnings, FDA decision)
- **After event**: Benefit from move, but IV crush risk
- **Standard**: Use expiration closest to event (but after)

**Time-Based** (No specific event):
- **30-45 days**: Standard volatility play
- **14-21 days**: Short-term speculation
- **60-90 days**: Expensive, more time for move

**Key**: Balance premium cost vs. time for move to develop

See [references/expiration-timing.md](references/expiration-timing.md).

### 6. Cost-Benefit Analysis

Compare straddle cost to historical moves:

```python
from scripts.historical_analyzer import analyze_historical_moves

analysis = analyze_historical_moves(
    symbol='NVDA',
    event_type='earnings',
    lookback_count=8  # Last 8 earnings
)

print(f"Average Earnings Move: {analysis['avg_move']:.1f}%")
print(f"Max Move: {analysis['max_move']:.1f}%")
print(f"Min Move: {analysis['min_move']:.1f}%")
print(f"Current Straddle Implies: {analysis['current_implied']:.1f}%")
```

**Decision**:
- If historical avg > implied: Straddle may be underpriced ✅
- If historical avg < implied: Straddle may be overpriced ❌

See [references/historical-analysis.md](references/historical-analysis.md).

### 7. Greeks Analysis

Monitor straddle Greeks:

```python
from scripts.greeks_calculator import calculate_straddle_greeks

greeks = calculate_straddle_greeks(
    strike=475.00,
    underlying_price=475.00,
    call_premium=22.50,
    put_premium=21.00,
    volatility=0.65,
    time_to_expiration=3/365
)

print(f"Delta: {greeks['delta']:.3f}")    # ~0 (neutral)
print(f"Gamma: {greeks['gamma']:.3f}")    # High (sensitive)
print(f"Theta: {greeks['theta']:.3f}")    # Very negative (decay)
print(f"Vega: {greeks['vega']:.3f}")      # Positive (gains from IV)
```

**Key Greeks**:
- **Delta**: Near zero at entry (neutral)
- **Gamma**: Very high (rapid delta change with moves)
- **Theta**: Very negative (time decay hurts)
- **Vega**: Very positive (benefits from IV increase)

See [references/greeks-guide.md](references/greeks-guide.md).

### 8. Position Sizing

Calculate appropriate contracts:

```python
from scripts.position_sizer import calculate_straddle_size

contracts = calculate_straddle_size(
    portfolio_value=100000,
    risk_per_trade=0.03,      # 3% max loss
    straddle_cost=4350         # $43.50 × 100
)
# Returns: 1 contract (max risk $4,350 = 4.35%)
```

**Sizing Rules**:
- Risk 2-5% of portfolio (straddles are risky)
- Account for 100% loss potential
- Don't oversize on single event

See [references/position-sizing.md](references/position-sizing.md).

### 9. Entry Execution

**Order Types**:
- **Straddle Order**: Single order for both legs (best pricing)
- **Limit Order**: Set max total premium willing to pay
- **Market Order**: Immediate fill (wider slippage)

**Best Practices**:
- Enter as single straddle order
- Set limit at mid-point of bid/ask
- Avoid entering immediately before event (IV peak)
- Enter 2-5 days before catalyst (balance cost vs. time)

**Timing Considerations**:
- **Too Early**: Pay for excess time decay
- **Too Late**: IV already elevated, expensive
- **Optimal**: 2-5 days before event (sweet spot)

### 10. Management and Exit

**Profit Targets**:
- **Quick Exit**: 20-30% profit (avoid theta decay)
- **Event Exit**: Close day of or after event
- **Breakeven Exit**: Stock reaches breakeven point

**Stop Loss**:
- **Time-Based**: Close if no move by event
- **Percentage-Based**: Close at 50-70% loss (cut losses)
- **IV Crush**: Exit immediately after event if IV drops

**Post-Event Management**:
- **Large Move**: Take profits quickly (theta accelerates)
- **Small Move**: Accept loss, exit position
- **IV Crush**: Exit immediately (vega loss)

See [references/management-strategies.md](references/management-strategies.md).

## Scripts

### Calculator

```bash
# Calculate long straddle metrics
python scripts/long_straddle_calculator.py \
  --underlying NVDA \
  --price 475 \
  --strike 475 \
  --call-premium 22.50 \
  --put-premium 21.00 \
  --contracts 1
```

### IV Analyzer

```bash
# Analyze IV rank and percentile
python scripts/iv_analyzer.py \
  --symbol NVDA \
  --current-iv 0.65 \
  --lookback 252
```

### Expected Move Calculator

```bash
# Calculate market's expected move
python scripts/expected_move_calculator.py \
  --price 475 \
  --total-premium 43.50 \
  --dte 3
```

### Historical Analyzer

```bash
# Analyze historical earnings moves
python scripts/historical_analyzer.py \
  --symbol NVDA \
  --event earnings \
  --lookback 8
```

## References

### Core Guides
- [quickstart-guide.md](references/quickstart-guide.md) - 5-minute overview
- [installation-guide.md](references/installation-guide.md) - Setup instructions
- [developer-guide.md](references/developer-guide.md) - Code standards

### Strategy-Specific
- [volatility-analysis.md](references/volatility-analysis.md) - IV rank, percentile, catalysts
- [iv-metrics-guide.md](references/iv-metrics-guide.md) - Calculate and interpret IV metrics
- [expected-move-calculation.md](references/expected-move-calculation.md) - Market's implied move
- [historical-analysis.md](references/historical-analysis.md) - Compare to past moves
- [strike-selection-guide.md](references/strike-selection-guide.md) - ATM strike selection
- [expiration-timing.md](references/expiration-timing.md) - Optimal entry timing
- [greeks-guide.md](references/greeks-guide.md) - Delta, gamma, theta, vega
- [position-sizing.md](references/position-sizing.md) - Risk management
- [management-strategies.md](references/management-strategies.md) - Profit targets, exits
- [examples.md](references/examples.md) - Real earnings plays

## Dependencies

**Required Packages**:
```
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
scipy>=1.10.0
yfinance>=0.2.0  # For historical IV data
```

**Installation**:
```bash
pip install -r requirements.txt
```

**Python Version**: 3.11+

## Risk Warnings

⚠️ **Key Risks**:
- **High Cost**: Straddles are expensive (both legs at ATM)
- **Time Decay**: Theta decay accelerates as expiration approaches
- **IV Crush**: Massive vega loss after event (50-80% drop possible)
- **Requires Large Move**: Need move beyond breakevens to profit
- **Both Breakevens**: Must overcome premium in either direction
- **Event Risk**: If event canceled/delayed, position loses value

**Risk Mitigation**:
- Only use on high-probability volatility events
- Exit quickly after event (avoid IV crush)
- Size positions appropriately (2-5% portfolio risk)
- Set stop loss at 50-70% of premium
- Have exit plan BEFORE entering
- Avoid holding through weekend/holiday (theta decay)

## When to Use Long Straddle

✅ **Ideal Scenarios**:
- Earnings with uncertain outcome
- FDA approvals (binary yes/no)
- Fed meetings with unclear direction
- Technical breakout/breakdown pending
- Historical moves >10% (sufficient to profit)
- IV rank 50-90 (elevated but not extreme)

❌ **Avoid When**:
- Low volatility environment (IV rank <30)
- Extreme IV (>90) - risk of IV crush
- No clear catalyst
- Sideways market with no expected move
- After event (IV already crushed)
- Can't accept 100% loss potential

## Comparison to Other Strategies

**vs. Long Strangle**:
- ❌ Higher cost (both ATM vs. OTM)
- ✅ Lower breakevens (smaller move needed)
- ✅ Higher gamma (more responsive)

**vs. Iron Condor**:
- ❌ Debit vs. credit (pay upfront)
- ✅ Unlimited profit potential
- ❌ Time decay hurts vs. helps

**vs. Directional Play (long call/put)**:
- ✅ No directional risk
- ❌ Double the cost
- ✅ Profit from move either way

## Example Trade

**Scenario**: NVDA earnings, stock at $475, IV rank 75

**Setup**:
- Buy 1 NVDA $475 call @ $22.50
- Buy 1 NVDA $475 put @ $21.00
- Total cost: $43.50 × 100 = $4,350
- Expiration: 3 days (day after earnings)
- Expected move: 8.5% ($40.25)

**Risk Profile**:
- Max Loss: $4,350 (if NVDA unchanged)
- Max Profit: Unlimited
- Upper Breakeven: $475 + $43.50 = $518.50 (+9.2%)
- Lower Breakeven: $475 - $43.50 = $431.50 (-9.2%)
- Required Move: 9.2% to breakeven

**Outcomes**:
- NVDA at $520 (9.5% up): Profit $150 ($5.20 - $4.35)
- NVDA at $510 (7.4% up): Loss $1,850 ($5.10 - $4.35)
- NVDA at $475 (0%): Loss $4,350 (max loss)
- NVDA at $430 (9.5% down): Profit $1,150 ($4.50 - $4.35)

## Version History

### v1.0 (2025-12-12)
- Initial release using SKILL_PACKAGE_TEMPLATE v3.0
- Anthropic + Claude Code compliant (<500 lines)
- Progressive disclosure with references/
- Complete IV analysis and expected move calculators
- Historical earnings comparison framework
- Greeks monitoring and position sizing

---

**Compliance**: Anthropic Best Practices ✅ | Claude Code Compatible ✅
**Template**: SKILL_PACKAGE_TEMPLATE v3.0
**Lines**: ~490 (under 500-line limit)
