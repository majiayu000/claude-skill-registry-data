---
name: triatu-supabase
description: "Supabase data access and security rules for Triatu. Use when editing DB-related code, policies, or adding new tables/queries."
---

# Triatu Supabase

## Quick start

- Validate inputs with Zod before any DB call.
- Domain must not talk to Supabase directly.
- Keep PII out of logs; use `lib/logger` and `debug` only in dev.

## Workflow

1) Define interfaces in Domain or Application.
2) Implement Supabase access in adapters (Infrastructure).
3) Call adapters from Application use cases.
4) Update policies and schemas in Supabase; note changes in docs.
5) Add/adjust tests before code (TDD).

## Guardrails

- No direct infrastructure calls from Domain.
- Avoid global state unless justified.
- Record new risks in `docs/PROJECT_AUDIT.md`.

## References

- `docs/SECURITY.md`
- `docs/PROJECT_AUDIT.md`
- `docs/CORE.md`
- `guia.md`
