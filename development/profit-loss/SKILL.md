---
name: profit-loss
description: >
  Generate a profit and loss statement for any date range.
---

# Profit & Loss Statement

## Overview
Build a standard income statement (P&L) showing revenue, cost of goods sold, gross profit, operating expenses, and net income. Calculates gross margin and net margin percentages.

## Wilson Tools Used
- `transaction_search` — pull all income transactions (positive amounts) and expense transactions (negative amounts) for the target period
- `spending_summary` — aggregate expenses by category to populate operating expense line items

## Workflow
1. Ask for the reporting period (e.g., "Q1 2026" or "January 2026").
2. Use `transaction_search` with `amount > 0` to find all revenue transactions in the period.
3. Use `transaction_search` with `amount < 0` to find all expense transactions.
4. Use `spending_summary` for the same period to get category-level expense totals.
5. Separate COGS categories (materials, supplies, direct labor) from operating expenses (rent, utilities, software, payroll, insurance).
6. Build the P&L using this format:

```
PROFIT & LOSS STATEMENT — [Period]
═══════════════════════════════════════
Revenue
  Sales Revenue                  $XX,XXX
  Service Revenue                $XX,XXX
───────────────────────────────────────
  Total Revenue                  $XX,XXX

Cost of Goods Sold
  Materials                      ($X,XXX)
  Direct Labor                   ($X,XXX)
───────────────────────────────────────
  Total COGS                     ($X,XXX)

GROSS PROFIT                     $XX,XXX
  Gross Margin                      XX.X%

Operating Expenses
  Rent                           ($X,XXX)
  Utilities                        ($XXX)
  Software & Subscriptions         ($XXX)
  Payroll                        ($X,XXX)
  Insurance                        ($XXX)
  Other                            ($XXX)
───────────────────────────────────────
  Total Operating Expenses       ($X,XXX)

NET INCOME                        $X,XXX
  Net Margin                        XX.X%
═══════════════════════════════════════
```

7. Calculate Gross Margin = (Gross Profit / Total Revenue) * 100.
8. Calculate Net Margin = (Net Income / Total Revenue) * 100.

## Without Wilson
1. Export transactions from your bank as CSV (Chase: Accounts > Activity > Download, select CSV; Amex: Statements & Activity > Download Your Transactions).
2. Open in Excel or Google Sheets.
3. Add a "Type" column. Mark each row as Revenue, COGS, or Operating Expense.
4. Use `=SUMIFS(Amount, Type, "Revenue")` for total revenue.
5. Use `=SUMIFS(Amount, Type, "COGS")` for total COGS (use absolute values).
6. Gross Profit = Revenue - COGS. Gross Margin formula: `=GrossProfit/Revenue*100`.
7. Use `=SUMIFS(Amount, Type, "Operating Expense")` for total OpEx.
8. Net Income = Gross Profit - Operating Expenses. Net Margin: `=NetIncome/Revenue*100`.
9. For multi-month P&L, add a `=TEXT(Date,"YYYY-MM")` column and use pivot tables to break out by month.

## Important Notes
- Wilson uses negative amounts for expenses and positive for income. The P&L should display expenses as positive numbers in parentheses.
- COGS vs. operating expense classification depends on your business type. A freelancer may have zero COGS. A product business should separate materials and shipping from overhead.
- This is a cash-basis P&L (based on transaction dates), not accrual. If you invoice Net-30, revenue appears when paid, not when invoiced.
