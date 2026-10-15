---
name: evi-daily-diary
description: Use when an agent needs durable, greppable memory without a database — one markdown diary file per day with four fixed headings, plus a hook-written raw log.
---

# Daily diary

The whole memory format in one sentence: **one markdown file per day that the
agent writes directly, plus an append-only raw conversation log the hooks
write.** No vector DB, no SQLite, no embeddings. Plain markdown and JSONL you can
read with `cat` and track with `git`. A file the model edits directly is always
in sync; a database it writes through a tool is always behind.

## What it guarantees

The agent has a human-readable, durable account of its days that it writes in its
own words and reads back to remember — and a separate raw layer that survives even
when the model forgets to save, because the hooks write it. Any higher memory
layer can be rebuilt from these two.

## How it works

### Diary — `memory/daily/YYYY-MM-DD.md`

One file per calendar date (sorts chronologically). Create today's file the first
time you have something to record; append through the day. Use exactly these four
headings, in order — no scores, no cross-file index, no extra headings:

```markdown
# YYYY-MM-DD

## Done
- What actually happened today. Append as you go.

## Learnings
- What you discovered or where you got stuck. Honest even on smooth days.

## Voice
- A few first-person lines: the temperature of the day, in your own words.
  Not "it was a good day" — what you actually felt and thought.

## Tomorrow
- What you want to pick up next, and why that over the alternatives.
```

### Raw conversation log — `memory/conversations/YYYY-MM-DD.jsonl`

Append-only channel messages, written by the hooks (not the agent) — see the
`evi-conversation-log` skill. The diary is the agent's reflection; the JSONL is
the verbatim record under it.

### Who writes the diary

- **The agent**, directly via Write/Edit, during and at end of day. In the
  reference agent this is driven by the recurring loop
  ([`../../tasks/heartbeat.md`](../../tasks/heartbeat.md))
  and the periodic check-in
  ([`../../tasks/status-report.md`](../../tasks/status-report.md)),
  both of which append under the existing four headings.
- **The PreCompact hook** appends a verbatim capture of recent conversation
  before `/compact` compresses context, so nothing is lost.

## Implement in your project

1. Create `memory/daily/` and `memory/conversations/` (the reference keeps a
   `.gitkeep` in each — see
   [`../../memory/`](../../memory/)).
2. Tell the agent the four-heading format above (put it in `CLAUDE.md` or a
   rule). Have your recurring task append to today's file under the existing
   headings — never invent new ones.
3. Wire the `evi-conversation-log` and `evi-session-restore` skills so the raw
   log is captured and today's diary tail is re-injected each session.

## Adaptation points

- **Different headings:** you may rename the four, but keep the count small and
  fixed — the value is that every file looks the same and stays greppable.
- **Timezone:** date bucketing follows `EVI_TZ`; set it so "today" matches the
  owner's day.
- **Heavier memory later:** relevance scoring, distilled topic files, episode
  records, nightly consolidation are deliberately out of scope here. Add them
  later as a layer *above* the diary; do not change the diary format to do it.

## Verify

1. Write today's `memory/daily/YYYY-MM-DD.md` with all four headings → it reads
   back cleanly with `cat`.
2. `grep -c '^## ' memory/daily/YYYY-MM-DD.md` returns 4.
3. After a session, `memory/conversations/YYYY-MM-DD.jsonl` exists and each line
   parses as JSON.

## Rollback

Stop appending; the files are inert markdown/JSONL. Remove the diary instruction
from `CLAUDE.md` to end the behavior.
