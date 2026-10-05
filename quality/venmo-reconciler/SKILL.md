---
name: venmo-reconciler
description: >
  Reconcile Venmo business transactions and separate personal from business.
---

# Venmo Reconciler

## Overview
Import and reconcile Venmo transaction exports, separating personal transfers from business income/expenses. Venmo mixes social payments with business transactions in a single feed — this skill classifies each transaction, flags ambiguous entries for review, and imports business-relevant transactions into Open Accountant.

## Wilson Tools Used
- `transaction_search` — check for duplicates and cross-reference with bank imports
- `categorize` — assign business categories to Venmo transactions
- `anomaly_detect` — flag transactions that look personal in a business context (or vice versa)
- `export_transactions` — export reconciled business transactions

## Column Mapping

| Venmo CSV Column | Open Accountant Field | Notes |
|---|---|---|
| `ID` | `reference_id` | Venmo transaction ID for dedup |
| `Datetime` | `date` | Transaction timestamp |
| `Note` | `description` | User-entered payment note |
| `From` | `description` (prefix) | Sender name |
| `To` | `description` (prefix) | Recipient name |
| `Amount (total)` | `amount` | Signed amount (+ received, - sent) |
| `Status` | — | Only import `Complete` transactions |
| `Type` | — | Payment, Charge, Transfer, etc. |
| `Funding Source` | `notes` | Venmo balance, bank, card |

## Workflow
1. Ask the user for the Venmo CSV file path.
2. Parse the CSV and validate Venmo column headers.
3. Filter by status: only `Complete` transactions.
4. Filter by type:
   - **Import**: `Payment` (sent/received money for goods or services)
   - **Import**: `Charge` (invoiced someone and they paid)
   - **Skip**: `Standard Transfer` and `Instant Transfer` (bank transfers, appear in bank import)
5. Classify each transaction as personal or business:
   - **Business signals**: notes containing keywords like "invoice," "payment for," business name, service description, dollar amounts > $100
   - **Personal signals**: notes with emoji, first-name-only, social language ("thanks for dinner," "splitting rent")
   - **Ambiguous**: flag for manual review
6. Present the classification for user confirmation:
   - Business transactions: import with appropriate categories
   - Personal transactions: skip (or import to a "Personal" category if user wants full tracking)
   - Ambiguous: ask user to classify each one
7. Deduplicate against existing transactions using Venmo ID.
8. Import confirmed business transactions.

## Without Wilson
To reconcile Venmo transactions manually:

### Downloading from Venmo
1. Log in at **venmo.com** (must use web, not the app)
2. Go to **Statements** (under Settings, or navigate to venmo.com/account/statement)
3. Select the date range (available in monthly chunks)
4. Click **Download CSV**
5. Alternative: In the Venmo app > Settings > **Tax Documents** for 1099-K if applicable (only if you exceed IRS thresholds: $5,000 in 2024+)

### Manual Reconciliation in a Spreadsheet
1. Open the CSV. Venmo CSVs have some quirks:
   - The first few rows may be metadata — delete them so your header row is the first row.
   - Amounts may be formatted as `+ $50.00` or `- $25.00` with spaces. Clean with Find & Replace: remove `$`, `+`, and spaces, then convert the column to Number format.
2. **Filter out transfers**: Remove rows where Type is "Standard Transfer" or "Instant Transfer."
3. **Add a "Classification" column** with values: `Business`, `Personal`, `Review`.
4. **Classify by keyword search**:
   ```
   =IF(OR(
     REGEXMATCH(Note,"(?i)invoice|payment for|consulting|freelance|order|service"),
     ABS(Amount)>100
   ), "Business",
   IF(OR(
     REGEXMATCH(Note,"(?i)dinner|lunch|drinks|rent|split|birthday|thanks"),
     LEN(Note)<10
   ), "Personal",
   "Review"))
   ```
5. **Manual review**: Go through "Review" rows and classify each one.
6. **Business summary**:
   ```
   Business Income:   =SUMIFS(Amount, Classification, "Business", Amount, ">0")
   Business Expenses: =ABS(SUMIFS(Amount, Classification, "Business", Amount, "<0"))
   ```
7. **Tax note**: If your Venmo business income exceeds $5,000/year (2024 threshold), Venmo issues a 1099-K. Your records should reconcile with this form.

### Reconciliation Tips
- Cross-reference Venmo transfers to your bank account with your bank statement. The "Standard Transfer" amounts in Venmo should match deposits in your bank.
- If you use Venmo for Business (separate business profile), those transactions are pre-classified — export them separately.

## Important Notes
- Venmo personal vs. business classification is a best-effort heuristic. Always review the results.
- Venmo notes are user-entered free text and often contain emoji, jokes, or vague descriptions. Categorization accuracy depends on note quality.
- The IRS reporting threshold for payment apps is $5,000 for 2024 and later tax years. If you receive business payments via Venmo above this threshold, you'll receive a 1099-K.
- Venmo "Standard Transfer" to your bank takes 1-3 business days. "Instant Transfer" is immediate but has a fee. Neither should be imported as revenue — they're just moving money to your bank.
- If you use both Venmo personal and Venmo for Business profiles, export and import them separately to avoid mixing.
- Venmo CSV downloads are only available through the website, not the mobile app.
