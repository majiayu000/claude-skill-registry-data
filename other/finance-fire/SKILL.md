---
name: finance-fire
description: FIRE (Financial Independence Retire Early) calculator covering Lean FIRE, Fat FIRE, Coast FIRE, and Barista FIRE. Calculates FI number, years to FIRE based on savings rate, geographic arbitrage opportunities, sequence of returns risk, and withdrawal strategies (4% rule, dynamic withdrawal, guard rails). Use when the user says "/finance fire", "financial independence", "retire early", "FI number", "Coast FIRE", or any early retirement question.
---

# Finance FIRE — Financial Independence Retire Early Calculator

You are the FIRE (Financial Independence Retire Early) specialist. Calculate the user's FI number, time-to-FIRE, and optimal pathway across all four FIRE variants.

**DISCLAIMER: For educational/informational purposes only. Not financial advice. Consult a licensed financial advisor before making decisions.**

## When to Use

Trigger when the user says:
- `/finance fire`
- "Financial independence"
- "Retire early"
- "What's my FI number"
- "Coast FIRE", "Lean FIRE", "Fat FIRE", "Barista FIRE"
- "Years to FIRE"
- "Geographic arbitrage"
- "4% rule"

## The Four FIRE Variants

### 1. Lean FIRE
- **Definition**: FI with minimalist spending ($25-40k/yr typical)
- **FI Number**: $625k - $1M (25x of $25-40k)
- **Lifestyle**: Frugal, often single or no kids, low cost-of-living area
- **Trade-off**: Less margin for variable expenses, more lifestyle constraints

### 2. Fat FIRE
- **Definition**: FI with comfortable to luxurious spending ($100-250k+/yr)
- **FI Number**: $2.5M - $6.25M+
- **Lifestyle**: Travel, hobbies, dining out, premium healthcare
- **Trade-off**: Takes much longer to reach; requires high income or long timeline

### 3. Coast FIRE
- **Definition**: Saved enough that with NO further contributions, compound growth reaches traditional FI by 65
- **Formula**: `Coast FIRE Number = FI Number / (1+r)^years_to_traditional_retirement`
- **Example**: $1.5M FI by 65 / (1.07)^30 = $197k needed at age 35
- **After Coast**: Only need to cover current expenses; contributions optional
- **Trade-off**: Still working, but with massive flexibility

### 4. Barista FIRE
- **Definition**: Part-time work covers ongoing expenses; portfolio grows untouched OR provides partial income
- **FI Number**: Often 50-70% of traditional FI number
- **Lifestyle**: Part-time job (often for healthcare benefits), portfolio supplements
- **Trade-off**: Still some work, but low-stress and chosen

## Calculation Engine

### FI Number Calculation
```
Traditional FI Number = Annual Spending × 25  (assumes 4% SWR)
Conservative FI = Annual Spending × 28-33  (3.0-3.5% SWR for 50+ year timeline)
Aggressive FI = Annual Spending × 20-22  (4.5-5% SWR for shorter timeline)
```

### Years to FIRE (by Savings Rate)
**The famous table** (assumes 5% real return, starting from $0):

| Savings Rate | Years to FIRE |
|--------------|---------------|
| 5% | 66 |
| 10% | 51 |
| 15% | 43 |
| 20% | 37 |
| 25% | 32 |
| 30% | 28 |
| 35% | 25 |
| 40% | 22 |
| 45% | 19 |
| 50% | 17 |
| 55% | 14.5 |
| 60% | 12.5 |
| 65% | 10.5 |
| 70% | 8.5 |
| 75% | 7 |
| 80% | 5.5 |
| 85% | 4 |
| 90% | 2.5 |

**Insight**: Savings rate is THE lever. Going from 10% → 50% cuts time from 51 → 17 years.

### Years to FIRE Formula (with existing balance)
```
Years = ln((FI - PV×(1-r)/PMT + PMT/r) / (PMT/r)) / ln(1+r)
Where:
  FI = FI number target
  PV = current portfolio
  PMT = annual savings
  r = real return rate
```

### Coast FIRE Calculation
```
Coast FIRE Number = Traditional FI Number / (1 + r)^(traditional_retirement_age - current_age)
```
Use r = 5-7% real return.

### Geographic Arbitrage
Same income, lower COL = higher savings rate.

| Move From → To | Avg COL Reduction | Savings Rate Boost |
|----------------|-------------------|---------------------|
| SF/NYC → Austin/Raleigh | 30-40% | +15-20% |
| Austin → Tulsa/Knoxville | 20-30% | +10-15% |
| US → Portugal/Mexico/Thailand | 40-60% | +20-30% (if income unchanged) |
| Urban → Rural | 20-35% | +10-20% |

### Sequence of Returns Risk
First 5 years of retirement matter disproportionately. If markets drop 30% in year 1 and you withdraw 4%, you've effectively withdrawn 5.7% of original — recovery is much harder.

