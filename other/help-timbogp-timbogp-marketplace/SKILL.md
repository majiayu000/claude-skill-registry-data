---
name: help
description: This skill should be used when the user asks for help with the lean-coach plugin — what it does, which skills, commands, agent, or roles it ships, or how to use a specific one. Triggers on the /lean-help command and on phrases like "help with lean-coach", "what can lean-coach do", "list the lean commands", "how do I use customer-interview", "what roles can the coach play", "explain the lean canvas skill". With no specific topic, give the full overview; with a named skill, command, agent, role, or concept, explain just that one. Do not use for actually doing lean work (building a canvas, running an interview) — that's the individual skills.
version: 0.1.0
---

# lean-coach help

Explain the **lean-coach** plugin to the user. This is the plugin's built-in guide: it answers "what can this do?" and "how do I use X?" without making the user read the docs tree.

## How to respond

Look at what the user asked for (the `$ARGUMENTS` from `/lean-help`, or the topic named in natural language):

- **No topic** → give the **full overview** below: the concept, the guide roles, the role-play personas, every skill, the commands, the agent, and the workspace — each in a line — then point to `docs/` and suggest a starting move.
- **A topic** (a skill, command, agent, role, or concept like "canvas", "risk", "pitch", "product/market fit") → resolve it to the matching item(s) and explain **just that**: what it does, when it triggers, how to invoke it on both Claude Code and Codex (`/lean-coach:<skill>`), and what it produces/writes. Then read that item's `docs/<item>.md` (or its `SKILL.md`) and fold in specifics. If ambiguous, list close matches and ask.

Lead with a one-line answer, keep it skimmable, link rather than dumping file contents.

## Full overview (use when no topic is named)

**lean-coach** is a Lean business-development coach built on Ash Maurya's *Running Lean*. Concept: **one coach, many hats** — it guides a venture through the methodology *and* role-plays the people you test it with, then debriefs.

It works across the methodology's spine (see `reference/methodology.md`): **document Plan A → identify the riskiest parts → systematically test**, iterating from an idea toward a plan that works. All venture state persists in a gitignored **`.lean/` workspace** (`reference/workspace.md`).

### Roles (the cast — `reference/roles.md`)
- **Guide roles** (the agent stays itself): **Coach** (navigator), **Strategist** (canvas + risk), **Analyst** (experiments + metrics).
- **Role-play roles** (the agent becomes a character, then debriefs): **Customer**, **Investor**, **Devil's advocate**, **Business partner**, **Mentor**.

### Skills (the cross-agent surface)

| Skill | Role | What it does |
|---|---|---|
| `lean-coach` | Coach | Navigator: where am I, what's riskiest, what's next; onboards the `.lean/` workspace and routes. |
| `lean-canvas` | Strategist | Build/refine the 9-block Lean Canvas; writes `.lean/canvas.md`. |
| `prioritize-risks` | Strategist | Classify & rank riskiest assumptions; pick where to start; writes `.lean/risks.md`. |
| `customer-interview` | Customer | Role-play Problem/Solution/MVP interviews + debrief; writes `.lean/interviews/`. |
| `investor-pitch` | Investor | Role-play a skeptical investor; pitch & traction stress-test + debrief; writes `.lean/pitch/`. |
| `run-experiment` | Analyst | Falsifiable hypothesis + smallest build (Build-Measure-Learn); writes `.lean/experiments/`. |
| `measure-fit` | Analyst | Funnels, cohorts, Sean Ellis test, retention; product/market-fit verdict; writes `.lean/metrics/`. |
| `lean-roles` | Business partner / Devil's advocate / Mentor | Front door to switch persona and run the role-play protocol. |
| `help` | — | This guide. |

Skills trigger automatically from natural language — you rarely name them.

### Commands (Claude Code conveniences)
- **`/lean-coach [topic]`** → the navigator (`lean-coach`).
- **`/lean-canvas [idea|path]`** → build/review the canvas (`lean-canvas`).
- **`/lean-interview [problem|solution|mvp]`** → interview role-play (`customer-interview`).
- **`/lean-role [persona]`** → switch persona (`lean-roles`).
- **`/lean-help [topic]`** → this help.

### Agent
- **`lean-mentor`** — a one-shot subagent that reads the `.lean/` workspace and returns a scored, prioritized "Lean review" (riskiest untested assumptions, stage assessment, weakest canvas blocks, next experiment). Invoked by asking for a mentor review; the interactive Mentor lives in `lean-roles`.

### Claude Code & Codex
The **skills are the shared, cross-agent surface**. On Codex they appear as slash commands (`/lean-coach:lean-canvas`, `/lean-coach:customer-interview`, …) and trigger from natural language on either agent. The `/lean-*` commands and the `lean-mentor` agent are Claude-Code conveniences over those skills; on Codex, invoke the skills directly.

### Where to go next
- Per-skill guides: `docs/README.md` and the per-skill pages in `docs/`.
- Plugin overview and install: `README.md`.
- A typical loop: `/lean-coach` (orient) → `/lean-canvas` (document Plan A) → `prioritize-risks` (find the riskiest assumption) → `/lean-interview problem` (test it) → `run-experiment` / `measure-fit` (verify) → `/lean-role mentor` or `/lean-interview` to rehearse along the way.

## Resolving a named topic

Map the user's word before explaining:
- **"canvas", "business model", "uvp", "unfair advantage"** → `lean-canvas`.
- **"risk", "riskiest", "where to start", "prioritize"** → `prioritize-risks`.
- **"interview", "talk to customers", "problem/solution/mvp interview", "play a customer"** → `customer-interview`.
- **"pitch", "investor", "fundraising", "VC"** → `investor-pitch`.
- **"experiment", "hypothesis", "validate", "smallest test", "landing page", "concierge"** → `run-experiment`.
- **"metrics", "product/market fit", "retention", "cohort", "sean ellis", "funnel", "engine of growth"** → `measure-fit`.
- **"devil's advocate", "business partner", "co-founder", "mentor", "review my model", "switch roles", "what roles"** → `lean-roles` (or the `lean-mentor` agent for a one-shot review).
- **"where am I", "what's next", "coach me", "get started"** → `lean-coach`.

Then open the matching `docs/<item>.md` (or `skills/<item>/SKILL.md`) and explain from it.
