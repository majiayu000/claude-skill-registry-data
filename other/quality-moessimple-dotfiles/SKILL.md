---
name: quality
description: Runs the project's quality gate and reports only what actually ran.
---

Run `quality` with the arguments from the current request. With no argument, run `quality fast`. `quality fast` already runs
the project's test suite by default (skippable per project via CLAUDE_QUALITY_SKIP_TESTS).
Only run `quality full` when the user explicitly requests the most thorough gate: whole-project
Pint and Rector, not just the dirty files `fast` covers.

Never call vendor/bin/pint, vendor/bin/phpstan, vendor/bin/pest, or vendor/bin/phpunit
directly. Always go through `quality`, so the run gets recorded and clears the pending
marker for this project.

Report PASS only on exit code 0. Exit code 3 means no supported tooling was found in
this project and is never a PASS.

Report in this shape:

## Result

PASS | FAIL | NOT CONFIGURED | NOT RUN

## Context

- Gate: `quality <mode>`
- Git-SHA: `<sha>`
- Working Tree: `clean` or `dirty`
- Exit Code: `<code>`

## Checks Run

Only checks whose execution is confirmed by the actual output.

## Coverage

Which intended behavior is covered by actual tests or constraints.

## Runtime Verification

Report separately as PASS, FAIL, or NOT RUN. Never infer it from the static gate.

## Not Checked

Relevant checks that did not run.

## Remaining Risks

Be specific, or report: No known material risks.
