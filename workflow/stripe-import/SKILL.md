---
name: stripe-import
description: >
  Import Stripe payment CSV exports with charges, fees, and refund handling.
---

# Stripe Import

## Overview
Import transaction data from Stripe CSV exports into Open Accountant. Handles charges (revenue), Stripe processing fees, and refunds as separate line items. Payouts are skipped since they appear in your bank import and would cause double-counting.

## Wilson Tools Used
- `transaction_search` — check for existing Stripe transactions to prevent duplicates
- `categorize` — assign categories to imported Stripe transactions
- `export_transactions` — export reconciled Stripe data

## Column Mapping

| Stripe CSV Column | Open Accountant Field | Notes |
|---|---|---|
| `id` | `reference_id` | Stripe charge ID (ch_xxx) |
| `Created (UTC)` | `date` | Transaction date |
| `Description` | `description` | Customer-facing description |
| `Amount` | `amount` | Gross charge amount (positive = income) |
| `Fee` | `amount` (separate row) | Stripe processing fee (negative = expense) |
| `Net` | — | Calculated field, not stored directly |
| `Currency` | `currency` | 3-letter ISO code |
| `Status` | — | Only import `succeeded` charges |
| `Customer Email` | `notes` | Optional, stored in notes |

## Workflow
1. Ask the user for the Stripe CSV file path.
2. Parse the CSV and validate expected Stripe column headers.
3. Filter rows:
   - **Import**: rows where `Type` is `charge` and `Status` is `succeeded`
   - **Import**: rows where `Type` is `refund`
   - **Skip**: rows where `Type` is `payout` or `transfer` (these appear in bank imports)
   - **Skip**: rows where `Status` is `failed` or `pending`
4. For each charge, create two transactions:
   - **Revenue**: positive amount from the `Amount` column, category "Revenue:Stripe"
   - **Fee**: negative amount from the `Fee` column, category "Fees:Payment Processing"
5. For refunds, create a negative revenue transaction with category "Revenue:Refunds"
6. Deduplicate using the Stripe charge ID (`id` column) as the reference.
7. Preview the import summary: total charges, total fees, total refunds, net revenue.
8. Insert transactions and confirm.

## Without Wilson
To work with Stripe exports manually:

### Downloading from Stripe
1. Log in to **dashboard.stripe.com**
2. Go to **Payments** (left sidebar)
3. Click **Export** (top right of the payments list)
4. Select date range and columns:
   - Recommended: `id`, `Created (UTC)`, `Description`, `Amount`, `Fee`, `Net`, `Currency`, `Status`, `Type`, `Customer Email`
5. Choose **CSV** format and download

### Manual Processing in a Spreadsheet
1. Open the CSV in Google Sheets or Excel.
2. **Filter out non-succeeded**: Data > Filter > Status column > select only "succeeded"
3. **Remove payouts**: Filter Type column > deselect "payout" and "transfer"
4. **Create revenue rows**:
   - Column for category: set to "Revenue:Stripe" for all charge rows
   - Amount column already has the gross charge amount
5. **Create fee rows**: Add rows for each charge with:
   - Same date
   - Description: "Stripe fee — [original description]"
   - Amount: negative value from the Fee column (e.g., if Fee = 2.90, enter -2.90)
   - Category: "Fees:Payment Processing"
6. **Handle refunds**: Refund rows should have negative amounts in the Amount column. Set category to "Revenue:Refunds"
7. **Summary formulas**:
   ```
   Gross Revenue:    =SUMIFS(Amount, Type, "charge", Status, "succeeded")
   Total Fees:       =SUMIFS(Fee, Type, "charge", Status, "succeeded")
   Total Refunds:    =ABS(SUMIFS(Amount, Type, "refund"))
   Net Revenue:      =GrossRevenue - TotalFees - TotalRefunds
   Effective Rate:   =TotalFees / GrossRevenue * 100
   ```
8. **Reconcile with bank**: Your bank payout amounts should equal the sum of `Net` column values between payout dates.

## Important Notes
- Stripe amounts are in the smallest currency unit in the API but in standard units in CSV exports (e.g., $10.00, not 1000).
- Multi-currency: if you accept payments in multiple currencies, each currency is imported with its original amount. Wilson does not perform currency conversion.
- Stripe fee percentage is typically 2.9% + $0.30 per transaction but varies by plan. The actual fee is in the CSV.
- **Do not import payouts.** Payouts are the transfer from Stripe to your bank account. These appear in your bank statement import and importing them from Stripe would double-count the money.
- Connect/platform charges: if you use Stripe Connect, application fees appear as separate line items. Import these under "Fees:Platform" if applicable.
