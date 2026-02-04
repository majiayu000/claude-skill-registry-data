---
name: wrap_up_gwexpy
description: gwexpy向けの一連の検証・整理・コミット手順をまとめて実行する
---

# Wrap Up (gwexpy)

This skill performs a full end-of-workflow wrap-up for gwexpy, aligned to available skills.

## Instructions

1. **Physics Review (if relevant)**
   * If the change affects physics/math behavior, run `check_physics`.
   * Otherwise, skip and note why.

2. **Tests**
   * Run `test_code` (full `pytest`).
   * If it is too slow, split into logical subsets and report coverage.

3. **Lint/Type Checks**
   * Run `lint` (`ruff check .` and `mypy .`).

4. **Docs Sync**
   * Run `sync_docs` to align docstrings and docs (EN/JA) with code changes.

5. **Directory Hygiene**
   * Run `organize` to confirm no misplaced files.
   * If tests created `tests/.home/`, remove it and add `tests/.home/` to `.gitignore` via `ignore`.

6. **Commit**
   * Run `git_commit` to clean caches and commit with a concise conventional message.
   * Do not delete non-standard files without confirmation.

7. **Report**
   * Summarize tests/lint results and whether full pytest completed.
   * Provide commit hash if created.
