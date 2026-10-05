---
name: handing-off-session
description: Generate structured session handoff notes for cross-session continuity. Use at end of session or when switching context.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Glob, Grep
  argument-hint: [output-path]
  context: inline
  stability: development
---

# Session Handoff

**Target**: $ARGUMENTS

Captures session state as a structured markdown note for the next session to
pick up. Stateless — markdown files only, no database, no daemon.

## Arguments

| Position | Name | Required | Default | Description |
|----------|------|----------|---------|-------------|
| 1 | `output-path` | no | auto | Where to write the handoff note. |

**Default output path:** `.claude/handoffs/YYYY-MM-DD-<short-description>.md`

The `<short-description>` is a 2-4 word slug derived from the session's primary
focus (e.g. `2026-04-06-session-handoff-skill.md`).

## When to Use

- End of a work session
- Switching context to a different project or task
- Before a long break
- When context window is getting full and you want to preserve state

## Workflow

1. **Scan conversation** — Identify completed actions, decisions, and pending work
   from the current session context.

2. **Check git state** — Run `git diff --stat` and `git log --oneline -10` to
   capture recent changes and commits.

3. **Extract signals** — Collect decisions made, alternatives rejected, blockers
   encountered, and open questions.

4. **Ensure output dir** — Create `.claude/handoffs/` if it doesn't exist.

5. **Write handoff note** — Use the template below. Be concise — enough to
   resume, no more.

## Output Template

```markdown
# Session Handoff — <date>

## What Was Done
[Completed work, key commits, PRs created/merged]

## What's Pending
[Open tasks, unfinished work, next steps]

## Key Decisions
[Architectural choices, trade-offs made, rejected alternatives]

## Modified Files
[List of files changed with brief reason]

## Blockers
[External dependencies, open questions, things that need user input]
```

## Picking Up a Handoff

Next session can read the latest handoff:

```bash
# Find latest handoff
ls -t .claude/handoffs/*.md | head -1
```

Or read all recent handoffs to rebuild context across multiple sessions.

## Quality Check

- Correct > Complete > Minimal (ACE-FCA)
- ~20-50 lines output per handoff
- Every item traces to a concrete action or artifact
- No raw dumps — structured summaries only
