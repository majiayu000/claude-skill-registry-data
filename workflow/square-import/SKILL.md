---
name: square-import
description: >
  Import Square sales CSV exports with tips, refunds, and fee handling.
---

# Square Import

## Overview
Import transaction data from Square POS CSV exports. Handles sales, tips, refunds, and Square processing fees. Maps Square's item-level detail into Open Accountant's transaction format.

## Wilson Tools Used
- `transaction_search` — check for existing Square transactions to prevent duplicates
- `categorize` — assign categories to imported Square transactions
- `export_transactions` — export reconciled Square data

## Column Mapping

| Square CSV Column | Open Accountant Field | Notes |
|---|---|---|
| `Date` | `date` | Transaction date |
| `Time` | — | Not stored |
| `Transaction ID` | `reference_id` | Square payment ID for dedup |
| `Description` or `Item` | `description` | Item or payment description |
| `Gross Sales` | `amount` | Total before fees (positive = income) |
| `Tips` | `amount` (separate row) | Tip amount (positive = income) |
| `Processing Fees` | `amount` (separate row) | Square fee (negative = expense) |
| `Refunds` | `amount` (separate row) | Refund amount (negative) |
| `Net Sales` | — | Calculated, not stored directly |
| `Payment Method` | `notes` | Cash, card, etc. |

## Workflow
1. Ask the user for the Square CSV file path.
2. Parse the CSV and validate Square column headers.
3. For each transaction row, create up to four entries:
   - **Sale**: gross sales amount (positive), category "Revenue:Sales"
   - **Tips**: tip amount (positive), category "Revenue:Tips" (if > $0)
   - **Fee**: processing fee (negative), category "Fees:Payment Processing" (if > $0)
   - **Refund**: refund amount (negative), category "Revenue:Refunds" (if > $0)
4. Cash transactions have $0 processing fees — still import the sale.
5. Deduplicate using Square Transaction ID.
6. Preview the import summary: total sales, total tips, total fees, total refunds, net.
7. Insert transactions and confirm.

## Without Wilson
To work with Square exports manually:

### Downloading from Square
1. Log in to **squareup.com** (Square Dashboard)
2. Go to **Transactions** (left sidebar)
3. Click **Export** (top right, or the download icon)
4. Select date range
5. Choose **Transactions CSV** (not Items CSV — that's inventory)
6. Download
7. Alternative: **Reporting** > **Sales** > **Export** for summary-level data

### Manual Processing in a Spreadsheet
1. Open the CSV in Google Sheets or Excel.
2. **Separate revenue streams**:
   - Column E: Gross Sales (your product/service revenue)
   - Column F: Tips (income, not taxed the same as sales in some jurisdictions)
   - Column G: Processing Fees (expense)
   - Column H: Refunds (negative revenue)
3. **Create separate category rows** (or use multiple category columns):
   - For each row with a tip > $0, create a new row for the tip amount
   - For each row with a fee > $0, create a new row with the negative fee
4. **Summary formulas**:
   ```
   Gross Sales:       =SUM(E:E)
   Total Tips:        =SUM(F:F)
   Total Fees:        =SUM(G:G)
   Total Refunds:     =SUM(H:H)
   Net Revenue:       =GrossSales + Tips - Fees - Refunds
   Effective Fee %:   =TotalFees / (GrossSales + Tips) * 100
   Avg Transaction:   =GrossSales / COUNTA(D:D)
   ```
5. **Reconcile with bank**: Square deposits funds daily or weekly. Sum Net Sales between deposit dates and match against your bank statement.

### Square Reports (No Export Needed)
Square Dashboard has built-in reports at **Reporting** > **Sales Summary** that show gross sales, fees, and net by day, week, or month. Use these for quick reference without exporting.

## Important Notes
- Square CSV exports can be either transaction-level or item-level. This skill expects transaction-level exports. Item-level exports have one row per item per sale, which requires grouping by Transaction ID first.
- Tips are separated because they may have different tax treatment than sales revenue.
- Cash transactions appear in Square if rung through the POS but have $0 processing fee. These are still imported.
- Square deposits to your bank are net of fees. Do not import deposit rows from your bank as Square revenue — use this skill for the gross breakdown instead.
- If you use Square for both in-person and online sales, both appear in the same export.
