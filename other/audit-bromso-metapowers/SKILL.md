---
description: Perform a deep-dive review of specific accounts or transactions
---

# Audit

Audit specific accounts or transactions for "$ARGUMENTS". Examine supporting documentation, test balances, and identify discrepancies or irregularities.

## Prerequisites

None — utility skill, run anytime. More effective when ledger data is available from Phase 3 or later.

## Process

1. **Define audit scope:**
   - Which accounts or transaction types are being audited?
   - What period is covered?
   - What is the audit objective? (accuracy, completeness, existence, valuation, disclosure)
   - What materiality threshold applies?

2. **Gather evidence:**
   - Pull account balances and transaction details from the ledger
   - Request supporting documentation (invoices, contracts, confirmations)
   - Identify the population and select a sample (statistical or judgmental)

3. **Perform audit procedures:**
   - **Vouching** — trace recorded transactions back to source documents (tests existence/occurrence)
   - **Tracing** — trace source documents forward to recorded transactions (tests completeness)
   - **Recalculation** — independently recalculate key amounts
   - **Confirmation** — verify balances with third parties (banks, customers, vendors)
   - **Analytical procedures** — compare to expectations, prior periods, or industry benchmarks

4. **Document findings:**
   - For each finding, record:
     - **Condition** — what was found
     - **Criteria** — what was expected
     - **Cause** — why the discrepancy exists
     - **Effect** — financial impact
     - **Recommendation** — corrective action

5. **Write the artifact** to `.metapowers/accounting/$ARGUMENTS/audit.md` with sections:
   - **Audit Scope & Objectives** — what was audited and why
   - **Procedures Performed** — tests conducted and samples selected
   - **Findings** — each finding with condition, criteria, cause, effect, recommendation
   - **Conclusion** — overall assessment of account accuracy and reliability

## Output

The audit written to `.metapowers/accounting/$ARGUMENTS/audit.md`. Present a summary highlighting:
- Number of findings by severity
- Total financial impact of discrepancies
- Key recommendations
