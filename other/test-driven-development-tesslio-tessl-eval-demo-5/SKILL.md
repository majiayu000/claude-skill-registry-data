---
name: test-driven-development
description: "Implements a feature or bug fix test-first: write one failing test, run it and watch it fail, write the minimal code to pass, then refactor with the tests green. Use when a change alters code behavior: a new feature, a bug fix, or a behavior change, whether the request comes alone or through delivery-flow."
---
# Test-Driven Development

Write the test first. Watch it fail. Write the minimal code to pass. Refactor with the tests green.

## The cycle

1. **Red.** Write one test for one behavior. Use a clear name and the real code, not mocks.
2. **Watch it fail.** Run the project's test command. The test must fail because the behavior is missing, not because of a typo or a missing import. If it passes, it tests nothing new: change the test.
3. **Green.** Write the simplest production code that makes it pass. Add nothing the test does not need.
4. **Watch it pass.** Run the full suite. Every test passes, with no errors or warnings.
5. **Refactor.** Clean up names and duplication. Run the suite again.

Repeat for the next behavior.

## Before you say it is done

- Each new behavior has a test that you saw fail first.
- The full suite passes on the final code.