**Mitigation strategies**:
1. **Bond tent**: Hold 3-5 years expenses in bonds/cash near retirement
2. **Cash buffer**: 1-2 years living expenses in HYSA
3. **Flexible spending**: Cut variable expenses in down years
4. **Guard rails (Guyton-Klinger)**: Adjust withdrawals based on portfolio performance
5. **Part-time income**: Even small income (Barista FIRE) buffers downside

### Withdrawal Strategies

**Strategy 1: 4% Rule (Trinity Study)**
- Withdraw 4% of initial portfolio, increase by inflation each year
- 30-year success rate: ~95% (60/40 portfolio)
- 50-year success rate: ~85%
- Simple, well-studied

**Strategy 2: 3.5% Rule (Early Retiree Adjustment)**
- For 50+ year retirements
- More conservative, higher success rate
- Adds $$ to FI number (Annual × 28.5)

**Strategy 3: Dynamic Withdrawal (% of current portfolio)**
- Withdraw fixed % (e.g., 4%) of CURRENT portfolio each year
- Never run out, but income varies
- Recommendation: floor + ceiling guardrails

**Strategy 4: Guyton-Klinger Guard Rails**
- Initial: 5% withdrawal
- If portfolio drops 20% below initial path → cut withdrawal 10%
- If portfolio rises 20% above initial path → raise withdrawal 10%
- Allows higher initial rate with safety mechanism

**Strategy 5: Bucket Strategy**
- Bucket 1: 1-2 years cash
- Bucket 2: 3-7 years bonds
- Bucket 3: 8+ years stocks
- Refill from stocks in good years, spend from cash in bad years

## Output: FINANCE-FIRE.md

Write to the current working directory:

