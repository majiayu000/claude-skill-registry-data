---
name: financial-goals
description: >
  Set savings goals with timelines and track monthly progress toward them.
---

# Financial Goals Tracker

## Overview
Helps you define specific savings goals (vacation, down payment, new car, etc.), calculates the required monthly savings for each, tracks progress from your transaction history, and alerts you when you are ahead or behind schedule.

## Wilson Tools Used
- `spending_summary` — determine current savings rate and available capacity for goals
- `transaction_search` — find deposits and transfers related to specific goals

## Workflow
1. Ask the user to define their goals. For each goal, collect: name, target amount, target date, and any dedicated savings account or label.
2. Run `spending_summary` for the last 3 months to calculate average monthly income and average monthly expenses. Derive the current monthly savings rate: `income - expenses`.
3. For each goal, calculate:
   - Months remaining: difference between today and target date
   - Required monthly savings: `(target amount - current progress) / months remaining`
4. Run `transaction_search` with `query: "<goal name> OR <account name>"` and `months: 6` for each goal to find related deposits or earmarked transfers.
5. Sum the deposits found to estimate current progress toward each goal.
6. Present a goals dashboard:

   ```
   FINANCIAL GOALS
   ═══════════════════════════════════════════════════════
   Vacation Fund
     Target: $3,000 by Dec 2026  |  Saved: $1,200 (40%)
     Required: $300/mo  |  On track: YES
     [████████░░░░░░░░░░░░] 40%

   Down Payment
     Target: $40,000 by Jun 2028  |  Saved: $12,000 (30%)
     Required: $1,120/mo  |  On track: NO (-$220/mo)
     [██████░░░░░░░░░░░░░░] 30%
   ═══════════════════════════════════════════════════════
   Total required: $1,420/mo  |  Available: $1,200/mo
   ```

7. If total required monthly savings exceeds available savings rate, flag the shortfall and suggest either extending timelines, reducing targets, or increasing income.
8. Prioritize goals by deadline and suggest an allocation order.

## Without Wilson
1. Open a spreadsheet and create columns: Goal Name, Target Amount, Target Date, Current Balance, Monthly Required.
2. For current balance, check the account(s) designated for each goal. If you use a single savings account for everything, you will need to track allocations manually (one row per goal with a running tally).
3. Calculate months remaining: in Google Sheets, `=DATEDIF(TODAY(), C2, "M")` where C2 is the target date.
4. Monthly required: `=(B2-D2)/E2` where B2 is target, D2 is current balance, E2 is months remaining.
5. Sum the "Monthly Required" column to see your total goal obligations.
6. Check your monthly savings capacity: review last month's bank statement, note total deposits minus total non-savings expenses.
7. If total required exceeds your capacity, either push target dates out or reduce amounts.
8. Apps that help: Ally Bank has built-in "Buckets" for goal tracking. Capital One 360 allows multiple savings accounts. YNAB has explicit goal tracking.
9. Set up automatic transfers for each goal amount on payday to avoid relying on willpower.

## Important Notes
- Wilson tracks transaction activity but does not know your account balances. You must provide starting balances for each goal.
- If you use a single savings account for multiple goals, Wilson cannot distinguish between goal contributions without descriptive memo fields on transfers.
- Reassess goals quarterly. Life changes, and rigid goals that no longer matter will drain motivation.
- Consider prioritizing goals with fixed deadlines (tax payments, tuition) over flexible ones (vacation, new car).
