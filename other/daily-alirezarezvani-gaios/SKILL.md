---
name: daily
description: Use at the start of a working day (or when the user asks "what should I focus on today / give me my brief / daily standup"). Produces a one-screen daily brief — today's top 3, open loops that need a nudge, what's slipping, and a suggested focus order. Trigger on "/daily", "daily brief", "what should I focus on today", "morning brief", "standup".
---

# Daily Brief

The Cadence layer: turn scattered priorities, commitments, and calendar into one focused screen so
the day starts pointed at leverage — not at the inbox.

## When to run
- Start of day, or any time the user asks what to focus on now.
- After a `/triage` dump, to fold new items into the day.

## The output (always this shape)
```
## Daily brief — <date>
**Today's 3** — the highest-leverage moves (tied to priorities). Each: action + why it matters.
1. … 2. … 3. …
**Open loops needing a nudge** — commitments owed by/to you, with next step.
- <loop> → <next step> (waiting on <who>)
**Slipping** — priorities/projects at risk, with the one action that unblocks.
**On the calendar** — meetings that need prep → offer `/prep`.
**Parked** — explicitly not today (so it's off the mind).
```

## Process
1. **Gather (read, don't guess):** `context/priorities.md` (the 90-day outcomes), `decisions/log.md` (recent calls), `projects/` (active workstreams), and open commitments — from `tools/open_loops.py` if present, else from notes/projects.
2. **Pull live where connected:** if a calendar/task/CRM MCP is wired (`connections.md`), pull today's meetings and due items. If nothing is connected, work from files and say so.
3. **Rank to 3.** Map candidates to priorities; pick the 3 with the most leverage (find-the-constraint). Everything else is loops/parked.
4. **Flag slippage.** Compare priorities to recent activity; name what's at risk + the single unblocking action.
5. **Offer next moves:** `/prep` for each meeting, `/structure` for any fuzzy item, `/draft` for comms owed.

## Autonomy
**L2 — drafts the brief; the human acts.** Never auto-sends anything it surfaces.

## Guardrails (from CLAUDE.md)
- Pull confidential figures live; never persist them to the repo.
- Route owners to the team by default; don't pool everything on the user.
- Any external comm it proposes is a **draft**, in `references/voice.md` register.
