---
name: lifestyle-creep
description: >
  Detect spending increases across categories over 6-12 months.
---

# Lifestyle Creep Detector

## Overview
Compares your spending categories over a 6-12 month period to identify gradual, often unnoticed increases in spending — the classic "lifestyle creep" that erodes savings as income grows. Highlights which categories have drifted upward and by how much.

## Wilson Tools Used
- `spending_summary` — pull category-level spending for multiple months to compare periods

## Workflow
1. Run `spending_summary` for the most recent 3 months to get current average spending by category.
2. Run `spending_summary` for the 3-month period from 6 months ago (e.g., if now is April 2026, pull October-December 2025) to get the baseline.
3. For each category, calculate:
   - Dollar change: current average - baseline average
   - Percentage change: `(current - baseline) / baseline * 100`
4. Flag any category where spending increased by more than 15% AND more than $50/month. These are lifestyle creep candidates.
5. Sort flagged categories by dollar increase descending.
6. Present results:

   ```
   LIFESTYLE CREEP ANALYSIS (6-month comparison)
   ══════════════════════════════════════════════════════
   Category         6mo Ago    Now        Change    %
   ──────────────   ────────   ────────   ───────   ────
   Dining Out       $280       $420       +$140     +50%  !!
   Shopping         $350       $480       +$130     +37%  !!
   Groceries        $520       $580       +$60      +12%
   Entertainment    $120       $165       +$45      +38%  !
   Transportation   $200       $195       -$5       -3%
   ══════════════════════════════════════════════════════
   Total Creep: +$370/mo  |  Annual Impact: +$4,440/yr
   ```

7. Calculate the total annual impact of all flagged increases.
8. For optional deeper analysis, repeat with a 12-month lookback to separate seasonal patterns from true creep.
9. Suggest a target: "If you returned Dining Out and Shopping to 6-month-ago levels, you would save $3,240/year."

## Without Wilson
1. Export 12 months of transactions from your bank as CSV.
2. Open in Google Sheets. Add a "Month" column using `=TEXT(A2, "YYYY-MM")` where A2 is the transaction date.
3. Create a pivot table: Rows = Category, Columns = Month, Values = SUM of Amount.
4. In a new row below each category, calculate the average of the first 3 months and the last 3 months.
5. Add a "Change" column: `=AVERAGE(last 3 months) - AVERAGE(first 3 months)`.
6. Add a "% Change" column: `=Change / ABS(AVERAGE(first 3 months)) * 100`.
7. Conditional format: highlight any row where Change > $50 AND % Change > 15% in red.
8. Create a line chart for each flagged category to visually confirm the upward trend (select the monthly totals row, Insert > Chart > Line).
9. Common lifestyle creep categories: dining out, coffee shops, clothing, subscription upgrades, grocery store purchases (premium brands replacing store brands), rideshare instead of transit.

## Important Notes
- Not all spending increases are lifestyle creep. Inflation, a new family member, or a necessary expense change are legitimate. Review flagged items in context.
- Seasonal effects can look like creep — holiday spending in Q4, summer travel, back-to-school shopping. The 6-month comparison helps smooth some of this.
- Lifestyle creep is most common after a raise, bonus, or debt payoff. Run this skill within 3 months of any income increase.
- The goal is not to eliminate all increases, but to make them intentional. Spending more on something you value is fine; drifting upward without noticing is the problem.
