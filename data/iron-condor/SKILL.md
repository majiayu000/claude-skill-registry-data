---
name: iron-condor
description: Analyzes iron condor credit spreads with OTM put and call spreads for range-bound trading. Requires numpy>=1.24.0, pandas>=2.0.0, matplotlib>=3.7.0, scipy>=1.10.0. Use when expecting sideways price action, want to collect premium in high IV, analyzing range-bound opportunities, or implementing neutral income strategies on stocks with defined trading ranges.
---

# Iron Condor Strategy

**Version**: 1.0
**Last Updated**: 2025-12-12

## Overview

An iron condor is a credit spread strategy that profits from range-bound price action. By selling an OTM put spread and an OTM call spread simultaneously, the trader collects premium upfront and profits when the stock remains between the short strikes through expiration, benefiting from time decay and volatility contraction.

**Quick Summary**: Sell OTM put spread + Sell OTM call spread = Collect credit, profit from range

## Strategy Characteristics

**Position Structure**:
- Sell 1 OTM put (short put)
- Buy 1 further OTM put (long put, protection)
- Sell 1 OTM call (short call)
- Buy 1 further OTM call (long call, protection)
- All same expiration, typically equal wing widths

**Risk Profile**:
- **Maximum Profit**: Net credit received
- **Maximum Loss**: Wing width - Net credit
- **Breakeven Points**:
  - Lower: Short put - Net credit
  - Upper: Short call + Net credit
- **Best Use**: Expect stock to stay range-bound, benefit from theta and IV crush

**Cost Components**:
- Put spread credit: Received
- Call spread credit: Received
- Net credit = Total received (keep if stock stays in range)
- Max risk = Wing width - Net credit
- Transaction costs: ~$0.65 per contract × 4 legs = $2.60

## Quick Start

Calculate iron condor metrics:

```python
from scripts.iron_condor_calculator import IronCondor

# Example: SPY at $450, expect to stay $440-$460
position = IronCondor(
    underlying_price=450.00,
    short_put=440.00,     # Sell $440 put
    long_put=435.00,      # Buy $435 put ($5 wide)
    short_call=460.00,    # Sell $460 call
    long_call=465.00,     # Buy $465 call ($5 wide)
    put_spread_credit=0.75,
    call_spread_credit=0.80,
    contracts=1
)

# Key metrics
print(f"Net Credit: ${position.net_credit:.2f}")
print(f"Max Profit: ${position.max_profit:.2f}")
print(f"Max Loss: ${position.max_loss:.2f}")
print(f"Breakevens: ${position.lower_breakeven:.2f} - ${position.upper_breakeven:.2f}")
print(f"Profit Zone: {position.profit_zone_width:.0f} points")
```

## Core Workflow

### 1. Identify Range-Bound Opportunity

Look for stocks likely to trade sideways:

**Ideal Scenarios**:
- **Post-Earnings Consolidation**: Stock settles after earnings volatility
- **Technical Range**: Trading between support/resistance
- **High IV Crush Candidate**: Elevated IV likely to contract
- **Sideways Trend**: Lack of directional catalyst
- **Index Products**: SPY, QQQ during low-volatility periods

**Market Conditions**:
- IV rank >50 (premium rich environment)
- Recent volatility >  Expected future volatility
- Clear support/resistance levels
- No major catalysts upcoming
- Historical range-bound behavior

See [references/range-identification.md](references/range-identification.md).

### 2. Wing Width Selection

**Narrow Wings** ($2.50-$5):
- Lower max risk ($250-$500 per contract)
- Lower credit collected (~$0.50-$1.50)
- Better risk/reward ratio (often 3:1 or better)
- Easier to manage (less capital at risk)
- Example: $440/$445 put spread + $455/$460 call spread

**Standard Wings** ($5-$10):
- Moderate max risk ($500-$1,000 per contract)
- Moderate credit (~$1.00-$2.50)
- Balanced approach (most common)
- Example: $435/$445 put spread + $455/$465 call spread

**Wide Wings** ($10-$20):
- Higher max risk ($1,000-$2,000 per contract)
- Higher credit (~$2.50-$5.00)
- Lower R:R ratio (often <2:1)
- More capital intensive
- Example: $430/$450 put spread + $450/$470 call spread

