---
name: smart-split
description: >
  Split a single transaction across multiple categories with custom amounts.
---

# Smart Split

## Overview
Split one transaction into multiple category allocations. Useful for mixed-purpose purchases like a Costco trip that includes groceries, household supplies, and electronics — or a business meal that's partially deductible.

## Wilson Tools Used
- `transaction_search` — find the transaction to split
- `categorize` — assign categories to the resulting split entries

## Workflow
1. Ask the user which transaction to split (by description, date, or amount).
2. Use `transaction_search` to find and confirm the target transaction.
3. Ask how the transaction should be split:
   - By specific dollar amounts (e.g., "$50 groceries, $30 household, $20 electronics")
   - By percentage (e.g., "50% groceries, 30% household, 20% electronics")
4. Validate that split amounts sum to the original transaction amount.
5. Mark the original transaction as a parent/split transaction.
6. Create child transactions for each split portion with:
   - Same date and description as the parent (with category suffix)
   - The allocated amount
   - The assigned category
7. Confirm the split with a summary table.

## Without Wilson
To split transactions manually in a spreadsheet:

1. Find the transaction row (e.g., "COSTCO" for -$100.00).
2. Change the amount in that row to the first split portion (e.g., -$50.00) and set its category (e.g., "Groceries").
3. Insert new rows below for each additional portion:
   | Date | Description | Amount | Category |
   |------|-------------|--------|----------|
   | 2025-03-15 | COSTCO (Groceries) | -50.00 | Groceries |
   | 2025-03-15 | COSTCO (Household) | -30.00 | Household |
   | 2025-03-15 | COSTCO (Electronics) | -20.00 | Electronics |
4. Verify the split: `=SUMIF(B:B,"COSTCO*",C:C)` should equal the original -$100.00.
5. Add a "Split" or "SplitGroup" column with a shared ID so you can trace splits back to the original.

### In YNAB or Mint
- **YNAB**: Click the transaction > "Split" button > add category lines with amounts.
- **Mint (now Credit Karma)**: Click the transaction > "Split transaction" > add categories and amounts.

## Important Notes
- Split amounts must sum exactly to the original transaction amount. Wilson will warn if there's a discrepancy.
- The original transaction is preserved with a `split: true` flag so reports can show either the consolidated or split view.
- Splits cannot be nested (you can't split a split).
- To undo a split, ask Wilson to merge the split entries back into the original transaction.
