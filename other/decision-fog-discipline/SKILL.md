---
name: decision-fog-discipline
version: "1.0.0"
user-invocable: false
description: "Hard discipline when the path is still foggy: state destination, maintain decision tickets, graduate fog before solution exploration or OpenSpec proposal; ask humans one ticket at a time via clarifying-question-discipline. Triggers — 「决策雾」「决策票」「清雾再方案」「目的地未清」「decision fog」 / decision fog discipline, decision tickets. Do NOT use as a name alias for wayfinder."
---

# Decision Fog Discipline

> Internal shared skill. Use when the agent cannot yet honestly list 2–5 solution directions because destination or key decisions are still foggy (including across turns). Hosts declare it in `dependencies` and abort if missing.
>
> **Name note:** intentionally **not** named `wayfinder`. Use this name only.

## Iron Law

**NO SOLUTION-EXPLORATION TABLE OR SOLUTION-PICKING PROPOSAL WHILE BLOCKING FOG REMAINS.**

Allowed while foggy: clarifying questions, analysis, OpenSpec scaffolding that does **not** pick a solution, fog-map / ticket notes.

## Loop

1. **Destination** — one short success picture (what “done” looks like).
2. **Tickets** — list open decisions (fog items). Keep short.
3. **Resolve** — one ticket at a time; human asks follow `clarifying-question-discipline` (recommended answer required).
4. **Graduate** — when blocking tickets are resolved or explicitly deferred with reason → enter host solution exploration / proposal.

**Skip:** user explicitly skips fog work → 留痕 `【决策雾跳过】reason=…` then proceed.

## Forbidden

- Jumping to a full solution comparison while critical tickets are open (unless skipped)
- Replacing OpenSpec behavioral specs with the fog map
- Renaming to `wayfinder` in this repository
- Multi-question dumps when resolving tickets

## Integration guide

- Hosts: before “探索方案” / solution review that picks a direction — if foggy, load this skill first.
- Distinct from `design-approval-gate` (post-choice impl gate) and `openspec-explore` (open stance, no ticket map).
- Prefer `user-invocable: false`.
