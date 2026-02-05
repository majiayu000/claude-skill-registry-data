---
name: session-manager
description: |
  Manage Claude Code sessions for the current branch. Use this skill when:
  - User asks "what's next?" or "where was I?"
  - User starts work on a new branch without a session
  - Before committing (to update session log)
  - When resuming work after a break
---

# Session Manager

Manage work sessions that persist context across conversation resets.

## When to Use This Skill

Proactively invoke when user:
- Asks about current work context
- Switches branches and needs session context
- Wants to create or update a session
- Is resuming work or asking "what's next?"

## Context Files (Auto-Injected)

- **sessions.yml**: Rules for session workflow (BLOCKING requirements)
- **sessions.md**: Detailed examples and patterns

Read these files for complete guidance. This skill provides quick reference only.

## Quick Reference

### Check Session Status
```bash
git branch --show-current
# Sanitize: replace / with -
# Read: .claude/branches/<sanitized>
# Read: .claude/sessions/<session>.md → focus on Next Steps
```

### Create Session
Use `/memento:session create` command.

### Update Session
Edit session file directly. Update triggers:
- Beginning work
- After milestone
- Before pause
- Before commit (atomic with code)

## Key Rules (from sessions.yml)

1. **Never guess current branch** — always `git branch --show-current`
2. **Session = Branch = Issue** (1:1:1 mapping)
3. **Atomic commits** — session + code together
4. **BLOCKING**: No source edits without active session

## What This Skill Does NOT Do

- Define session file format (see sessions.md)
- Define workflow patterns (see sessions.yml)
- Handle git operations (see git.yml/git.md via onus)
