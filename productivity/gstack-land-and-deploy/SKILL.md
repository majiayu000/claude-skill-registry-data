---
name: gstack-land-and-deploy
description: GStack land-and-deploy method for explicit landing and deployment workflows with tests, release notes, rollout gates, and rollback planning.
---

# GStack Land And Deploy Adapter

This is a Codex role-system adapter for Garry Tan's gstack `gstack-land-and-deploy` method.

## When To Use

Use this when:

- the user explicitly asks to land and deploy;
- deployment workflow must be planned or reviewed;
- release readiness spans code and ops;
- the user explicitly invokes `$gstack-land-and-deploy`.

## Workflow

1. Keep the active role boundary. Do not expand scope just because this gstack method is useful.
2. Read the relevant repo/docs/evidence first when the task depends on current state.
3. Read `../gstack/references/methodology.md` if you need the shared method map, then use the section named `QA, Security, And Release Methods`.
4. Produce: land/deploy checklist, tests, release notes, rollout gates, rollback plan, and final status.
5. Return the result in the active role's normal format, including boundaries, validation, and unresolved decisions when applicable.

## Boundaries

- Treat upstream gstack as external methodology, not local-owned project state.
- Do not run upstream gstack runtime, telemetry, browser-cookie import, upgrade checks, or host routing injection automatically.
- Do not create or edit `CLAUDE.md`, `.claude/`, `.agents/`, or upstream routing files unless the user explicitly asks for upstream gstack installation work.
- Do not write files, commit, push, deploy, restart, migrate, clean, delete, or change production unless the active role prompt explicitly allows it.
- Preserve this repository's `QA` versus `测试` split: formal test cases/reports belong to `测试` and `$test-case-report-builder`.
- Do not deploy or mutate production unless the user explicitly authorizes that action in this turn.
