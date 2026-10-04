---
name: thrunt-add-phase
description: Add phase to end of current milestone in huntmap
argument-hint: "<description>"
allowed-tools: Read, Write, Bash
---


<objective>
Add a new integer phase to the end of the current milestone in the huntmap.

Routes to the add-phase workflow which handles:
- Phase number calculation (next sequential integer)
- Directory creation with slug generation
- Huntmap structure updates
- STATE.md huntmap evolution tracking
</objective>

<execution_context>
@.github/thrunt-god/workflows/add-phase.md
</execution_context>

<context>
Arguments: $ARGUMENTS (phase description)

Huntmap and state are resolved in-workflow via `init phase-op` and targeted tool calls.
</context>

<process>
**Follow the add-phase workflow** from `@.github/thrunt-god/workflows/add-phase.md`.

The workflow handles all logic including:
1. Argument parsing and validation
2. Huntmap existence checking
3. Current milestone identification
4. Next phase number calculation (ignoring decimals)
5. Slug generation from description
6. Phase directory creation
7. Huntmap entry insertion
8. STATE.md updates
</process>
