---
name: create-skill
description: Create a new reusable Claude Code skill and register it for auto-discovery. Use when the user asks to save a technique, pattern, or workflow as a skill.
argument-hint: <skill-name> [description of what the skill should capture]
---

# Create a Claude Code Skill

## Skill Discovery

Claude Code discovers skills from these locations (no symlinks needed):

| Location | Path | Scope |
|----------|------|-------|
| **Personal** | `~/.claude/skills/<skill-name>/SKILL.md` | All projects |
| **Project** | `.claude/skills/<skill-name>/SKILL.md` | Current project only |

The user's personal skills are also stored in `~/dotfiles/claude-skills/` for version control.

## Process

1. **Choose a name**: kebab-case, descriptive of the capability (e.g. `visualize-se3-frames`, `fold-knowledge-into-data`)

2. **Create the skill file** with this structure:

```markdown
---
name: <skill-name>
description: <one-line description of when to use this skill — written for Claude, not humans>
argument-hint: <what arguments the user might pass>
allowed-tools: <comma-separated list of tools the skill needs, e.g. Read, Bash(cmd:*)>
---

# <Title>

<Brief explanation of the technique/pattern>

## Core Recipe

<Minimal, copy-paste-ready code or steps that accomplish the task>

## Variations

<Common adaptations, parameter choices, edge cases>

## When Applying This Skill

<Numbered checklist of decisions to make when using it>
```

3. **Install the skill**:
```bash
mkdir -p ~/dotfiles/claude-skills/<skill-name>
# Write SKILL.md here
ln -s ~/dotfiles/claude-skills/<skill-name> ~/.claude/skills/<skill-name>
```
The canonical copy lives in `~/dotfiles/claude-skills/` (version controlled). Symlink it into `~/.claude/skills/` for discovery.

## Skill Writing Guidelines

- The **description** field is how Claude decides whether to invoke the skill — make it specific about triggers and use cases
- The **argument-hint** tells the user what to type after the slash command
- Lead with a working **core recipe** — minimal code that solves the common case
- Include **variations** only for genuinely common alternatives, not every possibility
- Keep it concise: a skill is a recipe card, not a tutorial
- Code in skills should be self-contained snippets, not imports from the project
- Write for Claude as the reader: skills guide Claude's code generation, so frame instructions as "do this" not "you can do this"
- **Set `allowed-tools` in the frontmatter** when a skill needs specific tools without prompting. Use comma-separated tool names with parenthesized patterns for Bash: `allowed-tools: Read, Bash(ls:*), Bash(pyright:*)`. Without this, the user gets prompted for every tool call even if the skill describes which tools are permitted.
