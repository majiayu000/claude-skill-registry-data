---
name: julien-dev-skill-renamer
description: "Rename a skill across the marketplace. Use when: user wants to rename a skill, change skill name, or refactor skill naming."
license: Apache-2.0
metadata:
  author: "Julien"
  version: "1.0.0"
  category: "development"
triggers:
  - "rename skill"
  - "change skill name"
  - "refactor skill"
  - "renommer skill"
  - "changer nom skill"
  - "renommer une skill"
---

# Skill Renamer

Rename a skill and update all references across the marketplace.

## When to Use

- Renaming a skill (e.g., `skill-creator-pro` → `skill-creator`)
- Refactoring skill naming conventions
- Fixing typos in skill names

## Usage

```bash
python skills/julien-dev-tools-skill-renamer/scripts/rename-skill.py <old-name> <new-name>
```

### Examples

```bash
# Short name (auto-detects full folder name)
python skills/julien-dev-tools-skill-renamer/scripts/rename-skill.py skill-creator-pro skill-creator

# Full name
python skills/julien-dev-tools-skill-renamer/scripts/rename-skill.py julien-dev-tools-old julien-dev-tools-new

# Dry run first
python skills/julien-dev-tools-skill-renamer/scripts/rename-skill.py old-name new-name --dry-run
```

## What It Does

1. Finds the skill folder (supports short or full name)
2. Updates `name:` in SKILL.md
3. Replaces all references in:
   - `skills/**/*.md`
   - `configs/*.json`
   - `.claude-plugin/*.json`
   - `scripts/*.py`
4. Renames the folder

## After Running

```bash
git status          # Review changes
git diff            # Check replacements
git add -A && git commit -m "rename: old-name → new-name"
git push
```

## Skill Chaining

### Skills Required Before
- None

### Input Expected
- Old skill name (short or full)
- New skill name

### Output Produced
- Modified files with updated references
- Renamed skill folder

### Compatible Skills After
- **julien-workflow-sync-personal-skills**: Sync renamed skill to ~/.claude/skills/
