---
name: wise-import
description: >
  Import Wise (TransferWise) CSV exports with multi-currency handling.
---

# Wise Import

## Overview
Import transaction data from Wise (formerly TransferWise) CSV statement exports. Handles multi-currency accounts, conversion fees, and international transfers. Maps Wise's transfer-centric format into Open Accountant transactions.

## Wilson Tools Used
- `transaction_search` — check for existing Wise transactions to prevent duplicates
- `categorize` — assign categories to imported Wise transactions
- `export_transactions` — export reconciled Wise data

## Column Mapping

| Wise CSV Column | Open Accountant Field | Notes |
|---|---|---|
| `TransferWise ID` or `ID` | `reference_id` | Unique transfer ID for dedup |
| `Date` | `date` | Completion date |
| `Description` | `description` | Transfer description / recipient |
| `Amount` | `amount` | Transaction amount (signed) |
| `Currency` | `currency` | Source currency ISO code |
| `Running Balance` | — | Not stored |
| `Exchange Rate` | `notes` | Stored in notes for reference |
| `Total fees` | `amount` (separate row) | Wise fee (negative = expense) |

## Workflow
1. Ask the user for the Wise CSV file path and which currency account(s) to import.
2. Parse the CSV and validate Wise column headers.
3. Process each row:
   - **Incoming transfers**: positive amount, category "Income:Transfer"
   - **Outgoing transfers**: negative amount, category based on description
   - **Conversion fees**: separate negative entry, category "Fees:Currency Conversion"
   - **Card payments**: negative amount, categorize by vendor
4. For multi-currency transfers:
   - Record the transaction in the source currency
   - Store the exchange rate and target amount in notes
   - Create the fee entry separately (Wise charges a conversion fee distinct from the exchange rate)
5. Deduplicate using Wise transfer ID.
6. Preview import summary per currency: inflows, outflows, fees, net.
7. Insert transactions and confirm.

## Without Wilson
To work with Wise exports manually:

### Downloading from Wise
1. Log in at **wise.com**
2. Click on the relevant currency account (e.g., USD, EUR, GBP)
3. Go to **Statements** (right side or under account menu)
4. Select the date range
5. Choose **CSV** format (also available: PDF, XLSX)
6. Click **Download**
7. Repeat for each currency account you want to import

### Manual Processing in a Spreadsheet
1. Open the CSV in Google Sheets or Excel.
2. **Identify transaction types** by the Description and Amount sign:
   - Positive amounts = money received (income, incoming transfers)
   - Negative amounts = money sent (expenses, outgoing transfers, card payments)
3. **Separate fees**: Wise embeds fees in certain rows. Look for rows with "fee" in the description or where the Description references a parent transfer.
   - Some Wise CSVs have a `Total fees` column — use this directly.
   - If not, fees appear as separate rows with descriptions like "Conversion fee" or "Transfer fee."
4. **Multi-currency handling**:
   - If you have multiple currency accounts, keep them in separate sheets or add a "Currency" filter.
   - Do NOT sum amounts across currencies without converting first.
   - To convert: `=Amount * ExchangeRate` (use the rate from the Wise statement, not a live rate).
5. **Summary formulas** (per currency):
   ```
   Total Inflows:     =SUMIFS(Amount, Amount, ">0", Currency, "USD")
   Total Outflows:    =ABS(SUMIFS(Amount, Amount, "<0", Currency, "USD"))
   Total Fees:        =ABS(SUMIFS(TotalFees, Currency, "USD"))
   Net:               =Inflows - Outflows
   ```
6. **Reconcile**: The running balance in the last row should match your Wise account balance.

### Alternative: Wise API
For developers, Wise has a public API at `api.transferwise.com` that can pull statements programmatically. Requires an API key from your Wise business account settings.

## Important Notes
- Wise CSV format varies slightly between personal and business accounts. Business accounts include additional columns like `Batch ID` and `Reference`.
- Multi-currency: each currency account exports separately. If you converted USD to EUR, the debit appears in your USD statement and the credit in your EUR statement.
- Wise fees are typically lower than traditional banks (0.3-2% depending on corridor) but they appear as separate line items, not embedded in the exchange rate.
- "Balance cashback" rows are small interest payments from Wise — import these as "Income:Interest".
- Wise card transactions may appear with temporary merchant descriptions that update after settlement. If you import early, descriptions may change.
