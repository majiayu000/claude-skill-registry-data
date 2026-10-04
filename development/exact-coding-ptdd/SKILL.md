---
name: exact-coding-ptdd
description: Predictive Test-Driven Development with a complete up-front inactive test list, one-behavior Red-Green-Refactor cycles, and mandatory domain-boundary trials. Invoke when the user explicitly asks for this EXACT Coding Predictive TDD workflow.
---

# EXACT Coding Predictive TDD — TCR-Parity Port

Run one shared workflow: create the complete test list once, then implement one behavior at a time using Predictive TDD. This port retains the TCR trial workflow's non-method-specific test-list, domain-responsibility, stack, and lab contracts while replacing phase commits and hard resets with prediction, checking, and local undo.

## Preparation

1. Read `.pi/skills/test-list/SKILL.md`.
2. Read `.pi/skills/predictive-tdd/SKILL.md`.
3. Read the complete specification.
4. Determine the project's language and test framework. If `.pi/skills/exact-coding-ptdd/stacks/` contains a matching profile, read it before changing code.
5. Determine the project's inactive-test mechanism, full-suite command, and applicable quality gates from the profile and repository.
6. Establish the applicable baseline gates before creating the test list.

## Sequence

1. Create the complete ordered test list with every future behavior inactive.
2. Predict and run the full suite. Continue only when the inactive list leaves the suite green; correct the list without implementing behavior if it does not.
3. For exactly one behavior at a time, follow `.pi/skills/predictive-tdd/SKILL.md`:
   - activate exactly one behavior and reach the intended behavioral RED,
   - compare the predicted and actual result without committing or resetting,
   - make the smallest production change and verify GREEN,
   - review production and test code under the Four Rules of Simple Design,
   - perform the domain-responsibility review and mandatory boundary trial,
   - predict and verify each useful refactoring separately, undoing only the attempted refactoring when it fails or does not improve intent.
4. Continue until every listed behavior is executable and the full suite and all applicable quality gates from the active stack profile pass.

A test already satisfied by an earlier generalization is legitimate evidence. Do not manufacture a failure or production change. Predict the passing result, activate that test, run the suite, record the already-green outcome, and continue to the refactor review.

## Method boundary

This is Predictive TDD, not TCR. Do not stage phase changes, create `[TEST LIST]`, `[RED]`, `[GREEN]`, or `[REFACTOR]` commits, or run `git reset --hard` as a phase mechanism. The isolated repository is a controlled harness condition only. Preserve successful work in the working tree and undo an unsuccessful trial narrowly before continuing.

## Completion

The feature is complete only when every listed behavior has an executable test, all tests and applicable quality gates pass, prediction mismatches are explained, the Four Rules and domain-boundary reviews are complete, and no unagreed behavior was added.
