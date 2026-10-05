---
name: spending-review
description: >
  Generate a categorized spending breakdown with month-over-month trends.
---

# Spending Review

## Overview
Produces a categorized breakdown of your spending for a given period, compares it against prior months to show trends, and highlights categories where spending increased or decreased significantly.

## Wilson Tools Used
- `spending_summary` — get total spending grouped by category for any date range
- `transaction_search` — drill into specific categories for transaction-level detail

## Workflow
1. Run `spending_summary` for the current month to get category-level totals.
2. Run `spending_summary` for the previous month to establish a comparison baseline.
3. Calculate the dollar change and percentage change for each category between the two months.
4. Flag any category where spending increased by more than 20% or more than $100.
5. For each flagged category, run `transaction_search` with `category: "<flagged_category>"` and `months: 1` to pull the individual transactions driving the increase.
6. Present results as a summary table with columns: Category, This Month, Last Month, Change ($), Change (%), Trend Arrow.
7. Below the table, list the top 3 categories by absolute spending and the top 3 by percentage increase.
8. Provide a one-paragraph narrative summary describing the overall spending pattern and notable changes.

## Without Wilson
1. Export your last two months of transactions as CSV files from your bank (most banks: Account > Statements > Download > CSV format).
2. Open both CSVs in Google Sheets. Combine them into one sheet with a "Month" column added.
3. If your bank doesn't categorize transactions, manually add a "Category" column. Common categories: Groceries, Dining, Transportation, Utilities, Entertainment, Shopping, Health, Subscriptions.
4. Create a pivot table: Rows = Category, Columns = Month, Values = SUM of Amount.
5. Add a calculated column for change: `=B2-C2` (this month minus last month).
6. Add a percentage change column: `=IF(C2<>0, (B2-C2)/ABS(C2)*100, "New")`.
7. Conditional format the change column: red for increases, green for decreases (since spending is negative, reverse the logic or use absolute values).
8. Sort by absolute change descending to see your biggest movers.
9. For a quick visual, insert a bar chart from the pivot table showing this month vs. last month by category.

## Important Notes
- Category accuracy depends on your bank's auto-categorization or Wilson's categorization rules. Run the `categorize` tool first if many transactions are uncategorized.
- One-time large purchases (appliances, travel, medical) can skew month-over-month comparisons. Consider whether a spike is a true trend or an outlier.
- For a more meaningful view, compare against a 3-month rolling average rather than just the prior month.
