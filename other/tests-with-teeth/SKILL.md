---
name: tests-with-teeth
description: Use when writing or reviewing any test, or when about to accept "tests pass" as evidence.
---

## The rule

A test exists to fail when the thing it covers breaks. If you could delete the feature and the test stays green, it protects nothing. It's worse than no test, because it looks like coverage. Before accepting any test, run it through five questions.

This sharpens superpowers' test-driven-development: TDD's red step proves a brand-new test can fail; these questions hold for any test, including ones you didn't write.

## Fires when

Writing a new test, reviewing a test in a diff, inheriting a suite, or about to treat a green run as proof that something works.

## The five questions

1. **Removal** — mentally delete the line the test targets. Does the test now fail? If no, it's hollow.
2. **Reach** — list every guard and early return between setup and the assertion. Does the setup trip one of them first, so execution never reaches the target? Then the assertion is dead.
3. **Distinguishability** — would the test pass for a wrong implementation too? Give two inputs different values so the test can only pass if the right one was used.
4. **Environment gap** — what does the real feature rely on that the test harness lacks (a real database, say, or a network)? If the gap means the real path can't run, test at the lowest level that does run and label what it does and doesn't prove.
5. **Algorithm gap** — is the novel logic (a sort, a filter, a dedup) tested directly? An end-to-end test can produce the right final output through a compensating bug. Test the tricky function on its own with inputs that would expose a wrong algorithm.

## Worked example

You're testing a discount function. The test: `applyDiscount(cart)` returns a number >= 0. It passes. It's hollow. It passes whether the discount is 10%, 0%, or the function just returns the original total. Now make it distinguish: a $100 cart with a 10% code should return exactly $90. Delete the discount math and it returns $100, and the test fails. That version has teeth.

## Hollow-test smells

| Test smell | Why it's hollow |
|---|---|
| Asserts "does not crash" | Not crashing isn't correctness. |
| Asserts a value >= 0 / not null | Passes for almost any implementation. |
| Setup uses an input that triggers an early return | The assertion is never reached. |
| Same value passed for two different inputs | Can't tell which one the code used. |
| Only an end-to-end path, novel logic never tested alone | A compensating bug can hide. |

## Red flags

| Thought | Reality |
|---|---|
| "It asserts something, so it's coverage" | Coverage that can't fail is decoration. |
| "The suite is green, ship it" | Green only means these questions were never asked. |
