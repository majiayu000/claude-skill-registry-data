---
name: openspec-cli
description: Guidelines for using the OpenSpec CLI tool in non-interactive environments. Use this skill when validating specifications or changes to ensure commands run successfully without user intervention.
metadata:
  short-description: Run OpenSpec validation non-interactively
---

# OpenSpec CLI Guidelines

This skill provides instructions for using the `openspec` command-line interface (CLI) effectively within the MCP environment, where interactive prompts are not supported.

## Core Principles

- **Non-Interactive Mode**: Always use flags that bypass interactive prompts.
- **Explicit Targets**: Specify exactly what to validate to avoid ambiguity.

## Validation Commands

The default `openspec validate` command triggers an interactive mode which will cause the agent to hang or fail. Use the following explicit commands instead:

### Validate All
To validate the entire project:
```bash
openspec validate --all
```

### Validate Changes
To validate only the currently changed files (useful for quick checks):
```bash
openspec validate --changes
```

### Validate Specifications
To validate only the specification files:
```bash
openspec validate --specs
```

### Validate Specific Item
To validate a specific item by name:
```bash
openspec validate <item-name>
```
