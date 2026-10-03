---
name: queue-check
description: >-
  Reconcile the task queue against everything the user has asked in this
  session. Use when the user says "queue check", "you missed my prompt",
  "you didn't track that", "find missing todos", "what's outstanding", or when
  resuming after a context reset and the queue may have drifted.
---

# Queue Check

Reconcile the tracked task list against what the user actually asked for. A user request with no matching tracked item is a defect — fix the queue, then the work.

## Backlog scan

1. **Current message** — every deliverable in the latest user message, including sub-clauses.
2. **Session history** — walk prior user messages (including anything before a summary/context reset). List every ask: explicit, implied ("also…", "what about…", "and the rest"), and reported bugs (each "broken/not working" report is its own item: reproduce → fix → regression test → verify).
3. **Existing queue** — compare against current todos. Classify each ask: tracked & correct status / tracked but stale status / **untracked**.
4. **Backfill** — add every untracked ask; correct stale statuses honestly (nothing "completed" that wasn't verified; nothing "in progress" that isn't being worked).
5. **Prioritize** — user-stated order first, then blockers, then FIFO. Exactly one item in progress.

## Report (always emit)

```markdown
## Queue status
**In progress:** [item] — [where it stands]
**Pending:** 1. [item] 2. [item] …
**Completed this session:** [items, with verification evidence noted]
**Backfilled just now:** [items that had been missed, or "none — queue was accurate"]
**Dropped/cancelled:** [items the user explicitly dropped]
```

If the queue was accurate, say so in one line — do not invent corrections.

## After the report

Resume the highest-priority open item immediately unless the user redirects. Do not treat the queue check itself as progress on the work.
