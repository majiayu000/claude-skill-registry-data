---
name: tax-penalty-calc
description: >
  Estimate IRS underpayment penalties for missed quarterly tax payments.
---

# Tax Underpayment Penalty Calculator

## Overview

Estimates the IRS underpayment penalty (Form 2210) for taxpayers who did not pay enough estimated tax during the year. The penalty is essentially interest charged on the underpaid amount for each quarter, calculated from the quarterly due date to the payment date or April 15 filing deadline.

## Wilson Tools Used

- `transaction_search` — Find estimated tax payments made to the IRS, EFTPS, or state tax authorities with dates and amounts
- `spending_summary` — Summarize total tax payments for the year
- `export_transactions` — Export payment history for Form 2210 preparation

## Workflow

1. Determine the total tax liability for the year (from your completed return or estimate).
2. Calculate the required annual payment (lesser of 90% of current year tax or 100%/110% of prior year tax).
3. Divide the required annual payment by 4 to get the per-quarter minimum.
4. Use `transaction_search` to find all estimated tax payments, noting the date and amount of each.
5. For each quarter, compare what was paid by the due date against the required amount.
6. For any quarter with a shortfall, calculate the penalty:

### Penalty Calculation

```
penalty_per_quarter = underpayment_amount x (annual_rate / 365) x days_late
```

- The IRS penalty rate is set quarterly based on the federal short-term rate + 3 percentage points.
- As of early 2025, the rate is approximately **8% annually** (verify at irs.gov/newsroom for current quarter).
- Days late = number of days from the quarterly due date to the earlier of: the payment date or April 15.

### Quarterly Due Dates and Penalty Periods

| Quarter | Due Date | Penalty Runs Until |
|---------|----------|-------------------|
| Q1 | April 15 | Payment date or April 15 of following year |
| Q2 | June 15 | Payment date or April 15 of following year |
| Q3 | September 15 | Payment date or April 15 of following year |
| Q4 | January 15 | Payment date or April 15 |

### Example

- Required quarterly payment: $5,000
- Q2 payment made: $3,000 (shortfall of $2,000)
- Days from June 15 to April 15 = 304 days
- Penalty: $2,000 x (0.08 / 365) x 304 = **$133.15**

### Exceptions (Penalty May Be Waived)

- Total tax owed is less than $1,000 after withholding and credits.
- You paid at least 100% of prior year tax liability (110% if AGI > $150K).
- The underpayment was due to a casualty, disaster, or other unusual circumstance.
- You retired (after age 62) or became disabled during the tax year.

## Without Wilson

1. Get your total tax liability from Line 24 of Form 1040 (or estimate it).
2. Subtract withholding (Line 25) and credits. The remainder is what estimated payments should have covered.
3. Divide the required amount by 4.
4. List each estimated payment with its date.
5. For each quarter, calculate the shortfall (required minus paid).
6. Multiply: `shortfall x (IRS_rate / 365) x days_from_due_date_to_april_15`.
7. Sum all four quarters. This is your estimated penalty.
8. Compare against the $1,000 threshold and safe harbor rules to see if the penalty applies.
9. File Form 2210 to report the calculation or request a waiver.

## Important Notes

- The IRS penalty rate changes quarterly. Check irs.gov for the rate applicable to each quarter in your tax year.
- State penalties for underpayment are separate and calculated differently. Check your state's rules.
- If your income was uneven, the annualized installment method (Form 2210, Schedule AI) may reduce or eliminate the penalty for earlier quarters.
- Late payment of the balance due on April 15 incurs a separate penalty (0.5% per month) in addition to underpayment penalties on quarterly estimates.
- This is not tax advice. Consult a CPA or tax professional for filing decisions.
