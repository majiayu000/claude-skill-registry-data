---
name: hunt-validate-findings
description: Validate hunt conclusions against receipts, contradictory evidence, and success criteria
argument-hint: "[phase]"
allowed-tools: Read, Bash, Write, AskUserQuestion
---

<objective>
Validate the current hunt's findings.

`FINDINGS.md` and `EVIDENCE_REVIEW.md` remain the source of truth for validation.

**Creates or updates:**
- `.planning/FINDINGS.md`
- `.planning/EVIDENCE_REVIEW.md`
- `.planning/STATE.md`

**After this command:** Run `/hunt-publish`.
</objective>

<execution_context>
@.github/thrunt-god/workflows/hunt-validate-findings.md
@.github/thrunt-god/templates/findings.md
@.github/thrunt-god/templates/evidence-review.md
</execution_context>

<process>
Execute the validation workflow from @.github/thrunt-god/workflows/hunt-validate-findings.md.
Mark each hypothesis as supported, disproven, or inconclusive. Call out evidence gaps explicitly.
</process>
