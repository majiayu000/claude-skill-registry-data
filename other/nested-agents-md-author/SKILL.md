---
name: nested-agents-md-author
description: Generate scoped nested AGENTS.md files at meaningful repo boundaries. Use after scaffold or harness setup when apps, packages, docs, or service directories need local agent instructions without duplicating the root AGENTS.md.
---

# Nested AGENTS.md Author

## Purpose

Add local agent instructions only where directory-specific rules materially improve agent behavior.

## Inspect First

- root `AGENTS.md`, docs index, architecture boundaries, workspace layout, apps, packages, services, docs, scripts, and existing nested `AGENTS.md` files
- package manifests, local commands, generated-code areas, ownership rules, and testing conventions

## Procedure

1. Identify meaningful boundaries.
   - Use `scripts/suggest_nested_agents.py` when available.
   - Prefer boundaries such as `apps/web`, `apps/server`, `packages/api`, `packages/db`, `packages/ui`, `services/*`, and `docs`.
   - Treat suggestions as scored candidates, not mandatory output. Support packages such as config, env, auth, shared, types, or utils need nested files only when they have local commands, hazards, docs, or existing scoped policy.
   - Do not create `AGENTS.md` in every folder.

2. Write scoped files.
   - Use `assets/templates/nested-AGENTS.md.tmpl`.
   - Link to parent/root `AGENTS.md`.
   - Include only local purpose, read-first docs, local rules, local commands, generated-file warnings, and validation notes.
   - Keep detailed architecture/testing/product content in `docs/`.
   - Link local feature, progress, startup, termination, or handoff docs only when that directory owns those artifacts.

3. Preserve existing policy.
   - If a nested file already exists, inspect and update rather than overwrite.
   - Do not contradict root instructions.
   - Move broadly applicable rules back to the root `AGENTS.md` or docs.

4. Add validation.
   - Create or update target repo `scripts/check-nested-agents`.
   - Use `scripts/check_nested_agents.py` to detect missing root links, excessive files, and missing local purpose sections.
   - Use or recommend `check_instruction_snr.py` when nested files duplicate root rules.
   - Use `project-local-skill-generator` for repo-local workflows that are better expressed as triggerable `.codex/skills` than nested directory instructions.

## Validation

- Run `./scripts/check-nested-agents` when present.
- Confirm each nested file links upward and has directory-specific value.
- Confirm nested files do not duplicate root command lists or long docs.

## Completion Criteria

- Scoped agent instructions exist only at useful boundaries.
- Root `AGENTS.md` remains the repo map.
- Nested files are concise, linked, and validation-clean.
