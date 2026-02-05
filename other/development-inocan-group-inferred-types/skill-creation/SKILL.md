---
name: skill-creation
description: Use this skill when the user asks to create a new skill, custom command, or wants to know how skills work in Claude Code.
---

# How to Create Claude Code Skills

Skills are auto-triggered capabilities that Claude uses based on context relevance.

## Directory Structure

```
.claude/skills/<skill-name>/SKILL.md
```

- Each skill lives in its own subdirectory
- The file MUST be named exactly `SKILL.md` (case-sensitive)
- The directory name can be anything descriptive

## Required Format

Every SKILL.md must have YAML frontmatter:

```markdown
---
name: my-skill-name
description: Use this skill when [describe triggers]. [What it does].
---

# Skill Title

[Instructions for Claude on how to use this skill]
```

## YAML Frontmatter Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Identifier for the skill (kebab-case) |
| `description` | Yes | Tells Claude WHEN to auto-trigger this skill |

## The Description Field is Critical

The `description` determines when Claude automatically uses the skill. Write it as:
- "Use this skill when [specific triggers]"
- Be specific about contexts that should activate it
- Include key phrases the user might say

## Example: Creating a New Skill

To create a skill for database operations:

1. Create directory: `.claude/skills/database-ops/`
2. Create file: `.claude/skills/database-ops/SKILL.md`
3. Add content:

```markdown
---
name: database-operations
description: Use this skill when working with database queries, migrations, or schema changes in this project.
---

# Database Operations

## When to Use
- Running migrations
- Writing queries
- Modifying schema

## Instructions
[Detailed instructions for Claude...]
```

4. Restart Claude Code to load the skill

## Skills vs Slash Commands

| Feature | Skills | Slash Commands |
|---------|--------|----------------|
| Location | `.claude/skills/<name>/SKILL.md` | `.claude/commands/<name>.md` |
| Invocation | Auto-triggered by Claude | User types `/<name>` |
| Frontmatter | Required (name, description) | Optional |
| Use case | Context-aware automation | Explicit user actions |

## Common Mistakes to Avoid

1. **Wrong filename**: Must be `SKILL.md`, not `skill.md` or `<name>.md`
2. **Missing frontmatter**: The `---` YAML block is required
3. **File in wrong location**: Must be in a subdirectory, not directly in `.claude/skills/`
4. **Vague description**: Be specific about when to trigger
5. **Forgetting to restart**: Claude Code needs restart to load new skills
