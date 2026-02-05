---
name: metis
description: Flight Levels methodology for project and work management. Use when planning projects, decomposing work into tasks, deciding document types, managing phases, or coordinating initiatives. Applies Kanban-based pull systems and hierarchical work alignment (Vision -> Strategy -> Initiative -> Task). Teaches when and why to use Metis tools.
---

# Metis Flight Levels Skill

This skill teaches Flight Levels methodology for work management using Metis. It extends the Metis MCP server with judgment and methodology guidance.

## Prerequisites

- Metis MCP server connected and available
- A Metis workspace initialized (`metis init` or via MCP)

## What This Skill Provides

The Metis MCP server teaches you **how** to use the tools. This skill teaches you **when** and **why**.

- When to create which document type
- How to decompose work effectively
- When to transition between phases
- Common mistakes and how to avoid them
- Patterns for different project types

## Core Methodology

See [methodology/core-principles.md](methodology/core-principles.md) for:
- The Flight Levels hierarchy (Vision -> Strategy -> Initiative -> Task)
- Pull-based Kanban flow
- Value alignment and why hierarchy matters
- Phase-gated progress
- Source of truth (filesystem over database)

## Choosing a Configuration

See [methodology/preset-selection.md](methodology/preset-selection.md) for:
- Full vs Streamlined vs Direct presets
- Decision framework for choosing
- When to change presets
- Signs you chose wrong

## Breaking Down Work

See [methodology/decomposition.md](methodology/decomposition.md) for:
- When to decompose (ahead of capacity, not upfront)
- Sizing by scope, not time
- The explicit decompose phase and why it exists
- Decomposition patterns (vertical slices, risk-first, etc.)

## Moving Through Phases

See [methodology/phase-transitions.md](methodology/phase-transitions.md) for:
- Phase sequences for each document type
- Exit criteria patterns
- When and how to transition
- Monitoring phase health

## What Not to Do

See [methodology/anti-patterns.md](methodology/anti-patterns.md) for:
- Shadow work and shadow backlogs
- Too many active items (WIP limits)
- Skipping phases
- Stale work and metric gaming

## Project Patterns

Apply these patterns based on your situation:

- [patterns/greenfield.md](patterns/greenfield.md) - Starting new projects
- [patterns/tech-debt.md](patterns/tech-debt.md) - Debt reduction campaigns
- [patterns/incident-response.md](patterns/incident-response.md) - Handling urgent work
- [patterns/feature-development.md](patterns/feature-development.md) - Standard feature flow

## Decision Guides

When unsure what to do:

- [decision-trees/document-type.md](decision-trees/document-type.md) - Which document type to create
- [decision-trees/when-to-adr.md](decision-trees/when-to-adr.md) - When to record architectural decisions

## Quick Reference

### Document Types
| Type | Purpose | Parent Required |
|------|---------|-----------------|
| Vision | North star objectives | No |
| Strategy† | Coordinated approaches | Vision |
| Initiative | Capability increments | Strategy or Vision‡ |
| Task | Atomic work units | Initiative |
| Task (backlog) | Ad-hoc work (bug/feature/debt) | No* |
| ADR | Architectural decisions | No |

*Backlog items are tasks created with `backlog_category` parameter instead of `parent_id`. Use `reassign_parent` to move them into an initiative later, if desired.

†Strategy documents are only available in the **Full** preset. See [preset-selection.md](methodology/preset-selection.md).

‡In Streamlined preset (no Strategy), Initiatives parent directly to Vision.

### Common Operations

**Check existing work before starting:**
```
list_documents(project_path)  # See all active visions, initiatives, and tasks
```
Always check the current state before creating new documents. This prevents duplicate work and helps you understand where new items should fit in the hierarchy.

**Start a project:**
1. `initialize_project` with appropriate prefix
2. `create_document` for vision, then `read_document` and `edit_document` to fill in all sections
3. Transition vision to published when complete
4. Create initiatives aligned to vision (create → read → edit for each)
5. Decompose initiatives into tasks (create → read → edit for each)

**Do work:**
1. Pull tasks when capacity exists
2. Transition to active when starting
3. Complete when acceptance criteria met
4. Look up for next work when backlog is low

**Handle ad-hoc work (bugs, features, tech debt):**

When users say "create a bug/feature/tech debt ticket", create a backlog item:
```
create_document(type="task", title="...", backlog_category="bug")      # for bugs
create_document(type="task", title="...", backlog_category="feature")  # for features
create_document(type="task", title="...", backlog_category="tech-debt") # for tech debt
```
Then read and fill in the document with details. Either work independently (if critical) or feed into initiative later.

**Clean up completed work:**
```
archive_document(short_code="PROJ-I-0001")  # Archives initiative and all its tasks
```
Archive completed initiatives to keep active document lists focused. Archived documents are preserved but hidden from default listings.

### Key Principles

- **Work is pulled, never pushed** - Low backlog signals to look up
- **All work traces to vision** - If it doesn't align, question its value
- **Phases exist for a reason** - Don't skip them (transitions will fail if you try)
- **Filesystem is truth** - Database is just a cache
- **Scope over time** - Size by capability increment, not duration
- **Read before edit** - Always `read_document` before `edit_document`
- **Complete documents after creation** - Never leave a document with template placeholders. After `create_document`, immediately `read_document` then `edit_document` to fill in all required sections with actual content
- **Delete unused sections** - Templates contain optional sections; delete what doesn't apply rather than leaving empty placeholders
- **Update active tasks** - Use active tasks as working memory; record progress, findings, and decisions regularly
