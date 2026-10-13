---
name: coding
description: Guidelines for writing surgical, clean, and simple code.
---

# Coding

Guidelines for writing surgical, clean, and simple code.

## Core Guidelines

- **Surgical edits**: Modify only the requested lines. Avoid drive-by code cleanup or reformatting.
- **Match conventions**: Replicate the indent spacing, quote styles, naming patterns, and file layouts of surrounding code.
- **Remove orphans**: Delete any variables, imports, or helper functions that your changes make unused.
- **AST Safety**: Ensure all brackets, semicolons, and indentation levels are syntactically correct.
