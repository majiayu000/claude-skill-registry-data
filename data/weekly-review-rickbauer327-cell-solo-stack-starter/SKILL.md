---
name: weekly-review
description: Use when the user wants to review their week, plan the next one, or asks "what should I focus on". Pulls from the time log, meeting notes, client updates, and open actions to produce a short review and a focused plan.
---

# Weekly Review

Fifteen minutes on Friday that make Monday easy. Look back at what actually happened, look forward at what matters, and surface what's stuck.

## Step 1 — Gather (read what exists, skip what doesn't)
- `logs/time-log.md` — hours by client this week.
- `meetings/*.md` from this week — open actions with owner "Me" and any unresolved open questions.
- `projects/*/updates/` — this week's client updates: promised "next week" items.
- `invoices/` — anything overdue.
- `leads/`, `outreach/` — prospects awaiting follow-up (check follow-up schedules).
- Last week's review in `reviews/` — the plan you're checking against.
- `.solo/business.md` — active clients, to spot anyone who got zero attention.

## Step 2 — Ask two questions
Only two, and only if not answerable from files:
1. "Anything that happened this week that isn't in the files?"
2. "What's the one thing next week has to deliver?"

## Step 3 — Write
`reviews/<YYYY-MM-DD>.md`:

```markdown
# Week of <Mon date> — review

## What happened
- Hours: <total> (<client: h>, <client: h>)
- Delivered: <bullets, from updates/meetings>
- Won / lost / pipeline: <proposals sent, replies, new leads>

## Plan vs. reality
<Last week's plan items with ✅ done / ➡️ carried / ❌ dropped, one line each. Skip if no previous review.>

## Stuck
- <item> — <why> — <the smallest next step>

## Money
- Overdue: <invoices or "none"> · Unbilled: <hours/value or "none">

## Next week
**Must:** <the one thing>
**Should:** <2–3 items>
**Could:** <parking lot>

## Client check
<Any active client with no contact in 7+ days → "Send a note to X."> 

## One observation
<A single honest sentence about the week — pattern, energy, risk. No pep talk.>
```

## Rules
- Facts from files first; the user's answers fill gaps.
- "Must" is exactly one item. If the user gives three, ask which one.
- Every "Stuck" item gets a smallest-next-step, never just a complaint.
- Keep it under a page.

## Do not
- Do not moralize about productivity.
- Do not carry forward more than 5 items — force choices.
- Do not invent activity for days with no data; say "no data logged".
