---
description: Consolidate and validate financial data to establish a reliable baseline
---

# Assess

Consolidate and validate financial data for "$ARGUMENTS". Gather historical financials, verify data integrity, and establish the baseline from which all planning begins.

## Prerequisites

None — this is the first phase.

## Process

1. **Ask financial data questions:**
   - What type of business is this? (SaaS, e-commerce, services, marketplace, hardware)
   - What stage? (pre-revenue, early-stage, growth, mature)
   - What financial data is available? (P&L, balance sheet, cash flow, bank statements)
   - What period does the data cover?
   - What accounting method? (cash vs accrual)
   - What currency and fiscal year?

2. **Consolidate data sources:**
   - List all revenue streams and categorize them
   - List all cost categories (fixed, variable, one-time)
   - Identify the chart of accounts or cost centers
   - Note any data gaps or inconsistencies

3. **Validate and reconcile:**
   - Cross-check revenue against bank deposits or invoices
   - Verify expense categories are consistent across periods
   - Flag any anomalies, one-time items, or restatements
   - Calculate basic trends (MoM, YoY growth rates)

4. **Establish baseline metrics:**
   - Monthly Recurring Revenue (MRR) or equivalent
   - Gross margin
   - Burn rate and runway
   - Headcount and revenue per employee

5. **Write the artifact** to `.metapowers/finance/$ARGUMENTS/01-assess.md` with sections:
   - **Business Profile** — type, stage, accounting method, fiscal year
   - **Data Sources** — what data was provided and its quality
   - **Revenue Summary** — streams, trends, seasonality
   - **Cost Summary** — fixed vs variable, major categories
   - **Baseline Metrics** — key financial indicators
   - **Data Gaps** — missing information and impact on planning

## Output

The assessment written to `.metapowers/finance/$ARGUMENTS/01-assess.md`. Present a summary highlighting:
- Business profile and stage
- Revenue and cost structure overview
- Key baseline metrics
- Critical data gaps to resolve
