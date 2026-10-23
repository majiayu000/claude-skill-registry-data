---
name: test-driven-development
description: "Implements a feature or bug fix test-first: write one failing test, run it and watch it fail, write the minimal code to pass, then refactor with the tests green. Use when a change alters code behavior: a new feature, a bug fix, or a behavior change, whether the request comes alone or through delivery-flow."
---
# Test-Driven Development

Write the test first. Watch it fail. Write the minimal code to pass. Refactor with the tests green.

## Rules

- No production code without a failing test first. Code written before its test is deleted and written again from the test.
- A bug fix starts with a test that reproduces the bug.
- If the test is hard to write, the design is unclear: simplify the interface.
- When writing or changing a test, read [references/writing-good-tests.md](references/writing-good-tests.md).

## Before you say it is done

- Each new behavior has a test that you saw fail first.
- The full suite passes on the final code.
