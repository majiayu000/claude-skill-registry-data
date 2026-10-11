---
name: project-documentation
description: Create, review, and update accurate project documentation from the actual repository. Use when Codex needs to write or maintain README files, setup guides, developer onboarding docs, client handover notes, architecture docs, API docs, database notes, environment variable references, testing instructions, deployment guides, troubleshooting docs, known limitations, user/admin guides, or maintenance documentation for a software project without inventing commands, secrets, architecture, APIs, roles, or deployment behavior.
---

# Project Documentation

Use this skill when documentation must explain how a project works, how to run it, how to test it, how to deploy it, and what future developers, clients, or maintainers need to know.

## Core Rule

Document verified facts from the repository and supporting materials. Inspect existing docs and code before writing, update the closest existing document when possible, and clearly mark unknowns instead of inventing details.

## Workflow

1. Identify documentation purpose:
   - developer onboarding, client handover, internal maintenance, deployment, API usage, architecture, user guide, admin guide, troubleshooting, proposal support, or future development
2. Identify target reader:
   - developer, client, project manager, QA, DevOps, support, business owner, or non-technical stakeholder
3. Inspect existing documentation:
   - `README.md`, `docs/`, `CONTRIBUTING.md`, `CHANGELOG.md`, deployment docs, architecture docs, API docs, `.env.example`, setup notes, and existing handover documents
4. Inspect project structure:
   - frontend, backend, mobile, API, database, migrations, tests, Docker, CI/CD, scripts, shared packages, assets, and configuration files
5. Verify project overview:
   - project name, purpose, main users, major features, current status, and important limitations
6. Verify technology stack:
   - frontend, backend, mobile, database, ORM, auth, styling, state management, test tools, deployment tools, reverse proxy, CI/CD, and external services
7. Verify setup instructions:
   - prerequisites, install commands, env file setup, database setup, migrations, seed data, run commands, Docker commands, and local URLs
8. Document environment variables safely:
   - name, required/optional status, purpose, safe placeholder, where used, and notes; never include real secrets
9. Document architecture:
   - application layers, frontend responsibilities, backend responsibilities, database responsibilities, external services, auth flow, deployment architecture, and data flow
10. Document folder structure:
   - important folders and files only, with accurate purpose and ownership
11. Document APIs when present:
   - method, path, purpose, auth, role, request body/query, success response, error behavior, pagination/filtering, and file upload behavior when relevant
12. Document database notes when present:
   - main tables/entities, relationships, constraints, status fields, migrations, seed data, soft deletes, audit logs, indexes, and ownership rules
13. Document authentication and authorization:
   - login flow, session/token behavior, roles, permissions, protected routes, backend enforcement, and logout behavior
14. Document main user flows:
   - actor, steps, screens, backend actions, final result, and important failure cases
15. Document testing:
   - lint, unit, API, integration, E2E, build commands, test database requirements, and known test gaps
16. Document deployment:
   - target environment, required variables, build commands, Docker/VPS/platform steps, migrations, reverse proxy, health checks, logs, restart, rollback, and backups where known
17. Document troubleshooting:
   - common setup, database, env, CORS, Docker, migration, build, login, API, static asset, and health check failures
18. Document known limitations:
   - missing integrations, unimplemented features, manual processes, incomplete tests, operational gaps, and future work
19. Keep docs aligned with code changes:
   - update docs when setup, env vars, API contracts, database schema, auth, user roles, tests, deployment, integrations, or limitations change
20. Summarize docs changed, audience, sections covered, missing information, and follow-up.

Read `references/project-docs-checklist.md` for documentation types, repository inspection targets, section guidance, safety rules, and the final report format.

## Non-Negotiable Rules

- Do not invent commands, APIs, architecture, database tables, roles, or deployment steps.
- Do not include real secret values.
- Do not duplicate stale documentation when an existing document should be updated.
- Do not hide known limitations or missing information.
- Do not write developer-only detail for a client guide or marketing-only text for a developer handover.
- Do not document outdated behavior after code changes.
- Do not claim a command exists unless it was found in scripts, docs, config, or project conventions.
- Keep documentation practical, accurate, reader-specific, and maintainable.

## Output Contract

When using this skill, provide:

1. Documentation purpose and target reader.
2. Existing docs and repository areas inspected.
3. Documents created or updated.
4. Sections covered and why.
5. Files changed.
6. Verified commands, env vars, architecture, APIs, database, auth, testing, and deployment details included.
7. Missing information or unknowns.
8. Known limitations documented.
9. Recommended follow-up.
