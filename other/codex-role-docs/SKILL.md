---
name: codex-role-docs
description: Use for role-scoped FE/BE/DevOps/Admin/QA project docs under .codex/project-docs to preserve micro-context across long projects.
load_priority: on-demand
---

## TL;DR
Use this skill when a project needs durable FE/BE/DevOps/Admin/QA context. Initialize only the project brief by default; create role folders for the roles this project actually needs, then keep those docs current as code changes.

# Codex Role Docs

## Activation

1. Activate on `$role-docs`, `$init-docs`, or `$check-docs`.
2. Activate when the user asks for project docs, role docs, technical documentation, architecture notes, API docs, UI/UX docs, runbooks, or durable context.
3. Activate during long-running projects where micro-context can be lost across sessions.
4. Auto-use with agent personas when a role-owned file changes.

## Core Rule

Role docs are project-local artifacts, not always-loaded context. Read only the role docs needed for the current task, then update the same docs before completion when code behavior, contracts, architecture, UI patterns, deployment, admin flows, or tests changed.

## Commands

- Initialize minimal docs: `init_role_docs.py --project-root <path>` (project brief + ADR template only)
- Initialize selected roles: `init_role_docs.py --project-root <path> --roles frontend,qa`
- Initialize every role only when needed: `init_role_docs.py --project-root <path> --roles all`
- Update one doc: `update_role_docs.py --project-root <path> --role <role> --doc <doc-id> --summary <text> --files <csv>`
- Check impact: `check_role_docs.py --project-root <path> --changed-files <csv>`
- Rebuild index: `build_role_docs_index.py --project-root <path>`
- See `skills/.system/REGISTRY.md` for full script paths.

## Role Ownership

| Role | Owns |
| --- | --- |
| `frontend-specialist` | `frontend/FE-*`, admin UI flows, dashboards, reports |
| `backend-specialist` | `backend/BE-*`, admin permissions, contracts, data management |
| `devops-engineer` | `devops/DO-*` |
| `test-engineer` | `qa/QA-*` |
| `security-auditor` | auth/security, permissions, audit-log docs |
| `planner` | project brief, ADR template, admin scope |

## Update Discipline

1. Before editing, check whether relevant docs exist under `.codex/project-docs/`.
2. If missing and the task is project setup or planning, run `$init-docs`.
3. After code changes, run `$check-docs` or map changed files manually.
4. Update only the docs owned by the active agent's role.
5. Keep entries factual: decision, source files, constraints, risks, verification.
6. Do not block completion only because docs are missing unless the user explicitly made docs mandatory.

## Generated Structure

- Always: `PROJECT-BRIEF.md` and `decisions/ADR-0001-template.md`.
- On request: `frontend/FE-*.md`, `backend/BE-*.md`, `devops/DO-*.md`, `admin/AD-*.md`, and/or `qa/QA-*.md` for the selected roles.
- `index.json` is created only when the index builder runs.

## Resources

- `templates/role_docs_manifest.json`: canonical role docs, owners, and doc metadata.
- `templates/project-brief-template.md`: project-level context template.
- `templates/role-doc-template.md`: shared role-document template.
- `templates/adr-template.md`: decision record template.
