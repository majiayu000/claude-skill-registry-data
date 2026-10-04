---
name: config-reuse
description: Copy/sync Claude configs & rules from another project.
---

# Config Reuse

Import Claude Code configs (commands, skills, rules) from a source project into the current project or global config.

## Workflow

### 1. Detect Target Stack

Check current project for language indicators:

```bash
# Python?
[[ -f pyproject.toml ]] || [[ -f setup.py ]] || [[ -f requirements.txt ]] && echo python
# TypeScript?
[[ -f tsconfig.json ]] && echo typescript
# JavaScript?
[[ -f package.json ]] && echo javascript
# Rust?
[[ -f Cargo.toml ]] && echo rust
# Go?
[[ -f go.mod ]] && echo go
```

Save detected languages as `TARGET_LANGS`.

### 2. Scan Source

```bash
bash ~/.claude/skills/config-reuse/scripts/scan-configs.sh "$SOURCE_PATH"
```

Output: TSV with TYPE, REL_PATH, MD5, MARKERS per config file.

### 3. Compare

```bash
bash ~/.claude/skills/config-reuse/scripts/diff-configs.sh "$SOURCE_PATH" "$(pwd)"
```

Output: TSV with TYPE, REL_PATH, STATUS, MATCH_PATH.

### 4. Classify

Using script outputs + target stack:

**Skip:**
- `CLAUDE.local.md`, `.claudeignore` (always project-specific)
- Configs with `DOMAIN:*` markers (domain-specific)
- `identical_global` or `identical_project` status (already installed)
- Language-marked configs where language is NOT in `TARGET_LANGS`

**Auto-recommend:**
- `not_installed` configs with no `DOMAIN:*` markers AND (no language markers OR language in `TARGET_LANGS`)

**Needs judgment — read the file:**
- `differs_global` or `differs_project` status (merge decision)
- Root `CLAUDE.md` or `.claude/CLAUDE.md` (may have extractable sections)
- Rules with `paths:` frontmatter (check if glob matches target project)

### 5. Present and Copy

Show a table of recommendations grouped by action. Wait for approval.

Copy approved configs:
- **Commands** → `~/.claude/commands/` (global)
- **Skills** → `.claude/skills/` (project) or `~/.claude/skills/` (global, if general)
- **Rules** → `.claude/rules/` (project)
- Back up before overwriting: `cp <existing> ~/.claude/backups/<name>.bak.$(date +%s)`
- If a skill has a project name in `description:`, edit it after copying

## Safety

- Never copy `settings.local.json` or files matching `*secret*`, `*credential*`
- Back up before overwriting
