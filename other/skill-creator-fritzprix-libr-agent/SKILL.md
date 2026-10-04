---
name: skill-creator
description: Guide for creating and validating agent skills. Use when authoring or updating a SKILL.md, writing frontmatter, structuring scripts/references/assets, or checking a skill before deployment. Triggers on create skill, write skill, skill frontmatter, validate skill, fix skill YAML. For installing a finished skill, use skill-deployer instead.
---

# Skill Creator

Guidance for building lean, effective agent skills and validating them before deployment.

> **Deployment** (scope, target paths, verification in `<available_skills>`) is handled by **skill-deployer**. Finish creation and validation here first.

## Quick Process

1. **Understand** — gather concrete usage examples (see [creation-process.md](references/creation-process.md) Step 1)
2. **Plan** — identify scripts, references, and assets to bundle
3. **Implement** — write SKILL.md and bundled resources
4. **Validate** — `python scripts/validate_skill.py <skill-folder>` (see [validation.md](references/validation.md))
5. **Deploy** — hand off to **skill-deployer** when the skill should become available to agents
6. **Iterate** — refine after real usage, re-validate after edits

## Validation (required before deploy)

```bash
python scripts/validate_skill.py <path/to/skill-folder>
python scripts/validate_skill.py <path/to/skill-folder> --strict   # before deployment
```

Checks frontmatter (same rules as the Rust scanner) and warns about common path mistakes. Full checklist: [validation.md](references/validation.md).

## Core Rules

- **Concise body**: SKILL.md under ~150 lines; move detail to `references/`
- **Triggers in frontmatter**: all "when to use" guidance goes in `description`, not the body
- **Name matches folder**: `name:` in frontmatter must equal the directory name
- **Safe YAML**: use double quotes in `description` when text contains apostrophes (`"Telegram's"`, not `'Telegram\'s'`)
- **No duplicate reads**: information lives in SKILL.md *or* references, not both
- **Imperative voice** in body instructions
- **No auxiliary docs**: no README, CHANGELOG, or INSTALLATION_GUIDE in the skill folder

## Structure

See [anatomy.md](references/anatomy.md) for directory layout (`SKILL.md`, `scripts/`, `references/`, `assets/`).

## Design Guidance

- [design-principles.md](references/design-principles.md) — concision, degrees of freedom, progressive disclosure
- [creation-process.md](references/creation-process.md) — full walkthrough
- [validation.md](references/validation.md) — validate_skill.py usage and rules
- [workflows.md](references/workflows.md) — sequential and conditional workflow patterns
- [output-patterns.md](references/output-patterns.md) — template and example patterns

## Frontmatter Checklist

```yaml
---
name: skill-name
description: "What it does + specific triggers/contexts for when to use it."
---
```

Only `name` and `description` are required. The description is the primary trigger mechanism.
