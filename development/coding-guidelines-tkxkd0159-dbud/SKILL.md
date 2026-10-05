---
name: coding-guidelines
description: Baseline coding behavior. Use before writing, reviewing, debugging, or refactoring code. Establishes ground rules for assumptions, simplicity, surgical edits, and verification.
---

# Coding Guidelines

These are baseline rules for coding tasks. Apply them before writing, reviewing, debugging, refactoring, or testing code.

Bias toward small, correct, maintainable, verified changes.

For trivial tasks, do not add unnecessary process. For non-trivial tasks, define the goal, make a focused change, and verify it.

## 1. Assumptions and Clarification

Do not assume silently.

State assumptions when they materially affect:
- Correctness
- API design
- Data safety
- User-visible behavior
- Backward compatibility
- Implementation scope

Ask for clarification only when the answer would meaningfully change the implementation. For low-risk ambiguity with a conventional default, state the assumption and proceed instead of blocking.

Push back when the requested approach appears overcomplicated, risky, or misaligned with the stated goal.

## 2. Simplicity

Implement the minimum code that correctly solves the requested problem.

Do not add:
- Features that were not requested
- Abstractions for single-use logic
- Configuration that was not requested
- New dependencies unless clearly justified
- New files, frameworks, or public APIs unless necessary
- Error handling for impossible or irrelevant scenarios

Prefer existing project utilities and standard library functionality over new code or dependencies.

If the solution is much larger than the problem, simplify before proceeding.

## 3. Surgical Changes

Touch only what the request requires.

When editing existing code:
- Match existing style
- Preserve existing behavior unless asked to change it
- Preserve public APIs unless asked to change them
- Preserve file structure and naming unless change is necessary
- Do not refactor unrelated code
- Do not reformat unrelated code
- Do not fix unrelated bugs silently

Mention unrelated issues separately instead of changing them.

Clean up only artifacts caused by your own change:
- Unused imports
- Unused variables
- Dead helper functions you introduced
- Tests or files made obsolete by your change

Every changed line should trace directly to the user's request.

## 4. Comments

Default to no comments. Add one only when the *why* is non-obvious — a hidden constraint, subtle invariant, or workaround.

Do not:
- Restate what the code does
- Reference the current task, PR, or caller
- Leave markers like `// removed X` for deleted code

## 5. Goal and Plan

For non-trivial tasks, define success before editing.

Use a short plan:

```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Convert vague goals into verifiable goals:
- "Fix the bug" -> reproduce it, then make the reproducer pass
- "Add validation" -> test invalid input, then make the test pass
- "Refactor" -> prove behavior is unchanged
- "Improve performance" -> identify the bottleneck, then measure the change

Do not broaden the task silently.

## 6. Verification

Verify before claiming work is done. Do not claim something works without actually running it.

- For bugs: reproduce the failure first, then make the reproducer pass.
- For new behavior: add or update a targeted test.
- Run the smallest relevant test, typecheck, or lint.
- If verification cannot be run, say what was not run and why.
- If a check fails, decide whether your change caused it. Fix what you broke; surface unrelated failures separately.
