---
name: sales-tax-nexus
description: >
  Determine sales tax obligations by state based on economic nexus thresholds.
---

# Sales Tax Nexus Analysis

## Overview

Analyzes your revenue and transaction volume by state to determine where you have economic nexus and are required to collect and remit sales tax. After the 2018 Supreme Court decision in South Dakota v. Wayfair, most states impose sales tax obligations on remote sellers exceeding certain thresholds.

## Wilson Tools Used

- `transaction_search` — Find revenue transactions and identify customer locations by state
- `spending_summary` — Summarize total revenue by state for threshold comparison
- `export_transactions` — Export state-by-state revenue data for filing or advisor review

## Workflow

1. Use `transaction_search` to pull all revenue (income) transactions for the current or prior calendar year.
2. Group revenue by customer state (based on transaction descriptions, merchant data, or notes).
3. Use `spending_summary` to total revenue and count transactions per state.
4. Compare each state's totals against that state's economic nexus thresholds.
5. Flag any state where you exceed the threshold -- you likely have a collection obligation.
6. Use `export_transactions` to generate a report for your tax advisor or sales tax software.

### Common Economic Nexus Thresholds

Most states use one or both of these triggers (exceed **either** to create nexus):

| Threshold Type | Most Common Level | Notes |
|---------------|-------------------|-------|
| Revenue | $100,000 in sales | Some states use $500K (CA, NY, TX) |
| Transactions | 200 transactions | Not all states use a transaction count |

**States with no sales tax:** AK (no state tax, but local taxes exist), DE, MT, NH, OR.

**Notable exceptions to the $100K / 200 threshold:**
- California: $500,000 revenue only (no transaction count)
- New York: $500,000 revenue AND 100 transactions (must meet both)
- Texas: $500,000 revenue only

### Key Dates

- Nexus is typically measured on a rolling 12-month or prior calendar year basis.
- Once nexus is established, you must register, collect, and remit until you fall below the threshold for a specified period (varies by state).

## Without Wilson

1. Export all revenue transactions from your payment processor (Stripe, PayPal, Shopify, etc.).
2. Add a "Customer State" column based on shipping address or billing address.
3. Create a pivot table: State vs. Sum of Revenue and Count of Transactions.
4. Download the current nexus threshold table from your state's Department of Revenue or a resource like the Sales Tax Institute.
5. Compare each state's revenue and transaction count to the threshold.
6. For any state where you exceed the threshold, register for a sales tax permit and begin collecting.
7. Consider using automated sales tax software (e.g., TaxJar, Avalara) if you have nexus in multiple states.

## Important Notes

- Physical presence (office, warehouse, employee, inventory) still creates nexus regardless of revenue thresholds.
- SaaS and digital goods have different taxability rules by state. Some states tax them, others do not.
- Marketplace facilitators (Amazon, Etsy, eBay) typically collect and remit sales tax on your behalf for sales through their platforms. Those sales may still count toward your nexus threshold in some states.
- Filing frequency (monthly, quarterly, annually) depends on the state and your volume.
- Penalties for not collecting sales tax can include back taxes, interest, and fines. Some states offer voluntary disclosure agreements (VDAs) to limit lookback periods.
- This is not tax advice. Consult a CPA or tax professional for filing decisions.
