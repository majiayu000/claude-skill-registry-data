---
name: tdd
description: "Use when writing tests, adding test coverage, implementing a feature or fix test-first, creating a failing test before code, or discussing red-green-refactor, acceptance tests, unit tests, or test strategy."
---
# Test Driven Development

## When to use
- **Any code change** - every fix, feature, or refactor must have a corresponding test
- User asks to write tests, add test coverage, or create a failing test first
- User asks to implement a feature using TDD or test-first development
- User mentions "red-green-refactor", "acceptance test", or "unit test"
- User asks to verify that tests pass before committing

## Overview

Test Driven Development with acceptance tests and unit tests. The test comes first
and must fail before the implementation exists. That failure is the proof the test
is worth anything.

## Rules

1. Preserve file encoding
2. Analyse the test setup: which framework is actually used, how to build, how to run tests, how to read coverage (see the stack file in [`software-engineer`](../software-engineer/SKILL.md))
3. Create a failing acceptance test if it does not exist. It enters through the public surface and proves one behaviour end to end, one slice at a time ([`plan`](../plan/SKILL.md#rules-for-both-routes)). Add unit tests for small cases or technical parts.
4. Watch the test fail for the expected reason before writing any implementation
5. Implement what the failing test demands and nothing more, so the next behaviour's test still goes red. Check first that the function does not already exist.
6. Run tests and get feedback
7. Refactor

## Discipline

Implementation written before its test is deleted and restarted from the test. Not
kept as reference, not adapted while the test is written. Deleted.

A test that passes on first run proves nothing. Make it fail first, or find out why it
cannot fail and fix the test.

**Record the red run — quote it, never paraphrase it.** The final report carries the
command and its decisive output lines verbatim, copy-pasted from the real runs:

```
$ pytest -q
2 failed: test_parse_rejects_empty, test_parse_rejects_unknown_unit
$ pytest -q
35 passed
```

"Tests were written first and failed" is a claim; the quoted lines are evidence. A
reviewer who sees only the report cannot tell a paraphrased red run from one that
never happened — the quote settles it at the cost of two lines.

**Skipping is stated, never silent.** When red-first genuinely cannot apply (generated
code, pure config), the final report says so and why, in one line. A silent skip reads
as a broken promise when discovered later.

## Run tests and get feedback

Before committing, always run **all** tests in the solution or workspace. If the repo
contains several solution files, confirm which one to use before.

1. **Tests pass with assertions** - every test asserts expected behaviour, not just "no exception"
2. **Code coverage verified** - check the report for new or modified code (see `software-engineer` testing strategy)
