---
name: tests
description: Audit and improve tests for a target repo.
---

# Tests

You are improving tests for a GitHub repository.

## Environment

- The target repo is cloned at `o/repo/`. You have read and write access.
- You do not have access to bash. You cannot run tests — work statically.

## Instructions

1. Read `o/repo/AGENTS.md` and any documentation it references to learn:
   - Where tests live and how they are organized.
   - What conventions exist for testing.

2. Read through the codebase and existing tests. Understand what is tested and what is not. Look for:
   - Untested code, missing edge cases, gaps in error handling.
   - Tests that exercise code but don't verify outcomes.
   - Tests that depend on external state or are otherwise fragile.
   - Any other quality issues specific to this repo's test ecosystem.

   Adapt your analysis to whatever testing patterns the repo uses. Do not impose a fixed rubric.

3. Fix the most impactful issues. Prioritize:
   - Missing tests for important code paths.
   - Weak or missing assertions.
   - Tests that are clearly broken (syntax errors, wrong imports).

   For each fix:
   a. Follow the repo's conventions.
   b. Stage and commit with a descriptive message.

## Constraints

- Do not modify source files — only test files.
- Follow the repo's existing test conventions.

## Output

Write `o/tests/tests.json`:

```json
{
  "created": 0,
  "improved": 0,
  "findings": [
    {
      "area": "<module, feature, or test file>",
      "action": "<added|improved|flagged>",
      "notes": "<what was found and what was done>"
    }
  ]
}
```
