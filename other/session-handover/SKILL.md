---
name: session-handover
description: >
  Write an end-of-session handover LogEntry capturing current state,
  open threads, next action, and git context for session continuity.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-20260408_0000-SessionHandover
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: event-log
        purpose: Write the session.handover LogEntry with the structured details schema.
      - skill: workitem-management
        purpose: Query in-progress and blocked WorkItems to populate open_threads accurately.
    commands:
      - name: pk-wrapup
        args: ""
        description: "Generate a session handover document from current project state"
---

# Session Handover

## Intro

A session handover is a structured snapshot written at the end of a work
session — before a container restarts, a laptop closes, or a context window
ends. It is the primary mechanism for continuity across sessions. The
handover is a `session.handover` LogEntry, not a flat Markdown file: it
lives in `context/logs/` and is queryable by any downstream skill.

## Overview

### When to write a handover

Two trigger patterns exist — both are valid:

**Pattern A — container restart / shutdown handover**
The user is about to stop the container or close the session and wants the
next session to pick up exactly where this one left off. This is the primary
use case. The handover may be read days or weeks later.

**Pattern B — regular evening cadence**
The user writes a handover at the end of every work session as a habit.
`status-briefing` reads the most recent handover and weights it by age:
a same-day handover is the primary "what happened" source; an old handover
is context only.

Both patterns use identical handover content. The difference is only in how
frequently the skill is invoked.

### What to capture

Work through these sections before writing the entry:

**1. Current state (2–4 sentences)**
What is the overall state of the project right now? What was the last
significant thing completed? Is the codebase in a clean, broken, or
in-flight state?

**2. Open threads**
Every item that is in-progress, blocked, or needs a decision. Query
`workitem-management` for `state: in_progress` and `state: blocked` items.
Include informal threads that are not yet WorkItems — anything the next
session needs to know about.

**3. Next recommended action**
The single most important thing the next session should do first. Be
specific: not "continue working" but "review the auth PR in BACK-042 —
it's approved and ready to merge."

**4. Git context**
Current branch and commit SHA. If there are uncommitted changes, note them.
If there is a stash, note what is in it.

**5. Behavioral retrospective (brief)**
Before writing the entry, scan the session for execution gaps:

- What did I commit to ("I'll track that", "I'll file a workitem")
  but not execute in the same turn?
- What did I skip, defer, or forget that should not have been
  deferred?
- What surprised me, or what did the user have to correct?

For each item: either edit the relevant skill or AGENTS.md directly
(if it is a clear, reusable rule), or create a WorkItem. Do not
leave it as a mental note — the next session starts with the lessons
already encoded only if they are written down before this session
closes.

### Writing the LogEntry

**Step 1 — generate the ID:**

Use `generate_id("LogEntry", slug_text="session-handover")` to get
a collision-free ID following the project's configured format, e.g.:
`LOG-20260410_0020-SnowyEmber-session-handover`

**Step 2 — determine the file path:**

Apply date-based sharding (configured in index-management):
`context/logs/YYYY/MM/{id}.md`

Example: `context/logs/2026/04/LOG-20260410_0020-SnowyEmber-session-handover.md`

**Step 3 — write the file:**

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-{{YYYYMMDD_HHMM}}-{{WordPair}}-session-handover
  created: <ISO 8601 UTC>
spec:
  event_type: session.handover
  timestamp: <ISO 8601 UTC>
  actor: <ACTOR-id or agent name>
  summary: "Session handover — <one-line summary of session>"
  details:
    session_date: "<YYYY-MM-DD>"
    current_state: |
      <2-4 sentences on where things stand>
    open_threads:
      - "<item 1>"
      - "<item 2>"
    next_recommended_action: |
      <specific next step for the next session>
    branch: "<current branch>"
    commit: "<short SHA>"
    behavioral_retrospective:  # optional; omit if no gaps observed
      - "<observation + what was encoded or filed>"
---
```

### Trigger phrases

The agent should write a handover when it hears:
- "write a handover"
- "prepare for shutdown" / "shutting down"
- "save context" / "save state"
- "closing the container" / "restarting"
- "end of session"
- "write a session summary"

This skill also provides the `/pk-wrapup` command for direct invocation —
see `commands/pk-wrapup.md`.

## Gotchas

- **Writing the handover before work is complete.** The handover should
  reflect the actual state at the moment of writing — not the intended
  state. If a task is half-done, say so. The next session needs the truth,
  not the plan.
- **Vague current_state.** "Working on things" is not a current state.
  "BACK-042 auth refactor is merged; BACK-045 is in review and waiting
  for CI; nothing is broken on main" is a current state. Be specific
  enough that someone who wasn't in the session can orient immediately.
- **Using a flat path or wrong ID format.** The handover file must go
  in `context/logs/YYYY/MM/{id}.md` (date-sharded), not flat at
  `context/logs/`. The ID must come from `generate_id("LogEntry",
  slug_text="session-handover")` — not a hand-written slug.
- **Omitting git context.** The branch and commit are the most mechanical
  part of the handover and the easiest to forget. Always include them.
  If there are uncommitted changes, list the files — the next session
  may be working with a different HEAD.
- **Forgetting stashes.** A `git stash` is invisible to the next session
  unless it is noted in the handover. Check `git stash list` before
  writing the handover.
- **Listing only completed work instead of open threads.** A handover that
  only says what was done is a changelog, not a handover. The open threads
  — what is blocked, in-flight, or undecided — are the most important
  content for the next session.
- **next_recommended_action being a list instead of a single action.**
  The next session needs a clear starting point, not a prioritization
  problem to solve before any work can begin. Force yourself to pick one.
  Other items belong in open_threads.
- **Not querying WorkItem state before writing.** Open threads written from
  memory miss things. Always query `workitem-management` for in-progress
  and blocked items before finalizing the open_threads list.
- **Skipping the behavioral retrospective.** The retrospective is
  the mechanism that converts session failures into durable
  improvements. If the session had no corrections, note that
  explicitly in `behavioral_retrospective`. If corrections happened
  and are not encoded, the next session agent starts with the same
  failure modes.

## Full reference

### Relationship to status-briefing

`status-briefing` reads the most recent `session.handover` LogEntry and
weights it by age:

| Handover age | Weight in status briefing |
|---|---|
| < 24 hours | Primary source for "what happened last session" |
| 1–7 days | Secondary source — flagged as stale; git log + WorkItem state carry more weight |
| > 7 days | Skipped — briefing relies on git log and current WorkItem state only |

The handover is a best-effort enrichment, not a required source. If no
handover exists, `status-briefing` reconstructs context from git log and
WorkItem state.

### Handover vs. standup

| | session-handover | standup-context |
|---|---|---|
| **When** | Before shutdown / container restart | Any time; regular cadence |
| **Audience** | The next session (same person or agent) | The team / project record |
| **Focus** | Continuity — what to pick up next | Accountability — what was done |
| **LogEntry type** | `session.handover` | `session.standup` |

### Reading a prior handover

At session start, to find the most recent handover:

```
query_events(event_type="session.handover", limit=1, order="desc")
```

Check `details.session_date` to assess staleness before weighting the
content.

**Before starting any new workstream** identified in the handover,
query the skill index for a relevant skill:

```
search_entities(kind=skill, text=<workstream-keyword>)
```

or call `find_skill(<workstream-keyword>)`. Do this before acting on
any item in `open_threads` or `next_recommended_action` — a matching
skill may exist with processkit-specific conventions that general
knowledge does not carry.
