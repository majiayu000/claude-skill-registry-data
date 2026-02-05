---
name: readme-writing
description: Guidelines for writing folder READMEs. Use when creating README.md files for directories.
---

# README Writing

A folder README has one job: explain **why this folder exists**.

Users can run `ls` to see what's in a folder. They need you to explain the reasoning behind the organization, the mental model, and any non-obvious context that helps them understand where things belong.

## Good README

Explains purpose, organizational logic, and helpful context:

```markdown
# Converters

Transform field schemas into format-specific representations.

Field schemas are pure JSON Schema objects with `x-component` hints. Different systems need them in different formats: ArkType for runtime validation, Drizzle for SQLite column definitions.

Each converter takes the same input (a field schema) and produces output for a specific consumer. If you need field schemas in a new format, add a converter here.
```

## Bad README

File listing that duplicates what's visible:

```markdown
# Converters

- `to-arktype.ts` - Converts to ArkType
- `to-drizzle.ts` - Converts to Drizzle
- `index.ts` - Exports
```

## Guidelines

- Explain the "why" and the mental model
- Add context that helps developers know where to put new code
- Mention relationships to other folders when relevant
- Don't list files or duplicate what's obvious from the code
- Keep it scannable; a few sentences to a short paragraph is usually enough

Exception: Root project READMEs need installation, usage, etc. This skill is for internal folder documentation.
