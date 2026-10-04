---
name: audit
description: "Run all quality gate agents on the codebase: code review, security, performance, silent failures, comments."
allowed-tools: Read Grep Glob Bash
model: gpt-5.3-codex
---

# /audit — Full Quality Audit

Run every quality gate agent:

1. **Code review** — `agents/code-reviewer.md`
2. **Language review** — `.ts/.tsx/.js/.jsx` → `agents/typescript-reviewer.md` | `.py` → `agents/python-reviewer.md`
3. **Security** — `agents/security-reviewer.md` (OWASP, secrets, deps)
4. **Silent failures** — `agents/silent-failure-hunter.md` (empty catches, swallowed errors)
5. **Comments** — `agents/comment-analyzer.md` (accuracy, staleness, TODOs)
6. **Performance** — `agents/performance-optimizer.md` (bundle, algorithms, rendering)

Output: Per-category PASS/WARN/FAIL + overall verdict with severity counts.
