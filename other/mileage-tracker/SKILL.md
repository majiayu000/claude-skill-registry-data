---
name: mileage-tracker
description: >
  Track business mileage and calculate IRS standard mileage deduction.
---

# Business Mileage Tracker

## Overview

Tracks business miles driven and calculates the IRS mileage deduction. Cross-references fuel, toll, and parking transactions to validate driving activity. You must choose between the standard mileage rate and actual vehicle expenses for each vehicle -- you cannot use both methods for the same vehicle in the same year.

## Wilson Tools Used

- `transaction_search` — Find gas station, toll, and parking transactions to cross-reference against mileage logs
- `export_transactions` — Export vehicle-related expenses for recordkeeping

## Workflow

1. Ask for the total business miles driven (Wilson cannot track odometer readings directly).
2. Multiply business miles by the current IRS standard mileage rate: **$0.70/mile for 2025** (verify the current year rate at irs.gov).
3. Use `transaction_search` to find transactions matching gas stations, toll charges, and parking fees.
4. Cross-reference driving-related transactions against the mileage log dates to validate consistency.
5. Calculate the deduction: `business_miles x rate_per_mile`.
6. Report the deduction amount for Schedule C, Line 9 (Car and truck expenses).

### Standard Mileage Rate vs. Actual Expenses

| Method | What You Deduct | When to Use |
|--------|----------------|-------------|
| Standard mileage | Miles x IRS rate | Simpler; usually better for fuel-efficient or low-cost vehicles |
| Actual expenses | Gas, insurance, repairs, depreciation, registration, lease payments x business-use % | Better for expensive vehicles with high operating costs |

**You must choose one method per vehicle per year.** If you use standard mileage in the first year a vehicle is placed in service, you can switch to actual expenses later. If you start with actual expenses, you cannot switch to standard mileage for that vehicle.

### Required Mileage Log Fields

The IRS requires contemporaneous records. Each entry should include:

- Date of the trip
- Starting location and destination
- Business purpose of the trip
- Miles driven
- Odometer reading (start and end, at minimum annually)

## Without Wilson

1. Create a spreadsheet with columns: Date, From, To, Purpose, Miles.
2. Log every business trip as it happens (the IRS does not accept reconstructed logs).
3. At year end, sum the Miles column.
4. Multiply total business miles by the current IRS rate (e.g., 1,000 miles x $0.70 = $700).
5. Alternatively, total all actual vehicle expenses and multiply by your business-use percentage (business miles / total miles driven).
6. Enter the deduction on Schedule C, Line 9.
7. Keep the mileage log and supporting receipts for at least 3 years from the filing date.

## Important Notes

- The $0.70/mile rate is for 2025. The IRS adjusts this rate annually, sometimes mid-year. Always verify the current rate before filing.
- Commuting miles (home to regular office) are never deductible. Trips from a home office to a client site are deductible.
- If you use the standard mileage rate, you can still deduct parking fees and tolls separately on top of the mileage deduction.
- For vehicles used both personally and for business, only the business-use percentage is deductible.
- This is not tax advice. Consult a CPA or tax professional for filing decisions.
