---
name: runway-calculator
description: >
  Calculate months of cash runway at current burn rate.
---

# Runway Calculator

## Overview
Determine how many months your business can operate at its current spending rate before running out of cash. Calculates gross burn, net burn, and runway under multiple scenarios (current, lean, growth).

## Wilson Tools Used
- `spending_summary` — calculate average monthly expenses (gross burn) and net burn (expenses minus revenue)
- `transaction_search` — determine current cash position from recent balance and identify trends in burn rate

## Workflow
1. Ask for the current cash balance (or identify from the most recent account balance).
2. Use `spending_summary` for the past 3-6 months to calculate:
   - Gross Burn = average monthly total expenses
   - Monthly Revenue = average monthly total income
   - Net Burn = Gross Burn - Monthly Revenue
3. Use `transaction_search` to check if burn is trending up or down (compare last 3 months vs prior 3 months).
4. Calculate runway under three scenarios:

```
RUNWAY ANALYSIS — as of [Date]
═══════════════════════════════════════════════
Current Cash Balance              $150,000

                    Current   Lean (-20%)   Growth (+30%)
───────────────────────────────────────────────────────────
Gross Burn/mo        $25,000     $20,000       $32,500
Monthly Revenue      $15,000     $15,000       $15,000
Net Burn/mo          $10,000      $5,000       $17,500
Runway (months)         15.0        30.0          8.6
Cash-Out Date        Jul 2027    Oct 2028      Jan 2027
═══════════════════════════════════════════════════════════

Burn Trend: +8% over past 3 months ⚠
```

5. Runway = Cash Balance / Net Burn (monthly).
6. Cash-Out Date = Today + (Runway * 30 days).
7. Flag warning levels:
   - **Green**: 12+ months runway
   - **Yellow**: 6-12 months runway
   - **Red**: Under 6 months runway
8. If net burn is negative (revenue exceeds expenses), report as "Profitable — infinite runway" and show monthly cash accumulation instead.

## Without Wilson
1. Check your current bank balance across all business accounts.
2. Export the last 6 months of transactions as CSV.
3. In a spreadsheet, add a `Month` column: `=TEXT(Date,"YYYY-MM")`.
4. Pivot table: Rows = Month, Values = Sum of expenses (negative amounts), Sum of income (positive amounts).
5. Gross Burn = `=AVERAGE(MonthlyExpenses)` (use absolute values).
6. Avg Revenue = `=AVERAGE(MonthlyIncome)`.
7. Net Burn = `=GrossBurn - AvgRevenue`.
8. Runway = `=CashBalance/NetBurn`. Cash-Out Date = `=TODAY()+(Runway*30)`.
9. For the lean scenario, multiply expenses by 0.8. For growth, multiply by 1.3.
10. Track this monthly in a running spreadsheet. Plot cash balance over time to visualize the glide path.

## Important Notes
- Runway assumes constant burn and revenue. In reality, both fluctuate. Use the 3-month average to smooth noise, but watch the trend.
- Include all cash: checking, savings, money market. Exclude receivables unless collection is near-certain.
- For startups raising funding: investors want to see 18+ months of runway after their investment. Calculate post-raise runway as (Current Cash + Investment) / Net Burn.
- Net burn is what matters, not gross burn. A company spending $50K/month but earning $45K/month has a $5K net burn and 30 months of runway on $150K cash.
