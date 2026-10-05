---
name: tax-prep
description: >
  Organize business expenses by IRS Schedule C categories for tax filing.
---

# Schedule C Tax Prep

## Overview

Categorizes all business expenses into IRS Schedule C line items so you can hand your accountant a clean breakdown or file your own Schedule C (Form 1040). Maps every transaction to the correct deduction line.

## Wilson Tools Used

- `transaction_search` — Find all business expenses within the tax year
- `categorize` — Map transactions to Schedule C line item categories
- `export_transactions` — Export the categorized breakdown for your CPA or tax software

## Workflow

1. Set the date range to the tax year (e.g., January 1 through December 31).
2. Use `transaction_search` to pull all business-related expenses.
3. Use `categorize` to map each expense to a Schedule C line item using the mapping table below.
4. Review unmapped transactions and assign them manually.
5. Use `export_transactions` to generate a Schedule C-ready summary grouped by line item.
6. Cross-check totals against bank and credit card statements.

### Schedule C Line Item Mapping

| Line | Category | Examples |
|------|----------|----------|
| 8 | Advertising | Google Ads, Facebook Ads, print ads, business cards |
| 9 | Car and truck expenses | Gas, repairs, lease payments (if not using standard mileage) |
| 10 | Commissions and fees | Sales commissions, payment processing fees (Stripe, PayPal) |
| 11 | Contract labor | Freelancers, 1099 contractors |
| 13 | Depreciation (Form 4562) | Asset depreciation (see depreciation-schedule skill) |
| 15 | Insurance (other than health) | Business liability, E&O, property insurance |
| 16a | Mortgage interest | Interest on business property mortgage |
| 16b | Other interest | Business loan interest, credit line interest |
| 17 | Legal and professional services | Attorney fees, CPA fees, bookkeeping |
| 18 | Office expense | Office supplies, postage, software subscriptions |
| 19 | Pension/profit-sharing plans | SEP-IRA, SIMPLE IRA employer contributions |
| 20a | Rent — vehicles, machinery, equipment | Equipment leases |
| 20b | Rent — other business property | Office rent, coworking space |
| 22 | Supplies | Materials consumed in business operations |
| 23 | Taxes and licenses | Business licenses, state/local taxes, employer payroll taxes |
| 24a | Travel | Airfare, hotels, car rentals for business travel |
| 24b | Meals | Business meals (50% deductible) |
| 25 | Utilities | Electric, gas, water, phone, internet for business property |
| 27a | Other expenses | Anything not fitting the above (itemize on Part V) |

## Without Wilson

1. Export all transactions from your bank and credit card accounts as CSV files.
2. Open the CSV in a spreadsheet. Add a column called "Schedule C Line."
3. Sort transactions by merchant or description.
4. For each transaction, assign the appropriate line number from the table above.
5. Create a pivot table grouping by Schedule C Line, summing the amounts.
6. For Line 24b (meals), multiply the total by 0.50 to get the deductible amount.
7. Transfer the totals to your Schedule C form or give the spreadsheet to your CPA.

## Important Notes

- Line 24b meals are only 50% deductible. Wilson flags the full amount; you must halve it on the return.
- Mixed-use expenses (personal and business) must be split. Only the business portion goes on Schedule C.
- Keep receipts for any single expense over $75 or any lodging expense regardless of amount.
- If you have a home office, see the home-office-deduction skill for Line 30.
- This is not tax advice. Consult a CPA or tax professional for filing decisions.
