---
name: gstack-plan-ceo-review
description: GStack CEO/founder-mode plan review for strategy, customer value, scope, sequencing, business risk, and whether the work should be done now.
---

# GStack CEO Plan Review Adapter

This is a Codex role-system adapter for Garry Tan's gstack `gstack-plan-ceo-review` method.

## When To Use

Use this when:

- strategic scope or sequencing is uncertain;
- customer value or business logic needs pressure testing;
- architecture needs a do-now versus defer recommendation;
- the user explicitly invokes `$gstack-plan-ceo-review`.

## Workflow

1. Keep the active role boundary. Do not expand scope just because this gstack method is useful.
2. Read the relevant repo/docs/evidence first when the task depends on current state.
3. Read `../gstack/references/methodology.md` if you need the shared method map, then use the section named `Architecture And Product Methods`.
4. Produce: strategic risk list, recommendation, alternatives, and user decision points.
5. Return the result in the active role's normal format, including boundaries, validation, and unresolved decisions when applicable.

## Boundaries

- Treat upstream gstack as external methodology, not local-owned project state.
- Do not run upstream gstack runtime, telemetry, browser-cookie import, upgrade checks, or host routing injection automatically.
- Do not create or edit `CLAUDE.md`, `.claude/`, `.agents/`, or upstream routing files unless the user explicitly asks for upstream gstack installation work.
- Do not write files, commit, push, deploy, restart, migrate, clean, delete, or change production unless the active role prompt explicitly allows it.
- Preserve this repository's `QA` versus `测试` split: formal test cases/reports belong to `测试` and `$test-case-report-builder`.
