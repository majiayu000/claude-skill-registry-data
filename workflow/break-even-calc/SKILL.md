---
name: break-even-calc
description: >
  Calculate break-even revenue by separating fixed and variable costs.
---

# Break-Even Analysis

## Overview
Determine the revenue level at which total revenue equals total costs (zero profit). Separates expenses into fixed costs (rent, salaries, insurance) and variable costs (materials, commissions, shipping) to calculate the break-even point in both dollars and units.

## Wilson Tools Used
- `spending_summary` — aggregate expenses by category to classify as fixed or variable
- `transaction_search` — pull revenue data and detailed expense transactions for classification

## Workflow
1. Ask for the analysis period (recommend at least 3 months for accuracy) and average selling price per unit if applicable.
2. Use `spending_summary` to get all expense categories and totals.
3. Use `transaction_search` to pull total revenue for the period.
4. Classify each expense category:
   - **Fixed costs**: rent, salaries, insurance, software subscriptions, loan payments — costs that stay the same regardless of sales volume
   - **Variable costs**: materials, shipping, payment processing fees, sales commissions, packaging — costs that scale with sales volume
5. Calculate:
   - Total Fixed Costs per month
   - Variable Cost Ratio = Total Variable Costs / Total Revenue
   - Contribution Margin Ratio = 1 - Variable Cost Ratio
   - Break-Even Revenue = Fixed Costs / Contribution Margin Ratio
   - Break-Even Units = Break-Even Revenue / Price Per Unit (if applicable)
6. Present the analysis:

```
BREAK-EVEN ANALYSIS — [Period]
═══════════════════════════════════════
Monthly Fixed Costs
  Rent                           $2,000
  Salaries                       $8,000
  Software                         $500
  Insurance                        $300
  Total Fixed                   $10,800

Variable Cost Ratio                 35%
Contribution Margin                 65%

BREAK-EVEN REVENUE            $16,615/mo
Break-Even Units              166 units @ $100/unit

Current Revenue               $22,000/mo
Margin of Safety                  24.5%
═══════════════════════════════════════
```

7. Calculate Margin of Safety = (Current Revenue - Break-Even Revenue) / Current Revenue * 100.
8. Show sensitivity: what happens if fixed costs increase 10%, or variable costs rise 5%.

## Without Wilson
1. Export 3+ months of transactions from your bank as CSV.
2. In a spreadsheet, add a "Cost Type" column: mark each expense as "Fixed" or "Variable" (leave income rows blank).
3. Monthly Fixed Costs: `=SUMIFS(Amount, CostType, "Fixed") / NumberOfMonths` (use absolute values).
4. Monthly Variable Costs: `=SUMIFS(Amount, CostType, "Variable") / NumberOfMonths`.
5. Monthly Revenue: `=SUMIFS(Amount, Amount, ">0") / NumberOfMonths`.
6. Variable Cost Ratio: `=VariableCosts/Revenue`.
7. Break-Even Revenue: `=FixedCosts/(1-VariableCostRatio)`.
8. If you sell units at a known price: Break-Even Units = `=BreakEvenRevenue/PricePerUnit`.
9. For a quick check, use the SBA break-even calculator at sba.gov/business-guide/plan-your-business/calculate-your-startup-costs.

## Important Notes
- Some costs are semi-variable (e.g., electricity — base cost is fixed, usage varies). Assign these to whichever category dominates, or split them.
- Break-even assumes a constant product mix. If you sell multiple products at different margins, use a weighted average contribution margin.
- Service businesses often have very low variable costs (mostly labor, which may be fixed). The break-even for a solo consultant is essentially: Fixed Costs / Hourly Rate = Hours needed per month.
- Revisit this analysis quarterly. Fixed costs creep up as you add tools, staff, and space.
