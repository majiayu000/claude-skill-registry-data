---
name: timermeet-spec-driver
description: Maintain the Spec-Driven Development artifacts for the TimerMeet Python desktop app. Use when planning or refining features, turning a user request into requirements and acceptance criteria, updating scope after implementation, or keeping SDD/AGENTS/README aligned before commits.
---

# TimerMeet Spec Driver

## Overview

Keep TimerMeet grounded in a written spec before and after code changes. Use this skill to update scope, constraints, acceptance criteria, and validation notes in `SDD.md`, `AGENTS.md`, and `README.md`.

## Workflow

1. Read `SDD.md`, `AGENTS.md`, and `README.md` before proposing structural changes.
2. Translate the request into:
   - user goal
   - technical constraints
   - impacted files (usually under `timermeet_app/`)
   - acceptance criteria (prefer ones verifiable by `python -m unittest discover -s tests` or an observable behavior)
   - explicit non-goals when the scope must stay small
3. Update `SDD.md` before substantial implementation when the request changes product behavior, the `Meeting` data model, or architecture.
4. Keep the spec honest after implementation:
   - remove planned items that already shipped
   - add any new constraints discovered while coding
   - sync the verification checklist with what was actually tested
5. Keep docs concise. Prefer direct requirements and checklists over long narrative text.

## Project rules

- Preserve the `Meeting` field schema for backward compatibility with any `data/meetings.json` written by the legacy PHP app.
- Keep the default persistence model a single shared JSON file with merge-on-save (see `timermeet_app/storage.py`) -- this project folder lives inside OneDrive and may run on more than one PC.
- Keep Spanish as the default language (`i18n.DEFAULT_LANGUAGE`) and English fully supported; both dictionaries must stay key-for-key identical.
- Call out explicitly if a request would reintroduce a server/browser dependency -- that's the exact problem v2.0.0 was built to remove.
- Version numbers (`__version__`, README, SDD, git tag, GitHub release) must always move together; note the required bump type (patch/minor/major) in the spec update.

## Outputs

- Prefer small, auditable changes to `SDD.md`.
- Write acceptance criteria that can be verified with a command or a clearly observable behavior.
- If a request is vague, choose the smallest coherent scope and note deferred work explicitly in the backlog section.
