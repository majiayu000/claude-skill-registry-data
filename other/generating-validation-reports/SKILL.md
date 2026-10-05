---
name: generating-validation-reports
description: >-
  Guides writing an audit or fix report that survives interruption, links to the runs before and after it, closes with
  an honest status, and carries what a re-run needs so the loop converges.
when_to_use: >-
  Use when a checker or fixer starts a report file, or when a later run has to read an earlier report to decide what to
  check again.
compatibility: Requires write access to the repository's designated report directory.
---

# Generating Validation Reports

Temporary Files owns where a report lives, how it is named, and that it is written progressively, and its table of
adopter decisions records the timestamp timezone. [Priority and Reporting][priority-and-reporting] owns the fields of a
finding. This skill covers what else a report needs so that someone who never saw the run can act on it.

## Open the File Before the First Check

Create the report before any validation, marked in progress, with a header that answers what a later reader asks first:

- the scope checked, and the revision or content digest it was checked at;
- the run's own identifier, and its timestamp in the recorded timezone; and
- the report this run answers, if any.

A header written at the end is a header lost when the run is.

## Link Runs Through the Header

Keep the file name exactly as Temporary Files sets it, and carry the chain inside the file. A fix report names the audit
report it applies. A re-validation names the fix report it follows. Walking those references from any report recovers
the whole sequence, while file names stay short and every parallel run keeps an identifier of its own.

## Append, Then Close Honestly

Append each finding the moment it is established, and never rewrite an earlier entry. The final step adds totals per
criticality and sets one status: complete, partial, or failed.

A category that could not run is recorded as not run, never as zero findings. A missing count that reads as a clean one
is the failure Fail Closed exists to prevent.

The conversation receives a short summary and the report's path. The findings live in the file.

## Carry What the Next Run Needs

Check-fix loops re-run over the same content, and a report is the only memory between runs.

- **a finding was accepted as a false positive**
  - What the report records: an entry keyed by category, file, and short description, in a list later checkers read
    first
  - Why: the next checker logs a match as previously accepted, uncounted
- **a fix changed files**
  - What the report records: a section listing exactly those files
  - Why: a re-validation can narrow to them
- **a check is non-deterministic**
  - What the report records: its earlier result for unchanged content, marked as carried forward
  - Why: a flaky lookup cannot invent new findings on untouched text
- **an accepted false positive is raised again**
  - What the report records: the finding marked escalated, outside the count
  - Why: the disagreement is a rule question, not another cycle
- **the count has not fallen over several cycles**
  - What the report records: a convergence warning
  - Why: a stalled loop is visible before its ceiling

Narrowing to changed files is safe only for rules that read one file at a time. A rule that compares files, such as
consistency or link targets, re-checks every file it spans, because a fix in one file can break another. Deterministic
and Judgement Validation sets the matching rule for reusing a preflight's unchanged result.

## A Frozen Ledger Is Not a Streamed Report

A quality gate, such as [Rules Quality Gate](../../../repo-governance/workflows/quality/rules-quality-gate.md), follows
the [Ledger][gate-ledger] its contract defines instead. Each of its at most 3 cycles freezes that cycle's blocking rows,
and the gate's propagation, as the writer, rates each row's confidence when it re-validates the row; the checker leaves
that column empty. The rows need no run chain, and every row must reach a status.

For the levels a report carries, see
[Assessing Criticality and Confidence](../assessing-criticality-confidence/SKILL.md).

[priority-and-reporting]:
  ../../../repo-governance/development/quality/evidence/finding-criticality-and-confidence/003-priority-and-reporting.md
[gate-ledger]:
  ../../../repo-governance/development/workflow/quality-gate-contract/003-verdicts-ledger-and-relations.md#ledger
