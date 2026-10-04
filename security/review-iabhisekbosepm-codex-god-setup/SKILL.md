---
name: review
description: "Run the full code review pipeline on recent changes. Auto-selects reviewers based on file types."
argument-hint: "[file-or-path]"
allowed-tools: Read Grep Glob Bash
model: gpt-5.3-codex
---

# /review — Code Review Pipeline

Target: `$ARGUMENTS` (or all uncommitted changes if none provided)

1. **Detect scope** — `git diff --name-only` + `git diff --staged --name-only`
2. **General review** — Apply `agents/code-reviewer.md`
3. **Language review** — `.ts/.tsx/.js/.jsx` → `agents/typescript-reviewer.md` | `.py` → `agents/python-reviewer.md`
4. **Security scan** — `agents/security-reviewer.md` on auth/API/DB code
5. **Silent failure check** — `agents/silent-failure-hunter.md`
6. **Summary** — Severity counts + verdict (Approve / Warning / Block)
