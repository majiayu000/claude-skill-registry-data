---
name: emergency-fund
description: >
  Calculate emergency fund target and track savings progress toward it.
---

# Emergency Fund Calculator

## Overview
Calculates your emergency fund target based on 3-6 months of essential expenses, tracks your current savings progress, estimates how long it will take to reach your goal at your current savings rate, and suggests ways to accelerate funding.

## Wilson Tools Used
- `spending_summary` — calculate average monthly essential expenses to set the fund target
- `transaction_search` — find savings deposits and current savings activity

## Workflow
1. Run `spending_summary` for the last 3 months to get average monthly spending by category.
2. Identify essential expense categories: Housing/Rent, Utilities, Groceries, Transportation, Insurance, Minimum Debt Payments, Healthcare. Sum these to get your monthly essential expenses.
3. Calculate emergency fund targets:
   - **Minimum (3 months):** monthly essentials x 3
   - **Standard (4 months):** monthly essentials x 4
   - **Comfortable (6 months):** monthly essentials x 6
4. Run `transaction_search` with `query: "savings OR emergency fund OR transfer to savings"` and `months: 6` to find savings deposits.
5. Calculate your average monthly savings deposit amount from the results.
6. Ask the user for their current emergency fund balance.
7. Calculate months to reach each target: `(target - current balance) / average monthly savings deposit`.
8. Present a progress report:

   ```
   Monthly Essential Expenses:  $X,XXX
   Current Emergency Fund:      $X,XXX
   
   Target        Amount     Gap        Months to Goal
   ─────────     ────────   ────────   ──────────────
   3-month       $X,XXX     $X,XXX     X months
   4-month       $X,XXX     $X,XXX     X months
   6-month       $X,XXX     $X,XXX     X months
   
   Progress: [████████░░░░░░░░░░░░] 42%
   ```

9. If the savings rate is low, suggest categories from the spending summary where cuts could accelerate the timeline.

## Without Wilson
1. Export 3 months of bank transactions as CSV.
2. In a spreadsheet, categorize each transaction and filter to essential categories only: rent/mortgage, utilities (electric, gas, water, internet), groceries, transportation (gas, transit passes), insurance premiums, minimum loan payments, and healthcare.
3. Sum essential expenses for each month, then average: `=AVERAGE(B2:B4)` across 3 months.
4. Multiply the average by 3, 4, and 6 for your targets.
5. Check your savings account balance (log into your bank).
6. Calculate how much you saved last month: look at transfers from checking to savings, or compare beginning and ending savings balances on your statement.
7. Divide the gap (`target - current balance`) by your monthly savings amount.
8. To accelerate: review your spending summary for non-essential categories. Common cuts — dining out, subscriptions, shopping — can be redirected to savings.
9. Set up automatic transfers: most banks allow recurring transfers from checking to savings (Settings > Transfers > Recurring).

## Important Notes
- Essential expenses only — do not include dining out, entertainment, or shopping in your emergency fund calculation. You would cut those in an actual emergency.
- If you are self-employed or have irregular income, target 6 months minimum.
- Keep emergency funds in a high-yield savings account (currently 4-5% APY), not invested in stocks.
- If you have high-interest debt (above 8% APR), consider a starter $1,000 emergency fund while focusing on debt payoff, then build to 3-6 months after.
