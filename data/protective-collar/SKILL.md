---
name: protective-collar
description: Analyzes protective collar strategies combining long stock, long put protection, and short call income. Requires numpy>=1.24.0, pandas>=2.0.0, matplotlib>=3.7.0. Use when protecting stock positions with reduced cost, hedging downside while generating income, or implementing portfolio insurance with capped upside on mid to large-cap holdings.
---

# Protective Collar Strategy

**Version**: 1.0
**Last Updated**: 2025-12-12

## Overview

A protective collar combines stock ownership with options to create a defined-risk position. By purchasing a protective put (downside insurance) and selling a covered call (upside income), the strategy limits both loss and gain while typically reducing or eliminating the net cost of protection.

**Quick Summary**: Own stock + Buy OTM put + Sell OTM call = Protected position with capped upside

## Strategy Characteristics

**Position Structure**:
- Own 100 shares of stock (or multiples)
- Buy 1 OTM put (downside protection)
- Sell 1 OTM call (income generation)
- Same expiration date for options

**Risk Profile**:
- **Maximum Loss**: Stock purchase price - Put strike + Net premium
- **Maximum Profit**: Call strike - Stock purchase price - Net premium
- **Breakeven**: Stock purchase price + Net premium
- **Best Use**: Protecting gains while maintaining stock ownership

**Cost Components**:
- Stock purchase: Shares × stock price
- Put premium: Paid (debit)
- Call premium: Received (credit)
- Net premium: Put cost - Call income (often zero-cost or credit)
- Transaction costs: ~$0.65 per contract × 2 legs = $1.30

## Quick Start

Calculate protective collar metrics:

```python
from scripts.protective_collar_calculator import ProtectiveCollar

# Example: Protect 100 shares of AAPL at $175
position = ProtectiveCollar(
    stock_price=175.00,
    shares=100,
    put_strike=165.00,    # 5.7% OTM protection
    put_premium=3.50,
    call_strike=185.00,   # 5.7% OTM cap
    call_premium=3.25
)

# Key metrics
print(f"Net Cost: ${position.net_premium:.2f}")
print(f"Max Loss: ${position.max_loss:.2f}")
print(f"Max Profit: ${position.max_profit:.2f}")
print(f"Protected Range: ${position.put_strike}-${position.call_strike}")
```

## Core Workflow

### 1. Position Assessment

Identify stock position requiring protection:

**Ideal Candidates**:
- Large unrealized gains (want to protect)
- Concentrated position (reducing risk)
- Upcoming volatility (earnings, events)
- Long-term hold (maintain ownership)

**Criteria**:
- Own ≥100 shares (or willing to purchase)
- Moderate bullish to neutral outlook
- Acceptable to cap upside for protection
- Time horizon: 30-90 days

### 2. Put Strike Selection (Downside Protection)

Choose protective put strike based on risk tolerance:

**Conservative (5-10% OTM)**:
- Strike 5-10% below current price
- More protection, higher cost
- Delta: -0.25 to -0.35
- Example: Stock $100 → Put $90-95

**Moderate (10-15% OTM)**:
- Strike 10-15% below current price
- Balanced protection and cost
- Delta: -0.15 to -0.25
- Example: Stock $100 → Put $85-90

**Aggressive (15-20% OTM)**:
- Strike 15-20% below current price
- Minimal protection, low cost
- Delta: -0.10 to -0.15
- Example: Stock $100 → Put $80-85

See [references/strike-selection-guide.md](references/strike-selection-guide.md).

### 3. Call Strike Selection (Upside Cap)

Choose covered call strike based on upside willingness:

**Conservative (10-15% OTM)**:
- Strike 10-15% above current price
- More upside potential, less income
- Delta: 0.15-0.25
- Example: Stock $100 → Call $110-115

**Moderate (5-10% OTM)**:
- Strike 5-10% above current price
- Balanced upside and income
- Delta: 0.25-0.35
- Example: Stock $100 → Call $105-110

**Aggressive (ATM to 5% OTM)**:
- Strike at or near current price
- Maximum income, limited upside
- Delta: 0.40-0.50
- Example: Stock $100 → Call $100-105

### 4. Collar Configuration Analysis

Compare different collar configurations:

