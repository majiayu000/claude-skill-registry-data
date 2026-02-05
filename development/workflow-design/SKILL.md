---
name: workflow-design
description: Design, discover, and refactor multi-command workflows for Claude Code
---

# Workflow Design Skill

Define multi-command workflows that guide users through complex processes.

## Core Concepts

**Workflow:** Documented sequence of commands accomplishing a goal.

**Components:** Workflow document + individual command files + command-workflow links.

**Good candidates:** Multi-step processes with clear phases, repeatable processes, processes with decision points.

**Bad candidates:** Single-step operations, rarely-used sequences, completely linear with no decisions.

## Three Modes

### 1. Discovery Mode
**When:** Have related commands, need to identify workflow.

**Process:** List commands -> identify sequence -> find phase boundaries -> determine dependencies -> generate workflow doc -> update command metadata.

### 2. Design Mode
**When:** Creating new multi-step process from scratch.

**Process:** Clarify goal -> break into phases -> identify decision points -> create workflow doc -> scaffold command stubs -> implement commands.

### 3. Refactor Mode
**When:** Workflow exists but needs improvement.

**Analyze:** Completeness, ordering, clarity, consistency. Output updated docs and migration notes.

## Workflow Document Template

Location: `workflows/[workflow-name].md`

```markdown
# [Workflow Name]

## Overview
[1-2 sentence goal]

## When to Use
- [Use case 1]

## Phases

### 1. [Phase Name] (interactive/automated)
- **Command:** /command-name
- **Purpose:** What it accomplishes
- **Output:** What it produces
- **Repeatable:** yes/no (optional)

## Execution
- Manual: /command1 -> /command2
- Automated: /workflow-run [workflow-name]
```

## Command-Workflow Metadata

Commands reference workflows BELOW frontmatter:
```markdown
**Workflow:** [workflow-name] - **Phase:** phase-name (step X/Y) - **Next:** /next-command
```

## Phase Design Principles

1. **Clear Boundaries:** Distinct purpose, defined outputs, obvious transitions
2. **Single Responsibility:** One thing well per phase
3. **Checkpoints:** Interactive phases validate progress
4. **Automation-Friendly:** Questions answerable from codebase

## Workflow Patterns

- **Linear:** Phase 1 -> Phase 2 -> Phase 3 -> Done
- **Loop:** Phase 1 -> Phase 2 -> (repeat Phase 2) -> Done
- **Branching:** Phase 1 -> (choice) -> Phase 2a OR 2b -> Done
- **Parallel:** Phase 1 -> (2a + 2b parallel) -> Phase 3 -> Done

## Naming

Good: `epic-development.md`, `database-migration.md`, `feature-release.md`

Bad: `stuff.md`, `the-way-we-do-things.md`, `process-1.md`

## Key Principle

Workflows document existing patterns, they don't invent them. Commands remain primary. Workflows organize them. User stays in control.
