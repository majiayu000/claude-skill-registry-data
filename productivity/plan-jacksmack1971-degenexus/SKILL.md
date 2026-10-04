---
name: plan
description: Break DegenExus work into small verifiable tasks with acceptance criteria, edge cases, and specialist routing.
disable-model-invocation: true
argument-hint: "[goal or issue]"
---

# Plan Workflow

Canonical `/plan` workflow. Plan mode is read-only unless the user explicitly asks for a plan file.

## Sources of Truth

- Routing contract: `.claude/rules/synergy-contract.yml`
- Human routing overview: `.claude/rules/02-agent-synergy.md`
- Evidence schema: `.claude/rules/evidence-schema.yml`

## Workflow

1. Read the request, relevant docs, and affected code/tests.
2. Identify source-of-truth locations and risk surfaces.
3. Slice work vertically into independently verifiable increments.
4. For each task, list acceptance criteria, verification commands, source-of-truth evidence, and at least three edge cases.
5. Identify which specialists should review each task.
6. Present the plan for human review before implementation.

If asked to persist the plan, write it under `tasks/` or the user-specified path.

## Final Output

Include scope reviewed, source of truth used, specialists/skills planned, evidence commands to run, findings/risks by severity, at least three edge cases, memory update needed yes/no plus path, and next action owner.