**Selection Criteria**:
- Match wing width to risk tolerance
- Wider wings = more credit but worse R:R
- Target R:R ratio: 3:1 or better (credit:risk)

See [references/wing-width-selection.md](references/wing-width-selection.md).

### 3. Strike Placement Framework

**Delta-Based Approach** (Most Common):

**Conservative** (Wide profit zone):
- Short put: ~-0.10 delta (10% OTM)
- Short call: ~0.10 delta (10% OTM)
- Probability of profit: ~80%
- Example: Stock $100 → Short $90 put / Short $110 call

**Standard** (Balanced):
- Short put: ~-0.20 delta (7-8% OTM)
- Short call: ~0.20 delta (7-8% OTM)
- Probability of profit: ~70%
- Example: Stock $100 → Short $92 put / Short $108 call

**Aggressive** (Narrow profit zone):
- Short put: ~-0.30 delta (5% OTM)
- Short call: ~0.30 delta (5% OTM)
- Probability of profit: ~60%
- Higher credit, tighter range
- Example: Stock $100 → Short $95 put / Short $105 call

See [references/strike-placement-guide.md](references/strike-placement-guide.md).

### 4. Profit Zone Optimization

Compare different strike configurations:

```python
from scripts.condor_optimizer import optimize_profit_zone

configs = optimize_profit_zone(
    underlying_price=450.00,
    short_deltas=[0.10, 0.15, 0.20, 0.25, 0.30],
    wing_width=5.00,
    volatility=0.22,
    days_to_expiration=45
)

for config in configs:
    print(f"Delta {config['short_delta']:.2f}:")
    print(f"  Profit Zone: ${config['lower_short']:.2f} - ${config['upper_short']:.2f}")
    print(f"  Zone Width: {config['zone_width']:.0f} points ({config['zone_pct']:.1f}%)")
    print(f"  Credit: ${config['net_credit']:.2f}")
    print(f"  Max Risk: ${config['max_risk']:.2f}")
    print(f"  R:R Ratio: {config['rr_ratio']:.2f}:1")
```

See [references/profit-zone-optimization.md](references/profit-zone-optimization.md).

### 5. IV Rank and Premium Analysis

Assess volatility environment:

```python
from scripts.iv_analyzer import analyze_iv_for_condor

analysis = analyze_iv_for_condor(
    symbol='SPY',
    current_iv=0.22,
    lookback_period=252
)

print(f"IV Rank: {analysis['iv_rank']:.0f}")
print(f"IV Percentile: {analysis['iv_percentile']:.0f}")
print(f"Premium Rich: {analysis['is_premium_rich']}")
print(f"IV Crush Likely: {analysis['iv_crush_likely']}")
print(f"Optimal for Condor: {analysis['condor_optimal']}")
```

**Ideal IV Environment**:
- IV Rank: 50-90 (elevated premiums)
- IV Percentile: 60-90
- Recent IV spike (likely to contract)
- No major catalysts ahead (avoid IV expansion)

⚠️ **Avoid** when IV rank <30 (insufficient premium)

See [references/iv-analysis.md](references/iv-analysis.md).

### 6. Expiration Cycle Selection

**Short-Term Condors** (21-30 days):
- Faster theta decay benefit
- Less time for stock to breach
- More active management required
- Higher annualized return potential
- Best for: Active traders, high-probability setups

**Standard Condors** (30-45 days):
- Balanced theta and time
- Industry standard (most common)
- Moderate management
- Sweet spot for theta/gamma balance
- Best for: Most traders, most conditions

**Long-Term Condors** (45-60 days):
- Slower theta decay
- More time for adjustments
- Lower theta benefit
- More forgiving
- Best for: Less active traders, wider ranges

See [references/expiration-selection.md](references/expiration-selection.md).

### 7. Greeks Monitoring

Track condor Greeks:

