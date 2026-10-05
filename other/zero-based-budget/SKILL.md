---
name: zero-based-budget
description: >
  Allocate every dollar of income to a category using zero-based budgeting.
---

# Zero-Based Budget

## Overview
Creates a zero-based budget where every dollar of income is assigned a job — spending, saving, or debt repayment — until the remaining balance is exactly zero. Analyzes your current spending patterns to create a realistic starting budget, then identifies reallocation opportunities.

## Wilson Tools Used
- `spending_summary` — get current spending by category to inform budget allocations
- `transaction_search` — find income transactions to establish total monthly income

## Workflow
1. Run `transaction_search` with `query: "paycheck OR salary OR direct deposit OR income OR freelance"` and `months: 3` to identify all income sources.
2. Calculate average monthly income from the results. If income is variable, use the lowest of the 3 months as the planning baseline.
3. Run `spending_summary` for the last 3 months to get average spending per category.
4. Build the initial budget template using actual spending as the starting point:

   ```
   ZERO-BASED BUDGET
   ══════════════════════════════════════════════════
   Monthly Income:                         $X,XXX.XX
   ══════════════════════════════════════════════════

   NEEDS (Target: 50% = $X,XXX)
   ──────────────────────────────────────────────────
   Housing/Rent               $X,XXX   (actual: $X,XXX)
   Utilities                  $XXX     (actual: $XXX)
   Groceries                  $XXX     (actual: $XXX)
   Transportation             $XXX     (actual: $XXX)
   Insurance                  $XXX     (actual: $XXX)
   Minimum Debt Payments      $XXX     (actual: $XXX)
   Healthcare                 $XXX     (actual: $XXX)

   WANTS (Target: 30% = $X,XXX)
   ──────────────────────────────────────────────────
   Dining Out                 $XXX     (actual: $XXX)
   Entertainment              $XXX     (actual: $XXX)
   Shopping                   $XXX     (actual: $XXX)
   Subscriptions              $XXX     (actual: $XXX)
   Personal Care              $XXX     (actual: $XXX)

   SAVINGS & DEBT (Target: 20% = $X,XXX)
   ──────────────────────────────────────────────────
   Emergency Fund             $XXX
   Retirement                 $XXX
   Extra Debt Payment         $XXX
   Other Savings Goals        $XXX

   ══════════════════════════════════════════════════
   TOTAL ALLOCATED:                      $X,XXX.XX
   REMAINING TO ASSIGN:                  $0.00
   ══════════════════════════════════════════════════
   ```

5. Compare actual spending to the 50/30/20 guideline. Flag categories where actual exceeds the guideline.
6. If total actual spending exceeds income, identify the largest "wants" categories and suggest reductions to bring the budget to zero.
7. If there is surplus after covering all actuals, suggest allocating it to savings or debt repayment.
8. Present the final budget with all dollars assigned and remaining balance at exactly $0.

## Without Wilson
1. Calculate your monthly take-home pay. If you are salaried, check your pay stub for net pay and multiply by pay frequency (biweekly = x26/12, semi-monthly = x2). If variable, use your lowest recent month.
2. Export one month of transactions from your bank as CSV.
3. In a spreadsheet, categorize every transaction. Create a pivot table summing by category.
4. Open a new sheet and list every category with its actual average. Add a "Budget" column next to it.
5. Start with fixed expenses (rent, utilities, insurance, loan minimums) — these are non-negotiable. Enter them as-is in the Budget column.
6. For variable needs (groceries, gas), set the budget at or slightly below the 3-month average.
7. For wants (dining, entertainment, shopping), set budgets that fit within 30% of income.
8. Allocate remaining dollars to savings and debt categories.
9. Check: `=SUM(BudgetColumn)` should equal your income. If not, adjust until it does.
10. Free tools for ongoing tracking: YNAB (You Need A Budget) is built entirely around zero-based budgeting. EveryDollar (by Ramsey Solutions) is a free alternative.
11. Google Sheets template formula for remaining: `=Income - SUM(B2:B30)` — this cell should read $0.

## Important Notes
- Zero-based budgeting works best when done before each month starts, since every month has different needs (holidays, birthdays, irregular bills).
- The 50/30/20 split is a guideline, not a rule. High cost-of-living areas may require 60%+ on needs.
- If income is irregular (freelance, commission), budget based on the lowest expected month and treat extra income as a bonus to allocate.
- Review and adjust the budget monthly. A budget that does not evolve with your life will be abandoned.
