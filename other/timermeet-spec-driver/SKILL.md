---
name: timermeet-spec-driver
description: Maintain the Spec-Driven Development artifacts for the TimerMeet EasyPHP project. Use when planning or refining features, turning a user request into requirements and acceptance criteria, updating scope after implementation, or keeping SDD/agents/docs aligned before commits.
---

# TimerMeet Spec Driver

## Overview

Keep `TimerMeet` grounded in a written spec before and after code changes. Use this skill to update scope, constraints, acceptance criteria, and validation notes in the project docs.

## Workflow

1. Run `git rev-parse --show-toplevel` and locate the project folder `monitoreos/timermeet`.
2. Read `SDD.md`, `AGENTS.md`, and `README.md` in that project folder before proposing structural changes.
3. Translate the request into:
- user goal
- technical constraints
- impacted files
- acceptance criteria
- explicit non-goals when the scope must stay small
4. Update `SDD.md` before substantial implementation when the request changes product behavior or architecture.
5. Keep the spec honest after implementation:
- remove planned items that already shipped
- add any new constraints discovered while coding
- sync the verification checklist with what was actually tested
6. Keep docs concise. Prefer direct requirements and checklists over long narrative text.

## Project Rules

- Treat `PHP 5.4.31` compatibility as a hard constraint.
- Keep the default persistence model file-based unless the user explicitly asks for a database.
- Call out that browser alarms still depend on an open tab.
- Call out that the Git repo root is wider than the `timermeet` folder when GitHub publication is discussed.

## Outputs

- Prefer small, auditable changes to `SDD.md`.
- Write acceptance criteria that can be verified with commands or visible behavior.
- If a request is vague, choose the smallest coherent scope and note deferred work explicitly.
