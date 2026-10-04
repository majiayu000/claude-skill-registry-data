---
name: handoff-doc
description: Creates a portable handoff document when switching between chats, tasks, or sessions. Captures context, decisions, and next steps so nothing is lost.
---

# Handoff Doc Skill

Creates a structured handoff document that captures the current session's context. Use when switching between Cowork tasks, moving from mobile Claude to desktop, or ending a session to resume later.

## When to Activate

- User says "handoff", "hand off", "wrap up", "switch task", "continue later", "save progress"
- User is about to end a session with unfinished work
- User wants to move context from mobile Claude chat to Cowork
- User wants to start a new task and carry over context

## Handoff Document Format

Create a markdown file at `_context/handoffs/{date}-{slug}.md`:

```markdown
# Handoff: {Task Title}

**Created:** {ISO timestamp}
**From:** {Source - e.g., "Cowork task", "Claude mobile", "Claude web"}
**Status:** {In progress / Blocked / Ready for next step}

## Context

{2-4 sentences: What were we working on? Why does it matter?}

## Decisions Made

{Bullet list of key decisions and their reasoning. Include links to any files created.}

## Current State

{What exists right now? Files created, progress made, where things stand.}

## Open Questions

{Anything unresolved that the next session needs to address.}

## Next Steps

{Ordered list of what to do next. Be specific enough that a fresh Claude session can pick this up cold.}

## Files Referenced

{List of files created or modified during this session, with one-line descriptions.}
```

## Usage Patterns

### End of Session
When the user wraps up:
1. Generate the handoff doc from conversation context.
2. Save to the shared folder.
3. Tell the user: "Handoff saved. Start your next session by sharing this file."

### Mobile to Desktop
When the user says they have notes from mobile:
1. Ask them to paste or upload the mobile conversation summary.
2. Parse it into the handoff format.
3. Resume work from the handoff context.

### Receiving a Handoff
When a handoff doc is provided at session start:
1. Read the doc.
2. Summarize it back to the user in 2-3 sentences.
3. Confirm the next steps.
4. Begin working from where the previous session left off.

## Rules

- Keep handoff docs under 500 words. Concise beats complete.
- Include file paths relative to the shared folder.
- Always list next steps. A handoff without next steps is just a summary.
- Do not include sensitive data (API keys, passwords) in handoff docs.
- Use the slug from the task name for the filename (lowercase, hyphens).

## Handoff Directory

Store all handoffs in `_context/handoffs/`. This becomes a session history over time.

```bash
mkdir -p _context/handoffs
```

## Manifest References

When creating a handoff, check for active manifests:

```bash
ls .claude/manifests/$(date -u +%Y-%m-%d)/*.jsonl 2>/dev/null
```

If manifests exist, include them in the handoff:

```markdown
## Manifests
- `.claude/manifests/{date}/{agent}.jsonl` - {N} entries, key finding: {summary}
```

The next session uses the `session-init` skill to read these manifests automatically. Including them in the handoff ensures nothing is lost even if the session-init is skipped.

## Quick Handoff

For fast handoffs when the user is in a hurry:

```markdown
# Quick Handoff: {Title}
**Status:** {status}
**Resume with:** {single most important next action}
**Key files:** {comma-separated list}
**Manifests:** {list manifest paths if any}
```
