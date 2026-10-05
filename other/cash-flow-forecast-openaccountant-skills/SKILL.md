---
name: cash-flow-forecast
description: >
  Project future cash flow using historical trends and recurring patterns.
---

# Cash Flow Forecast

## Overview
Project future cash inflows and outflows using a 3-month moving average methodology. Identifies recurring revenue and expenses, detects seasonal patterns, and produces a monthly projection table.

## Wilson Tools Used
- `spending_summary` — get monthly expense totals and category breakdowns for trend analysis
- `anomaly_detect` — identify recurring transactions (subscriptions, regular payments, payroll) that form the predictable baseline
- `transaction_search` — pull historical cash position and transaction data

## Workflow
1. Ask for the forecast horizon (default: 3 months) and current cash balance.
2. Use `transaction_search` to pull the last 6-12 months of transactions.
3. Use `spending_summary` for each of the past 6 months to get income and expense totals.
4. Use `anomaly_detect` to identify recurring transactions (subscriptions, payroll, rent, retainers).
5. Calculate the 3-month moving average for income and expenses:
   - Moving Avg Income = (Month-1 + Month-2 + Month-3) / 3
   - Moving Avg Expenses = (Month-1 + Month-2 + Month-3) / 3
6. Separate recurring (predictable) from variable (estimated) cash flows.
7. Generate the projection:

```
CASH FLOW FORECAST — [Start Month] to [End Month]
══════════════════════════════════════════════════════════
                      Month 1     Month 2     Month 3
──────────────────────────────────────────────────────────
Opening Balance       $XX,XXX     $XX,XXX     $XX,XXX

INFLOWS
  Recurring Revenue    $X,XXX      $X,XXX      $X,XXX
  Variable Revenue     $X,XXX      $X,XXX      $X,XXX
  Total Inflows        $X,XXX      $X,XXX      $X,XXX

OUTFLOWS
  Payroll             ($X,XXX)    ($X,XXX)    ($X,XXX)
  Rent                ($X,XXX)    ($X,XXX)    ($X,XXX)
  Subscriptions         ($XXX)      ($XXX)      ($XXX)
  Variable Expenses   ($X,XXX)    ($X,XXX)    ($X,XXX)
  Total Outflows      ($X,XXX)    ($X,XXX)    ($X,XXX)

NET CASH FLOW          $X,XXX      $X,XXX      $X,XXX
Closing Balance       $XX,XXX     $XX,XXX     $XX,XXX
══════════════════════════════════════════════════════════
```

8. Flag any month where projected closing balance drops below a safety threshold (suggest 2 months of expenses as minimum).

## Without Wilson
1. Export the last 12 months of transactions from your bank as CSV.
2. In Google Sheets, add a `Month` column: `=TEXT(Date,"YYYY-MM")`.
3. Create two pivot tables: one for income by month, one for expenses by month.
4. For the 3-month moving average, use: `=AVERAGE(B2:B4)` sliding across the monthly totals.
5. For recurring items, sort by description and look for entries that repeat monthly. Sum these separately.
6. Build the projection manually: Opening Balance + Avg Income - Avg Expenses = Closing Balance. Closing Balance of Month N = Opening Balance of Month N+1.
7. For a more accurate forecast, use Excel's `=FORECAST.ETS()` function on monthly totals, which handles seasonality automatically.
8. Google Sheets alternative: `=FORECAST(target_date, known_values, known_dates)`.

## Important Notes
- The 3-month moving average smooths volatility but lags behind trend changes. If your business is growing or shrinking rapidly, weight recent months more heavily.
- Forecasts are estimates. Build in a 10-20% buffer on expenses for unexpected costs.
- Seasonal businesses should use 12-month data minimum to capture full cycles. A 3-month average in retail would badly miss holiday spikes.
- This is cash-basis forecasting. Outstanding invoices and unpaid bills are not reflected until money moves.
