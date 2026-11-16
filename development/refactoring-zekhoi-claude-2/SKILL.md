---
name: refactoring
description: Restructure existing code to improve its design without changing behavior, protected by tests run before and after. Use when the user asks to refactor, clean up, tidy, simplify, deduplicate, extract, rename across modules, or reorganize code, or says code is hard to read or messy, while keeping it working the same. Do not use for fixing bugs, adding features, performance work that changes behavior, or reviewing code without changing it (use agent-kit:code-review or agent-kit:overengineering-review).
---

# Refactoring

A refactoring changes structure, never behavior. If behavior must change, stop and say so; that is a separate change.

## 1. Pin down current behavior

- Identify the code in scope and everything that depends on it: callers, exports, public APIs, serialized formats, and configuration.
- Run the existing tests that cover it and record the result before changing anything.
- If the code has no meaningful tests, add characterization tests that capture current behavior first, including edge cases and current error behavior, even if that behavior looks wrong. Report anything that looks like a bug instead of fixing it during the refactoring.

## 2. Refactor in small steps

- Make one structural change at a time: extract, inline, rename, move, or deduplicate. Run the tests after each meaningful step.
- Preserve public interfaces unless the user asked to change them. When a rename crosses module boundaries, update every reference; search for dynamic or string-based uses too.
- Follow the project's existing patterns. Do not introduce new abstractions, frameworks, or dependencies to make the code "cleaner" unless asked.
- Keep the change focused. Note other improvements you notice instead of making them.

## 3. Verify and report

- Run the full relevant test suite, type checks, and linters, and confirm the results match the baseline.
- Report what was restructured and why it is better, the tests run before and after with their results, any characterization tests added, and suspected bugs left unchanged.

## Examples

- Use: "Refactor the pricing module to remove the duplicated discount logic." "Split this 600-line file into smaller modules."
- Skip: "Fix the double discount bug." (debugging) "Add coupon support." (feature implementation)
