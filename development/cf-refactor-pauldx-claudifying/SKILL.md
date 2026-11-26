---
name: refactor
description: When the user asks to refactor code, clean up tech debt, improve code quality, or says "this is messy" — activate this skill for structured refactoring with test verification
---

# Refactor Skill

## Goal

Identify concrete structural issues and apply targeted refactorings one at a time, verifying with tests after each change. Same inputs must produce same outputs.

## Constraints

- Ask the user for scope and constraints before starting (preserve API? no new deps?)
- Apply one refactoring at a time — run tests between each
- Commit each refactoring separately for clean git history and easy revert
- Don't refactor code that doesn't need it. Three similar lines is fine. Premature abstraction is worse than duplication.

## What to Look For

- Long methods (> 30 lines) → extract
- Deep nesting (> 3 levels) → guard clauses / early returns
- Duplicate blocks → shared function (only if 3+ copies)
- God objects → split by responsibility
- Misleading names → rename to match actual behavior

## Output

For each issue: before snippet, after snippet, why it's better. Let the user approve before applying.

## Gotchas

- **Don't break the public API** unless the user explicitly says it's OK. Internal refactoring should be invisible to callers.
- **Tests must pass between each refactoring step.** If there are no tests, warn the user before proceeding — refactoring without tests is gambling.
- **Avoid refactoring and adding features simultaneously.** One or the other per commit.
- **Watch for side effects.** Extracting a method that reads/writes shared state can introduce bugs if the execution order changes.
- **IDE rename is safer than find-replace.** When renaming, grep for string references too (log messages, error strings, API responses that include the old name).
