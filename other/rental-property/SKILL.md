---
name: rental-property
description: >
  Track rental income, expenses, ROI, and cap rate per property.
---

# Rental Property Analysis

## Overview
Calculate key rental property metrics: net operating income (NOI), cash-on-cash return, cap rate, and ROI per property. Tracks rental income against property-specific expenses for Schedule E tax preparation.

## Wilson Tools Used
- `transaction_search` — find all income and expenses related to a specific property by vendor, description, or tag
- `spending_summary` — aggregate property expenses by category (mortgage, insurance, repairs, management fees)
- `export_transactions` — export property-specific transactions for tax filing (Schedule E)

## Workflow
1. Ask for the property (address or name), purchase price, down payment, and current market value. If multiple properties, repeat for each.
2. Use `transaction_search` to find all rental income for the property (tenant payments, security deposits).
3. Use `transaction_search` to find all property expenses (mortgage, insurance, property tax, HOA, repairs, management fees, utilities paid by owner).
4. Use `spending_summary` to aggregate expenses by category for the property.
5. Calculate key metrics:

```
RENTAL PROPERTY ANALYSIS — [Property Name]
══════════════════════════════════════════════════════
Property: 123 Main St, Unit A
Purchase Price: $250,000   Down Payment: $50,000
Current Value: $275,000    Loan Balance: $192,000

ANNUAL INCOME & EXPENSES — [Year]
──────────────────────────────────────────────────────
Gross Rental Income                          $24,000
  Vacancy Loss (est. 5%)                    ($1,200)
Effective Gross Income                       $22,800

Operating Expenses
  Property Tax                              ($3,000)
  Insurance                                 ($1,200)
  Property Management (10%)                 ($2,400)
  Repairs & Maintenance                     ($1,800)
  HOA Fees                                  ($2,400)
  Total Operating Expenses                 ($10,800)

NET OPERATING INCOME (NOI)                   $12,000
  Mortgage Payment (P&I)                   ($11,520)

CASH FLOW (after debt service)                  $480

KEY METRICS
  Cap Rate          = NOI / Purchase Price  =  4.8%
  Cash-on-Cash ROI  = Cash Flow / Down Pmt  =  1.0%
  Total ROI         = (Cash Flow + Equity +
                       Appreciation) / Down  = 18.2%
  Expense Ratio     = OpEx / Gross Income   = 45.0%
  1% Rule Check     = Rent / Price          =  0.8%
══════════════════════════════════════════════════════
```

6. For total ROI, include:
   - Annual cash flow: $480
   - Equity buildup from mortgage principal paydown (check amortization schedule)
   - Appreciation: (Current Value - Purchase Price) / Years Owned, annualized
   - Total ROI = (Cash Flow + Annual Equity Gain + Annual Appreciation) / Total Cash Invested * 100
7. Use `export_transactions` for property-specific transactions to prepare Schedule E.

## Without Wilson
1. Export bank transactions from the account used for the rental property.
2. In a spreadsheet, filter to only property-related transactions. Tag each with the property name if you own multiple.
3. Sum rental income (positive deposits from tenants).
4. Sum operating expenses by category. Common Schedule E categories: advertising, auto/travel, cleaning/maintenance, commissions, insurance, legal/professional, management fees, mortgage interest, repairs, supplies, taxes, utilities.
5. NOI = Gross Rent - Vacancy Allowance - Operating Expenses.
6. Cap Rate = `=NOI/PurchasePrice*100`.
7. Cash-on-Cash = `=(NOI - AnnualMortgagePayments)/DownPayment*100`.
8. For the mortgage principal paydown, check your loan amortization schedule (available from your lender's portal or use bankrate.com/calculators/mortgages/amortization-calculator).
9. For Schedule E filing: IRS Form Schedule E lines map to specific expense categories. Use TurboTax Rental Properties or FreeTaxUSA for guided entry. Depreciation is calculated as Purchase Price (minus land value) / 27.5 years for residential.

## Important Notes
- Cap rate does not include mortgage payments — it measures the property's return independent of financing. Use it to compare properties.
- Cash-on-cash ROI includes financing and measures return on your actual cash invested. It can be negative if mortgage payments exceed NOI.
- The 1% rule (monthly rent should be >= 1% of purchase price) is a quick screening heuristic, not a hard rule. Many profitable properties do not meet it, especially in high-cost markets.
- Depreciation is a non-cash expense that reduces taxable income but not actual cash flow. Residential rental property depreciates over 27.5 years. This is a significant tax benefit not reflected in the cash flow numbers above.
- Track capital improvements separately from repairs. Repairs are expensed immediately; improvements (new roof, HVAC) are depreciated over their useful life.