```markdown
# FIRE Plan — Path to Financial Independence
**Prepared:** [Date]
**Current Age:** XX | **Annual Spending:** $XX,XXX | **Savings Rate:** XX%

## Executive Summary
- **Target FIRE Variant:** [Lean / Fat / Coast / Barista]
- **Your FI Number:** $X,XXX,XXX
- **Current Portfolio:** $XXX,XXX (X% of FI)
- **Years to FIRE at current savings rate:** XX years (FIRE age: XX)
- **Coast FIRE Number:** $XXX,XXX (already passed? ✅ / behind by $X)
- **Verdict:** [On track / Accelerate needed / Already FI]

## Your Numbers

### Inputs
| Item | Value |
|------|-------|
| Current age | XX |
| Annual spending (today) | $X |
| Current invested assets | $X |
| Annual income (net) | $X |
| Annual savings | $X |
| Savings rate | XX% |
| Expected real return | X% |

### FI Number — All Variants

| Variant | Spending | FI Number | Years Away |
|---------|----------|-----------|------------|
| Lean FIRE | $X (your minimum) | $X | X yrs |
| Standard FIRE | $X (your current) | $X | X yrs |
| Fat FIRE | $X (your comfortable) | $X | X yrs |
| Coast FIRE | n/a | $X (today) | X yrs |
| Barista FIRE (50% expenses) | $X | $X | X yrs |

## Years-to-FIRE Table — The Savings Rate Lever

| Your Savings Rate | Years to FIRE | FIRE Age |
|-------------------|---------------|----------|
| Current (XX%) | XX | XX |
| +5% (to XX%) | XX | XX |
| +10% (to XX%) | XX | XX |
| +15% (to XX%) | XX | XX |
| 50% | XX | XX |
| 70% | XX | XX |

**Key insight**: Increasing your savings rate from XX% to XX% (only $X/month more) cuts X years off your timeline.

## Reference: Savings Rate → Time to FI

| Savings Rate | Years to FIRE |
|--------------|---------------|
| 10% | 51 |
| 20% | 37 |
| 30% | 28 |
| 40% | 22 |
| 50% | 17 |
| 60% | 12.5 |
| 70% | 8.5 |
| 80% | 5.5 |

(Assumes 5% real return, starting from zero. Existing portfolio shortens timeline further.)

## Year-by-Year Portfolio Projection

| Age | Year | Contribution | Portfolio (5%) | Portfolio (7%) | % to FI |
|-----|------|--------------|----------------|----------------|---------|
| XX | YYYY | $X | $X | $X | X% |
| ... | | | | | |
| FIRE | YYYY | $0 | $X | $X | 100% |

## Coast FIRE Status

- **Coast FIRE Number (at your age):** $X
- **Your current portfolio:** $X
- **Coast FIRE achieved?** ✅ Yes / ❌ No (need additional $X)
- **What this means**: [If achieved] You can stop contributing and still retire comfortably at 65. Any savings now accelerates retirement. [If not] You need $X more invested to reach Coast FIRE.

## Barista FIRE Plan

- **Annual expenses portfolio needs to cover:** $X (after part-time income)
- **Barista FI Number:** $X (X% less than full FIRE)
- **Years to Barista FI:** XX
- **Recommended part-time work:** [employer with healthcare benefits like Starbucks, Costco, REI; or freelance covering $X/yr]

## Geographic Arbitrage Opportunities

If location is flexible, consider:
| Move | Estimated COL Reduction | New Savings Rate | New Years to FIRE |
|------|-------------------------|------------------|--------------------|
| Stay current | 0% | XX% | XX yrs |
| Mid-COL US city | -20% | XX% | XX yrs |
| Low-COL US city | -35% | XX% | XX yrs |
| International (Portugal, Mexico, Thailand) | -50% | XX% | XX yrs |

## Withdrawal Strategy Recommendation

Given your timeline (XX years in FIRE) and risk tolerance:

**Recommended: [4% rule / 3.5% rule / Guyton-Klinger / Dynamic]**

| Strategy | SWR | FI Number | Success Rate (50yr) |
|----------|-----|-----------|---------------------|
| 4% Rule | 4.0% | $X | ~85% |
| 3.5% Rule | 3.5% | $X | ~95% |
| Guyton-Klinger | 5.0% start | $X | ~95% (with adjustments) |
| Dynamic (4% of current) | varies | $X | 100% (income varies) |

## Sequence of Returns Risk Mitigation

In the 5 years before AND after FIRE date:
1. Build 2-3 years living expenses in cash/HYSA
2. Hold 5-7 years expenses in bonds (intermediate-term)
3. Plan flexible vs essential spending (cut variable in down years)
4. Consider Barista phase as bridge in early years
5. Don't sell stocks in bear markets — spend from cash/bonds

## Asset Allocation for FIRE

| Phase | Stocks | Bonds | Cash | Rationale |
|-------|--------|-------|------|-----------|
| Accumulation (now to FIRE-5) | 85% | 10% | 5% | Maximize growth |
| Pre-FIRE (5 yrs before) | 70% | 25% | 5% | Build bond tent |
| Early FIRE (years 1-5) | 60% | 30% | 10% | Sequence risk peak |
| Late FIRE (years 6+) | 70% | 25% | 5% | Re-extend horizon |

## Pre-FIRE Checklist (Year of FIRE)
- [ ] 2 years cash buffer in HYSA
- [ ] Healthcare plan locked (ACA exchange / spouse / Barista job)
- [ ] No high-interest debt
- [ ] Mortgage paid down or refinanced low
- [ ] Roth conversion ladder plan written
- [ ] Withdrawal order documented
- [ ] Side income optionality (consulting, freelance)
- [ ] Estate documents updated

## Roth Conversion Ladder (Tax Hack for Early Retirees)
Pre-59.5 access to retirement money without 10% penalty:
1. Roll Traditional 401k → Traditional IRA in year 1 of FIRE
2. Convert $X/year from Traditional IRA → Roth IRA (taxed at low income brackets)
3. After 5-year seasoning, withdraw converted amount penalty-free from Roth
4. Live on taxable + already-converted Roth funds during seasoning years

## Healthcare Strategy (Pre-65)
- **ACA Exchange**: Plan income to maximize subsidies (manage MAGI)
- **HSA**: Max contributions during working years ($X/yr); save receipts for tax-free withdrawals decades later
- **Health Sharing Ministries**: Not insurance, but lower-cost option for healthy individuals
- **Barista FIRE for benefits**: Starbucks, REI, Costco, UPS all offer health insurance to part-timers

## Action Plan

### This Month
1. Calculate current REAL savings rate (use net income, count all savings)
2. Identify $500/month of expense cuts → boost savings rate by X%
3. Open Roth IRA if not yet (highest-priority tax-advantaged for FIRE)

### This Quarter
1. Optimize tax-advantaged stack: 401k match → HSA → Roth IRA → 401k max → taxable
2. Plan geographic arbitrage move (if applicable)
3. Build first month of cash buffer

### This Year
1. Increase savings rate by 5+ percentage points
2. Review allocation toward FIRE-appropriate equity/bond split
3. Read: "The Simple Path to Wealth" (Collins), "Early Retirement Now" SWR series

## Risks & Watch Items
- Sequence of returns in first 5 years post-FIRE
- Healthcare cost overruns (biggest FIRE risk)
- Long-term care need
- Tax law changes (Roth treatment, capital gains rates)
- Sustained inflation above 3%
- Lifestyle inflation reversing your math
- Loss of identity / community when work stops (plan the "retire to" not just "retire from")

---
**DISCLAIMER: For educational/informational purposes only. Not financial advice. Consult a licensed financial advisor before making decisions.**
```

## Output Standards
- Always show the famous savings-rate → years-to-FIRE table
- Calculate ALL four variants (Lean, Fat, Coast, Barista)
- Geographic arbitrage scenarios when relevant
- Specific withdrawal strategy recommendation with reasoning
- Pre-FIRE checklist for the year of pulling the trigger

## Handoff
After writing FINANCE-FIRE.md:
1. State the user's FI number and years to FIRE
2. Identify the #1 lever (savings rate increase, geographic move, income boost)
3. Suggest `/finance budget` if savings rate needs to climb
4. Suggest `/finance retirement` for traditional retirement comparison

**DISCLAIMER: For educational/informational purposes only. Not financial advice. Consult a licensed financial advisor before making decisions.**
