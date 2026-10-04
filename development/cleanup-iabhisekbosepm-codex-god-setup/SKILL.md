---
name: cleanup
description: "Refactoring sprint: remove dead code, eliminate duplicates, simplify complex code."
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.3-codex
---

# /cleanup — Refactoring Sprint

See `agents/refactor-cleaner.md` and `agents/code-simplifier.md`.

1. **Detect** — `npx knip`, `npx depcheck`, `npx ts-prune`. Categorize: SAFE/CAREFUL/RISKY.
2. **Remove** — Order: deps → exports → files → duplicates. Build-verify after each batch.
3. **Simplify** — Extract nested logic, early returns, remove console.log/commented code, consolidate duplicates.
4. **Verify** — Full build + test suite pass.

Rules: Behavior-preserving only. Be conservative. Don't run during active development.
