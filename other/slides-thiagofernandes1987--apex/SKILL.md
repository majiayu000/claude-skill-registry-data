---
name: ckm:slides
description: Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies.
argument-hint: "[topic] [slide-count]"
metadata:
  author: claudekit
  version: "1.0.0"
skill_id: design.slides
executor: LLM_BEHAVIOR
status: ADOPTED
security: { level: standard, pii: false, approval_required: false }
anchors:
  - design
  - frontend
  - engineering
tier: 2
input_schema:
  - name: code_or_task
    type: string
    description: "Code snippet, script, or task description to process"
    required: true
  - name: context
    type: string
    description: "Additional context or background information"
    required: false
output_schema:
  - name: plan
    type: string
    description: "Strategic plan or design document"
  - name: next_steps
    type: array
    description: "List of recommended next steps"
what_if_fails: >
  FALLBACK: If Ckm:Slides cannot complete, provide partial results with
  explicit gaps noted. Never block workflow silently.
  ESCALATE: If core capability is unavailable, suggest nearest alternative skill.
  RULE: Always explain what failed and what manual steps can substitute.
---

# Slides

Strategic HTML presentation design with data visualization.

<args>$ARGUMENTS</args>

## When to Use

- Marketing presentations and pitch decks
- Data-driven slides with Chart.js
- Strategic slide design with layout patterns
- Copywriting-optimized presentation content

## Subcommands

| Subcommand | Description | Reference |
|------------|-------------|-----------|
| `create` | Create strategic presentation slides | `references/create.md` |

## References (Knowledge Base)

| Topic | File |
|-------|------|
| Layout Patterns | `references/layout-patterns.md` |
| HTML Template | `references/html-template.md` |
| Copywriting Formulas | `references/copywriting-formulas.md` |
| Slide Strategies | `references/slide-strategies.md` |

## Routing

1. Parse subcommand from `$ARGUMENTS` (first word)
2. Load corresponding `references/{subcommand}.md`
3. Execute with remaining arguments

## Why This Skill Exists
<!-- TODO: describe why this skill was created and what problem it solves -->
Provides specialized `slides` capability to the APEX system.

## When to Use
<!-- TODO: describe when to invoke this skill vs alternatives -->
Use this skill when working with `slides` tasks in the `design` domain.

## What If Fails
<!-- TODO: describe fallback behavior -->
FALLBACK: Use a related skill in the `design` domain.
RULE: Never block workflow — always suggest manual alternative.