```python
from scripts.collar_analyzer import analyze_collar_configurations

configs = analyze_collar_configurations(
    stock_price=175.00,
    shares=100,
    put_otm_percent=[5, 10, 15],    # Put 5%, 10%, 15% OTM
    call_otm_percent=[5, 10, 15],   # Call 5%, 10%, 15% OTM
    volatility=0.25,
    days_to_expiration=60
)

for config in configs:
    print(f"Put ${config['put_strike']} / Call ${config['call_strike']}")
    print(f"  Net Cost: ${config['net_premium']:.2f}")
    print(f"  Protected Range: {config['protection_width']:.1f}%")
```

See [references/collar-configurations.md](references/collar-configurations.md).

### 5. Zero-Cost Collar Optimization

Adjust strikes to achieve zero net premium:

```python
from scripts.zero_cost_optimizer import find_zero_cost_collar

result = find_zero_cost_collar(
    stock_price=175.00,
    target_put_delta=-0.25,  # Desired protection level
    volatility=0.25,
    days_to_expiration=60
)

print(f"Put Strike: ${result['put_strike']:.2f}")
print(f"Call Strike: ${result['call_strike']:.2f}")
print(f"Net Cost: ${result['net_cost']:.2f}")  # ~$0
```

**Trade-off**: Zero-cost collar typically requires wider strikes (less protection, more upside cap).

See [references/zero-cost-optimization.md](references/zero-cost-optimization.md).

### 6. Expiration Cycle Selection

**Standard Cycles**:
- **30-45 days**: Active management, frequent adjustments
- **60-90 days**: Quarterly protection, less management
- **90-180 days**: Long-term hedging (LEAPS)

**Considerations**:
- Cost of protection (longer = more expensive)
- Call income (longer = more premium)
- Portfolio turnover preferences
- Upcoming catalysts (earnings, events)

See [references/expiration-analysis.md](references/expiration-analysis.md).

### 7. Greeks Analysis

Monitor collar Greeks:

```python
from scripts.greeks_calculator import calculate_collar_greeks

greeks = calculate_collar_greeks(
    stock_price=175.00,
    put_strike=165.00,
    call_strike=185.00,
    volatility=0.25,
    time_to_expiration=60/365
)

print(f"Delta: {greeks['delta']:.3f}")    # ~1.0 (stock-like)
print(f"Theta: {greeks['theta']:.3f}")    # Minimal (offset legs)
print(f"Vega: {greeks['vega']:.3f}")      # Near zero (offsetting)
```

See [references/greeks-guide.md](references/greeks-guide.md).

### 8. Entry Execution

**Order Sequence**:
1. **Verify stock ownership**: Confirm 100+ shares
2. **Buy protective put**: Establish downside protection first
3. **Sell covered call**: Generate income to offset put cost
4. **Or use collar order**: Single order for both options

**Best Practices**:
- Enter options simultaneously (if possible)
- Protect downside before selling upside
- Use limit orders for better pricing
- Target net debit ≤ $0.50 or net credit

### 9. Management and Adjustments

**At Expiration**:

**Scenario 1: Stock between strikes (most common)**:
- Both options expire worthless
- Keep stock, establish new collar if desired
- Profit/Loss: Net premium paid/received

**Scenario 2: Stock below put strike**:
- Exercise put or sell stock at market
- Downside protection realized
- Loss limited to put strike - stock cost + net premium

**Scenario 3: Stock above call strike**:
- Stock called away at call strike
- Profit capped at call strike - stock cost - net premium
- Reestablish position if desired

**Early Management**:
- **Roll collar**: Close current, open new (extend time)
- **Adjust strikes**: Widen for more room, narrow for more protection
- **Close early**: Lock in protection if outlook changes

See [references/management-strategies.md](references/management-strategies.md).

### 10. Tax Considerations

⚠️ **Important Tax Implications**:

**Qualified Covered Call**:
- Call must be >30 days to expiration
- Call must be OTM (specific IRS rules)
- Preserves long-term capital gains treatment

**Unqualified Covered Call**:
- Stops holding period for long-term gains
- Converts future gains to short-term
- Consult tax advisor

See [references/tax-considerations.md](references/tax-considerations.md).

## Scripts

### Calculator

```bash
# Calculate protective collar metrics
python scripts/protective_collar_calculator.py \
  --stock AAPL \
  --price 175 \
  --shares 100 \
  --put-strike 165 \
  --put-premium 3.50 \
  --call-strike 185 \
  --call-premium 3.25
```

### Configuration Analyzer

