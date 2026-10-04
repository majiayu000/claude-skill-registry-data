---
name: use-ship
version: 0.2.0
description: >
  Route ambiguous software-delivery requests to the smallest useful Ship workflow:
  one skill, a phase bundle, or /ship:auto. Use at session start, when the user
  asks how to use Ship, or when they say build/check/ship without a phase.
allowed-tools:
  - Read
  - Bash
  - Agent
---

# Ship: Use Ship

Choose the smallest useful Ship workflow for the request, state the route
briefly, then invoke the matching skill(s). Each skill's own description is
the primary routing signal — this file only settles the ambiguous cases.
Do not force the full pipeline unless the user explicitly wants
production delivery.

## Routes

| Need | Route |
|------|-------|
| Understand scope, write a plan, de-risk approach | `/ship:design` |
| Architecture/API/data-model decision, ADR, trade-off analysis | `/ship:arch-design` (thinking) → `/ship:write-docs` (record), then `/ship:design` if implementation follows |
| Implement a well-scoped change | `/ship:design` → `/ship:dev` |
| Implement from an existing approved plan | `/ship:dev` |
| Add durable browser/API/CLI coverage | `/ship:e2e` |
| Check code correctness | `/ship:review` |
| Verify runtime behavior | `/ship:qa` |
| Harden a completed change | `/ship:e2e` → `/ship:review` → `/ship:qa` → `/ship:refactor` |
| Prepare delivery after work is complete | `/ship:handoff` |
| End-to-end production delivery (explicit ask only) | `/ship:auto` |

Ambiguous phrasings default to a bounded bundle, never the full pipeline:
"plan this" → design; "build this" → design → dev; "check this change" →
review and/or qa; "make this production-ready" → the hardening bundle;
"ship this all the way" → auto.

## Boundaries

- **Standalone:** atomic skills work without `/ship:auto` or any task
  directory. If the user names a phase, run that phase directly.
- **State:** during full flows, raw input lives at
  `.ship/tasks/<task_id>/input/requirement.md`; orchestrator state is
  minimal and orchestrator-owned. Markdown artifacts and repository code
  are the real deliverables.
- **Durable production artifacts:** use the repository's existing
  convention first; otherwise create only the needed subfolders under
  `docs/ship/<task-id>/` (`input/`, `product/`, `design/`, `engineering/`,
  `quality/`, `delivery/`, `archive/`). Prefer Markdown; use YAML/JSON
  only when a later agent or script consumes the structure.
