---
name: gstack-plan-devex-review
description: GStack developer-experience plan review for setup, local commands, docs, test loops, onboarding friction, and maintainability before implementation.
---

# GStack DevEx Plan Review Adapter

This is a Codex role-system adapter for Garry Tan's gstack `gstack-plan-devex-review` method.

## When To Use

Use this when:

- a task changes setup, commands, docs, or contributor workflow;
- implementation may be hard to verify locally;
- architecture wants DX acceptance criteria;
- the user explicitly invokes `$gstack-plan-devex-review`.

## Workflow

1. Keep the active role boundary. Do not expand scope just because this gstack method is useful.
2. Read the relevant repo/docs/evidence first when the task depends on current state.
3. Read `../gstack/references/methodology.md` if you need the shared method map, then use the section named `Architecture And Product Methods`.
4. Produce: DX risks, command/doc requirements, and validation feedback-loop recommendations.
5. Return the result in the active role's normal format, including boundaries, validation, and unresolved decisions when applicable.

## Boundaries

- Treat upstream gstack as external methodology, not local-owned project state.
- Do not run upstream gstack runtime, telemetry, browser-cookie import, upgrade checks, or host routing injection automatically.
- Do not create or edit `CLAUDE.md`, `.claude/`, `.agents/`, or upstream routing files unless the user explicitly asks for upstream gstack installation work.
- Do not write files, commit, push, deploy, restart, migrate, clean, delete, or change production unless the active role prompt explicitly allows it.
- Preserve this repository's `QA` versus `测试` split: formal test cases/reports belong to `测试` and `$test-case-report-builder`.
