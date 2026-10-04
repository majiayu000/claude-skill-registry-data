---
description: Compare actual financial results against budget or forecast
---

# Variance

Perform variance analysis for "$ARGUMENTS". Compare actual results to budget, forecast, or prior period and explain the differences.

## Prerequisites

None — utility skill, run anytime. More effective when financial data is available from Phase 7 (statements) or Phase 4 (trial balance).

## Process

1. **Establish comparison basis:**
   - What are we comparing? (actual vs. budget, actual vs. forecast, actual vs. prior period)
   - What level of detail? (total entity, department, account, line item)
   - What period? (month, quarter, year)

2. **Calculate variances:**
   - For each line item, compute:
     - **Dollar variance** — actual minus budget/forecast
     - **Percentage variance** — dollar variance divided by budget/forecast
   - Classify as favorable (F) or unfavorable (U)
   - Highlight variances exceeding materiality thresholds

3. **Analyze root causes:**
   - For each significant variance, identify the driver:
     - Volume variance (more or fewer units)
     - Price variance (higher or lower unit cost/price)
     - Mix variance (different product/service mix)
     - Timing variance (recognized in a different period)
     - One-time items (non-recurring events)
   - Quantify each driver where possible

4. **Write the artifact** to `.metapowers/accounting/$ARGUMENTS/variance.md` with sections:
   - **Variance Summary** — high-level overview of actual vs. budget with key metrics
   - **Detailed Variance Table** — line-by-line comparison with dollar and percentage variances
   - **Root Cause Analysis** — explanation of significant variances
   - **Recommendations** — actions to address unfavorable variances or capitalize on favorable ones

## Output

The variance analysis written to `.metapowers/accounting/$ARGUMENTS/variance.md`. Present a summary highlighting:
- Top favorable and unfavorable variances
- Key root causes identified
- Recommended actions
