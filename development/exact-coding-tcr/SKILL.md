---
name: exact-coding-tcr
description: Test-Driven Development with a complete up-front test list, one-behavior Red-Green-Refactor cycles, Test-Commit-Revert discipline, and configurable human checkpoints. Invoke when the user explicitly asks for EXACT Coding with TCR or TCRDD. Do not invoke for ordinary coding tasks where this workflow was not requested.
---

# EXACT Coding TCR

Run one shared workflow: create the complete test list once, then implement one behavior at a time using TCRDD. Every RED, GREEN, and REFACTOR phase is verified and either committed or reverted.

## Preparation

1. Read `.pi/skills/test-list/SKILL.md`.
2. Read `.pi/skills/tcrdd/SKILL.md`.
3. Read `.pi/skills/exact-coding-tcr/human-in-the-loop.md`.
4. Read the complete specification.
5. Determine the project's language and test framework. If `.pi/skills/exact-coding-tcr/stacks/` contains a matching profile, read it before changing code.
6. Determine the project's inactive-test mechanism, full-suite command, and applicable quality gates from the profile and repository.
7. Require a clean Git working tree before creating the test list.

## Sequence

1. Create the complete ordered test list with every future behavior inactive.
2. Stage the test list, run the full suite, and commit it only if the suite passes:

   ```bash
   git add -A
   <full-test-suite-command>
   git commit -m "[TEST LIST] <feature>"
   ```

   If the suite fails, discard the test-list change with `git reset --hard HEAD`.
3. For exactly one behavior at a time, follow `.pi/skills/tcrdd/SKILL.md`:
   - activate exactly one behavior and reach the intended behavioral RED,
   - commit the verified RED or revert it,
   - apply the Red checkpoint,
   - make the smallest production change and commit the verified GREEN or revert it,
   - apply the Green checkpoint,
   - review production and test code under the Four Rules of Simple Design,
   - apply each useful refactoring as its own commit-or-revert step,
   - apply the Refactor checkpoint.
4. Continue until every listed behavior is executable and the full suite and all applicable quality gates from the active stack profile pass.
5. Apply the Task-End checkpoint.

A test already satisfied by an earlier generalization is legitimate evidence. Do not manufacture a failure or production change. Activate that test, run the full suite, and commit the passing test as `[GREEN] <already-satisfied behavior>`.

## Human-in-the-loop

`.pi/skills/exact-coding-tcr/human-in-the-loop.md` is the single source of truth for checkpoints. This lab profile selects its `autonomous` level because the harness runs unattended.

At each checkpoint, wait for explicit approval when the configured autonomy level requires it. Do not stage, test, commit, or revert the next phase while waiting.

## Completion

The feature is complete only when every listed behavior has an executable test, all tests and applicable quality gates pass, the Four Rules review is complete, and the working tree is clean.
