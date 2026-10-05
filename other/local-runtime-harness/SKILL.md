---
name: local-runtime-harness
description: Make a project reproducible and inspectable locally for coding agents. Use when a repo needs dev server scripts, .env.example, Docker Compose, seed/reset commands, health checks, local logs, or runtime debugging instructions.
---

# Local Runtime Harness

## Purpose

Give agents runtime reality: a way to boot the app, reproduce bugs, inspect behavior, reset state, and verify fixes locally.

## Inspect First

- existing dev scripts and package manager
- env vars, secret usage, `.env*` files, and `.gitignore`
- database, queues, caches, external services, Docker files
- app URLs, ports, API health routes, log output
- seed data and migrations

## Procedure

1. Define local prerequisites.
   - Package manager and runtime versions.
   - Required services.
   - Required environment variables.

2. Create stable runtime scripts.
   - `scripts/dev`
   - `scripts/healthcheck`
   - `scripts/db-reset` when a database exists.
   - `scripts/seed` when seed data exists or is needed.
   - `scripts/logs` when logs are inspectable locally.
   - For databases or queues, add a readiness wait before any push, migrate, reset, or seed operation.

3. Create environment docs.
   - `.env.example` with non-secret example values.
   - `docs/development/environment.md`.
   - `docs/development/local-setup.md`.

4. Add local services when justified.
   - Use Docker Compose for local databases or queues if project-native setup does not already exist.
   - Keep external hosted services optional in local dev when possible.
   - Use a stack-native readiness check such as `pg_isready` when available; otherwise use `assets/templates/wait-for-port.sh.tmpl` as the target repo pattern.

5. Add diagnostics.
   - Healthcheck command should verify the main app or API is reachable.
   - Logs command should expose local logs without requiring external observability platforms.
   - Use `project-local-skill-generator` to create `project-runtime-debugging` when runtime docs and commands are stable enough for a repo-local skill.

## Runtime Rules

- Never commit real secrets.
- Preserve existing `.env.example` values and add missing keys.
- Prefer deterministic reset and seed commands over manual setup notes.
- Document ports and URLs explicitly.
- Database reset order is: start service, wait until ready, apply schema or migrations, seed when configured, run healthcheck.

## Validation

- Run `./scripts/dev` if feasible and stop it cleanly.
- Run `./scripts/healthcheck`.
- Run reset/seed commands for databases when safe.
- Confirm `.env.example` and environment docs match.

## Completion Criteria

- A new agent can boot the repo locally or has a precise blocker.
- Local state can be reset safely.
- Runtime inspection is documented with commands, ports, and expected output.
