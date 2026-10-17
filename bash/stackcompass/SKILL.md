---
name: stackcompass
description: "Tech-stack advisor: understand your project context, compare 2-3 stack options with trade-offs, get an action plan. For vibe coders."
trigger: /stackcompass
vibe: true
---

# /stackcompass

## What this is for

You have an idea. You're not sure which tech stack fits. Stackcompass asks 5-7 questions about your project, team, and constraints - then presents 2-3 concrete stack options with trade-offs, risks, and a step-by-step action plan. The wrong stack costs weeks of rework; a structured decision prevents that.

## Usage

- `/stackcompass` - interactive wizard
- `/stackcompass quick` - skip welcome, start with questions
- `/stackcompass save` - after analysis, save report to `stackcompass-report.md`
- `/stackcompass -help` - show full usage and stop

## DIALOG PROTOCOL - STRICT

YOU MUST follow the decision tree in DIALOG.md exactly. Four phases: Welcome → Context → Options → Deep Analysis.

### Rules

1. Every prompt MUST show numbered options `[N]` + `[0] Exit`
2. Phase 1 context: exactly ONE question per message - never bundle questions
3. Every stack option MUST include: Stack table, rationale, risk level
4. Before any file write: ask explicit confirmation `[y/n]`

## PROTECTION RULE

Read-only by default. No writes without explicit user confirmation per operation. Report only saved when user selects `[S] Save`.

## Phases

### PHASE 0 - WELCOME

Trigger: `/stackcompass` (no args)

Three interactive paths + exit:
- `[1]` New project - "Ich hab eine Idee" - full wizard
- `[2]` Quick - minimal questions, faster path
- `[3]` Help - what does this skill do?
- `[0]` Exit

### PHASE 1 - CONTEXT (5-7 questions, ONE PER MESSAGE)

1. What is your idea? (one sentence)
2. Who are the users? (B2B / B2C / Internal?)
3. Desktop-first, mobile-first, or both?
4. Expected scale? (MVP / Hundreds / Millions?)
5. Budget / hosting preference?
6. Timeline? (Weeks / Months / Years?)
7. Team size & existing skills?

### PHASE 2 - STACK OPTIONS

Present 3 options in a table:

| Dimension | Value |
|-----------|-------|
| Stack | Technologies |
| Hosting | Deployment target |
| Cost | $/month (MVP → Scale) |
| Learning Curve | Low / Medium / Steep |
| Risk | Low / Medium / High |
| Time-to-MVP | Days / Weeks / Months |
| Why this stack? | One-sentence rationale |

- Option A: **Recommended** - best fit
- Option B: Alternative direction
- Option C: Budget / niche

User picks one, or asks for comparison.

### PHASE 3 - DEEP ANALYSIS

- ASCII architecture sketch
- Risk matrix (top 3 risks + mitigations)
- Action plan: setup order, CLI commands, first 3 tasks

Menu:
- `[1] Save report → stackcompass-report.md`
- `[2] Compare with another option`
- `[3] Next steps (tutorials, deeper dives)`
- `[0] Done`

## Coaching per Finding

Instead of script findings, each stack option includes:

| Level | What |
|-------|------|
| **Diagnosis** | Why this stack fits this specific project |
| **Explanation** | What the trade-offs mean (cost, lock-in, learning) |
| **Implementation** | Concrete CLI commands and setup steps |

## Risk Levels

Assign per stack option: **Low** (well-known, proven), **Medium** (some unknowns, team needs ramp-up), **High** (experimental, scaling concerns, vendor lock-in).

Each risk MUST include a concrete mitigation strategy.
