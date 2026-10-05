---
name: flow-review
description: Review a code diff or explicit file set through independent correctness and QA lenses. Use when the user asks for a code review, test-coverage assessment, pre-merge audit, or review gate in a PWDEV Flow workflow.
---

# Review code and test evidence

Read [collaboration](../../references/collaboration.md), [artifacts](../../references/artifacts.md), and [safety](../../references/safety.md) before reviewing.

Review is read-only. Do not implement fixes unless the user separately requests changes.

## Establish the contract

1. Resolve the scope from an explicit file list, diff range, active Flow state, or working-tree diff.
2. Read applicable `AGENTS.md`, the relevant acceptance criteria, quality rules, and prohibitions.
3. If scope is ambiguous, inspect safely and state the bounded scope used.

## Correctness lens

- Read the complete diff, not only a summary.
- Check behavior, error paths, boundary cases, security, concurrency, data integrity, compatibility, conventions, and unnecessary complexity.
- Report only actionable findings with severity, file, tight line range, consequence, and concrete remediation.
- Use inline code comments when the runtime supports them.

## QA lens

- Map each acceptance criterion and changed behavior to existing tests.
- Run the relevant test commands when safe and non-mutating beyond normal local build artifacts.
- Identify untested failure paths and explain the smallest valuable missing test.
- Distinguish environmental failures from product failures.

Run the two lenses sequentially by default. Use separate collaborating workers only when the user explicitly requests delegation or parallel agent work, following [collaboration](../../references/collaboration.md).

## Verdict

Use the worst applicable result:

- `APPROVED`: no critical or major finding and evidence is adequate;
- `CHANGES_REQUESTED`: at least one major finding or material test gap;
- `BLOCKED`: scope, evidence, or environment prevents a responsible review.

Return findings first, ordered by severity, followed by assumptions, test evidence, and verdict. Persist a report only when the user requested it or this is an active Flow phase with artifact persistence already authorized.
