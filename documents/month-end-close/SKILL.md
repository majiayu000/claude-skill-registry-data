---
name: month-end-close
description: >
  Run a monthly bookkeeping close checklist with reconciliation.
---

# Month-End Close

## Overview
A structured checklist for closing your books each month. Ensures all transactions are categorized, anomalies are reviewed, accounts reconcile, and reports are generated before moving on.

## Wilson Tools Used
- `anomaly_detect` — find uncategorized transactions, duplicate entries, and unusual amounts that need review
- `spending_summary` — generate the monthly summary for reconciliation against bank statements
- `categorize` — apply categories to any uncategorized transactions found during close
- `transaction_search` — pull the full month of transactions for review

## Workflow
1. Ask which month is being closed (defaults to previous month).
2. Run the close checklist in order:

**Step 1: Pull all transactions**
Use `transaction_search` for the full month to get the complete transaction set.

**Step 2: Find uncategorized transactions**
Use `anomaly_detect` to identify transactions without categories. Report the count and total dollar amount uncategorized.

**Step 3: Categorize outstanding items**
Use `categorize` to assign categories to uncategorized transactions. Ask the user to confirm any ambiguous ones.

**Step 4: Detect anomalies**
Use `anomaly_detect` to flag duplicates, unusually large transactions, and amounts that deviate significantly from patterns.

**Step 5: Generate monthly summary**
Use `spending_summary` for the month. Compare totals against the bank statement ending balance.

**Step 6: Reconciliation check**
Present the reconciliation:

```
MONTH-END CLOSE — [Month Year]
═══════════════════════════════════════
Checklist                        Status
───────────────────────────────────────
Transactions imported            ✓ 247 transactions
Uncategorized resolved           ✓ 0 remaining
Anomalies reviewed               ✓ 3 flagged, 3 resolved
Duplicates checked               ✓ None found

RECONCILIATION
Bank Statement Ending Balance    $XX,XXX
Wilson Calculated Balance        $XX,XXX
Difference                            $0
Status                           RECONCILED

MONTHLY SUMMARY
Total Income                     $XX,XXX
Total Expenses                  ($XX,XXX)
Net Income                        $X,XXX
═══════════════════════════════════════
```

**Step 7: Archive**
Confirm the month is closed. Recommend exporting a PDF or CSV snapshot for records.

## Without Wilson
1. Download your bank statement PDF for the month (Chase: Statements & Documents; Amex: Statements; most banks: Settings > Documents > Statements).
2. Export the month's transactions as CSV from your bank.
3. Open the CSV in a spreadsheet. Check for blank categories — filter the Category column for blanks.
4. Manually categorize each blank row.
5. Check for duplicates: sort by Amount, then by Date, and look for identical rows.
6. Sum all transactions: `=SUM(Amount)`. Compare to the net change on your bank statement (ending balance minus starting balance).
7. If there is a difference, sort by date and compare line-by-line against the bank statement PDF.
8. Common discrepancies: pending transactions that posted the next month, bank fees not yet downloaded, or split transactions.
9. Save the reconciled spreadsheet with the naming convention: `YYYY-MM-close.xlsx` (e.g., `2026-03-close.xlsx`).

## Important Notes
- Close the books within the first 5 business days of the following month while transactions are fresh.
- The reconciliation step is critical. If Wilson's total and your bank statement do not match, do not skip it. Track down every dollar of difference.
- Keep a running list of recurring items that need manual attention each month (owner draws, transfers between accounts, reimbursements).
- If you have multiple bank accounts or credit cards, close each one separately, then do a combined summary.
