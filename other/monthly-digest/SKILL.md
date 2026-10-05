---
name: monthly-digest
description: >
  Generate a monthly financial summary with metrics, trends, and anomalies.
---

# Monthly Digest

## Overview
Produce a concise monthly financial digest covering income, expenses, savings rate, notable transactions, spending anomalies, and month-over-month trends. Designed to be a quick "state of your finances" snapshot.

## Wilson Tools Used
- `spending_summary` — category-level spending totals for the month
- `transaction_search` — find largest transactions and income entries
- `anomaly_detect` — flag unusual spending patterns or amounts

## Workflow
1. Determine the target month (default: previous calendar month).
2. Use `spending_summary` to get category totals for the month.
3. Use `spending_summary` for the prior month to calculate month-over-month changes.
4. Use `transaction_search` to find:
   - Top 5 largest expenses
   - All income transactions
   - Any new vendors (first-time transactions)
5. Use `anomaly_detect` to flag:
   - Unusual amounts (significantly above category average)
   - New recurring charges
   - Missing expected recurring charges
6. Compile the digest using the template below.
7. Display the digest and optionally export as Markdown.

## Digest Template
```
# Monthly Digest — [Month Year]

## Key Numbers
| Metric | Amount | vs. Last Month |
|--------|--------|----------------|
| Total Income | $X,XXX | +/-XX% |
| Total Expenses | $X,XXX | +/-XX% |
| Net (Income - Expenses) | $X,XXX | — |
| Savings Rate | XX% | +/-X pts |

## Spending by Category
| Category | Amount | % of Total | vs. Last Month |
|----------|--------|------------|----------------|
| ... | ... | ... | ... |

## Top 5 Expenses
1. [Description] — $XXX on [Date]
2. ...

## Anomalies & Alerts
- [flag icon] [Description of anomaly]

## New This Month
- First time seeing: [vendor name]
```

## Without Wilson
To create a monthly digest manually:

1. **Export the month's transactions** from your bank as CSV.
2. **Open in Google Sheets** and add a Category column if missing.
3. **Key numbers**:
   ```
   Total Income:   =SUMIFS(Amount, Amount, ">0", Date, ">="&DATE(2025,3,1), Date, "<="&DATE(2025,3,31))
   Total Expenses: =ABS(SUMIFS(Amount, Amount, "<0", Date, ">="&DATE(2025,3,1), Date, "<="&DATE(2025,3,31)))
   Savings Rate:   =(Income - Expenses) / Income * 100
   ```
4. **Category breakdown**: Create a pivot table grouped by Category, summing Amount.
5. **Top expenses**: Sort by Amount ascending, take the first 5 rows.
6. **Month-over-month**: Keep last month's totals in a separate tab and calculate `=(ThisMonth - LastMonth) / LastMonth * 100` for each category.
7. **Anomaly detection (manual)**: Calculate the average and standard deviation per category over the last 6 months. Flag any category where this month's spending exceeds the average + 2 standard deviations.

## Important Notes
- The digest defaults to the previous calendar month. Ask for a specific month if needed.
- Savings rate is calculated as `(income - expenses) / income`. If income is zero, savings rate is shown as N/A.
- Anomaly detection uses a rolling 6-month window. New users with less history will see fewer anomaly flags.
- The digest does not include transfers between your own accounts (e.g., savings transfers) in the income/expense totals.
