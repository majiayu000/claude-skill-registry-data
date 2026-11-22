---
name: incomplete-refactor
description: Detect an incomplete refactor — old names still referenced, removed files still present, stale tests still calling the old API — before calling the refactor done. Use after every rename, move, or API migration, and in CI on refactor branches. A green test suite does not prove a refactor is complete. Only invoke via the orcinus router.
license: MIT
user-invocable: false
compatibility: Requires Python 3.11+.
---

# INCOMPLETE-REFACTOR — is the old thing really gone?

A refactor is done only when the old thing is gone everywhere: code, tests, docs, config. A green suite does not prove that. The compiler does not read docs, dead code compiles, and a test that still calls the old name is a test the refactor never reached. This skill checks the refactor's own definition of done, with a script, not by eye.

## Rules

- Define the scope before refactoring: the old identifiers, the paths that must disappear, and the new names. A refactor without a written scope cannot be checked.
- Run the checker before calling the refactor done. A leftover is a finding, not a note.
- The checker supplements the four commands (build, lint, typecheck, test); it does not replace them. Both must be green.
- Every allowlist entry must be justified in the report. An allowlist that hides a leftover is a lie.
- Never delete the checker's output. It is the evidence the refactor finished.

## Steps, in order

### 1. Scope

Write down, before touching code:

- Old identifiers: every function, type, variable, and file name that must disappear (for example `budgetWarning`).
- Removed paths: every file or directory that must no longer exist (for example `src/budget-old.ts`).
- Allowlist: the files allowed to mention an old name on purpose — a CHANGELOG entry, a migration guide. Each entry needs a reason.

### 2. Refactor

Do the refactor (rename, move, migrate) one slice at a time, following `build`.

### 3. Run the checker

```bash
python3 skills/incomplete-refactor/scripts/check_refactor.py \
  --root . \
  --old budgetWarning \
  --removed src/budget-old.ts \
  --allow CHANGELOG.md
```

It exits 0 when clean and 1 when it finds a leftover — or when the scan was incomplete (a file it could not read, a root that does not exist, an empty `--old` list, a symlink pointing outside the root). It scans the files git knows about (tracked plus untracked, respecting `.gitignore`); when the root is not a git repository it walks the tree and skips generated directories and lockfiles (overridable with `--skip-dirs` / `--skip-files`). The allowlist matches a relative path only, never a bare basename (`--allow ./CHANGELOG.md` works). A symlink whose target stays inside the root is read; one pointing outside it is not read. It reports:

- Old identifier still referenced, with file and line — including in tests (a stale test) and in docs and comments (a forgotten mention). Identifiers that start with `$` are matched as whole identifiers.
- Removed path still present.
- TODO or FIXME comments that name the old identifier — a migration the refactor left half-done.
- How many files were checked, skipped (generated dirs/lockfiles), skipped (non-UTF-8), binary, unreadable, and skipped (symlink outside the scan root). A clean result covers only the files scanned — generated dirs, lockfiles and outside symlinks are not scanned, and the summary says how many. A scan that did not cover everything is INCOMPLETE, never clean.

### 4. Run the four commands

Build, lint, typecheck, test. A leftover the compiler catches is still a leftover; a leftover the compiler does not catch is the reason this skill exists.

### 5. Verdict

- PASS: the checker is clean and the four commands are green. The refactor is done.
- FAIL: any leftover, or any red command. Fix the leftover — do not add it to the allowlist to make the report green.

## Report

Return the report in this form:

- Scope: old identifiers, removed paths, allowlist with a reason per entry.
- The exact checker command and its exit code.
- Each leftover, with file, line, and kind (old name / removed path / stale test).
- The four commands and their results.
- Verdict: PASS or FAIL, and what remains.

## Scope

Textual leftovers only. The checker finds names and paths; it does not find semantic incompleteness — duplicated logic under a different name, or a call site that was deleted instead of migrated. Those are caught by tests, coverage, and review, not by this checker. A bare "TODO: migrate" that never names the old thing is a human-review item, not a checker item.

## Sources

Written from scratch for ORCINUS. No ready skill was found for this in the 0–100 research: generic refactoring skills (for example code-refactoring-skill, MIT) teach how to refactor, none check that a refactor actually finished. The checker script is original code, shipped under this repo's MIT licence.
