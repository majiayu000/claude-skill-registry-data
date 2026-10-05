---
name: invoice-aging
description: >
  Track unpaid invoices by age bucket and flag overdue payments.
---

# Invoice Aging Report

## Overview
Analyze accounts receivable by sorting outstanding invoices into aging buckets: Current (0-30 days), 31-60 days, 61-90 days, and 90+ days. Identifies clients with chronically late payments and calculates total exposure.

## Wilson Tools Used
- `transaction_search` — find payment transactions matched to known clients or invoice references, identify gaps where expected payments are missing

## Workflow
1. Ask for the list of outstanding invoices (client name, invoice amount, invoice date, due date) or ask the user to describe their invoicing pattern.
2. Use `transaction_search` to find all incoming payments from each client over the past 6 months.
3. Cross-reference received payments against known invoice amounts and dates.
4. For each unpaid or partially paid invoice, calculate days outstanding from the due date.
5. Sort into aging buckets:

```
ACCOUNTS RECEIVABLE AGING — as of [Date]
═══════════════════════════════════════════════════════
Client          Current   31-60    61-90     90+     Total
────────────────────────────────────────────────────────
Acme Corp       $2,500      —        —        —     $2,500
Beta LLC            —    $1,800      —        —     $1,800
Gamma Inc           —       —     $3,200      —     $3,200
Delta Co            —       —        —     $5,000   $5,000
────────────────────────────────────────────────────────
TOTALS          $2,500   $1,800   $3,200   $5,000  $12,500
% of Total       20.0%    14.4%    25.6%    40.0%    100%
═══════════════════════════════════════════════════════
```

6. Flag any client with invoices in the 90+ bucket.
7. Calculate weighted average days outstanding.
8. Recommend follow-up actions: send reminder (31-60), escalate (61-90), consider collections (90+).

## Without Wilson
1. Export your invoice list from your invoicing tool (QuickBooks: Reports > Customers & Receivables > A/R Aging Summary; FreshBooks: Reports > Accounts Aging; Wave: Reports > Aged Receivables).
2. If no invoicing tool, create a spreadsheet with columns: Client, Invoice #, Amount, Invoice Date, Due Date, Paid Date, Paid Amount.
3. Calculate days outstanding: `=IF(PaidDate="", TODAY()-DueDate, PaidDate-DueDate)`.
4. Assign buckets with: `=IF(DaysOutstanding<=0,"Current",IF(DaysOutstanding<=30,"Current",IF(DaysOutstanding<=60,"31-60",IF(DaysOutstanding<=90,"61-90","90+"))))`.
5. Pivot table: Rows = Client, Columns = Bucket, Values = Sum of Amount.
6. For weighted average: `=SUMPRODUCT(Amount,DaysOutstanding)/SUM(Amount)`.

## Important Notes
- Wilson tracks cash transactions, not invoices directly. This skill works best when you can provide a list of issued invoices to cross-reference against bank deposits.
- Partial payments should be tracked. If an invoice is $5,000 and $3,000 was received, the remaining $2,000 is still outstanding.
- Consider offering early payment discounts (e.g., 2/10 Net 30) for clients consistently in the 61-90+ buckets.
