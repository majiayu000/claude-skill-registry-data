---
name: test-driven-development
description: "Implements a feature or bug fix test-first: write one failing test, run it and watch it fail, write the minimal code to pass, then refactor with the tests green. Use when a change alters code behavior: a new feature, a bug fix, or a behavior change, whether the request comes alone or through delivery-flow."
---
# Test-Driven Development

Test first, then code: see the test fail, make it pass with the least code, then tidy up with the tests green.

## Steps

1. **Red.** Write one test for one behavior. Give it a clear name and use the real code, not mocks.
2. **Watch it fail.** Run the project's test command. The test must fail because the behavior is missing, not because of a typo or a missing import. If it passes, it tests nothing new: change the test.
3. **Green.** Write the simplest production code that makes it pass. Add nothing the test does not need.
4. **Watch it pass.** Run the full suite. Every test passes, with no errors or warnings.
5. **Refactor.** Tidy names and remove duplication. Run the suite again.

Repeat for the next behavior.

## Rules

- No production code without a failing test first. Code written before its test is deleted and written again from the test.
- A bug fix starts with a test that reproduces the bug.
- If the test is hard to write, the design is unclear: simplify the interface.
- When writing or changing a test, read [references/writing-good-tests.md](references/writing-good-tests.md).

## Before you report the work as done

- Each new behavior has a test that you saw fail first.
- The full suite passes on the final code.
