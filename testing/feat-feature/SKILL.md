---
name: feat-feature
description: >
  Use when the user wants a full feature action plan (backend + frontend + tests) with the
  PWDEVIA 7-question method before any code is written — 'planejar a feature X', 'criar plano
  de feature', 'plan the user CRUD'. Interviews the human (max 2 rounds) and writes
  .planning/feat/features/{slug}/plan.md. Do NOT use to write code (feat-exec), for small
  1–3 file changes (feat-quick), backend-only or UI-only scope (feat-backend / feat-frontend),
  tests for existing code (feat-test) or code review (feat-review).
metadata:
  version: 3.2.1
---

# Feature plan

Plan type **feature** — full scope: backend, frontend, tests and documentation as applicable,
split into clearly ordered Execution Steps. You run in the MAIN session: you interview the
human, so never delegate this skill to a subagent.

## Procedure

1. **Language** — resolve `lang` (`references/language.md`).
2. **Method** — follow `references/pwdevia-method.md` end to end: read context (project
   instructions file, `.planning/feat/codebase.md`, all four `.planning/feat/context/*.md`,
   map staleness, memory), interview (max 2 rounds), answer the 7 questions, render
   `templates/plan.md` with `plan_type: feature`, lint it, present the summary.
3. **Focus for this type**
   - Persona: full-stack engineer on the project's real stack (from the context documents).
   - Order the steps: data/migrations → domain/services → API → UI → tests → docs.
   - Every business rule becomes at least one `AC-*`; every AC has a verification.
   - With UI (`**UI:** yes`): include the E2E scenario files
     (`<tests-dir>/e2e/scenarios/E2E-nnn-*.scenario.json`) and their exported specs
     (`<tests-dir>/e2e/generated/E2E-nnn-*.spec.ts`) in §4 and `playwright-cli` checks
     in §5 — `references/testing.md`.
   - Consider validation, error handling, authorization and migrations explicitly.

## Prohibitions

- Never write code — only the plan.
- Never skip any of the 7 questions or leave an AC without verification.
- Never create a plan with more than 10 steps — split into several plans.

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
