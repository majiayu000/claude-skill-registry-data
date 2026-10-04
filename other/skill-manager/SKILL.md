---
name: skill-manager
description: Install, remove, and manage Claude Code skills dynamically with hot-reload. Use when the user wants to add or remove skills, list available or installed skills, check the skill catalog, search for skills, or troubleshoot skill installation. Covers all 519 skills across 21 categories.
allowed-tools: Bash, Read
version: 2.0.0
author: Intent Solutions IO <jeremy@intentsolutions.io>
license: MIT
compatibility: Designed for Claude Code
tags: [skills, installation, management, catalog]
---

# Skill Manager

Manage Claude Code skills dynamically without restarting. Supports all 519 skills across 21 categories from the claude-code-plugins-plus-skills catalog.

## Live Skill Catalog

!`ccpi skills list --json 2>/dev/null | python3 -c "import json,sys; skills=json.load(sys.stdin); cats={}; [cats.setdefault(s['category'],[]).append(s['name']) for s in skills]; [print(f'{cat}: {len(names)} skills ({\"installed\" if any(s[\"installed\"] for s in skills if s[\"category\"]==cat) else \"none installed\"})') for cat,names in sorted(cats.items())]" 2>/dev/null || echo "ccpi not available — run from the claude-code-plugins-plus-skills repo"`

## Platform Surfaces

| Surface       | Path                            | Scope                 |
| ------------- | ------------------------------- | --------------------- |
| `claude`      | `~/.claude/skills/`             | Global (all projects) |
| `project`     | `<git-root>/.claude/skills/`    | Current project only  |
| `antigravity` | `~/.gemini/antigravity/skills/` | Antigravity AI        |
| `gemini`      | `~/.gemini/skills/`             | Gemini CLI            |
| `cursor`      | `~/.cursor/skills/`             | Cursor IDE            |

## When to Use

Use this skill when the user wants to:

- Install a skill from the 519-skill catalog
- Remove an installed skill
- List available or installed skills
- Search for skills matching a topic
- Check if a specific skill is installed

## Proactive Skill Suggestions

When working on a project, if the user's request matches an uninstalled skill's description from the catalog above:

1. Inform the user: _"The `<skill-name>` skill covers this — want me to install it?"_
2. If yes, install with: `ccpi skills install <skill-name> --surface project`
3. Confirm: "✓ installed and immediately available via hot-reload"

**Examples of proactive suggestions:**

- User asks about Kubernetes → suggest `kubernetes-architect` (if in catalog)
- User asks about security scanning → suggest `code-injection-detector`, `dependency-vulnerability-checker`
- User asks about AWS → suggest skills from `13-aws-skills` category

## Workflow

### Search for Skills

```bash
ccpi search <query>
```

Shows matching skills (with category) and plugins. Offers interactive install prompt.

### List Available Skills

```bash
ccpi skills list                          # all 519 skills, grouped by category
ccpi skills list --category security      # filter to security categories
ccpi skills list --surface project        # check what's installed in current project
ccpi skills list --json                   # machine-readable (for scripting)
```

### Install a Skill

```bash
# Project-local (recommended — scoped to current git repo)
ccpi skills install <skill-name> --surface project

# Global (available in every project)
ccpi skills install <skill-name> --surface claude

# Install all skills in a category
ccpi skills install --category security --surface project

# Install all 519 skills
ccpi skills install --all --surface project
```

Check installation status first:

```bash
WORKSPACE_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
ls "$WORKSPACE_ROOT/.claude/skills/" 2>/dev/null | sort
```

### Remove a Skill

```bash
ccpi skills remove <skill-name> --surface project
```

## Important Notes

- **Hot-reload**: Installed skills are immediately available without restarting Claude Code
- **Symlinks**: Skills are symlinked from the repo source — updates propagate instantly
- **Source**: All 519 skills live in `skills/<category>/` in this repo
- **Safety**: Always confirm before removing skills

## Examples

**User:** "List available skills"
→ Run `ccpi skills list --surface project` → display grouped output

**User:** "Install hooks-mastery skill"
→ `ccpi skills install hooks-mastery --surface project`
→ "✓ hooks-mastery installed → .claude/skills/ — ready to use!"

**User:** "What security skills are available?"
→ `ccpi skills list --category security` → show 50 security skills
→ Ask which to install

**User:** "Remove project-bootstrapper"
→ Confirm → `ccpi skills remove project-bootstrapper --surface project`
→ "✓ project-bootstrapper removed (symlink only, source intact)"

**User:** "Is there a skill for Kubernetes?"
→ `ccpi search kubernetes` → show matches
→ Offer to install

## Tutorials

```bash
ccpi tutorials      # list 11 tutorial notebooks
ccpi tutorials 7    # open "What is a Skill?" in Jupyter
```
