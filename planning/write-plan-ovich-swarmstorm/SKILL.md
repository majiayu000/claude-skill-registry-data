---
name: write-plan
description: Use when something non-trivial is to be built or reworked and its implementation plan has to be written, from an idea or from a board, or when a plan has to be redrawn after an increment landed. Produces, through an interview, the one plan document that holds the design, the decisions, the phases and seats, the tracker execute-plan runs from and the orchestrator's mandate. Not for keeping an open discussion (brainstorm), not for writing a phase's tasks (orchestrate-plan, at the phase's open) and not for carrying the plan out (execute-plan).
---

# Write a plan

**One document holds the design and the plan.** What the interview settles is written
once, there, and each task points into it, narrowed to its scope.

**The plan is written for an agent that was not in the conversation.** Read alone, it gives
every decision, its reason and every detail the work needs, so that agent is as aligned as
the person and you are now. Nothing settled lives only in the chat.

**No code in the repository for the thing being planned until the plan is approved.**

1. **Open `YYYY-MM-DD-<topic>.plan.md` before the first question**, through the `aiview` skill: kind `plan`, tags = topic, in the group aiview gives a plan, shared with its task documents when a task needs one. With a roadmap, the slot's slug is a tag. Its two parts, Design and Execution, are `references/skeleton.md`, read before writing the first section. A board on the topic is the starting point: its agreed decisions become rows, numbered in this plan with the board's id in their source (`board <topic>.board#D2`), and are not asked again.
2. **Run the `interview` skill** on the decisions table, and write each section as its decisions land. If the person declines it, offer its short mode; a decision still unasked is a row with source `agent default`. A request that is several independent systems is split first, one plan each. One plan per increment: it stops where the next increment would begin.
3. **Every major area is a deep module**, designed as the `deepen-module` skill says, in the plan's modules section. A module the interview cannot settle there gets its own `module` document, and the plan quotes its entry.
4. **When no row is open, ask once what else this should cover.**
5. **Settle the phases before the cut**: the plan runs on N seats, phase by phase, on the board of the `swarm-board` skill. Read `references/phases.md` now; then ask `phases:`, `seats:` and `verify:`, one per message, as the `orchestrate-plan` skill's `references/mandate.md` says.
6. **Cut the phases** as `references/phases.md` and the `orchestrate` skill's `references/tasks.md` say, **and draw the tracker** to `references/tracker.md`, from `references/tracker-skeleton.md`, both read first. The `execute-plan` skill keeps it from then on. `aiview mermaid-check <plan>`, `aiview tracker check <plan>` and `scripts/decisions.mjs <the plan's folder>` after every edit: the last says whether a topic, an id or a citation collides or points nowhere.
7. **Before the mandate, dispatch a fresh subagent on the `cold-read` skill**, with the plan's id and none of the conversation; discuss with it as a peer, explaining your intent and asking how it read each part, until you understand each other; every point you settle goes into the plan, and it re-reads until it says `ready`.
8. **Close the interview with the orchestrator's mandate**: the questions of the `orchestrate-plan` skill's `references/mandate.md`, the answers in the plan's *Mandate* section and in the one line under the tracker. `tests: at the plan end` adds the tests phase to the tracker then. Whatever the mandate changed in the plan, the cold reader re-reads, until it says `ready` again.
9. **Stop and ask the person to approve the plan.** The request opens on the `agent default` rows, numbered, `contract` ones first, "4 decisions are mine: … confirm them, or name the ones to change", and the link to the plan comes after the list. The approval goes in the status line with the defaults it confirmed, then `aiview plan check <plan>`. No task is written now: each is written at its phase's open.

## Red flags

| Thought | Reality |
|---|---|
| "I'll plan the whole feature while I have the context" | The next plan is written with this increment's learning in hand, which you do not have yet. |
