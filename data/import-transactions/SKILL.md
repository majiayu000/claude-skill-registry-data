---
name: import-transactions
description: >
  Import transactions from CSV, OFX, or QIF bank exports and deduplicate.
---

# Import Transactions

## Overview
Import financial transactions from bank export files. Automatically detects file format by extension (.csv, .ofx, .qif) and identifies the bank (Chase, Amex, BofA, or generic) by inspecting column headers. Previews parsed transactions, deduplicates against existing data, and inserts new records.

## Wilson Tools Used
- `transaction_search` — check for existing transactions to prevent duplicates
- `categorize` — apply categorization rules to newly imported transactions

## Workflow
1. Ask the user for the file path to their bank export.
2. Detect the file format by extension:
   - `.csv` — parse as CSV, inspect headers to identify bank
   - `.ofx` / `.qfx` — parse as OFX (Open Financial Exchange)
   - `.qif` — parse as QIF (Quicken Interchange Format)
3. For CSV files, identify the bank by header patterns:
   - **Chase**: `Transaction Date,Post Date,Description,Category,Type,Amount,Memo`
   - **Amex**: `Date,Description,Amount` (or `Reference,Date,Description,Card Member,Amount`)
   - **Bank of America**: `Date,Description,Amount,Running Bal.`
   - **Generic**: any CSV with recognizable date, description, and amount columns
4. Preview the first 5 parsed transactions for the user to confirm.
5. Deduplicate by matching date + amount + description against existing transactions.
6. Report how many new vs. duplicate transactions were found.
7. Insert new transactions into the database.
8. Offer to run `categorize` on the newly imported transactions.

## Without Wilson
You can import transactions manually into any spreadsheet or accounting tool:

### Downloading Exports

**Chase:**
1. Log in at chase.com
2. Go to the account > **Statements & Documents**
3. Click **Download account activity** (top right of transaction list)
4. Select date range and format: **CSV**, **OFX/QFX**, or **QIF**
5. File downloads to your computer

**American Express:**
1. Log in at americanexpress.com
2. Go to **Statements & Activity**
3. Click **Download your Transactions** (right side or under the kebab menu)
4. Select date range, choose **CSV** or **OFX/QFX**
5. Download

**Bank of America:**
1. Log in at bankofamerica.com
2. Go to the account > **Information & Services** tab
3. Click **Download transactions**
4. Select date range and format: **Microsoft Excel (.csv)**, **Quicken (.qfx)**, or **QuickBooks (.qbo)**
5. Download

**Generic / Other Banks:**
Most banks offer CSV or OFX export from their transaction history page. Look for "Download," "Export," or a download icon near the date range selector.

### Manual Import into a Spreadsheet
1. Open the CSV in Excel or Google Sheets.
2. Normalize columns to: `Date`, `Description`, `Amount`, `Category`.
3. Make amounts negative for expenses, positive for income/credits.
4. Remove duplicate rows using **Data > Remove Duplicates** (Excel) or the `=UNIQUE()` function (Sheets).
5. Sort by date.

### OFX/QIF Files
- OFX files are XML-based. You can open them in a text editor to inspect, or import directly into GnuCash, Quicken, or YNAB.
- QIF files are plain text. Each transaction starts with `D` (date), `T` (amount), `P` (payee). You can convert QIF to CSV with online tools like qif2csv.com.

## Important Notes
- Chase CSV exports use negative amounts for payments/credits and positive for charges. Wilson normalizes this (negative = expense, positive = income).
- Amex CSV has amounts where charges are positive. Wilson inverts the sign on import.
- OFX files contain a date range in the header — Wilson uses this to scope deduplication.
- Deduplication is based on date + amount + description. If you manually edited a transaction description in your bank's app, the edited version may import as a new record.
- Large imports (1000+ transactions) are batched in groups of 500 for performance.
