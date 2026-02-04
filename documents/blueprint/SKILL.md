---
name: blueprint
description: Provides unified CLI access for Blueprint framework - gate validation, document templates, FrontMatter schemas, worker handoffs, constitutions, and worker registry.
allowed-tools: Bash, Read
---

# Blueprint

Unified CLI for the Blueprint orchestration framework.

## Quick Reference

| Submodule | Purpose | Data Source |
|-----------|---------|-------------|
| `aegis` | Gate validation & aspects | `blueprint/gates/` |
| `forma` | Document templates | `blueprint/templates/` |
| `frontis` | FrontMatter search & schemas | `blueprint/front-matters/` |
| `hermes` | Worker handoff forms | `blueprint/forms/` |
| `lexis` | Constitution viewer | `blueprint/constitutions/` |
| `polis` | Worker registry | `.claude/agents/` |

## Commands

```bash
# General
blueprint.sh --help
blueprint.sh --list

# Aegis - Gates
blueprint.sh aegis --list                # List all gates
blueprint.sh aegis <gate>                # Show gate definition
blueprint.sh aegis <gate> --aspects      # List aspects for gate
blueprint.sh aegis <gate> <aspect>       # Show specific aspect

# Forma - Templates
blueprint.sh forma list                  # List available templates
blueprint.sh forma show <name>           # Show template content

# Frontis - FrontMatter
blueprint.sh frontis search <field> <value> [path]  # Search by FrontMatter
blueprint.sh frontis show <file> [file...]          # Show frontmatter
blueprint.sh frontis schema <type>                  # View schema
blueprint.sh frontis schema --list                  # List schemas

# Hermes - Handoffs
blueprint.sh hermes --list               # List all handoff forms
blueprint.sh hermes <from> <to>          # Show specific handoff

# Lexis - Constitutions
blueprint.sh lexis --list                # List all workers
blueprint.sh lexis <worker>              # Show base + worker constitution
blueprint.sh lexis --base                # Show base constitution only

# Polis - Workers
blueprint.sh polis --list                # List all workers with descriptions
blueprint.sh polis <worker>              # Show worker instruction
```

## Examples

```bash
# Find all spec documents
blueprint.sh frontis search type spec

# View spec-lib template
blueprint.sh forma show spec-lib

# Check gate aspects
blueprint.sh aegis documentation --aspects

# View handoff format between workers
blueprint.sh hermes orchestrator specifier

# Check worker constitution
blueprint.sh lexis specifier

# List available workers
blueprint.sh polis --list
```

## When to Use

Use this skill when working with Blueprint Framework:

- **Creating documents**: Use `forma` for templates, `frontis` for schemas
- **Validating work**: Use `aegis` for gate criteria and aspects
- **Worker communication**: Use `hermes` for handoff formats
- **Understanding roles**: Use `lexis` for constitutions, `polis` for worker info
