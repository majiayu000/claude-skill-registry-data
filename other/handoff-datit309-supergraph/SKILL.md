---
name: handoff
description: Compact current session context into a handoff document for seamless continuation in a new session. Use when context window is exhausted, switching machines, handing work to another agent, or ending a long session mid-task.
---

# /supergraph:handoff

Compress session state to a compact document. The next session picks up exactly where this one left off.

Announce: "📦 /supergraph:handoff — compacting session state..."

## Steps

### 1. Capture current state

Gather live state — do not rely on memory:

```bash
git status --short
git log --oneline -10
```

Read active plan file (if any) from `docs/supergraph/plans/`.

### 2. Write handoff document

Save to `$TMPDIR/supergraph-handoff-<YYYY-MM-DD>.md` — NOT in the workspace (avoids accidental commits).

```markdown
# Supergraph Handoff — <YYYY-MM-DD>

## Goal
[One sentence: what we were trying to accomplish]

## Status
[In-progress / Blocked / Ready for next phase]

## Active Plan
Path: [docs/supergraph/plans/<slug>.md]
Current task: Task N — [description]
Remaining tasks: [list with Status values]

## What Was Done
- [Completed task summaries — brief, no code]

## What Is Left
- [Remaining tasks, in order]
- [Any stuck tasks and why]

## Blockers / Open Questions
- [List — or "none"]

## Key Files Changed
- [path] — [what changed, one line]

## Git State
Branch: [branch name]
Last commit: [hash] [message]
Uncommitted: [list or "none"]

## Environment Context
[Copy from plan's Environment Context section]

## Suggested Skills for Next Session
1. /supergraph:scan (always first)
2. /supergraph:execute plan <slug> (continue tasks)
   or /supergraph:tdd (if resuming single task)
3. /supergraph:fix → /supergraph:verify → /supergraph:review

## Notes
[Anything non-obvious a fresh agent needs to know]
```

Rules for content:
- Reference artifacts by **path or URL only** — never duplicate code or file content
- Keep the document under 150 lines
- No session-specific context (e.g., "as I said earlier") — self-contained

### 3. Report handoff location

```
✅ /supergraph:handoff complete
- Document: $TMPDIR/supergraph-handoff-<date>.md
- Status: [current status]
- Resume: /supergraph:scan → read handoff doc → /supergraph:execute plan <slug>
```

## Rules

- Never save to workspace — always `$TMPDIR`
- References only, no content duplication
- Under 150 lines — force brevity
- Always include "Suggested Skills" so the next session has a clear entry point
