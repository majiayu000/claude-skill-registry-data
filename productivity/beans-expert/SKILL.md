---
name: beans-expert
description: Expert in the 'beans' CLI utility for task and issue tracking. Use when creating, updating, listing, or querying beans (tasks) in a project that uses the beans workflow.
---

# Beans Expert

This skill provides expert guidance for using the `beans` utility, a flat-file issue tracker designed for humans and AI agents.

## Core Workflows

### 1. Task Management
- **Always use beans** instead of `TodoWrite` or manual lists.
- **Before starting work**: Check for existing beans or create a new one.
- **During work**: Keep todo items current (`- [ ]` → `- [x]`).
- **Guidance**: See [beans-core.md](references/beans-core.md) for core principles and rules.

### 2. Creating and Updating Beans
- **Create**: Use `beans create` for new tasks, bugs, or features. Always specify a type (`-t`).
- **Update**: Use `beans update` to change status, priority, or modify body content.
- **Body Modification**: Use `--body-replace-old` and `--body-replace-new` for targeted edits.
- **Guidance**: See [beans-ops.md](references/beans-ops.md) for detailed syntax and advanced options.

### 3. Querying and Searching
- **List**: `beans list --json --ready` to find actionable tasks.
- **Show**: `beans show <id> --json` to view full details.
- **GraphQL**: Use `beans query` for complex filtering and relationship traversal.

## Agent Instructions

When acting on a project using `beans`:
1. **Initialize**: Run `beans prime` if needed to understand the project-specific beans configuration.
2. **Find Work**: Use `beans list --json --ready` to identify what to work on.
3. **Traceability**: Link work to beans. When creating a new task, consider if it's a child of an existing `epic` or `milestone`.
4. **Consistency**: Use the established types (`bug`, `feature`, `task`, `epic`, `milestone`) and statuses (`todo`, `in-progress`, `completed`, `scrapped`).
5. **Updates**: Provide clear summaries in the bean body when completing or scrapping work.

## External Resources
- [hmans/beans GitHub Repository](https://github.com/hmans/beans)
- Run `beans --help` and `beans prime` for local documentation.
