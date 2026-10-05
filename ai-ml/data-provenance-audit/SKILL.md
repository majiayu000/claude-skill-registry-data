---
name: data-provenance-audit
description: Use this skill to ensure every material number in a stock analysis is sourced, derived from sourced inputs, user-provided, or explicitly labeled as an assumption. Trigger for valuations, source checks, data lineage, orphan-number audits, existing valuation note reviews, or preventing fabricated financial inputs.
---

# Data Provenance Audit Skill

## Purpose

Ensure every number used in investment analysis is traceable to a human-verifiable source.

## Trigger Examples

- "Audit my AAPL valuation note for orphan numbers."
- "Check whether every number in this stock analysis has a source."
- "Verify data provenance before using these valuation inputs."
- "Find unsourced revenue, FCF, debt, share count, or price assumptions."

## Trigger Conditions

Activate whenever:

- A valuation model is run
- Fundamental metrics are calculated
- A report includes current price, revenue, earnings, cash flow, debt, shares, or margins
- A scorecard uses numerical inputs
- User asks to verify sources or prevent AI-fabricated data

## Required Inputs

- Text, table, report, model input packet, or list of numbers to audit
- Source metadata where available: document, URL/path, filing date, period, provider, and confidence
- Formulas for derived metrics, or enough input IDs to reconstruct them
- User-provided assumptions explicitly marked as assumptions

If the user asks to audit a note but does not provide the note, ask for it or return a blocked audit with the missing input.

## Hard Rule

No orphan numbers.

Every number must be one of:

- Sourced raw data
- Derived data with formula and sourced inputs
- Explicit model assumption
- Explicit user input

Unsourced numbers must not drive valuation.

## Workflow

1. Collect all numerical inputs.
2. Assign data IDs.
3. Attach source metadata.
4. Classify raw / derived / assumption / user input.
5. Check freshness.
6. Check confidence.
7. Reconcile conflicts across sources.
8. Produce Source Annotation Table.
9. Block valuation if critical source data is missing.

## Script Mapping

- Provenance implementation: `scripts/audit/data_provenance_audit.py`
- Input packet schema: `schemas/valuation_input_packet.schema.json`
- Data provenance policy: `references/data_source_policy/data_provenance_policy.md`

## Minimal Output Contract

Return sourced raw data, derived metrics, assumptions/user inputs, and blockers. If a critical number is unsourced, say it cannot drive valuation or action guidance.

## Output

```markdown
## Data Provenance Audit

### Source Annotation Table

| Data ID | Metric | Value | Period | Source | URL / Path | Confidence |
|---|---:|---:|---|---|---|---:|

### Derived Metric Table

| Data ID | Metric | Formula | Input IDs | Result |
|---|---|---|---|---:|

### Unverified / Assumption Table

| Item | Value | Reason | Impact |
|---|---:|---|---|

### Blockers

- Missing source:
- Conflicting source:
- Stale source:
```
