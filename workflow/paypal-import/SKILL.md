---
name: paypal-import
description: >
  Import PayPal CSV exports with fee, refund, and currency handling.
---

# PayPal Import

## Overview
Import transaction data from PayPal CSV exports. Handles payments received, fees, refunds, and currency conversions. PayPal CSVs include many transaction types — this skill filters to financially meaningful entries and maps them to Open Accountant's format.

## Wilson Tools Used
- `transaction_search` — check for duplicates against existing transactions
- `categorize` — assign categories to imported PayPal transactions
- `export_transactions` — export reconciled PayPal data

## Column Mapping

| PayPal CSV Column | Open Accountant Field | Notes |
|---|---|---|
| `Date` | `date` | Transaction date (MM/DD/YYYY format) |
| `Time` | — | Not stored, date is sufficient |
| `Name` | `description` | Counterparty name |
| `Type` | — | Used for filtering (see workflow) |
| `Status` | — | Only import `Completed` transactions |
| `Gross` | `amount` | Transaction amount before fees |
| `Fee` | `amount` (separate row) | PayPal fee (negative = expense) |
| `Net` | — | Calculated, not stored directly |
| `Transaction ID` | `reference_id` | PayPal transaction ID for dedup |
| `Currency` | `currency` | 3-letter ISO code |
| `Subject` or `Item Title` | `notes` | Optional detail |

## Workflow
1. Ask the user for the PayPal CSV file path.
2. Parse the CSV (PayPal uses comma-separated with quoted fields).
3. Filter by transaction type:
   - **Import**: `Payment Received`, `Mobile Payment`, `Website Payment`, `Invoice Received`
   - **Import**: `Refund`, `Reversal`, `Chargeback`
   - **Import**: `Subscription Payment`
   - **Skip**: `Transfer to Bank`, `Bank Deposit` (appears in bank import)
   - **Skip**: `Currency Conversion` (handled as part of the parent transaction)
   - **Skip**: `Authorization`, `Pending`, `Temporary Hold`
4. Filter by status: only `Completed` transactions.
5. For each payment received, create two transactions:
   - **Revenue**: gross amount (positive), category "Revenue:PayPal"
   - **Fee**: fee amount (negative), category "Fees:Payment Processing"
6. For refunds/reversals, create a negative revenue transaction.
7. For currency conversions: attach the conversion rate to the parent transaction notes.
8. Deduplicate using PayPal Transaction ID.
9. Preview and confirm import.

## Without Wilson
To work with PayPal exports manually:

### Downloading from PayPal
1. Log in at **paypal.com**
2. Go to **Activity** (top navigation)
3. Click **Statements** > **Activity download** (or **Reports** > **Activity download** in business accounts)
4. Select date range (max 1 year at a time)
5. File type: **CSV**
6. Click **Download**
7. For business accounts: **Reports** > **All reports** > **Transactions** > select date range > **Download CSV**

### Manual Processing in a Spreadsheet
1. Open the CSV. PayPal CSVs use the encoding Windows-1252 — if you see garbled characters, re-open with UTF-8 encoding.
2. **Filter Status**: Keep only "Completed" rows.
3. **Filter Type**: Remove "Transfer to Bank," "Bank Deposit," "Currency Conversion," and "Authorization" rows.
4. **Split revenue and fees**:
   - For each payment, the Gross column is revenue and the Fee column is the PayPal fee.
   - Create a new row for each fee with the negative fee amount.
5. **Handle refunds**: Refund rows already have negative Gross amounts. Keep as-is.
6. **Currency conversion**: If you received a payment in EUR but your account is in USD, PayPal creates two rows — one in EUR and one with the USD conversion. Use the USD row and note the original currency.
7. **Summary formulas**:
   ```
   Gross Revenue:  =SUMIFS(Gross, Type, "Payment Received", Status, "Completed")
   Total Fees:     =ABS(SUMIFS(Fee, Type, "Payment Received", Status, "Completed"))
   Total Refunds:  =ABS(SUMIFS(Gross, Type, "Refund", Status, "Completed"))
   Net Revenue:    =GrossRevenue - TotalFees - TotalRefunds
   Fee Rate:       =TotalFees / GrossRevenue * 100
   ```

### Reconciliation
- PayPal transfers to your bank should match the sum of Net amounts between transfer dates.
- If they don't match, check for held funds, disputes, or currency conversion differences.

## Important Notes
- PayPal CSV encoding can cause issues. If the file won't parse, try saving as UTF-8 first.
- PayPal date format is MM/DD/YYYY (US accounts) or DD/MM/YYYY (international). Wilson auto-detects based on account locale.
- "General Payment" type in PayPal can be either sent or received — check the sign of the Gross amount.
- PayPal business accounts have more detailed CSVs than personal accounts. The column mapping above covers both.
- Do not import "Transfer to Bank" rows — these are the PayPal-to-bank transfers that appear in your bank statement.
