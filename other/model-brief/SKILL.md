---
name: model-brief
description: "Creates the model brief: purpose, model class, mechanisms, data, validation level, team, timeline and risks."
argument-hint: "[model name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /model-brief — Model Brief

**Category:** Scoping & Design · **Primary agent:** `project-planning-specialist`

Creates the model brief: purpose, model class, mechanisms, data, validation level, team, timeline and risks.

Arguments: `$ARGUMENTS`

## Purpose
Write the model brief: the one document that says what a model is for and what it is not for, which class it belongs to, which mechanisms it must contain, what data it needs, how deeply it will be validated, who will build it, by when, and what could go wrong. The output is the reference against which every later decision and the final validation are judged.

**Use it when** a modeling project has been scoped and the model class chosen, before specification starts.

**Do not use it when** the work is exploratory and labeled as such (`/quick-model`), or the question is not yet precise (`/scope-question`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - docs/briefs/<name>-scope.md (recommended)
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `project-planning-specialist` — primary agent; coordinates the work and integrates results
- `economic-reasoning-specialist` — Frames the economic question and tests whether results make economic sense
- `modeling-methodology-specialist` — Chooses methods and architecture across model families, sets code and data standards, and resolves technical trade-offs between traditional, structural and AI approaches
- `model-risk-governance-specialist` — Defines model risk levels and validation depth, enforces builder-validator independence, governs AI/LLM use and recommends release or block

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Purpose | forecasting, policy analysis, scenario, research | Validation focus |
| Risk level | low, medium, high | Validation depth and sign-offs |
| Ownership | studio team, counterpart, shared | Documentation and training |
| Timeline | weeks, months | Model size and scope |

## Workflow
1. Collect the scoping note, the chosen model class and available resources
2. Draft the brief from `docs/templates/model-brief.md`, one section at a time, with approval for each
   - State non-purposes explicitly
3. Assign risk level with the model-risk-governance-specialist
4. Set milestones sized to the model class and flag dependencies
   - Include data, validation and documentation milestones

## Checkpoints with the user
- After each section of the brief
- After risk assignment: confirm validation depth

## Common pitfalls
- No non-purposes, so the model is later used for everything
- Timelines that ignore validation
- Unclear ownership after delivery

## Output
`docs/models/<name>/model-brief.md`

The brief covers purpose and non-purposes, model class, mechanisms, data, validation level, team, timeline, risks and dependencies.

## Gate / verdict
- Purpose and non-purposes are stated
- Risk level and validation depth are agreed
- Milestones include validation and documentation
- Ownership after delivery is stated

## Suggested next steps
- `/literature-review`
- `/model-spec`
