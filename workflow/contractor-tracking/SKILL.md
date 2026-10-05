---
name: contractor-tracking
description: >
  Monitor 1099 contractor payments and flag $600 threshold.
---

# 1099 Contractor Payment Tracking

## Overview
Track payments to independent contractors throughout the tax year. Total payments by vendor, flag anyone approaching or exceeding the $600 IRS reporting threshold, and prepare data for 1099-NEC filing.

## Wilson Tools Used
- `transaction_search` — find all payments to contractor-related vendors by name or category
- `export_transactions` — export contractor payment details for tax filing preparation

## Workflow
1. Ask for the tax year (defaults to current year) and any known contractor names or payment categories.
2. Use `transaction_search` to find all outgoing payments categorized as contractor, freelancer, consulting, or professional services.
3. Also search by specific vendor names if provided (e.g., "John Smith", "Design LLC").
4. Group results by vendor/payee and sum total payments per vendor for the year.
5. Generate the tracking report:

```
1099-NEC CONTRACTOR TRACKING — Tax Year [Year]
══════════════════════════════════════════════════
Contractor           Payments   YTD Total   Status
──────────────────────────────────────────────────
Jane Smith Design        8      $12,400     REPORTABLE
Mike's IT Services       4       $3,200     REPORTABLE
Sarah Copywriting        2         $550     APPROACHING
Tom Photography          1         $200     Under threshold
──────────────────────────────────────────────────
Total Contractors: 4
Reportable (>=$600): 2
Approaching ($400-$599): 1
Total Contractor Spend: $16,350
══════════════════════════════════════════════════
```

6. Flag contractors as:
   - **REPORTABLE**: Total >= $600 (1099-NEC required)
   - **APPROACHING**: Total $400-$599 (may cross threshold)
   - **Under threshold**: Total < $400
7. Use `export_transactions` to create a CSV of all contractor payments for tax preparation.

## Without Wilson
1. Export your full year of bank transactions as CSV from your bank.
2. In a spreadsheet, filter for outgoing payments (negative amounts in Chase CSV, or debit transactions).
3. Add a "Contractor" column. Manually tag each contractor payment with the contractor's name.
4. Create a pivot table: Rows = Contractor name, Values = Sum of Amount (absolute value).
5. Add a status column: `=IF(ABS(Total)>=600,"REPORTABLE",IF(ABS(Total)>=400,"APPROACHING","Under threshold"))`.
6. For 1099-NEC filing, you need each contractor's legal name, address, and TIN/SSN. Keep a W-9 on file for every contractor you pay.
7. E-file 1099-NECs through IRS FIRE system (fire.irs.gov) or use a service like Tax1099.com, Track1099.com, or QuickBooks 1099 filing. Due date: January 31 of the following year.

## Important Notes
- The $600 threshold applies to payments for services, not goods. Payments to corporations (S-corp, C-corp) are generally exempt unless for legal or medical services.
- Collect W-9 forms from contractors BEFORE making the first payment. Backup withholding (24%) is required if no W-9 is provided.
- This tracks calendar year totals. If you need to check mid-year, specify the date range from January 1 through the current date.
- Payments made via credit card or payment processor (PayPal, Stripe) are reported by the processor on 1099-K, not by you on 1099-NEC.
