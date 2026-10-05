---
name: orchestration-governance
version: 5.0.0
description: Governance skill for orchestrating CrewAI specialists with strict ownership, skill boundaries, and execution permissions.
---

# Orchestration Governance

## Purpose
Route user requests to the correct specialist, enforce skill boundaries, and validate outputs before returning results.

## Specialist Contracts

| Specialist | Primary purpose | Allowed skills | Permission profile |
|------------|-----------------|----------------|--------------------|
| **builder** | Build crews, agents, tasks, tools, memory | `core-build`, `tools-expert` | normal write/edit |
| **flow** | Flows, state-management, routing, orchestration, decorators | `flows` | normal write/edit |
| **auditor** | Investigation, auditing, validation | `core-build`, `flows`, `tools-expert` | read-only |
| **docs** | Documentation authoring and maintenance | `core-build`, `flows` | write/edit only `*.md`; bash read-only |

## Routing Rules

- **Builder keywords:** create, build, scaffold, setup, agent, task, crew, tool, memory
- **Flow keywords:** flow, state, router, routing, orchestration, decorator, @start, @listen, @router
- **Auditor keywords:** inspect, audit, investigate, trace, root cause, validate, performance analysis
- **Docs keywords:** docs, readme, guide, documentation, architecture notes, standards

## Canonical Command Ownership

- `/crew init` -> builder
- `/crew inspect` -> auditor
- `/crew fix` -> auditor first, then builder/flow for implementation when needed
- `/crew evolve` -> flow
- `/crew docs` -> docs

## Delegation Pattern

Write plain-language delegation with:
1. Goal
2. Context and file paths
3. Specialist skill constraints
4. Deliverables
5. Validation criteria

## Auditor Rule

Auditor executes read-only analysis and returns:
- findings
- risk assessment
- recommendations
- validation steps

Auditor does not patch files.

## Validation Checklist

- Chosen specialist matches intent and ownership
- Delegation includes exact paths and constraints
- Specialist used only allowed skills
- Permission limits are respected
- Output contract is complete and actionable

## Supporting Files

- Subagent directory: `references/subagent-directory.md`
- Delegation patterns: `references/delegation-patterns.md`
- Question templates: `references/questioning-guide.md`
- Delegation template: `assets/delegation-template.md`
