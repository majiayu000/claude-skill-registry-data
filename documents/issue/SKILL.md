---
name: issue
description: This skill should be used when the user asks to "create an issue", "write an issue", "add an issue", "log an issue", "report a bug", "document a problem", or wants to track tasks, bugs, or feature requests in the issues folder.
---

# Issue Writing Guidelines

Create and manage issues in the `issues/` folder at the project root.

## Workflow

1. Ensure the `issues/` folder exists (create if needed)
2. Generate a unique filename using date and title
3. Write the issue file with proper frontmatter
4. Confirm the issue was created

## Issue File Format

Each issue is a Markdown file with YAML frontmatter:

```markdown
---
date: YYYY-MM-DD
title: <concise issue title>
status: open
---

# <Issue Title>

## Description

<Detailed description of the issue, bug, or feature request>

## Context

<Any relevant context, steps to reproduce, or background information>
```

## File Naming Convention

`issues/YYYY-MM-DD-<slug>.md`

- Use the current date
- Convert title to kebab-case slug
- Keep slug under 50 characters
- Use only lowercase letters, numbers, and hyphens

### Examples

- `issues/2025-12-27-fix-parser-crash.md`
- `issues/2025-12-27-add-type-annotations.md`
- `issues/2025-12-27-improve-error-messages.md`

## Status Values

| Status | Meaning |
|--------|---------|
| `open` | New issue, not yet addressed |
| `in-progress` | Currently being worked on |
| `closed` | Issue resolved or no longer relevant |

## Writing Good Issue Descriptions

- Be specific about the problem or feature
- Include steps to reproduce for bugs
- Mention expected vs actual behavior
- Reference related files or code when relevant
- Keep descriptions focused and actionable

## Example Issue

```markdown
---
date: 2025-12-27
title: Parser fails on empty input
status: open
---

# Parser fails on empty input

## Description

The parser crashes with an index out of bounds error when given an empty string as input.

## Context

- File: `Ziku/Parser.lean`
- Error occurs in the `parse` function
- Expected: Return an empty AST or appropriate error
- Actual: Crashes with uncaught exception

## Steps to Reproduce

1. Run `ziku parse ""`
2. Observe the crash
```
