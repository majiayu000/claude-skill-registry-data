---
name: tdd-workflow
description: |
    Use this skill for developing software in TDD (Test-Driven Design).
---

# TDD Workflow

## Overview

A strict 7-step TDD cycle that produces high-quality, well-tested code. Each step must be
**verified and confirmed** before proceeding. Status is only updated after real verification
- never hallucinated.

Core principle: **RED (failing test) -> GREEN (minimal implementation) -> REFACTOR**.

---

## Step 0 - Check Existing Progress

At the start of each session, before doing anything else:

- List `tdd-summary/` to check for existing step reports (e.g. `step-1.md`, `step-2.md`).
- If reports exist, read them to understand prior context, then **resume from the next step**.

---

## Step 1 - Understand Intent

- Explore the codebase for relevant context.
- Derive functional requirements from the available information (user prompt + codebase).
- If any requirement is ambiguous, document the assumption explicitly in `step-1.md` under
  an "Assumptions" section rather than asking for clarification.

Write `tdd-summary/step-1.md`:

```markdown
# Step 1 - Understand Intent

## Functional Requirements

### FR-1: <title>
<description>

### FR-2: <title>
<description>

## Assumptions

- <any ambiguous point and the assumption made>
```

---

## Step 2 - Write Scenario Docs

For each functional requirement, create a scenario document at `docs/scenario/<name>.md`:

```markdown
# Scenario: <Title>
- Given: <precondition>
- When: <action>
- Then: <expected outcome>

## Test Steps

- Case 1 (happy path): <brief description>
- Case 2 (edge case): <brief description>
- Case N: ...

## Status
- [x] Write scenario document
- [ ] Write solid test according to document
- [ ] Run test and watch it failing
- [ ] Implement to make test pass
- [ ] Run test and confirm it passed
- [ ] Refactor implementation without breaking test
- [ ] Run test and confirm still passing after refactor

**IMPORTANT**: Only update above status when a step is confirmed complete. Do not hallucinate.
```

**Invariant**: Count of FR = count of scenario documents. Verify before continuing.

Write `tdd-summary/step-2.md`:

```markdown
# Step 2 - Write Scenario Docs

## Scenario Documents Created

- FR-1: <title> - `docs/scenario/<name>.md`
- ...
```

---

## Step 3 - Write Failing Test (RED)

For each scenario document:

- Write tests at `tests/scenario/test_<name>.py` (or equivalent).
- Each scenario must have **at least 2 test cases**. Add edge cases if missing.
- All acceptance criteria from the scenario document must be covered.
- Tests must **not** be empty or dummy.
- Update scenario status: check `- [x] Write solid test according to document`.

After writing, **run each test** and verify it fails:

- **Expected failure** (e.g. feature not found, endpoint missing) - this is correct.
    - Update scenario status: check `- [x] Run test and watch it failing`.
- **Unexpected failure** (e.g. import error, missing dependency) - fix the environment first.
- **Test passes** - the feature is not implemented yet; there is no reason it should pass. Fix the test.

**Invariant**: Count of scenario documents = count of test files. Verify before continuing.

Write `tdd-summary/step-3.md`:

```markdown
# Step 3 - Write Failing Test

## Failing Tests Created

- FR-1: <title> - `docs/scenario/<name>.md` - `tests/scenario/test_<name>.py`
- ...
```

---

## Step 4 - Implement to Make Tests Pass (GREEN)

For each failing test:

- Write the **minimal production code** necessary to make the test pass. Nothing more.
- Do not introduce changes unrelated to the current functional requirement.
- Update scenario status: check `- [x] Implement to make test pass`.
- Run the test. If it fails, fix the implementation and retry.
- After confirming it passes, update scenario status: check `- [x] Run test and confirm it passed`.

Write `tdd-summary/step-4.md`:

```markdown
# Step 4 - Implement to Make Tests Pass

## Implementations Completed

- FR-1: <title> - `docs/scenario/<name>.md` - Implementation in `<module>`
- ...

All tests now pass. Scenario documents updated.
```

---

## Step 5 - Refactor for Maintainability

For each scenario where tests now pass:

- Improve readability, structure, and maintainability **without changing external behavior**.
- Update scenario status: check `- [x] Refactor implementation without breaking test`.
- Run the tests again after refactoring.
    - If tests fail: fix the refactoring. If impossible, **rollback to the pre-refactor version**.
- After confirming tests still pass, update scenario status: check `- [x] Run test and confirm still passing after refactor`.

Write `tdd-summary/step-5.md`:

```markdown
# Step 5 - Refactor for Maintainability

## Refactorings Completed

- FR-1: <title> - `docs/scenario/<name>.md` - <what was improved>
- ...

All tests still pass after refactoring. Scenario documents updated.
```

---

## Step 6 - Regression Test

Run the **complete test suite** (all tests, not just those added in this session):

- If regression occurs in unrelated tests:
    - Analyze the failure and understand its impact on existing functionality.
    - Fix the implementation to restore all passing tests.
    - Re-run the complete suite until everything passes.

**NEVER modify existing tests that are unrelated to the current functional requirements.**

Write `tdd-summary/step-6.md`:

```markdown
# Step 6 - Regression Test

## Regression Test Results

- Complete test suite executed: `<command>`
- All tests pass: Yes / No
- If regression found: <brief description of fix applied>
```

---

## Step 7 - Final Review

Verify that **every scenario document has all status checkboxes checked**.

Review:
- Every FR has a corresponding scenario document and test file.
- All tests pass and code is clean.

Write `tdd-summary/step-7.md`:

```markdown
# Step 7 - Final Review

## Summary

- Functional requirements addressed:
    - FR-1: ...
- Scenario documents: `docs/scenario/...`
- Test files: `tests/scenario/...`
- Implementation complete and all tests passing after refactoring.

## How to Test

Run: `<test command>`
```

Finally, archive the summary folder:

```bash
mv tdd-summary/ completed-tdd-archives/tdd-$(date +%Y%m%d-%H%M%S)
```

TDD workflow complete.

---

## Iron Rules

- **Do not skip steps.** Each step must be verified before the next begins.
- **Do not edit tests** during implementation or refactor steps, unless the test itself was
  obviously written incorrectly in Step 3.
- **Do not hallucinate status.** Only check a status checkbox after real, confirmed verification.
- **Keep counts equal.** FR count = scenario doc count = test file count at all times.
- **Step gates**: If running interactively, present each step report and wait for confirmation
  before continuing. If running as a delegated subagent, proceed automatically through all steps.
- **If changes are requested at any step**, loop back to the appropriate step and adjust all
  downstream artifacts accordingly.
