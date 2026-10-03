---
name: safe-skill
description: >-
  A simple code formatting skill. Reformats code to follow project conventions.
  Use when the user asks to "format code", "clean up formatting", or "fix style".
allowed-tools: ""
---

# Code Formatter

Reformat the specified file(s) to match the project's code style conventions.

## Rules

1. Use consistent indentation (detect from existing code: tabs or spaces)
2. Normalize trailing whitespace
3. Ensure files end with a single newline
4. Align object properties when they're on consecutive lines
5. Sort imports alphabetically within each group

## When to Use

- User asks to format or clean up a file
- As a final step after refactoring

## When NOT to Use

- During a code review (formatting changes obscure logic changes)
- On generated files (formatters can break generated code)
