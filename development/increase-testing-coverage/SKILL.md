---
name: increase-testing-coverage
description: Find and implement a valid quick-win testing coverage improvement in the current project. Use when the user asks to increase test coverage, improve coverage, add focused tests, find low-risk test gaps, or make a testing improvement without broad refactoring. The skill must prioritize meaningful tests over artificial coverage gains and must explain the completed change plus provide an accurate git commit message in the required format.
---

# Increase Testing Coverage

## Goal

Increase test coverage with a small sensible change that improves confidence in real behavior. Prefer focused tests for existing code paths, edge cases, regression risks, or public APIs over broad rewrites or tests that only exercise implementation details.

## Workflow

1. Inspect the project structure, test framework, package scripts, and existing test style before editing.
2. Find a quick-win coverage opportunity by comparing source files with nearby tests, recent gaps, uncovered branches, simple error handling, input validation, boundary cases, or small public helpers.
3. Choose one improvement that is valid on its own merits. Do not add tests solely to execute lines, snapshot trivial output, assert mocks were called without behavior, or lock in meaningless implementation details.
4. Add or update tests using the project's existing framework, naming conventions, fixtures, helpers, and style.
5. Keep production-code edits out of scope unless a tiny testability fix is necessary and justified by the discovered gap.
6. Run the most relevant test command. If coverage tooling is available and cheap to run, run it too; otherwise run the focused test file or nearest suite.
7. If tests fail, fix the test or code only when the failure reveals an issue directly related to the chosen coverage improvement. Do not chase unrelated failures.
8. Review the diff before responding so the explanation and git message describe only actual changes. Include the change in coverage % in your explanation.

## Good Quick Wins

Prefer tests for:

- Untested branches in existing logic, especially error handling or fallback behavior.
- Public functions, components, CLI commands, routes, reducers, serializers, validators, or hooks that have no nearby tests.
- Boundary values such as empty input, invalid input, missing optional fields, duplicate entries, ordering, parsing, or permission/state transitions.
- Previously untested integration between small units when existing helpers make the setup straightforward.
- Bugs discovered during inspection, as long as the change remains focused and verified.

Avoid:

- Tests that assert only that a function exists or returns a mocked value without meaningful behavior.
- Brittle snapshots when explicit assertions would be clearer.
- Large fixture churn, unrelated refactors, broad formatting, or mass-generated tests.
- Lowering coverage thresholds, deleting assertions, skipping tests, or weakening test expectations.
- Inventing behavior not supported by existing code, docs, or product context.

## Reporting

After completing the change, tell the user:

- What test coverage change was made.
- Why it is a meaningful coverage improvement and what behavior is now protected.
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
```