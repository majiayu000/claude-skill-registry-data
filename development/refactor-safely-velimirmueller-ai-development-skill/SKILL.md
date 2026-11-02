---
name: refactor-safely
description: Use when a function or module has grown — long method, feature envy, god class, duplicated code — and must change shape without changing behavior.
---

# Refactor Safely

Changes the structure of code without changing its behaviour, one smell at a time, under a green test.
The smell vocabulary and Boy-Scout rule are here; readability rules are in
[write-readable-code](../write-readable-code/SKILL.md).

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null | head -20
git status --short 2>/dev/null
ls tests 2>/dev/null || find . -name "*_test.*" -o -name "*.test.*" 2>/dev/null | head
```

Confirm two preconditions before touching anything: the tree is clean (or changes are committed) and a
test covers the code you will move. If neither holds, stop and say so — refactoring without a safety net
is editing, not refactoring.

## 2. Name the smell

| Smell | Symptom | Refactor |
|---|---|---|
| Long method | a function that scrolls | Extract method, then extract until each does one thing |
| Feature envy | a method calls another object's data more than its own | Move the method to the object it envies |
| God class | one class with many reasons to change | Extract class by responsibility |
| Duplication | the same block in two places | Extract and link; one source of truth |
| Magic number | a bare literal in logic | Name the constant |
| Dead code | a path nothing reaches | Delete (git keeps it) |
| Data clump | the same 2–3 fields always passed together | Group into one value/struct |
| Switch over type | a conditional on a discriminator | Replace with a union + per-kind function |

## 3. Refactor in discipline

- One smell at a time, and run the tests after each move — never a batch that changes many things at once.
- Separate refactoring from behaviour change: refactor and feature land in different PRs.
- Prefer mechanical, reversible moves (extract, rename, inline, move) over clever rewrites.
- Leave the Boy-Scout rule as the default: make the touched code cleaner than you found it, but do not
  expand the blast radius to unrelated files.

## Verify

The tests pass unchanged (you did not edit them except to add one), the public behaviour is identical,
and the diff reads as moves and renames. State the smell found and the refactor applied in the note.

## When to deviate

- No tests and no easy way to add one: make the smallest mechanical move and label it unverified.
- The smell is actually load-bearing performance: measure before changing (see
  [engineering-principles.md](../../core/_shared/engineering-principles.md) — measure before optimizing).
