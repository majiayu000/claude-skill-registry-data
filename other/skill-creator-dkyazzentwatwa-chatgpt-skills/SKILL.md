---
name: skill-creator
description: Create or update agent skills with concise SKILL.md instructions, bundled resources, agent metadata, validation, and packaging. Use when building or refactoring skills.
---

# Skill Creator

Design or refactor skills so they are small, triggerable, and mechanically valid.

## Workflow

1. Define the exact user requests that should trigger the skill.
2. Keep `SKILL.md` short and put deep detail in `references/`.
3. Add only the scripts, assets, or references that make execution materially more reliable.
4. Generate `agents/openai.yaml` and validate before packaging.

## Scripts

- `scripts/init_skill.py` initializes a new skill with optional resource folders and `agents/openai.yaml`.
- `scripts/generate_openai_yaml.py` writes `agents/openai.yaml` from explicit interface values.
- `scripts/quick_validate.py` enforces strict frontmatter, directory naming, agent metadata, and script dependency rules.
- `scripts/package_skill.py` validates first, then zips the skill for distribution.

## Rules

- Keep frontmatter to `name` and `description` only.
- Make `description` do the trigger work: what the skill does and when to use it.
- Match the folder name exactly to `name`.
- Prefer one focused workflow over a kitchen-sink skill.
- Remove placeholder files and generic boilerplate before publishing.

## Typical Commands

```bash
python3 skill-creator/scripts/init_skill.py my-skill --path .
python3 skill-creator/scripts/generate_openai_yaml.py my-skill \
  --interface display_name="My Skill" \
  --interface short_description="One-line summary" \
  --interface default_prompt="Help me use this skill."
python3 skill-creator/scripts/quick_validate.py my-skill
python3 skill-creator/scripts/package_skill.py my-skill ./dist
```
