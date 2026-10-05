---
name: pricing-optimizer
description: >
  Analyze pricing against costs and margins to optimize profitability.
---

# Pricing Optimizer

## Overview
Compare your current pricing against actual costs to calculate true margins per product or service. Identifies underpriced offerings, estimates the revenue impact of price adjustments, and suggests target pricing based on desired margin.

## Wilson Tools Used
- `spending_summary` — calculate COGS and direct costs per category to determine cost basis
- `transaction_search` — pull revenue by product or service line, identify transaction volumes and average transaction size

## Workflow
1. Ask for the analysis period and list of products/services offered (or detect from transaction categories).
2. Use `transaction_search` to find all revenue transactions, grouped by product/service type.
3. Calculate: average sale price, total units sold, total revenue per offering.
4. Use `spending_summary` to identify direct costs associated with each product/service.
5. Calculate per-offering economics:

```
PRICING ANALYSIS — [Period]
════════════════════════════════════════════════════════════
Product/Service    Avg Price   Unit Cost   Margin   Volume   Revenue
────────────────────────────────────────────────────────────────────
Web Design Pkg      $3,000      $1,200      60%       8     $24,000
Monthly Retainer    $1,500        $900      40%      12     $18,000
Logo Design           $500        $350      30%      15      $7,500
Rush Projects       $2,000      $1,600      20%       5     $10,000
────────────────────────────────────────────────────────────────────
```

6. Flag offerings with margins below 40% as candidates for price increases.
7. For each underpriced offering, calculate the target price for a desired margin:
   - Target Price = Unit Cost / (1 - Desired Margin)
   - Example: $350 cost, 50% target margin = $350 / 0.50 = $700
8. Estimate revenue impact of price changes assuming 0-10% volume loss per 10% price increase.
9. Rank offerings by total profit contribution (margin * volume) to prioritize optimization effort.

## Without Wilson
1. Create a spreadsheet with columns: Product/Service, Price Charged, Direct Cost, Units Sold.
2. Direct Cost includes materials, labor hours * hourly rate, software, and any cost that only exists because of this product.
3. Unit Margin: `=Price-DirectCost`. Margin %: `=UnitMargin/Price*100`.
4. Total Profit: `=UnitMargin*UnitsSold`.
5. Target Price at desired margin: `=DirectCost/(1-DesiredMarginPercent)`.
6. Revenue Impact estimate: `=NewPrice*UnitsSold*0.95` (assuming 5% volume drop per 10% price increase — adjust based on your price sensitivity).
7. For services billed hourly, calculate your effective rate: `=TotalClientPayments/TotalHoursWorked`. Compare to market rates on Glassdoor, Upwork, or industry salary surveys.
8. Use the pricing calculator at priceintelligently.com or profitwell.com/tools for SaaS-specific analysis.

## Important Notes
- Cost-plus pricing (cost + desired margin) is a floor, not a ceiling. Value-based pricing often supports higher prices than cost-plus suggests.
- Volume sensitivity varies wildly. Commodity products are price-sensitive; specialized services are not. A 20% price increase on a niche service may lose 0% of clients.
- Do not optimize purely on margin percentage. A 30% margin on $10,000 deals ($3,000 profit) beats a 60% margin on $500 deals ($300 profit) if volume is similar.
- Test price increases on new clients first before changing existing client rates.
