---
name: seasonal-patterns
description: >
  Detect seasonal revenue and expense patterns across 12+ months of data.
---

# Seasonal Pattern Detection

## Overview
Identify cyclical trends in your revenue and expenses over a 12-month or multi-year window. Reveals which months are historically strong or weak, enabling better cash management, staffing, and marketing timing.

## Wilson Tools Used
- `spending_summary` — pull monthly income and expense totals across 12+ months to build a seasonal profile

## Workflow
1. Ask for the analysis window (minimum 12 months, 24+ months preferred for statistical confidence).
2. Use `spending_summary` for each month in the window to get monthly revenue and expense totals.
3. Calculate the monthly index: Month Index = Month Revenue / Average Monthly Revenue * 100.
   - Index > 100 = above-average month
   - Index < 100 = below-average month
4. Identify peaks and troughs.
5. Generate the seasonal profile:

```
SEASONAL PATTERN ANALYSIS — [Period]
══════════════════════════════════════════════════════════
Month    Avg Revenue   Index   Avg Expenses   Trend
──────────────────────────────────────────────────────────
Jan        $8,200        82      $6,100       Slow start
Feb        $7,800        78      $5,900       ▼ Trough
Mar        $9,500        95      $6,500       Recovering
Apr       $11,200       112      $7,200       ▲ Above avg
May       $12,500       125      $7,800       ▲ Strong
Jun       $13,000       130      $8,200       ▲▲ Peak
Jul       $11,800       118      $7,500       ▲ Above avg
Aug       $10,200       102      $7,000       Average
Sep       $10,500       105      $7,200       Average
Oct       $11,000       110      $7,500       ▲ Above avg
Nov        $9,500        95      $8,500       Expense spike
Dec        $6,800        68      $9,000       ▼▼ Low + high cost
──────────────────────────────────────────────────────────
Annual   $122,000       100     $88,400
Peak Month: June (130)    Trough Month: December (68)
Seasonal Range: 62 points
══════════════════════════════════════════════════════════
```

6. Calculate the seasonal range (peak index - trough index). Over 50 points indicates significant seasonality.
7. Provide actionable recommendations:
   - Build cash reserves during peak months for trough months
   - Time major expenses (equipment, marketing campaigns) for peak-revenue months
   - Consider seasonal pricing or promotions during slow months

## Without Wilson
1. Export 12-24 months of transactions from your bank as CSV.
2. In a spreadsheet, add a `Month` column: `=TEXT(Date,"YYYY-MM")` and a `MonthNum` column: `=MONTH(Date)`.
3. Create a pivot table: Rows = MonthNum, Values = Average of Income, Average of Expenses (use separate columns for multi-year averaging).
4. Overall Average: `=AVERAGE(AllMonthlyRevenues)`.
5. Seasonal Index per month: `=MonthAvgRevenue/OverallAvg*100`.
6. In Google Sheets, create a line chart of monthly revenue with a trendline to visualize the pattern.
7. For statistical detection, use Excel's `=FORECAST.ETS.SEASONALITY(values, timeline)` to auto-detect the seasonal period length.
8. Google Sheets alternative: chart the data and add a polynomial trendline (order 4-6) to see the seasonal curve.

## Important Notes
- You need at least 12 months of data for meaningful seasonal analysis. With only one year, you cannot distinguish seasonal patterns from one-time events. Two or more years dramatically improves confidence.
- Not every business is seasonal. If your seasonal range is under 20 points, your revenue is relatively stable month-to-month.
- Expense seasonality matters too. Insurance renewals, annual software subscriptions, and quarterly tax payments create predictable expense spikes.
- Overlay seasonal patterns onto your cash flow forecast for more accurate projections.
