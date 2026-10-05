---
name: depreciation-schedule
description: >
  Track asset depreciation using MACRS schedules and Section 179 expensing.
---

# Depreciation Schedule

## Overview

Tracks business asset purchases and calculates annual depreciation deductions using the Modified Accelerated Cost Recovery System (MACRS). Also covers Section 179 immediate expensing for qualifying assets. Reports to Schedule C, Line 13 via Form 4562.

## Wilson Tools Used

- `transaction_search` — Find asset purchases (equipment, furniture, vehicles, property)
- `categorize` — Tag transactions as depreciable assets with their asset class
- `export_transactions` — Export asset list and depreciation schedule for Form 4562

## Workflow

1. Use `transaction_search` to find large purchases that qualify as business assets (typically items with a useful life over 1 year).
2. For each asset, determine:
   - Date placed in service
   - Cost basis (purchase price + sales tax + delivery/installation)
   - Asset class and recovery period (see table below)
3. Decide whether to use Section 179 expensing, bonus depreciation, or regular MACRS.
4. Calculate the annual depreciation for each asset.
5. Use `export_transactions` to generate a depreciation schedule for Form 4562.

### MACRS Recovery Periods

| Recovery Period | Asset Class | Examples |
|----------------|-------------|----------|
| 3-year | Certain tools, livestock | Tractor units, rented personal property |
| 5-year | Computers, office equipment | Laptops, printers, copiers, automobiles, light trucks |
| 7-year | Office furniture, fixtures | Desks, chairs, shelving, most machinery |
| 15-year | Land improvements | Parking lots, fences, landscaping |
| 27.5-year | Residential rental property | Rental houses, apartments |
| 39-year | Commercial real property | Office buildings, retail space, warehouses |

### MACRS Depreciation Rates (200% Declining Balance, Half-Year Convention)

**5-Year Property:**

| Year | Rate |
|------|------|
| 1 | 20.00% |
| 2 | 32.00% |
| 3 | 19.20% |
| 4 | 11.52% |
| 5 | 11.52% |
| 6 | 5.76% |

**7-Year Property:**

| Year | Rate |
|------|------|
| 1 | 14.29% |
| 2 | 24.49% |
| 3 | 17.49% |
| 4 | 12.49% |
| 5 | 8.93% |
| 6 | 8.92% |
| 7 | 8.93% |
| 8 | 4.46% |

### Section 179 Expensing

- Allows you to deduct the **full cost** of qualifying assets in the year purchased, instead of depreciating over time.
- 2025 limit: approximately $1,220,000 (adjusted annually for inflation; verify at irs.gov).
- Phase-out begins when total asset purchases exceed approximately $3,050,000.
- Cannot create a business loss -- deduction limited to net business income.
- Applies to tangible personal property (equipment, furniture, vehicles), off-the-shelf software, and certain improvements to nonresidential real property.

### Bonus Depreciation

- 100% bonus depreciation expired after 2022. The rate phases down: 80% (2023), 60% (2024), 40% (2025), 20% (2026), 0% (2027+).
- Applies to new and used property with a recovery period of 20 years or less.
- Can create a business loss (unlike Section 179).

## Without Wilson

1. Create a spreadsheet with columns: Asset Description, Date Placed in Service, Cost Basis, Recovery Period, Method (179/MACRS/Bonus), Annual Depreciation.
2. For each asset, look up the recovery period from the table above.
3. For MACRS, multiply the cost basis by the applicable year's percentage rate.
4. For Section 179, deduct the full cost in year 1 (up to the annual limit).
5. For bonus depreciation, multiply cost basis by the applicable year's bonus rate.
6. Sum all annual depreciation amounts. Enter the total on Schedule C, Line 13.
7. File Form 4562 with your return listing each asset.

## Important Notes

- Land is never depreciable. When purchasing real property, allocate the cost between land and building.
- Vehicles have additional depreciation limits (luxury auto caps). For 2025, the first-year limit for passenger automobiles is approximately $12,400 (verify annually).
- If business use of an asset drops below 50%, you must recapture excess depreciation and switch to straight-line.
- Keep purchase receipts and records of when each asset was placed in service.
- Real property (27.5-year and 39-year) uses straight-line depreciation, not accelerated.
- This is not tax advice. Consult a CPA or tax professional for filing decisions.
