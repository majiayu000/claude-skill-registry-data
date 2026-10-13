---
name: document-review
description: Use when a spec or plan document exists and needs a focused review for gaps, scope bloat, missing constraints, or risky assumptions. To interrogate the author about the plan instead, use grilling.
---

# Document Review

Review the document itself before using it as a source of truth.

## Workflow

1. Read the document and classify it as spec or plan.
2. Check it against current repo context and any authoritative project docs.
3. Look for:
   - internal inconsistency
   - missing constraints or unverifiable claims
   - scope bloat
   - missing tests or verification
   - security, data, or performance risks when relevant
4. Report findings by default — a review does not edit the document. Apply unambiguous wording or structure fixes inline only when the user asked for the review to be applied (or the invoking workflow says so).
5. Surface decision-level issues instead of rewriting intent, even when applying.
6. This review can itself be the independent pass. Add another reviewer only for a distinct material risk or an explicit requirement, following the shared delegation policy.
