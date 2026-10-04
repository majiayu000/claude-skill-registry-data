---
name: quick-fix
description: "Fast bug fix: diagnose the issue, apply minimal fix, verify build passes, run targeted review."
argument-hint: "[bug-description]"
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.3-codex
---

# /quick-fix — Rapid Bug Fix

Fix: **$ARGUMENTS**

1. **Diagnose** — Read errors/stack traces, trace execution via `agents/code-explorer.md` approach, find root cause
2. **Fix** — Minimal change to root cause. No refactoring, no features, no "while I'm here" improvements.
3. **Verify** — `tsc --noEmit`, `npm run build`, run related tests
4. **Quick review** — Check fix for security issues, swallowed errors, edge cases
