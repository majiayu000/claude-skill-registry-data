---
name: fix-build
description: "Fix build errors and type errors with minimal changes. No refactoring — just get the build green."
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.3-codex
---

# /fix-build — Build Error Resolution

Fix all build/type errors with **minimal diffs only**. See `agents/build-error-resolver.md`.

1. **Collect** — `npx tsc --noEmit --pretty 2>&1` and `npm run build 2>&1`
2. **Categorize** — type inference, missing types, imports, config, deps
3. **Fix** — Add type annotations, null checks, fix imports, install deps. No refactoring.
4. **Verify** — Re-run build after each batch

Success: build exits 0, minimal lines changed (<5% of affected file).
