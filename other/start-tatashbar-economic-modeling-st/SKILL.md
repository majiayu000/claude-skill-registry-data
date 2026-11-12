---
name: start
description: "First-time entry point. Asks what you want to model, detects project stage, and routes you to the right workflow."
argument-hint: "[none]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /start — Start

**Category:** Onboarding · **Primary agent:** `project-planning-specialist`

First-time entry point. Asks what you want to model, detects project stage, and routes you to the right workflow.

Arguments: `$ARGUMENTS`

## Purpose
Be the first stop for a new user: find out what they want to achieve (answer a question, build a model, produce a forecast, validate a model or adopt an existing one), the size of the work, the audience and the deadline, check what already exists, and recommend the first three skills with reasons. Nothing is written until the user chooses.

**Use it when** a user opens the studio for the first time or starts a new piece of work.

**Do not use it when** the user already knows which skill to run.

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - production/stage.txt (optional)
   - studio-config.yaml
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `project-planning-specialist` — primary agent; coordinates the work and integrates results
- `economic-reasoning-specialist` — Frames the economic question and tests whether results make economic sense
- `modeling-methodology-specialist` — Chooses methods and architecture across model families, sets code and data standards, and resolves technical trade-offs between traditional, structural and AI approaches

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Workflow
1. Greet the user and ask what they are trying to achieve: a question to answer, a model to build, a forecast to produce, a model to validate, an existing model to adopt, code to translate to another language, or a research note, plan or objective (in any form, with or without data) to turn into modeling work
   - If the user brings a note, plan, objective or brief, recommend `/research-plan` first
   - If the user brings code to move to another language or software, recommend `/translate-code` (or `/code-inventory` to look first)
2. Ask the model size class (small, medium, large), the audience and the deadline
3. Run `/project-stage-detect` logic to see what already exists
4. Recommend the first three skills to run, with reasons, and wait for the user's choice
   - Mention existing lego sets that could be reused or extended
5. Write the choice to `production/session-state/active.md`

## Common pitfalls
- Recommending a large model for an urgent, narrow question
- Ignoring existing work in the project

## Output
`production/session-state/active.md`

The session-state file records the user's goal, size class, audience, deadline and chosen path.

## Gate / verdict
- The user has chosen a path; nothing is written before the user agrees
- Recommendations are explained with reasons

## Suggested next steps
- `/scope-question`
- `/research-plan`
- `/adopt`
- `/translate-code`
- `/project-stage-detect`
