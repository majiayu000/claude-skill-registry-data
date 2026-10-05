---
name: flow-execute
description: Execute approved PWDEV Flow plans one atomic task at a time with test-first implementation, fresh verification, blocker handling, and durable evidence. Use after the plan gate is approved or for approved Flow correction tasks.
---

# Execute approved tasks

Read [execution](../../references/execution.md), [planning](../../references/planning.md), [collaboration](../../references/collaboration.md), [memory](../../references/memory.md), [artifacts](../../references/artifacts.md), and [safety](../../references/safety.md).

## Entry gate

Require an approved plan, satisfied dependencies, and identifiable verification commands. Stop if the plan is stale, contradicts the specification, or overlaps unrelated user changes unsafely.

## Procedure

1. Execute inline by default. Select one ready task; do not mix tasks or waves in one implementation unit.
2. Read the full task, linked specification clauses, required context, applicable instructions, relevant memory, and current Git status.
3. Confirm allowed files and state the task contract before editing.
4. For behavior changes, write the focused failing test first and observe the expected failure.
5. Implement only the approved actions with the smallest sufficient change.
6. Run focused verification, then the relevant broader suite.
7. Inspect the complete diff for scope, correctness, safety, and prohibited behavior.
8. Write the execution summary specified by [execution](../../references/execution.md) and update state only from fresh evidence.
9. Continue to the next ready task only when the current result is `COMPLETE` or an accepted `CAVEATS`.
10. After all tasks, set `REVIEW_REQUIRED` and recommend `$flow-simplify` or `$flow-review`.

## Blockers and corrections

On `NEEDS_ADVICE`, stop edits, persist the structured question, and request one decision. For fix plans, follow the same lifecycle and enforce the maximum correction cycles. Never silently redesign scope.

## Collaboration and Git

Use collaborating workers only when the user explicitly requests delegation or parallel agent work. Never assign overlapping writers and independently verify returned claims.

Do not commit, push, create a branch, clean files, or rewrite history unless the user explicitly authorizes that exact action. Leave the diff reviewable.

## Output

Return task status, summary path, changed files, verification evidence, open concerns, phase state, and next valid action.
