---
name: state-tax-estimator
description: >
  Estimate state income tax liability based on income and state of residence.
---

# State Income Tax Estimator

## Overview

Estimates state income tax based on your total income and state of residence. State income tax rates vary dramatically, from 0% in states like Texas and Florida to 13.3% in California. This skill helps you approximate your state tax bill for planning and quarterly payment purposes.

## Wilson Tools Used

- `spending_summary` — Pull total income (wages, self-employment, investment) for the tax year
- `transaction_search` — Find state tax payments already made (withholding or estimated payments)
- `export_transactions` — Export income and payment data for state return preparation

## Workflow

1. Ask the user for their state of residence (and work state, if different).
2. Use `spending_summary` to determine total gross income for the tax year.
3. Apply standard deductions or known adjustments for the state.
4. Look up the state's tax brackets and calculate the estimated tax.
5. Use `transaction_search` to find state tax payments already made (look for state tax authority names, "state withholding," or similar).
6. Calculate the remaining balance or overpayment.

### States With No Income Tax

These states impose **no state income tax** on earned income:

Alaska, Florida, Nevada, New Hampshire (interest/dividends only, fully repealed as of 2025), South Dakota, Tennessee, Texas, Washington, Wyoming.

**Note:** Washington imposes a 7% capital gains tax on gains exceeding $270,000. New Hampshire historically taxed interest and dividends but phased this out entirely by 2025.

### Representative State Tax Rates (2025, approximate)

| State | Top Marginal Rate | Structure | Notes |
|-------|-------------------|-----------|-------|
| California | 13.3% | Progressive (10 brackets) | Highest in the nation; 1% mental health surcharge above $1M |
| New York | 10.9% | Progressive (9 brackets) | NYC adds 3.078-3.876% |
| New Jersey | 10.75% | Progressive | Kicks in above $1M |
| Oregon | 9.9% | Progressive (4 brackets) | No sales tax offsets higher income tax |
| Minnesota | 9.85% | Progressive (4 brackets) | |
| Massachusetts | 5% flat + 4% surtax | Flat + surtax | 4% surtax on income above $1M (effective 2023) |
| Illinois | 4.95% | Flat rate | |
| Colorado | 4.4% | Flat rate | Reduced from 4.55% in 2024 |
| Arizona | 2.5% | Flat rate | Reduced to flat rate in 2023 |
| North Carolina | 4.5% | Flat rate | Phasing down to 3.99% by 2026 |
| Pennsylvania | 3.07% | Flat rate | One of the lowest flat rates |

### Multi-State Considerations

- If you live in one state and work in another, you generally owe tax to both but receive a credit from your home state for taxes paid to the work state.
- Remote workers: tax obligations depend on both where the work is performed and employer location. Some states have "convenience of the employer" rules (notably New York).
- If you moved mid-year, you may need to file part-year returns in both states.

## Without Wilson

1. Determine your total gross income from all sources.
2. Look up your state's standard deduction (or itemize if your state allows it).
3. Subtract the deduction from gross income to get taxable income.
4. Find your state's current tax brackets at your state Department of Revenue website.
5. Apply the brackets progressively:
   - Example for a progressive state: first $10,000 at 2%, next $30,000 at 4%, remainder at 6%.
   - For flat-rate states: multiply taxable income by the rate.
6. Subtract any state tax credits you qualify for.
7. Subtract withholding and estimated payments already made.
8. The result is your estimated balance due (or refund).

## Important Notes

- State tax brackets, rates, and deductions change frequently. Always verify current rates at your state's Department of Revenue website before filing.
- Some states conform to federal taxable income as a starting point; others calculate state income independently. Deductions allowed federally may not be allowed by your state.
- Local income taxes (city, county) exist in some states (Ohio cities, NYC, Portland, etc.) and are separate from state taxes.
- State estimated tax payments follow similar quarterly schedules to federal but deadlines may differ.
- If you have income in multiple states, consult a tax professional to avoid double taxation and ensure proper credit allocation.
- This is not tax advice. Consult a CPA or tax professional for filing decisions.
