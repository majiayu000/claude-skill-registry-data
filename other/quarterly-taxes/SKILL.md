---
name: quarterly-taxes
description: >
  Estimate quarterly tax payments using income totals and safe harbor rules.
---

# Quarterly Tax Estimator

## Overview

Calculates estimated quarterly tax payments for self-employed individuals and business owners filing Form 1040-ES. Uses your year-to-date income, effective tax rate, and IRS safe harbor rules to determine how much to pay each quarter.

## Wilson Tools Used

- `spending_summary` — Pull income totals for the current tax year
- `transaction_search` — Find estimated tax payments already made (IRS, state tax authority)
- `export_transactions` — Export payment history for recordkeeping

## Workflow

1. Use `spending_summary` to get total income received year-to-date.
2. Project annual income: (YTD income / months elapsed) x 12.
3. Determine your effective tax rate. If unknown, use 25-30% as a starting estimate for federal + self-employment tax.
4. Calculate annual estimated tax: projected annual income x effective tax rate.
5. Divide by 4 to get the quarterly payment amount.
6. Use `transaction_search` to find payments already made to "IRS," "EFTPS," "US Treasury," or your state tax authority.
7. Subtract payments already made from the amount due for the current quarter.
8. Apply safe harbor rules (see below) to determine the minimum payment to avoid penalties.

### Quarterly Due Dates (Form 1040-ES)

| Quarter | Income Period | Due Date |
|---------|--------------|----------|
| Q1 | Jan 1 – Mar 31 | April 15 |
| Q2 | Apr 1 – May 31 | June 15 |
| Q3 | Jun 1 – Aug 31 | September 15 |
| Q4 | Sep 1 – Dec 31 | January 15 (following year) |

### Safe Harbor Rules

To avoid underpayment penalties, you must pay the lesser of:

- **100% of prior year tax liability** divided by 4 (110% if prior year AGI exceeded $150K, or $75K if married filing separately)
- **90% of current year tax liability** divided by 4

If your income is uneven throughout the year, you can use the annualized installment method (Form 2210, Schedule AI) to potentially reduce earlier quarter payments.

### Estimation Formula

```
quarterly_payment = (projected_annual_income x effective_tax_rate) / 4
amount_due = quarterly_payment - payments_already_made_this_quarter
```

## Without Wilson

1. Open a spreadsheet. In cell A1, enter your total income received year-to-date.
2. In B1, calculate projected annual income: `=A1 / (MONTH(TODAY()) / 12)`.
3. In C1, enter your effective tax rate as a decimal (e.g., 0.30 for 30%).
4. In D1, calculate quarterly payment: `=B1 * C1 / 4`.
5. In E1, enter estimated tax payments already made this year.
6. In F1, calculate remaining per quarter: `=D1 - (E1 / quarters_remaining)`.
7. Compare against your prior year total tax (from Line 24 of your prior 1040) divided by 4.
8. Pay the lesser of the two amounts to satisfy safe harbor.

## Important Notes

- Self-employment tax (15.3% on 92.35% of net earnings) is separate from income tax. Include it in your effective rate.
- State estimated taxes are separate. Most states follow the same quarterly schedule but check your state's requirements.
- If you also receive W-2 income, you can increase withholding on your W-4 instead of making estimated payments.
- The penalty for underpayment is calculated per quarter, not annually. Late Q1 payments accrue penalties even if Q4 is overpaid.
- This is not tax advice. Consult a CPA or tax professional for filing decisions.
