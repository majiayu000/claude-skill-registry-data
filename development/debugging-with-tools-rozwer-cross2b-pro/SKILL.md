---
name: debugging-with-tools
description: Use for investigation-heavy work. Prefer tool-driven evidence (search, logs, diffs) before changing code.
---

## Workflow

1. Confirm the symptom and collect a single source of truth (error output/log).
2. Search the codebase for the error string / endpoint / symbol.
3. Trace control flow (entrypoint → callers → side effects).
4. Inspect configuration and environment assumptions.
5. Make one change at a time and re-check the symptom.

## Tooling checklist

- `rg` for string/symbol search
- `git diff` / `git status` for change review
- Minimal, focused test/run commands
