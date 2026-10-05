---
name: year-end-summary
description: >
  Generate an annual financial review with totals, trends, and highlights.
---

# Year-End Summary

## Overview
Comprehensive annual financial review covering full-year income and expenses, monthly trends, category breakdowns, year-over-year comparisons, and financial highlights. Useful for tax preparation, goal setting, and understanding your overall financial picture.

## Wilson Tools Used
- `spending_summary` — monthly and category-level aggregates for the full year
- `transaction_search` — find notable transactions, income sources, largest expenses
- `anomaly_detect` — identify year-level anomalies and trend shifts
- `export_transactions` — export the full report as Markdown or CSV

## Workflow
1. Determine the target year (default: previous calendar year).
2. Use `spending_summary` for each month of the year to build a monthly trend table.
3. Use `spending_summary` for the full year grouped by category.
4. If prior year data exists, pull the same data for year-over-year comparison.
5. Use `transaction_search` to identify:
   - Top 10 largest expenses
   - All income sources and totals
   - Most frequent vendors
   - First and last transactions of the year
6. Use `anomaly_detect` across the full year to find:
   - Months with unusually high or low spending
   - Categories with significant year-over-year changes
7. Compile the report with sections below.
8. Export as Markdown file.

## Report Sections
```
# Year-End Summary — [Year]

## Annual Overview
| Metric | [Year] | [Prior Year] | Change |
|--------|--------|--------------|--------|
| Total Income | $XX,XXX | $XX,XXX | +/-XX% |
| Total Expenses | $XX,XXX | $XX,XXX | +/-XX% |
| Net Savings | $XX,XXX | $XX,XXX | +/-XX% |
| Savings Rate | XX% | XX% | +/-X pts |

## Monthly Trend
| Month | Income | Expenses | Net |
|-------|--------|----------|-----|
| Jan | ... | ... | ... |
| ... | ... | ... | ... |

## Spending by Category (Full Year)
| Category | Amount | % of Total | vs. Prior Year |
|----------|--------|------------|----------------|
| ... | ... | ... | ... |

## Top 10 Expenses
1. ...

## Income Sources
| Source | Total | Frequency |
|--------|-------|-----------|
| ... | ... | ... |

## Year Highlights
- Highest spending month: [Month] ($X,XXX)
- Lowest spending month: [Month] ($X,XXX)
- Biggest single expense: [Description] ($X,XXX)
- Most frequent vendor: [Vendor] (XX transactions)
```

## Without Wilson
To build a year-end summary in a spreadsheet:

1. **Gather data**: Export 12 months of transactions from your bank(s) as CSV. Combine into one sheet.
2. **Monthly trend pivot table**:
   - Rows: Month (use `=TEXT(A2,"YYYY-MM")` to extract)
   - Columns: Income vs. Expense (use `=IF(C2>0,"Income","Expense")`)
   - Values: SUM of Amount
3. **Category pivot table**:
   - Rows: Category
   - Values: SUM of Amount, COUNT of transactions
4. **Year-over-year**:
   - Keep prior year data in a separate tab
   - Use `=VLOOKUP` to pull prior year category totals next to current year
   - Calculate change: `=(Current - Prior) / ABS(Prior) * 100`
5. **Key formulas**:
   ```
   Annual Income:      =SUMPRODUCT((YEAR(A:A)=2025)*(C:C>0)*C:C)
   Annual Expenses:    =ABS(SUMPRODUCT((YEAR(A:A)=2025)*(C:C<0)*C:C))
   Savings Rate:       =(Income-Expenses)/Income*100
   Highest Month:      Use MAX on monthly totals pivot
   Most Frequent:      =INDEX(B:B,MATCH(MAX(COUNTIF(B:B,B:B)),COUNTIF(B:B,B:B),0))
   ```
6. **Export**: Copy the summary tables into a Google Doc or Word document for your records.

## Important Notes
- Year-over-year comparison requires at least partial data from the prior year. If unavailable, that column is omitted.
- Savings rate uses gross income (before taxes) unless you've categorized tax payments separately.
- The report includes all transaction types. Transfers between your own accounts are excluded from income/expense totals if properly categorized.
- This report pairs well with the `tax-deduction-tracker` skill for tax season preparation.
