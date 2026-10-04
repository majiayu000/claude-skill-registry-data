---
name: review
description: Review a branch or PR for merge readiness and produce a QA report.
---

# Review

## Invocation

This skill defaults to running in the `QA` persona. If you are not already running as `QA` (for example, the user invoked `/review` directly or you are the parent agent), delegate execution to a `QA` subagent and stop. If you are already running as `QA`, continue with the steps below.

## Objective

Review a branch or PR for merge readiness, document findings, and save the QA report to `docs/qa/reports/{yyyy-mm-dd}-{branch-or-pr-slug}.md`.

## Instructions

1. Ask what to review: PR URL, branch name, or a described set of changes.
2. Compare against your base branch by default.
3. Run or report the most relevant automated checks for the change.
4. Review for:
   - correctness and regressions
   - missing verification
   - risky auth or data handling changes
   - dead code, temporary debugging, or partial cutovers
   - missing documentation where the change needs it
5. Read `templates/qa-report-template.md` and save the report under `docs/qa/reports/`.
6. End with a clear decision, the highest-severity findings, skipped checks if any, and required next actions.

## Decision Levels

- `PASS` when the change is merge-ready
- `PASS WITH RECOMMENDATIONS` when the change can merge but still has non-blocking follow-up
- `BLOCK` when correctness, safety, or required verification is missing
