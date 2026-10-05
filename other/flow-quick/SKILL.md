---
name: flow-quick
description: Deliver a small, bounded code change through inspection, a mini-plan, implementation, testing, review, and adversarial verification. Use for bug fixes, configuration changes, and features expected to touch no more than five files.
---

# Deliver a bounded change

Read [workflow](../../references/workflow.md), [artifacts](../../references/artifacts.md), and [safety](../../references/safety.md) before implementation.

## Scope gate

Use quick mode only when all conditions hold:

- the objective and acceptance criteria can be stated precisely;
- at most five implementation files are expected;
- no architectural fork, schema migration, or destructive operation is required;
- the relevant verification command can be identified.

If any condition fails, stop before editing and recommend the full Flow workflow.

## Procedure

1. Inspect applicable instructions, affected code, tests, and working-tree status.
2. Protect unrelated user changes. Stop if the requested files contain overlapping edits that cannot be preserved safely.
3. State a mini-contract with objective, acceptance criteria, allowed files, prohibitions, and verification commands.
4. For behavior changes, write a failing test first and confirm the expected failure.
5. Implement the smallest change that satisfies the contract.
6. Run focused verification, then the relevant broader suite.
7. Review the full resulting diff for correctness, scope, security, maintainability, and missing tests.
8. Apply safe corrections and rerun all affected verification.
9. Build a truth list and try to refute completion using fresh commands.
10. If `.planning/flow/` is initialized, persist the mini-contract and final report using [artifacts](../../references/artifacts.md).

## Git policy

- Do not commit, push, create a branch, rewrite history, or clean unrelated files unless the user explicitly requests that action.
- Report the final diff scope and leave changes reviewable.

## Verdict

Return `COMPLETE` only when every acceptance criterion has fresh evidence and no critical review finding remains. Otherwise return `CAVEATS`, `REJECTED`, or `ESCALATED`, with exact evidence and next action.
