---
name: prioritize
description: Recommend what to work on now and give a short plan, drawing on open tasks, deadlines, active projects, cooling relationships and the calendar. Use when the user says "what should I focus on", "prioritize", "plan my day", "where do I start", "help me triage", "what's most important".
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, planning, tasks]
    related_skills: [task-roundup, recall]
    requires_toolsets: [second_brain]
---

# Prioritize (Hermes edition)

`sb_agenda` gathers; it deliberately does not rank. Ranking is the whole value you add, so do not
hand back the tool's lists reordered by due date — that is a sort, not a recommendation.

1. `sb_brief` — the profile says what the user is actually optimising for this quarter.
2. Optional, if Google is configured: `sb_calendar()` for today, and pass its `events` into
   `sb_agenda(calendar=[...])` so commitments and tasks are weighed together.
3. `sb_agenda(horizon_days=7)`. Read `signals` first: it names the tensions worth resolving.
4. Rank on four axes, in this order:
   - **Consequence** — what breaks, and for whom, if this slips another week.
   - **Blocking others** — an item someone is waiting on outranks a bigger solo item.
   - **Decay** — a decision with `one-way` reversibility, or a relationship cooling past 60 days,
     gets harder the longer it waits.
   - **Effort** — only as a tiebreaker. Never rank by what is quick.
5. Say what to drop. A priority list that keeps everything is not a priority list. Name one or two
   items to renegotiate or abandon, with the sentence the user could send to renegotiate it.
6. Answer in the working language, at most one screen:
   - **Now** — one item, and the first concrete step.
   - **Today** — three at most, each with why it beats the rest in a half-line.
   - **This week** — the rest, grouped.
   - **Drop or renegotiate** — with the reason.
   - **Waiting on** — who owes what, and whether a nudge is due.
7. If `counts.open_total` is 0, say TODO.md may be stale and offer `/task-roundup` rather than
   concluding there is nothing to do.
8. Read-only skill: propose, never write. If the user accepts a plan, capture it with `/braindump`.
