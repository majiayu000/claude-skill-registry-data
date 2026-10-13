---
name: code-review
description: Use for substantive code review or to verify and act on review findings. Routine final diff inspection is not a separate review workflow.
---

# Code Review

Review implemented changes against requirements and consequential risks. Routine
final diff inspection follows AGENTS.md without requiring this full workflow.

## Select a mode

- `inline` or combined: review requirements and quality on the supplied scope.
- `spec` / `quality`: a dispatched role with its corresponding verdict contract.
- `re-review`: resolve prior findings and new breakage in the fix delta.
- `feedback`: verify and act on incoming review findings within authorization.

Dispatched reviewers and structured re-reviews use `references/review-contract.md`.
Feedback handling uses `references/feedback.md`; producing a review is read-only,
whereas applying feedback requires implementation authority.

## Establish scope and evidence

Use the supplied diff/package and requirements. Infer an obvious supplied base
or working-tree scope; ask only when the choice changes what should be reviewed.
For uncommitted work, use `git diff <base> -- <owned paths>` and inspect in-scope
untracked files separately. `BASE..HEAD` covers committed work only. Distinguish
pre-existing edits using the task baseline; filenames alone do not establish ownership.

Read enough surrounding code and affected callers to evaluate concrete risks.
Treat implementer reports and reviewer claims as evidence to verify, not authority.
A package saves repeated reads but does not forbid necessary source inspection.
If requirements are missing, state that spec compliance is unverified and review
quality against the known task; do not invent requirements from the diff.

Record failing/unavailable checks with their scope and impact. They may prevent
approval but do not prevent a useful review of inspectable code. Reuse applicable
check evidence; run focused additional checks when a consequential doubt remains.
Read-only review must preserve checkout, index and refs; use permitted isolated
facilities for checks that need mutations.

## Review

Check missing, extra and misunderstood requirements before quality. Examine
correctness, error handling, compatibility, data migration, ownership and relevant
invariants. Judge tests by whether they detect meaningful failures with independent
expectations; changes to tests are not inherently defects. Apply the security
skill's relevant boundary controls for material security changes.

Report actionable defects introduced or exposed by the change, with file/line,
trigger, consequence and evidence. Separate pre-existing issues and uncertainty.
Leave formatting to configured tools; do not treat harmless warnings as defects.

Severity follows consequence: Critical for severe safety/data-loss or operational
failure; Important for acceptance or correctness issues blocking trust; Minor for
nonblocking improvements. Preference alone is not a finding.

End with findings, actual checks, limits and a justified verdict. Explicitly say
when no defects were found; do not invent praise or findings to fill a template.