```python
from scripts.greeks_calculator import calculate_condor_greeks

greeks = calculate_condor_greeks(
    short_put=440.00,
    long_put=435.00,
    short_call=460.00,
    long_call=465.00,
    underlying_price=450.00,
    volatility=0.22,
    time_to_expiration=45/365
)

print(f"Delta: {greeks['delta']:.3f}")    # ~0 (neutral)
print(f"Gamma: {greeks['gamma']:.3f}")    # Negative (position speeds up outside range)
print(f"Theta: {greeks['theta']:.3f}")    # Positive (earns decay)
print(f"Vega: {greeks['vega']:.3f}")      # Negative (benefits from IV drop)
```

**Key Insights**:
- **Delta**: Near zero (directionally neutral)
- **Gamma**: Negative (accelerates against you outside range)
- **Theta**: Positive (earns time decay daily)
- **Vega**: Negative (benefits from IV contraction)

See [references/greeks-guide.md](references/greeks-guide.md).

### 8. Position Sizing

Calculate risk-appropriate contracts:

```python
from scripts/position_sizer import calculate_condor_size

contracts = calculate_condor_size(
    portfolio_value=100000,
    risk_per_trade=0.02,      # 2% max risk
    max_loss_per_condor=345   # Wing width $5 - Credit $1.55
)
# Returns: 5 contracts (max risk $1,725 = 1.73%)
```

**Sizing Guidelines**:
- Risk 1-3% of portfolio per condor
- Account for max loss (wing width - credit)
- Consider deploying multiple condors at different ranges
- Leave room for adjustments

See [references/position-sizing.md](references/position-sizing.md).

### 9. Entry Execution

**Order Types**:
- **Iron Condor Order**: Single order for all 4 legs (best execution)
- **Credit Limit Order**: Set minimum net credit willing to accept
- **Separate Spreads**: Enter put spread and call spread separately (suboptimal)

**Best Practices**:
- Always enter as iron condor order (one ticket)
- Set limit at mid-point of condor bid/ask
- Adjust by $0.05-$0.10 if not filled
- Verify equal wing widths before sending
- Confirm credit received (not debit)

**Entry Timing**:
- Enter when IV rank >50
- After volatility spike (IV likely to contract)
- Avoid day before earnings/events
- Best: 30-45 days to expiration

### 10. Management and Adjustments

**Profit Taking**:
- **50% max profit**: Standard target (close at 50% of credit)
- **21 DTE**: Rolling point (close and re-establish if desired)
- **75% max profit**: Near optimal, theta slowing

**Defensive Adjustments** (Stock approaching short strike):

**Roll Untested Side**:
- Stock moving up: Close call spread, roll to higher strikes
- Stock moving down: Close put spread, roll to lower strikes
- Keep tested side, collect more credit

**Convert to Iron Butterfly**:
- Close breached spread
- Sell ATM spread on opposite side
- Tightens profit zone but collects credit

**Close and Re-establish**:
- Accept loss on current condor
- Open new condor at different range
- Fresh premium, reset probabilities

See [references/adjustment-strategies.md](references/adjustment-strategies.md).

## Scripts

### Calculator

```bash
# Calculate iron condor metrics
python scripts/iron_condor_calculator.py \
  --underlying SPY \
  --price 450 \
  --short-put 440 \
  --long-put 435 \
  --short-call 460 \
  --long-call 465 \
  --put-credit 0.75 \
  --call-credit 0.80
```

### Optimizer

```bash
# Optimize profit zone configuration
python scripts/condor_optimizer.py \
  --underlying SPY \
  --price 450 \
  --short-deltas 0.10 0.15 0.20 0.25 0.30 \
  --wing-width 5 \
  --dte 45
```

### IV Analyzer

```bash
# Analyze IV environment for condor
python scripts/iv_analyzer.py \
  --symbol SPY \
  --current-iv 0.22 \
  --lookback 252
```

## References

### Core Guides
- [quickstart-guide.md](references/quickstart-guide.md) - 5-minute overview
- [installation-guide.md](references/installation-guide.md) - Setup instructions
- [developer-guide.md](references/developer-guide.md) - Code standards

