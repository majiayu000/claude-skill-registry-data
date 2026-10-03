---
name: gstack-guard
description: GStack guard method for strengthening scope boundaries, forbidden actions, stop conditions, and validation gates for an agent or workstream.
---

# GStack Guard Adapter

This is a Codex role-system adapter for Garry Tan's gstack `gstack-guard` method.

## When To Use

Use this when:

- a role prompt needs stronger boundaries;
- the agent risks touching forbidden files or actions;
- architecture wants guardrails before delegation;
- the user explicitly invokes `$gstack-guard`.

## Workflow

1. Keep the active role boundary. Do not expand scope just because this gstack method is useful.
2. Read the relevant repo/docs/evidence first when the task depends on current state.
3. Read `../gstack/references/methodology.md` if you need the shared method map, then use the section named `Engineering Execution Methods`.
4. Produce: guardrails, forbidden scope, stop conditions, validation gates, and revised prompt wording.
5. Return the result in the active role's normal format, including boundaries, validation, and unresolved decisions when applicable.

## Boundaries

- Treat upstream gstack as external methodology, not local-owned project state.
- Do not run upstream gstack runtime, telemetry, browser-cookie import, upgrade checks, or host routing injection automatically.
- Do not create or edit `CLAUDE.md`, `.claude/`, `.agents/`, or upstream routing files unless the user explicitly asks for upstream gstack installation work.
- Do not write files, commit, push, deploy, restart, migrate, clean, delete, or change production unless the active role prompt explicitly allows it.
- Preserve this repository's `QA` versus `测试` split: formal test cases/reports belong to `测试` and `$test-case-report-builder`.
