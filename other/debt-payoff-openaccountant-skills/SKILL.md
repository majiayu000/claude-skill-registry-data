---
name: debt-payoff
description: >
  Build avalanche or snowball debt payoff plans with payment schedules.
---

# Debt Payoff Plan

## Overview
Helps you create a structured debt payoff plan using either the avalanche method (highest interest rate first) or snowball method (smallest balance first). Identifies your current debt payments, calculates extra payment capacity from your budget, and generates a month-by-month payoff schedule.

## Wilson Tools Used
- `transaction_search` — find recurring debt payments (loans, credit cards, lines of credit)
- `spending_summary` — calculate total income vs. expenses to find extra payment capacity

## Workflow
1. Run `transaction_search` with `query: "payment OR loan OR credit card OR interest OR minimum"` and `months: 3` to identify recurring debt payments.
2. Group the results by creditor/lender to determine your current monthly payment for each debt.
3. Ask the user to provide for each debt: current balance, interest rate (APR), and minimum payment. Wilson cannot determine balances from transactions alone.
4. Run `spending_summary` for the last 3 months to calculate average monthly income and average monthly expenses.
5. Compute extra payment capacity: `(average monthly income) - (average monthly expenses) - (sum of minimum payments already in expenses)`. If this is negative, flag that the user is overspending.
6. Generate an **Avalanche Plan** — order debts by interest rate descending. Apply all extra payment capacity to the highest-rate debt while paying minimums on all others.
7. Generate a **Snowball Plan** — order debts by balance ascending. Apply all extra payment capacity to the smallest balance while paying minimums on all others.
8. For each plan, produce a month-by-month schedule in this format:

   ```
   Month | Debt Name     | Payment | Principal | Interest | Remaining Balance
   ------+---------------+---------+-----------+----------+------------------
   1     | Credit Card A | $350    | $320.83   | $29.17   | $1,679.17
   1     | Student Loan  | $150    | $112.50   | $37.50   | $14,887.50
   ```

9. Calculate and display: total months to payoff, total interest paid, and total cost for each method.
10. Compare the two methods side by side and recommend the one that saves more in interest (avalanche) or provides faster psychological wins (snowball).

## Without Wilson
1. List all your debts in a spreadsheet with columns: Creditor, Balance, APR, Minimum Payment.
2. Calculate your monthly extra payment: check your bank statement, sum income deposits, subtract all non-debt expenses. Whatever remains beyond minimum payments is your extra payment.
3. For the **avalanche method**: sort the spreadsheet by APR descending. For **snowball**: sort by Balance ascending.
4. In a new sheet, build a payoff schedule. For each month and each debt:
   - Monthly interest = `Balance * (APR / 12)`
   - Payment = minimum payment (+ extra for the target debt)
   - Principal paid = Payment - Interest
   - New Balance = Old Balance - Principal Paid
5. Use these Google Sheets formulas for a single debt amortization:
   - Interest: `=B2*(C2/12)` where B2 is balance, C2 is APR as decimal
   - Principal: `=D2-E2` where D2 is payment, E2 is interest
   - New Balance: `=B2-F2`
6. When one debt reaches $0, redirect its full payment amount to the next debt in your priority order.
7. Free calculators: unbury.me, powerpay.org, or the NerdWallet debt payoff calculator.
8. Total interest comparison: sum the Interest column for each method to see which saves more.

## Important Notes
- Avalanche saves the most money in interest. Snowball provides faster wins by eliminating small debts quickly. Both are valid — choose the one you will stick with.
- This plan assumes fixed interest rates. Variable-rate debts may change your optimal strategy.
- If extra payment capacity is less than $50/month, focus on increasing income or cutting expenses before accelerating debt payoff.
- Do not reduce emergency fund contributions to zero to accelerate debt payoff. A $1,000 starter emergency fund is recommended while paying off debt.
