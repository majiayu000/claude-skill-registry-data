---
name: obsidian-worklog
description: Ensures project worklogs and documentation are written to an Obsidian vault with proper naming conventions
---

# Obsidian Worklog Skill

## Purpose

This skill ensures that project worklogs, plans, and documentation are written to an Obsidian vault instead of project directories.

## Worklog Location and Naming Convention

**CRITICAL**: When working on any project and Claude needs to create worklogs, plans, documentation, or notes:

1. **Location**: Write to the Obsidian worklog folder at `~/Documents/Main Vault/10-19 Logs/15 Worklogs`
2. **Naming Convention**: `{project-name}/{YYYY-MM-DD}-{title}.md`
   - Example: `my-app/2025-11-05-initial-setup.md`
   - Example: `website-redesign/2025-11-05-navigation-refactor.md`

## When to Use This

Apply this convention when:

- Creating project plans or roadmaps
- Documenting work sessions
- Writing progress updates
- Creating TODO lists or task breakdowns
- Documenting decisions or architectural notes
- Any other project documentation

## Do NOT Use This For

- Code files (`.py`, `.js`, `.tsx`, etc.) - these go in the project directory
- Configuration files
- README files that should live in the project repo
- Build artifacts or generated files

## File Format

Use standard Markdown with frontmatter:

```markdown
---
project: { project-name }
date: { YYYY-MM-DD }
tags: [worklog, { relevant-tags }]
---

# {Title}

{Content}
```

## Example Usage

User: "Let's plan out the authentication feature for my-app"

Claude should create: `~/obsidian-vault/worklog/my-app/2025-11-05-authentication-planning.md`

## Path Resolution

- If the user mentions their Obsidian vault location explicitly, use that path
- Default to `~/obsidian-vault/worklog/` if not specified
- Create subdirectories as needed for each project

## Important Notes

- Always confirm the Obsidian vault path with the user on first use
- Create the project subdirectory if it doesn't exist
- Use kebab-case for project names and titles in filenames
- Date format must be ISO 8601 (YYYY-MM-DD)
