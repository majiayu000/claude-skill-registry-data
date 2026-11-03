---
name: accounting-audit
description: Audit specific accounts or transactions — vouching, tracing, recalculation, confirmation and analytical procedures — with each finding's cause, effect and fix. Use when the user suspects a balance is wrong or wants an account tested against its supporting documents. Not for explaining the gap between one account and its statement; see /accounting-reconciliation.
metadata:
  argument-hint: "[project] [--skip-checks]"
---

# Audit

Audit specific accounts or transactions for "$ARGUMENTS". Examine supporting documentation, test balances, and identify discrepancies or irregularities.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"accounting-audit","workflow":"accounting","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

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

5. **Write the artifact** to `.singularskills/accounting/<project>/audit.md` with sections:
   - **Audit Scope & Objectives** — what was audited and why
   - **Procedures Performed** — tests conducted and samples selected
   - **Findings** — each finding with condition, criteria, cause, effect, recommendation
   - **Conclusion** — overall assessment of account accuracy and reliability

## Output

The audit written to `.singularskills/accounting/<project>/audit.md`. Present a summary highlighting:
- Number of findings by severity
- Total financial impact of discrepancies
- Key recommendations

End the artifact with this paragraph, verbatim:

> **Not financial or tax advice.** This artifact is generated analysis for review by a qualified accountant or financial professional before any filing, reporting or decision relies on it.
