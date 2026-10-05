---
name: finance-report
description: |
  Quarterly or annual financial report with KPI cards, charts, and narrative.
  Use for "financial report", "quarterly report", "earnings", "P&L".
triggers:
  - "financial report"
  - "quarterly report"
  - "earnings report"
  - "P&L"
  - "income statement"
df:
  mode: prototype
  platform: desktop
  scenario: operations
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Finance Report Skill

Produce a financial report page with data visualization.

## Sections
1. **Header** — company name, report period, currency.
2. **Executive summary** — 3–4 sentence narrative.
3. **KPI cards** — Revenue, Net Income, EBITDA, Margin. Big numbers + YoY delta.
4. **Charts** — inline SVG:
   - Revenue trend (line chart, 8 quarters).
   - Expense breakdown (donut/pie chart).
   - Cash flow (stacked bar, 4 quarters).
5. **Detailed tables** — P&L, Balance Sheet highlights. Clean grid, right-aligned numbers.
6. **Footnotes** — accounting policy notes.

## Rules
- Numbers in mono, right-aligned.
- Positive deltas in green, negative in red (use subtle tones, not neon).
- Tables with zebra striping.
- `data-df-id` on each KPI card and chart.

## Output
Single `index.html`, inline CSS.
