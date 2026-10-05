---
name: agents-md-author
description: Generate or maintain a minimal high-signal AGENTS.md for coding agents. Use whenever a repo needs agent instructions, an existing AGENTS.md is too long or vague, or project docs/scripts need a concise routing map for Codex.
---

# AGENTS.md Author

## Purpose

Create a short `AGENTS.md` that routes agents to authoritative docs and commands without becoming a giant project knowledge dump.

Use `nested-agents-md-author` after the root file is healthy when apps, packages, or docs need scoped local instructions.

## Inspect First

- existing `AGENTS.md` or other agent instruction files
- `docs/00-index.md`, README, architecture docs, testing docs, and command docs
- manifests and scripts to confirm standard commands

## Procedure

1. Keep `AGENTS.md` short.
   - Target under 120 lines.
   - Put detailed knowledge in `docs/`.
   - Link to docs instead of repeating them.

2. Include only stable operating contract.
   - Read-first docs.
   - Standard commands.
   - Non-negotiable repo rules.
   - Architecture and quality gate pointers.
   - Validation expectations.

3. Preserve local policy.
   - If existing instructions contain project-specific constraints, keep them or move them to the right doc and link back.
   - Remove stale, duplicated, or framework-generic prose.

4. Update related docs.
   - If `AGENTS.md` references a missing doc, create or update that doc through `repo-knowledge-base-builder`.
   - If commands changed, update `docs/development/commands.md`.
   - If directory-specific rules are needed, keep root `AGENTS.md` as the map and create scoped files through `nested-agents-md-author`.
   - If control-loop artifacts exist, link to feature state, progress, decisions, startup readiness, definition of done, and session handoff docs.
   - If instructions are long or duplicated, run or recommend `check_instruction_snr.py`.
   - Use `project-local-skill-generator` when project-specific workflows belong in `.codex/skills` instead of root `AGENTS.md`.

## Required Shape

Use this structure unless the repo already has a stronger convention:

```markdown
# Agent Instructions

This file is a map. The authoritative project knowledge is in `docs/`.

## Read first

- `docs/00-index.md`
- `docs/architecture/overview.md`
- `docs/architecture/boundaries.md`
- `docs/development/commands.md`
- `docs/testing/strategy.md`
- `docs/quality/code-style.md`

## Standard commands

- Dev: `./scripts/dev`
- Lint: `./scripts/lint`
- Typecheck: `./scripts/typecheck`
- Test: `./scripts/test`
- Build: `./scripts/build`
- Full validation: `./scripts/validate`

## Rules

- Inspect existing code and docs before changing behavior.
- Prefer established patterns over new abstractions.
- Add or update tests for behavior changes.
- Update docs when commands, environment variables, routes, schemas, or architecture change.
- Run the narrowest relevant check first, then `./scripts/validate`.
- If validation cannot run, state the exact command, error, and likely cause.

## Architecture boundaries

See `docs/architecture/boundaries.md`.
```

## Validation

- Check every linked doc exists.
- Check every listed command exists or is documented as intentionally absent.
- Check the file is concise and not duplicating architecture, product, or testing docs.
- Check root instructions route to state and handoff files when the repo uses them.

## Completion Criteria

- `AGENTS.md` is a routing file, not a manual.
- It contains no stale commands or missing links.
- It preserves project-specific constraints in the right location.
