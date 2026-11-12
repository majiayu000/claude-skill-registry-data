---
name: settings
description: "Views or changes studio configuration: rigor level, default languages, review requirements and confidentiality defaults."
argument-hint: "[show|set <key> <value>]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
---

# /settings — Settings

**Category:** Onboarding · **Primary agent:** `project-planning-specialist`

Views or changes studio configuration: rigor level, default languages, review requirements and confidentiality defaults.

Arguments: `$ARGUMENTS`

## Purpose
View or change the studio's configuration (rigor level, default languages, review requirements, confidentiality defaults) with the consequences of every change explained before it is made. Changes that weaken validation or confidentiality require explicit confirmation.

**Use it when** a team wants to adapt the studio to its stack, risk appetite or institutional rules.

**Do not use it when** setting up a new environment (`/setup-environment`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - studio-config.yaml
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `project-planning-specialist` — primary agent; coordinates the work and integrates results

## Workflow
1. Show current settings with explanations
2. On a change request, explain the consequence (e.g. lowering rigor skips independent validation for small models)
3. Ask for confirmation, then edit `studio-config.yaml`
4. Warn if a change conflicts with `.claude/docs/model-risk-levels.md`

## Common pitfalls
- Lowering rigor for high-risk models
- Changing confidentiality defaults without reviewing data already in the project

## Output
`studio-config.yaml`

The configuration file is updated, and the conversation records what changed and why.

## Gate / verdict
- Changes that weaken confidentiality or validation need explicit user confirmation
- Each change is explained before it is applied

## Suggested next steps
- `/help`