```bash
# Compare collar configurations
python scripts/collar_analyzer.py \
  --stock AAPL \
  --price 175 \
  --put-otm 5 10 15 \
  --call-otm 5 10 15 \
  --dte 60
```

### Zero-Cost Optimizer

```bash
# Find zero-cost collar strikes
python scripts/zero_cost_optimizer.py \
  --stock AAPL \
  --price 175 \
  --put-delta -0.25 \
  --dte 60
```

## References

### Core Guides
- [quickstart-guide.md](references/quickstart-guide.md) - 5-minute overview
- [installation-guide.md](references/installation-guide.md) - Setup instructions
- [developer-guide.md](references/developer-guide.md) - Code standards

### Strategy-Specific
- [strike-selection-guide.md](references/strike-selection-guide.md) - Put and call strike frameworks
- [collar-configurations.md](references/collar-configurations.md) - Compare protection levels
- [zero-cost-optimization.md](references/zero-cost-optimization.md) - Achieve zero net premium
- [expiration-analysis.md](references/expiration-analysis.md) - 30/60/90 day comparison
- [greeks-guide.md](references/greeks-guide.md) - Delta, theta, vega calculations
- [management-strategies.md](references/management-strategies.md) - Rolling, adjustments, exits
- [tax-considerations.md](references/tax-considerations.md) - Qualified vs unqualified calls
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
- **Limited Upside**: Capped at call strike (opportunity cost)
- **Assignment Risk**: Call may be assigned if ITM
- **Early Assignment**: Possible on calls (especially near dividends)
- **Tax Impact**: Unqualified call stops holding period
- **Gap Risk**: Protection not continuous (put strike to zero)
- **Rollover Cost**: Must re-establish at expiration if continuing

**Risk Mitigation**:
- Define acceptable upside cap before entry
- Monitor call for early assignment (if deep ITM)
- Use qualified covered calls (>30 DTE, OTM)
- Set calendar reminders for expiration
- Have plan for rolling or closing

## When to Use Protective Collar

✅ **Ideal Scenarios**:
- Protecting large unrealized gains
- Reducing concentrated position risk
- Hedging through volatility (earnings, macro events)
- Maintaining stock ownership while limiting risk
- Generating income while protecting downside
- Cost-effective alternative to married put

❌ **Avoid When**:
- Strongly bullish (don't want upside capped)
- Need unlimited profit potential
- Don't own stock (use different strategy)
- Very short time frame (<30 days)
- Unwilling to have stock called away

## Comparison to Other Strategies

**vs. Married Put**:
- ✅ Lower cost (call income offsets put cost)
- ❌ Limited upside (call cap)
- ✅ Often zero-cost or net credit

**vs. Covered Call**:
- ✅ Downside protection (put insurance)
- ❌ Higher cost (unless zero-cost collar)
- ✅ Defined risk

**vs. No Hedge**:
- ✅ Downside protection
- ❌ Upside capped
- ✅ Sleep better at night

## Example Trade

**Scenario**: Own 200 shares MSFT at $350, protect through earnings

**Setup**:
- Stock: 200 shares @ $350
- Buy 2 MSFT $335 puts @ $5.00 (4.3% OTM protection)
- Sell 2 MSFT $370 calls @ $4.75 (5.7% OTM cap)
- Net debit: $0.25 × 100 × 2 = $50 total
- Expiration: 60 days

**Risk Profile**:
- Max Loss: ($350 - $335 + $0.25) × 200 = $3,050 (worst case)
- Max Profit: ($370 - $350 - $0.25) × 200 = $3,950 (if called away)
- Protected Range: $335 - $370 (10% range)
- Breakeven: $350.25

**Outcomes**:
- MSFT at $360: Profit $1,950 (stock gain - net debit)
- MSFT at $340: Loss $2,050 (limited by put)
- MSFT at $330: Loss $3,050 (max loss)
- MSFT at $380: Profit $3,950 (capped at call strike)

## Version History

### v1.0 (2025-12-12)
- Initial release using SKILL_PACKAGE_TEMPLATE v3.0
- Anthropic + Claude Code compliant (<500 lines)
- Progressive disclosure with references/
- Complete calculator and configuration analyzer
- Zero-cost collar optimization framework
- Tax considerations guide

---

**Compliance**: Anthropic Best Practices ✅ | Claude Code Compatible ✅
**Template**: SKILL_PACKAGE_TEMPLATE v3.0
**Lines**: ~470 (under 500-line limit)
