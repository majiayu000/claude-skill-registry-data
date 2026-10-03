---
name: improve-testing
description: Find and implement a valid quick-win improvement to the quality of preexisting tests in the current project. Use when the user asks to improve tests, strengthen test quality, make existing tests more meaningful, reduce brittleness, clarify assertions or fixtures, or make a small testing improvement that is not necessarily about coverage. The skill must prioritize better confidence, clearer behavior, and maintainable tests over artificial coverage gains, and must explain the completed change plus provide an accurate git commit message in the required format.
---

# Improve Testing

## Goal

Improve the quality of existing tests with a small sensible change that increases confidence in real behavior. Prefer strengthening, clarifying, or de-brittling nearby tests over adding tests solely to increase coverage.

## Workflow

1. Inspect the project structure, test framework, package scripts, and existing test style before editing.
2. Review preexisting tests for quick-win quality opportunities such as weak assertions, missing edge expectations, excessive mocking, brittle snapshots, unclear fixtures, duplicated setup, async timing risks, state leakage, poor test names, or behavior that is implied but not directly protected.
3. Choose one improvement that is valid on its own merits. Do not optimize for coverage percentage, add tests only to execute lines, snapshot trivial output, assert mocks were called without behavior, or lock in meaningless implementation details.
4. Add or update tests using the project's existing framework, naming conventions, fixtures, helpers, and style.
5. Keep production-code edits out of scope unless a tiny testability or correctness fix is necessary and justified by the discovered testing gap.
6. Run the most relevant test command, usually the focused test file or nearest suite. Run broader tests only when the change touches shared helpers or cross-cutting behavior.
7. If tests fail, fix the test or code only when the failure reveals an issue directly related to the chosen test-quality improvement. Do not chase unrelated failures.
8. Review the diff before responding so the explanation and git message describe only actual changes.

## Good Quick Wins

Prefer improvements that:

- Replace vague assertions with behavior-focused expectations.
- Add a missing assertion to an existing test that already sets up the relevant scenario.
- Cover a nearby edge case in an existing test file when the behavior is clear from code, docs, or current tests.
- Replace brittle snapshots with explicit assertions for the meaningful behavior.
- Reduce over-mocking when a local helper, fixture, or integration-style assertion makes the test more trustworthy without heavy setup.
- Improve async, timer, cleanup, or state-isolation behavior in tests that could pass or fail for the wrong reason.
- Clarify confusing test names, duplicated setup, or fixtures when that makes the tested behavior easier to maintain.
- Add regression protection for a bug discovered during inspection, as long as the change remains focused and verified.

Avoid:

- Tests that assert only that a function exists or returns a mocked value without meaningful behavior.
- Adding or changing tests solely to increase coverage metrics.
- Brittle snapshots when explicit assertions would be clearer.
- Large fixture churn, unrelated refactors, broad formatting, or mass-generated tests.
- Lowering coverage thresholds, deleting assertions, skipping tests, or weakening test expectations.
- Inventing behavior not supported by existing code, docs, or product context.

## Reporting

After completing the change, tell the user:

- What test-quality change was made.
- Why it is a meaningful improvement and what behavior is now better protected or easier to maintain.
- Which verification command ran and whether it passed. If verification could not run, explain why.
- A git commit message that follows the exact format below and describes only the actual diff.

Use this commit message format exactly:

```text
<main message>

<explaining sentence 1>
<explaining sentence 2>
<explaining sentence 3 - optional>
```

Main message rules:

- Write one sentence that summarizes the whole change.
- Use imperative mood, such as `Add`, `Fix`, `Refactor`, or `Remove`.
- Keep it under about 60 characters where possible.
- Capitalize the first word and do not end with a period.
- Be specific about the component, feature, or behavior affected.

Description rules:

- Write 2 sentences, or 3 only when the change genuinely needs it.
- Explain what changed and why, not a line-by-line account of how.
- Make every sentence complete and grammatical, ending with a period.
- Mention side effects, behavioral changes, or anything a reviewer must know.

Accuracy rules:

- Describe only changes visible in the diff.
- Do not invent files, functions, motivations, or effects.
- If the reason is not evident, describe the effect rather than guessing intent.
- If the diff is too ambiguous to describe safely, say so in one line instead of fabricating.
