---
name: home-office-deduction
description: >
  Calculate home office deduction using simplified or actual expense method.
---

# Home Office Deduction

## Overview

Calculates the home office deduction (Form 8829 or simplified method) for self-employed individuals who use part of their home regularly and exclusively for business. Two methods are available: the simplified method ($5 per square foot) and the actual expense method (percentage of real housing costs).

## Wilson Tools Used

- `transaction_search` — Find mortgage/rent, utilities, insurance, and repair transactions
- `spending_summary` — Summarize housing-related expenses for the tax year
- `export_transactions` — Export housing expenses for Form 8829 or CPA review

## Workflow

1. Confirm the home office qualifies: the space must be used **regularly and exclusively** for business.
2. Ask for the square footage of the office and the total square footage of the home.
3. Calculate the business-use percentage: `office_sq_ft / total_home_sq_ft`.
4. Choose a method:

### Method 1: Simplified

- Multiply office square footage by $5/sq ft.
- Maximum: 300 sq ft = **$1,500 max deduction**.
- No depreciation, no Form 8829 required.
- Enter on Schedule C, Line 30.

### Method 2: Actual Expenses (Form 8829)

5. Use `transaction_search` to find these expense categories:
   - Mortgage interest or rent
   - Property taxes
   - Homeowners/renters insurance
   - Utilities (electric, gas, water, internet, phone)
   - Repairs and maintenance
   - Depreciation of the home (residential, 27.5-year MACRS for the business-use portion)
6. Use `spending_summary` to total each category for the tax year.
7. Multiply each total by the business-use percentage.
8. Sum all adjusted amounts. This is the actual expense deduction.
9. Compare to the simplified method result and use whichever is larger.

### Comparison

| Factor | Simplified | Actual Expenses |
|--------|-----------|----------------|
| Max deduction | $1,500 | No cap |
| Recordkeeping | Minimal | Must track all housing costs |
| Depreciation | Not allowed | Allowed (but recaptured on sale) |
| Form required | None (report on Schedule C) | Form 8829 |
| Best for | Small offices, simple situations | Large offices, high housing costs |

## Without Wilson

1. Measure your office space in square feet.
2. **Simplified method:** Multiply sq ft (max 300) by $5. That is your deduction.
3. **Actual expense method:**
   - Gather 12 months of mortgage/rent statements, utility bills, insurance declarations, and repair receipts.
   - Sum each category for the year.
   - Calculate business-use percentage: office sq ft / total home sq ft.
   - Multiply each expense category total by the business-use percentage.
   - Add all adjusted amounts together.
   - Fill out Form 8829 and attach to your Schedule C.
4. Compare both methods and use the higher deduction (you can switch methods year to year).

## Important Notes

- "Regular and exclusive use" is strictly enforced. A guest bedroom with a desk in the corner does not qualify unless the desk area is used only for business.
- Employees working from home generally cannot claim this deduction (eliminated for W-2 employees under the Tax Cuts and Jobs Act through 2025). Only self-employed individuals qualify.
- If you use actual expenses and claim depreciation on your home, you may owe depreciation recapture tax when you sell.
- The deduction cannot create a business loss. Any excess carries forward to next year.
- If you rent, use your rent payment instead of mortgage interest and property taxes.
- This is not tax advice. Consult a CPA or tax professional for filing decisions.
