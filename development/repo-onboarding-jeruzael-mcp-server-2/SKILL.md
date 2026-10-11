---
name: repo-onboarding
description: Inspect and understand an unfamiliar or existing software repository before making code changes. Use when Codex is opening a new repo, returning after a long break, preparing feature work, bug fixes, refactors, handover, project review, client takeover, or technical assessment and needs to identify stack, structure, entry points, commands, environment config, database, auth, tests, deployment, conventions, risks, and next steps without editing files.
---

# Repo Onboarding

Use this skill to understand a repository before implementation work. The goal is to prevent blind edits, duplicated patterns, missed conventions, and unsafe assumptions.

## Rules

- Do not edit files during onboarding unless explicitly asked.
- Do not assume the stack; inspect project files first.
- Do not expose secrets or sensitive values.
- Do not install packages, run migrations, or use destructive commands.
- Prefer read-only commands such as `rg --files`, `Get-ChildItem`, `Get-Content`, `git status`, and package/script inspection.
- Report uncertainty honestly.

## Workflow

1. Inspect repository structure:
   - top-level folders and files
   - docs, app roots, source roots, config roots, tests, deployment files
2. Identify technology stack:
   - frontend, backend, language, database, ORM, styling, state, tests, package manager, deployment
3. Locate main application areas:
   - frontend routes/screens/components/API clients
   - backend entry/routes/services/models/middleware/validation/errors
   - shared contracts, database schema, deployment structure
4. Identify available commands:
   - install, run dev, test, lint, format, build, migrations, Docker, deploy
5. Inspect environment configuration:
   - `.env.example`, sample configs, Docker env, deployment docs
   - warn if real secrets appear, but do not reveal values
6. Identify database and data flow:
   - schema, migrations, seed files, entities, relationships, data access path
7. Identify auth and authorization:
   - login/session/JWT/OAuth, protected routes, middleware, role checks
8. Identify tests and quality gates:
   - unit, integration, e2e, API tests, configs, scripts, coverage gaps
9. Identify deployment setup:
   - Docker, CI, Caddy/Nginx, Vercel/Netlify/Railway/Render/VPS scripts, build commands
10. Produce the onboarding summary.

Read `references/onboarding-report.md` for the expected output format and checklist.

## Common Files To Check

- `README.md`, `docs/**`
- `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `requirements.txt`, `pyproject.toml`, `composer.json`, `go.mod`, `Cargo.toml`
- `Dockerfile`, `docker-compose.yml`, `.github/workflows/**`
- `.env.example`, `.env.sample`
- `src`, `app`, `pages`, `components`, `server`, `api`, `services`
- `database`, `migrations`, `prisma`, `models`, `routes`, `controllers`, `tests`

## Output Contract

When using this skill, provide:

1. Project overview.
2. Technology stack.
3. Repository structure.
4. Main entry points.
5. Frontend/backend/database/auth/testing/deployment summaries where applicable.
6. Available commands.
7. Project conventions.
8. Risks, missing information, and recommended next steps.