### Strategy-Specific
- [range-identification.md](references/range-identification.md) - Finding sideways opportunities
- [wing-width-selection.md](references/wing-width-selection.md) - Choosing spread width
- [strike-placement-guide.md](references/strike-placement-guide.md) - Delta-based framework
- [profit-zone-optimization.md](references/profit-zone-optimization.md) - Optimize range
- [iv-analysis.md](references/iv-analysis.md) - IV rank, percentile, premium environment
- [expiration-selection.md](references/expiration-selection.md) - 21/30/45 day comparison
- [greeks-guide.md](references/greeks-guide.md) - Delta, gamma, theta, vega
- [position-sizing.md](references/position-sizing.md) - Risk management
- [adjustment-strategies.md](references/adjustment-strategies.md) - Rolling, defending
- [examples.md](references/examples.md) - Real range-bound setups

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
- **Limited Profit**: Capped at net credit received
- **Undefined Risk (if not managed)**: Max loss = Wing width - Credit
- **Gamma Risk**: Position accelerates against you outside range
- **Assignment Risk**: Short options can be assigned early
- **Pin Risk**: Stock settling at short strike (complex scenarios)
- **Gap Risk**: Overnight gaps can breach strikes
- **Adjustment Cost**: Rolling can be expensive in losses

**Risk Mitigation**:
- Only trade in high IV environments (IV rank >50)
- Set max loss at 2-3× credit received
- Close early if breached (don't hope)
- Monitor approaching earnings/events
- Use mechanical profit taking (50% rule)
- Size conservatively (1-3% portfolio risk)
- Have adjustment plan before entry

## When to Use Iron Condor

✅ **Ideal Scenarios**:
- Range-bound market (sideways trend)
- High IV environment (IV rank >50)
- Post-earnings consolidation
- No major catalysts upcoming
- Clear support/resistance levels
- Want to collect premium with defined risk
- Comfortable with active management

❌ **Avoid When**:
- Low IV environment (IV rank <30)
- Trending market (strong directional bias)
- Pre-earnings or major catalyst
- Wide bid/ask spreads (illiquid)
- Can't actively monitor (vacations)
- Uncertain market conditions

## Comparison to Other Strategies

**vs. Iron Butterfly**: Wider profit zone and lower max loss probability, but lower credit.

**vs. Long Butterfly**: Collect credit vs. pay debit. Benefits from time decay.

**vs. Straddle/Strangle**: Defined risk with wings. Opposite thesis (want no move vs. big move). Collect premium.

## Example Trade

**Scenario**: SPY at $450, IV rank 72, expect to stay $435-$465 over 45 days

**Setup**:
- Sell 1 SPY $440 put @ $1.25
- Buy 1 SPY $435 put @ $0.50 (Put spread credit: $0.75)
- Sell 1 SPY $460 call @ $1.30
- Buy 1 SPY $465 call @ $0.50 (Call spread credit: $0.80)
- Net credit: $1.55 × 100 = $155 per condor
- Contracts: 10 condors
- Expiration: 45 days

**Risk Profile**:
- Max Profit: $155 × 10 = $1,550 (if SPY $440-$460 at expiration)
- Max Loss: ($5 wing - $1.55 credit) × 100 × 10 = $3,450
- Lower Breakeven: $440 - $1.55 = $438.45
- Upper Breakeven: $460 + $1.55 = $461.55
- Profit Zone: $438.45 - $461.55 (23-point range, ±5.1%)
- Risk/Reward: 2.2:1 (excellent)
- Probability of Profit: ~75%

**Outcomes**: SPY $440-$460 = max profit $1,550; at $461 = breakeven; outside wings = max loss $3,450

**Management**: Target 50% max profit ($775) or 21 DTE; stop if SPY approaches wings

## Version History

### v1.0 (2025-12-12)
- Initial release using SKILL_PACKAGE_TEMPLATE v3.0
- Anthropic + Claude Code compliant (<500 lines)
- Progressive disclosure with references/
- Complete condor optimizer and IV analyzer
- Delta-based strike placement framework
- Adjustment strategies and profit zone optimization

---

**Compliance**: Anthropic Best Practices ✅ | Claude Code Compatible ✅
**Template**: SKILL_PACKAGE_TEMPLATE v3.0
**Lines**: ~490 (under 500-line limit)
