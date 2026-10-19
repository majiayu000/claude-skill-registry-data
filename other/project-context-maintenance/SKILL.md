---
name: project-context-maintenance
description: Maintain fixed project rules, AI context adapters, and repository-owned skills without provider-specific drift.
---

# Project Context Maintenance

## Use when

Project policy, agent instructions, reusable procedures, or provider adapters need to be added or changed.

## Procedure

1. Read `project-rules/INDEX.md`, `docs/AI_WORKING_GUIDE.md`, `AGENTS.md`, and `skills/INDEX.md`.
2. Decide whether the change is a fixed rule or a reusable task procedure. Fixed boundaries belong in `project-rules/`; optional procedures belong in `skills/`.
3. Keep one canonical rule text. Provider files should link to canonical files instead of maintaining policy forks.
4. Any agent may add a skill without prior approval. Use `skills/<lowercase-kebab-name>/SKILL.md`, valid `name`/`description` frontmatter, bounded steps, constraints, and observable completion criteria.
5. Update the relevant index, ensure provider adapters point to canonical rules and skills, then run `python tools/validate_project_context.py`.

## Constraints

- Skills supplement but never override `project-rules/`.
- Do not write secrets, machine-specific paths, unverified ownership claims, or unsupported hardware promises into context files.
- Do not assume a provider auto-loads a file unless documented; keep provider adapters explicit.

## Done when

The canonical rule/skill exists in the repository, indexes and adapters resolve, and the project-context validator passes.