---
name: "session-context"
description: "Load development context at session start: git branch, uncommitted changes, CONTEXT.md / TODO.md / open issues. Use when: starting a new coding session, resuming interrupted work, or when the agent needs to orient itself quickly before acting. Inspired by: disler/claude-code-hooks-mastery session_start pattern."
---

# Session Context Skill

## When to trigger

- Starting a new session
- "orient yourself", "load context", "what's the current state"
- "nhắc lại context", "tóm tắt trạng thái"
- Session start hooks firing

## What to do

### Step 1 — Git state
```bash
git status --short
git log --oneline -5
git branch --show-current
```

Report: current branch, uncommitted files, last 5 commits.

### Step 2 — Context files (read if present)
- `CONTEXT.md` — project-specific session context
- `TODO.md` — open action items
- `CLAUDE.md` — agent instructions
- `AGENTS.md` — agent entry point

Do not fail if files are missing — skip silently.

### Step 3 — Session summary

Output a compact summary:
```
Branch: [branch-name]
Uncommitted: [N files or "clean"]
Last commit: [message]
Open todos: [count or "none found"]
Active context: [key points from CONTEXT.md or "none"]
```

## Graceful degradation

- Missing git: skip git section, note "not a git repo"
- Missing context files: skip sections, do not error
- Never block the session — always complete with partial data if needed

## Output format

Plain text, compact. Max 20 lines. No headers unless content is long.
