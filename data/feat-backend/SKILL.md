---
name: feat-backend
description: >
  Use when the user wants a backend-only action plan — API endpoints, services, models,
  migrations, jobs and their tests — 'plano de backend para o endpoint X', 'plan the orders
  API'. Writes .planning/feat/features/{slug}/plan.md with the PWDEVIA method. Do NOT use for
  UI work (feat-frontend), full features spanning backend and UI (feat-feature), writing code
  (feat-exec) or quick 1–3 file fixes (feat-quick).
metadata:
  version: 3.2.1
---

# Backend plan

Plan type **backend**. You run in the MAIN session and interview the human.

## Procedure

1. **Language** — resolve `lang` (`references/language.md`).
2. **Method** — follow `references/pwdevia-method.md` with `plan_type: backend`; context
   documents: architecture, conventions, testing.
3. **Focus for this type**
   - Persona: backend engineer on the project's real stack (Laravel, Node, Django, Go...).
   - §3 lists entities with fields and types, endpoints with methods, request/response shapes
     and status codes.
   - §5 covers API contracts, validation, authorization, error responses, and UNIT/INT tests
     (`references/testing.md`); integration tests may only be `NOT_APPLICABLE` with a reason.
   - Migrations are explicit steps with rollback considered.

## Prohibitions

- Never write code — only the plan.
- Never skip database migration steps when the schema changes.
- Never plan without validation and error handling.
- Never allow N+1 queries or raw SQL without parameter binding.

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
