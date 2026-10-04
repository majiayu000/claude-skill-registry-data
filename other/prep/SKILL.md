---
name: prep
description: Use when the user has a meeting, call, 1:1, a person to meet, or a decision coming up and needs to walk in prepared. Assembles a one-page brief from context/, wiki/, connections, open loops, and the knowledge graph — who · what · goal · history · open loops · the ask · risks. Trigger on "/prep", "prep me for", "brief me on <person/meeting>", "what do I need to know before", "get me ready for".
---

# Prep

Chief-of-Staff prep: walk into anything already briefed. Pull the scattered context into one page.

## When to run
- Before a meeting / call / 1:1, meeting a person, or making a decision.
- Surfaced by `/daily` ("on the calendar → offer `/prep`").

## The output (always this shape)
```
## Prep — <meeting / person / topic> · <date · time>
**Goal** — what a good outcome looks like for you, in one line.
**Who** — attendees + the one thing that matters about each.
**Context** — the 3–5 facts / history you need (each with a source).
**Open loops** — what's owed by/to them (open-loops · wiki · threads).
**Your move** — the ask, 2–3 talking points, the decision you want.
**Risks / landmines** — what could go sideways + how to handle it.
```

## Process
1. **Scope it.** Identify the meeting / person / topic and the user's goal.
2. **Gather (read, don't guess):** `context/` (about-me, business, team, priorities), `wiki/` (past thinking), `decisions/log.md`, open loops (`tools/open_loops.py`), and `/graph-query` to surface non-obvious connections (who/what relates to this).
3. **Pull live where connected.** If calendar / CRM / notes MCPs are wired (`connections.md`), pull the invite, the account, and the last meeting notes. If nothing is connected, work from files and say so.
4. **Synthesize to one page** in the shape above. Cite a source for each fact (Verification Gate); flag anything unconfirmed.
5. **Offer next moves:** `/draft` a pre-read or follow-up; `/decide` if a decision is the point.

## Autonomy
**L2** — assembles the brief; the human runs the meeting. Read-only on external systems.

## Guardrails (from CLAUDE.md)
- **Cite, don't invent** — every fact traces to a source; flag gaps.
- Pull confidential specifics live; never persist them to the repo.
- Respect the sensitive-data line — no PHI/PII in the brief or the repo.
