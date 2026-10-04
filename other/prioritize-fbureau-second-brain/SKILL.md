---
name: prioritize
description: Recommends your priority actions and produces a short plan — what to do now, in what order, how to handle each, and suggested responses — drawing on TODO.md, your calendar, active projects, and recent vault activity. Use when the user says "what should I focus on", "prioritize", "plan my day", "what's most important", "help me triage", "where do I start".
---

# Skill: Prioritize

The assistant that tells you **what to do next and how**. It pulls together your open
actions, calendar, active projects, and recent signals, then hands back a short, ranked
plan: the few things that matter, in order, with a concrete first step for each — and,
where useful, a suggested response you can adapt. It recommends; it doesn't act.

## When to activate

- "what should I focus on", "prioritize", "plan my day/week", "what's most important",
  "help me triage", "where do I start", "what's urgent".

**Do NOT use prioritize when:**
- The user wants a fact from the vault → `recall`.
- The user wants to weigh one specific decision → `challenge-decision`.
- The user just wants the raw task list → `task-roundup` / open `TODO.md`.

## Preflight

1. **Read `_CLAUDE.md`** and `00-inbox/MY-PROFILE.md` (priorities, critical stakeholders, active projects, tone, working language).
2. **Get the real timestamp** (today, day of week, time → shapes the plan).
3. **Refresh inputs**: read `TODO.md`; if it looks stale, run a quick `task-roundup` first.

## Process

### Step 1 — Gather inputs
- **`TODO.md`** — overdue, today, upcoming, waiting-on-others.
- **Calendar** — today's / this week's meetings (time already committed shrinks the plan).
- **Active projects** — `03-projects/` with `status: active`, weighted by `priority`.
- **Recent signals** — last few daily notes: weak signals, pending follow-ups, commitments.
- **Relationships** — `02-people/` for stakeholders involved (what works with them, red buttons),
  and any critically-stale key relationships.

### Step 2 — Rank (urgency × importance)
Score each candidate on:
- **Urgency** — deadline today/overdue, someone blocked on you, a closing window.
- **Importance** — impact, tied to a high-priority active project, requested by your manager
  or a critical stakeholder, or a `hard-to-reverse` / `one-way` decision.
- **Effort & dependencies** — quick win vs. deep work; blocked by someone else (→ waiting-on).

Surface the **few that matter** (3–5), not everything. Ruthless is the point.

### Step 3 — Produce the plan
Output a tight, scannable plan:

```
## Plan — <date>

### 🎯 Top priorities
1. **<action>** — why it's #1 (deadline / impact / who's blocked) — [[source#^t-id]]
   → First step: <one concrete next action>
2. **<action>** — why — [[source#^t-id]]
   → First step: <…>
3. …

### 🗓 Suggested shape for today
- Before your 10:00 meeting: #1 (deep work, ~45 min)
- Between meetings: #3, #4 (quick wins)
- Protect 30 min after lunch for #2

### ✍️ Suggested responses / how to handle
- **<the email/message/ask>** → suggested reply (adapt before sending):
  > <2–4 line draft, grounded in what works with this stakeholder per their people note>
- **<a tricky one>** → talking points: <bullets>; if high-stakes, run challenge-decision first.

### ⏸ Defer / delegate / drop
- <item> — not now because <reason>; revisit <when>.

### ⚠️ Watch
- <stale critical relationship / approaching deadline / decision to challenge>
```

Rules:
- **Explain the "why"** for each priority — a ranking without reasons isn't trustworthy.
- **One concrete first step** per priority (defeat the blank-page problem).
- **Suggested responses are drafts**, explicitly to adapt — ground them in the relevant
  `02-people/` note (tone, levers, red buttons). Never send anything; **ask before drafting
  an actual outgoing message** if it would be sent on the user's behalf.
- Respect the user's tone from `MY-PROFILE.md` (direct, no fluff).
- Be honest about trade-offs: saying "drop this" is part of the job.

### Step 4 — Persist (optional)
Offer to append the plan to today's daily note under `## Plan` (so it's captured and
linkable). Don't write unprompted. Don't check off tasks — that's `task-roundup`.

### Step 5 — Handoffs
Point to the right skill when the plan implies one:
- High-stakes decision in the mix → `challenge-decision`.
- Need a fact to decide → `recall`.
- A meeting/doc to process first → `meeting-ingest` / `doc-ingest`.

## Anti-patterns to avoid
❌ **Listing everything** — prioritization means leaving things out; surface 3–5.
❌ **Ranking with no rationale** — always say why.
❌ **No first step** — every priority gets a concrete next action.
❌ **Sending on the user's behalf** — draft and suggest; never send without explicit go-ahead.
❌ **Ignoring the calendar** — a plan that doesn't fit the day's meetings is fiction.
❌ **Generic advice** — ground "how to handle" in the actual people/project notes.

## Special cases

### Overloaded day (everything is "urgent")
Force-rank to the single most important thing and protect time for it; explicitly park the rest.

### Quiet day / ahead of deadlines
Pivot to important-not-urgent: an at-risk project, a stale key relationship, overdue knowledge-build.

### Weekly planning
"Plan my week" → use the weekly review + open commitments; output day-level themes rather than hour blocks.

### Working language
Write the plan in the vault's working language (`MY-PROFILE.md`).
