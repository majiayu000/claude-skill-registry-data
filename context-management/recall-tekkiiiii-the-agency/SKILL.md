---
name: recall
description: >
  Quick single-project context check. Reads next-session.md directly (no subagent)
  and outputs a 6-field briefing. For multi-project resume, use /pd-resume instead.
  Invoke as /recall [slug] or when user says 'resume session', 'pick up where we left off'.
  SSOT for project paths is ~/.claude/memory/medium-term.md.
---

# Recall

Direct-read briefing for one project. No subagents, no temp files.
For multi-project autonomous resume, use `/pd-resume` instead.

## SSOT

Project registry: `~/.claude/memory/medium-term.md` — Active Projects table.
Read it FIRST. This is the ONLY project-to-path map.

## If Slug Not Found

1. Check `~/.claude/memory/medium-term.md` Active Projects table.
2. If not found → output: `PROJECT NOT FOUND: {slug}` and stop.

## Step 1 — Resolve Project Path

1. Read `~/.claude/memory/medium-term.md`
2. Find the slug in the Active Projects table → get project path
3. If not found → stop with error

## Step 2 — Read Briefing

Read `{project-path}/memory/next-session.md` directly using the Read tool.
**Do NOT spawn a subagent for this.**

next-session.md is self-contained — save-state writes phase, next action,
blockers, decisions, mid-flight, and delegated statuses into it.

If the file doesn't exist or is empty, output:
```
RECALL — {slug}
Phase: unknown
Next: read project memory and assess current state
Blockers: none
Decisions: none
Mid-flight: none
Context: no prior session found
```

## Step 3 — Output Briefing

Format the content from next-session.md into:

```
RECALL — {slug}

Phase: [from next-session]
Next: [from next-session]
Blockers: [from next-session, or "none"]
Decisions: [from next-session, or "none"]
Mid-flight: [from next-session, or "none"]
Context: [from next-session status/notes, 1-2 sentences]
```

Output only the briefing. No preamble, no commentary, no follow-up questions.
