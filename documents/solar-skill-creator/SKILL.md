---
name: solar-skill-creator
description: >
  Solar-native guide for creating or updating skills in this repository. Use when a
  user needs a new reusable skill, a migration from external skills, or a cleanup of
  existing skills to match Solar governance (core vs planet scope, English in core,
  lean structure, and minimal dependencies).
---

# Solar Skill Creator

Create and maintain skills that fit Solar architecture without depending on external skill folders.

## Purpose

Define a consistent process to:
- create new skills in `core/skills/` or `planets/<planet-name>/skills/`,
- migrate external skills into Solar-owned skills,
- keep skills lean, testable, and easy to maintain.

## Scope Rules

- Put a skill in `core/skills/` only if reused by 2+ planets or 3+ times.
- Put planet-specific skills in `planets/<planet-name>/`.
- Keep `core` content in English.
- Planet skills may use the user preferred language.

## Required MCP

None

## Script Usage Documentation

If a skill includes executable files inside `scripts/`, the `SKILL.md` must explain how to use them.
This is a documentation rule, not a required section title.
The explanation can live in `Workflow`, `Troubleshooting`, or any other relevant section.

```bash
# Package/validate one modified skill (standard per-skill flow)
python3 core/skills/solar-skill-creator/scripts/package_skill.py <skill-path> /tmp

# Initialize a new skill scaffold
python3 core/skills/solar-skill-creator/scripts/init_skill.py <skill-name> --path <target-dir>

# Sync resource changes to local clients (when core/ resources changed)
solar client sync
```

## Governance validation

After changing `AGENTS.md` at root, core, or planet level, use the checklist in `references/governance-validation.md` (formerly command `solar-validate-governance`).

## Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name + description
│   └── Markdown instructions
└── Optional resources:
    ├── scripts/     - deterministic execution
    ├── references/  - large or variant details
    └── assets/      - output templates/files
```

Do not add auxiliary docs like README/INSTALL/CHANGELOG inside skill folders.

## Context Sustainability Gate

When creating or modifying any Solar skill, preserve capability while minimizing always-loaded context:

- Keep `SKILL.md` as a concise operational index: purpose, trigger, required MCP, critical workflow, validation, and links to references.
- Move long examples, edge cases, background, provider variants, and troubleshooting detail to `references/` inside the same skill.
- Keep deterministic behavior in `scripts/`; document only the commands the agent must choose from.
- Keep reusable templates or static resources in `assets/`.
- Avoid duplicating governance from root, `core/AGENTS.md`, or planet `AGENTS.md`; link to the canonical source instead.
- Before finishing, review whether the changed `SKILL.md` grew because of detail that belongs in `references/`.

This is not a mechanical line-count reduction. The goal is lower context load with equal or better operational capability.

## Workflow

1. Capture 2-3 concrete usage examples.
2. Decide destination: `core` or `planet`.
3. Create or update folder and `SKILL.md`.
4. Add only required resources (`scripts`, `references`, `assets`).
5. Validate:
   - clear trigger description,
   - no duplicated content,
   - lean size (prefer references for long details),
   - no extraneous files.
6. If migrating from external source, rewrite into Solar-owned language and structure.

## Required Checks

- Frontmatter includes only `name` and `description`.
- Description states what it does and when to use it.
- Body stays procedural and concise.
- Core skills remain vendor-neutral and Solar-owned.
- `SKILL.md` acts as an index; long detail is moved to `references/` inside the skill.
- Critical commands remain visible enough that an agent can choose the right workflow without loading every reference.
- Skill body includes these required sections:
  - `Required MCP`
- `Fallback if MCP missing` is required only when `Required MCP` is not `None`.
- If `scripts/` has files, `SKILL.md` must document how those scripts are used (no fixed section title required).
- If a skill exposes long-running local runtime endpoints (webhook, bridge, local server, tunnel), include `Laptop runtime note (optional)` in that skill `SKILL.md`:
  - host sleep can stop runtime availability,
  - this is a host operations concern (not a mandatory skill dependency),
  - if multiple laptops are used, only one active host should serve the same public route.
- Do not add `Laptop runtime note` to skills that are not runtime-host dependent.
- If skill scripts manage `.env`, they must write a skill-scoped compact block:
  - header comment identifying the skill,
  - contiguous variables with no blank lines inside the block,
  - preserve existing values unless explicit overwrite is requested.
- If a skill is intended to run via `solar-system` orchestration, include a short `System activation` subsection in that skill `SKILL.md` with:
  - required `SOLAR_SYSTEM_FEATURES` token(s),
  - install/status commands for `solar-system`,
  - a pointer to keep operational ownership in `core/skills/solar-system/`.
- If a skill is modified, validate that specific skill with:
  - `python3 core/skills/solar-skill-creator/scripts/package_skill.py <skill-path> /tmp`
  - do not use `--no-validate` in normal flow.

## Migration Rule

If source exists outside Solar:
- reuse concepts, not blind copy,
- remove platform-specific installation noise,
- avoid external runtime dependencies unless explicitly needed,
- keep attribution/license notes when required.

## Bundled References in This Skill

- `references/workflows.md`
- `references/output-patterns.md`

## Provenance

Based on cross-agent skill-creator concepts, adapted for Solar architecture.
