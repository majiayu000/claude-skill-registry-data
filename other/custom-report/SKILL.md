---
name: custom-report
description: >
  Build custom financial reports with user-defined date ranges and categories.
---

# Custom Report

## Overview
Generate tailored financial reports by specifying date ranges, category filters, transaction types, and output format. Combine spending summaries with transaction-level detail in a single report.

## Wilson Tools Used
- `spending_summary` — aggregate spending by category for the specified period
- `transaction_search` — pull detailed transactions matching filters
- `export_transactions` — export report data to CSV or Markdown

## Workflow
1. Ask the user what the report should cover:
   - **Date range**: specific dates, "last 3 months," "Q1 2025," "year to date"
   - **Categories**: all, specific categories, or exclude certain categories
   - **Transaction type**: expenses only, income only, or both
   - **Minimum amount**: optional threshold (e.g., "only transactions over $50")
2. Use `spending_summary` to generate category-level aggregates for the date range.
3. Use `transaction_search` to pull individual transactions matching the filters.
4. Compile the report with:
   - Summary table (category totals, percentages)
   - Top transactions by amount
   - Transaction count and average per category
   - Date range and filter parameters noted at the top
5. Ask the user for output format: terminal display, Markdown file, or CSV export.
6. If Markdown or CSV, use `export_transactions` to write the file.

## Without Wilson
You can build custom reports in a spreadsheet:

### Google Sheets / Excel Setup
1. Import or paste your transactions into a sheet with columns: `Date`, `Description`, `Amount`, `Category`.
2. **Date filtering**: Add a filter or use `=FILTER(A:D, A:A >= DATE(2025,1,1), A:A <= DATE(2025,3,31))` for Q1 2025.
3. **Category summary pivot table**:
   - Select your data > Insert > Pivot Table
   - Rows: Category
   - Values: SUM of Amount, COUNT of Amount
   - Filter: Date range
4. **Manual summary formulas**:
   ```
   Total Expenses:  =SUMIFS(C:C, C:C, "<0", A:A, ">="&DATE(2025,1,1), A:A, "<="&DATE(2025,3,31))
   Total Income:    =SUMIFS(C:C, C:C, ">0", A:A, ">="&DATE(2025,1,1), A:A, "<="&DATE(2025,3,31))
   Category Total:  =SUMIFS(C:C, D:D, "Groceries", A:A, ">="&DATE(2025,1,1), A:A, "<="&DATE(2025,3,31))
   ```
5. **Top transactions**: Sort by Amount (ascending for biggest expenses) and take the top 10.

### CLI Alternative (csvkit)
```bash
# Filter by date range
csvgrep -c Date -r "2025-0[1-3]" transactions.csv | csvsort -c Amount | head -20
# Summary by category
csvstat -c Amount --group Category transactions.csv
```

## Important Notes
- Date ranges are inclusive on both ends.
- Spending summary shows absolute values (positive numbers) for expenses to improve readability.
- Reports can be re-run with different parameters without re-importing data.
- Markdown export includes a YAML header with report metadata (date generated, filters applied).
