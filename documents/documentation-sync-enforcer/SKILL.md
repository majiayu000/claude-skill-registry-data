---
name: documentation-sync-enforcer
description: Detect and prevent docs drift in agent-ready repos. Use when commands, environment variables, routes, migrations, schemas, public APIs, package scripts, architecture, or release behavior changes and docs may need updates.
---

# Documentation Sync Enforcer

## Purpose

Keep repo-local memory synchronized with code so agents do not follow stale instructions.

## Inspect First

- git diff or changed files when available
- manifests, package scripts, env examples, routes, schemas, migrations, docs index, command docs, architecture docs, testing docs, and release docs

## Procedure

1. Detect drift triggers.
   - Commands or package scripts changed.
   - Environment variables changed.
   - Routes, APIs, generated clients, schemas, migrations, or public contracts changed.
   - Architecture, runtime, CI, security, dependency, or release behavior changed.

2. Compare docs.
   - Use `scripts/check_docs_drift.py` when available.
   - Report both changed files and recommended docs to inspect.
   - Update `docs/00-index.md` ownership and update triggers when new docs are added.

3. Add enforcement.
   - Create or update target repo `scripts/check-docs`.
   - Include it in `scripts/validate`.

4. Report exceptions.
   - If no docs update is required, state why.
   - If a docs update is deferred, add it to the technical debt register.

## Validation

- Run `./scripts/check-docs` in the target repo when present.
- Confirm docs reference real commands and files.
- Confirm `.env.example` and environment docs agree.

## Completion Criteria

- Docs changed with code when needed.
- Stale or missing docs are detected by a repeatable check.
