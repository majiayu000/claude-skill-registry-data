---
name: wrap-up
description: "Close a task: list the changes, fix stale docs, run checks, draft the commit. Use when the user says \"wrap up\" or \"ready to commit\"."
license: MIT
metadata:
  author: Tony Gorb
  source: https://github.com/tonygorb/skills
  category: workflow
  cover: "done"
---

# Wrap up

The end-of-task pass: changes, docs, build, tests, a drafted commit. **Never commits.**

## Steps

### 1. Inventory the changes

Run `git status` and `git diff --stat HEAD` (in a repo with no commits yet, `git status` alone).
List new, modified and deleted files.
Nothing changed: stop and say "nothing to wrap up".

### 2. Check the scope

If the diff spans unrelated projects or packages, stop and suggest wrapping up each one separately.

### 3. Refresh the docs the diff made stale

For each changed source file, search the docs folder for its path and the names it exports.
Where a doc still describes the old path, name or behaviour, re-read the code and fix the doc.
Keep a list of the docs you touched.

### 4. Build and typecheck

Run the project's build and typecheck scripts. On failure, show the errors and stop: no commit
message for a broken build.

### 5. Tests, once

Run the unit tests in single-run mode (no watch). Skip slow end-to-end suites; mention them instead.

### 6. Draft the commit

Pick a Conventional Commit type (`feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `chore`…), an
optional lowercase scope, and an imperative subject without a full stop. Then print exactly:

```
Changed files:
  <list>

Docs refreshed:
  <list or "none">

Build: PASS/FAIL
Typecheck: PASS/FAIL
Tests: PASS/FAIL/SKIPPED

Suggested commit:
  <type>(<scope>): <subject>
```

### 7. Never commit

Don't run `git add`, `git commit` or `git push`. The user reviews the draft and commits.
