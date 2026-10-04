---
name: session-init
description: Lightweight session initialization. Reads latest manifests and handoffs to resume context. Loads only what the current task needs. Trigger on session start, "resume", "pick up where I left off", "continue from last session", "init".
---

# Session Init Skill

Initializes a session with minimal context. Checks for prior work to resume, cleans stale data, and reports readiness.

## When to Activate

- First message of a new session (if user wants to resume prior work)
- User says "resume", "init", "pick up where I left off", "continue from last session"

## Protocol

### Step 1: Check for Active Handoffs

```bash
ls -lt _context/handoffs/*.md 2>/dev/null | head -3
```

If a handoff exists from the last 48 hours, read and summarize the most recent one in 2 sentences.

### Step 2: Check for Active Manifests

```bash
# Today's manifests
ls .claude/manifests/$(date -u +%Y-%m-%d)/*.jsonl 2>/dev/null
# Yesterday's manifests
ls .claude/manifests/$(date -u -v-1d +%Y-%m-%d)/*.jsonl 2>/dev/null
```

If manifests exist from today or yesterday:
1. Count total entries across all files
2. Extract entries with `type: "followup"` or `type: "error"`
3. Summarize: N findings, N decisions, N follow-ups, N errors

### Step 3: Clean Stale Data

```bash
# Archive manifest folders older than 7 days
find .claude/manifests/ -maxdepth 1 -type d -mtime +7 -not -name archive -not -name manifests 2>/dev/null | while read dir; do
  mv "$dir" .claude/manifests/archive/ 2>/dev/null
done
```

### Step 4: Report

Present a brief session context (under 150 tokens):

```
Session ready.
- Handoff: {title} ({date}): {1-line summary}
- Manifests: {N} entries from {date}. Follow-ups: {list}
- Suggested next: {action from handoff or open follow-ups}
```

If nothing exists:
```
Clean session. No prior handoffs or manifests.
```

## Rules

- NEVER load other skills proactively. Skills load on demand by trigger.
- Keep init output under 150 tokens. The point is to stay lean.
- If user explicitly states what they want to work on, skip resume checks and go straight to their task.
- Do NOT read MEMORY.md here; it is auto-loaded by Claude Code already.
