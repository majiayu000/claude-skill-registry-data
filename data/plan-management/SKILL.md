---
description: Generate technical implementation plan and task list from PRD and architecture documents
---

# Plan Management Skill

## Overview

This skill generates a technical implementation plan and granular task list from the PRD and architecture documentation. It bridges the gap between requirements and actual development work for the PLG Lead Qualification Tool.

## Purpose

Transform project documentation into:

1. **Technical Plan** (`docs/plan.md`) - High-level implementation approach with phases, milestones, and dependency graphs
2. **Task List** (`docs/tasks.md`) - Granular, executable tasks with dependencies, parallel markers, and doc references
3. **Project Context** (`CLAUDE.md`) - Updated persistent context for all sessions

## Core Principles

### 1. Functional-First Ordering

Tasks are ordered to achieve **working software quickly**:

- **Vertical Slices First** - Build end-to-end functionality before breadth
- **Milestones Over Phases** - Each milestone produces visible, testable progress
- **Quick Wins** - Get something functional as early as possible

### 2. Dependency-Based Concurrency

Tasks include explicit dependency metadata enabling:

- **Parallel Work** - Independent tasks can run concurrently
- **Clear Blocking** - Dependencies explicitly state what must complete first
- **Flexible Ordering** - Non-blocking tasks can be reordered based on context

### 3. Documentation References

Every task references its relevant documentation:

- **UI Tasks** → `screens.md`, `design-system.md`
- **Database Tasks** → `architecture.md#database-schema`
- **Worker Tasks** → `architecture.md#background-workers`
- **AI Tasks** → `ai-prompt.md`, `domain.md`
- **Deployment Tasks** → `railway-sqlite-setup.md`

## When to Use

- Before starting any implementation work
- When requirements change significantly (use `/plan refresh`)

## Workflow Modes

### Mode 1: Initial Planning (`/plan`)

Full plan generation from scratch:

1. **Gather Requirements**
   - Read `docs/prd.md` completely
   - Read `docs/architecture.md` for system design
   - Read `docs/domain.md` for C-PACE qualification logic
   - Read `docs/design-system.md` for MudBlazor UI patterns
   - Read `docs/screens.md` for UI specifications
   - Read `docs/ai-prompt.md` for AI evaluation prompt
   - Read `docs/railway-sqlite-setup.md` for deployment config

2. **Research Library Documentation**
   - For each technology in the stack, fetch current documentation:
     - Use `mcp__context7__resolve-library-id` to find Context7 library IDs
     - Use `mcp__context7__query-docs` to fetch setup guides and best practices
     - Use `WebSearch` as fallback for libraries not in Context7
   - Focus on: MudBlazor components, EF Core patterns, Blazor Server, Background Services
   - Note any version-specific considerations

3. **Generate Plan**
   - Create `docs/plan.md` using PLAN-TEMPLATE.md
   - Define phases aligned with architecture components
   - Include dependency graph showing phase relationships
   - Include parallel work opportunities
   - Mark milestones (M1-M6) at key functional points
   - Mark MVP boundary clearly
   - Include Documentation Reference Map
   - List external dependencies
   - Incorporate best practices from documentation research

4. **User Approval**
   - Present plan summary
   - Wait for explicit approval before proceeding
   - Allow user to request changes

5. **Generate Tasks**
   - Create `docs/tasks.md` using TASKS-TEMPLATE.md
   - Order tasks for functional milestones first
   - Include dependency metadata (`deps:`, `parallel:`)
   - Include documentation references (`docs:`)
   - Add file references and verification steps
   - Add milestone markers at key tasks
   - Include concurrency guide section

6. **Update Context**
   - Update `CLAUDE.md` with project conventions
   - Include tech stack, structure, and session protocol

7. **Report Summary**
   - Total phases and tasks
   - Milestone progression
   - Parallel work opportunities
   - MVP scope
   - Estimated task count per phase

### Mode 2: Refresh Planning (`/plan refresh`)

Update existing plan while preserving progress:

1. **Read Current State**
   - Parse `docs/plan.md` for phases and structure
   - Parse `docs/tasks.md` for completion status
   - Identify completed vs pending tasks

2. **Detect Changes**
   - Compare docs/ files to existing plan
   - Note new requirements or architecture changes
   - Identify obsolete tasks

3. **Update Documents**
   - Preserve all completed tasks (checked items)
   - Regenerate incomplete tasks if requirements changed
   - Update dependency metadata if affected
   - Add new phases/tasks as needed
   - Remove obsolete uncompleted tasks

4. **Update Context**
   - Refresh `CLAUDE.md` if conventions changed

## Input Requirements

### Required Files

| File                          | Purpose                                    |
| ----------------------------- | ------------------------------------------ |
| `docs/prd.md`                 | Project requirements and evaluation criteria |
| `docs/architecture.md`        | System architecture with background workers  |
| `docs/domain.md`              | C-PACE lead qualification domain knowledge   |
| `docs/design-system.md`       | MudBlazor theme and component patterns       |
| `docs/screens.md`             | UI wireframes and component composition      |
| `docs/ai-prompt.md`           | Claude/OpenAI evaluation system prompt       |
| `docs/railway-sqlite-setup.md`| Deployment and database configuration        |

### Optional Files (for refresh)

| File            | Purpose                      |
| --------------- | ---------------------------- |
| `docs/plan.md`  | Existing plan to update      |
| `docs/tasks.md` | Existing tasks with progress |

## Output Files

### docs/plan.md

**Location:** docs/ folder
**Purpose:** Technical approach bridging requirements to implementation

Key sections:

- Overview and architecture summary
- Task ordering philosophy
- Milestone progression table
- Implementation phases with dependencies
- Dependency graph (ASCII diagram)
- Parallel work opportunities
- Critical path
- MVP boundary definition
- External dependencies
- Documentation reference map
- Open questions

### docs/tasks.md

**Location:** docs/ folder
**Purpose:** Granular, executable task list with checkboxes

Key sections:

- Task ordering philosophy
- Dependency legend
- Progress summary by phase
- Milestone markers table
- Phase-grouped tasks with:
  - `deps:` - Dependencies
  - `parallel:` - Concurrent tasks
  - `docs:` - Documentation references
  - Files and verification steps
- Concurrency guide
- Task log for tracking

### CLAUDE.md

**Location:** Project root
**Purpose:** Persistent context for all Claude Code sessions

Key sections:

- Project overview
- Tech stack
- Project structure
- Commands and conventions
- Session protocol

## Task Format Requirements

### Every Task Must Include

```markdown
- [ ] {N.N.N}: {Action verb} {what} {context}
  - deps: {comma-separated task IDs or 'none'}
  - parallel: {tasks that can run alongside} (optional)
  - docs: {doc-file.md#section} (when relevant)
  - Files: {comma-separated file paths}
  - Test: {how to verify completion}
```

### Documentation Reference Rules

**Always include `docs:` for tasks involving:**

| Task Type | Required Documentation |
|-----------|----------------------|
| UI components | `screens.md#component`, `design-system.md#pattern` |
| Database schema | `architecture.md#database-schema` |
| API endpoints | `architecture.md#api-endpoints` |
| Background workers | `architecture.md#background-workers` |
| AI evaluation | `ai-prompt.md` |
| State eligibility | `domain.md#state-eligibility` |
| Deployment | `railway-sqlite-setup.md` |

## Task Granularity Guidelines

### Good Task Size (10-15 minutes)

- "Create Contact entity with EF Core configuration"
- "Add dashboard API endpoint"
- "Implement QualificationChip Blazor component"
- "Write unit tests for StateEligibilityService"

### Too Large (break down further)

- "Implement the lead evaluation system"
- "Build the dashboard"
- "Set up the database"

### Too Small (combine with related work)

- "Add a single using statement"
- "Fix a typo"
- "Change a variable name"

## Phase Structure

### Phase 0: Project Foundation (Always First)

Every plan starts with Phase 0 covering:

- .NET project initialization
- EF Core and SQLite configuration
- Folder structure creation
- Basic build verification
- **Milestone: M1 - First Build**

### Subsequent Phases

Align with architecture components:

- Phase 1: Database layer and entities → **M2 - Data Layer**
- Phase 2: PLG API integration → **M3 - External Data**
- Phase 3: Background workers (sync + evaluation)
- Phase 4: AI evaluation service
- Phase 5: Blazor UI pages and components → **M4 - First Lead Visible**, **M5 - MVP Complete**
- Phase 6: Deployment configuration → **M6 - Deployed**

### Milestone Requirements

Each milestone represents **functional progress**:

| Milestone | Criteria |
|-----------|----------|
| M1 | Project builds and runs |
| M2 | Database operational with entities |
| M3 | Can fetch from external API |
| M4 | User can see real data on screen |
| M5 | All core features functional |
| M6 | Live in production |

### MVP Boundary

Always explicitly mark:

- Which phases are MVP
- Which are post-MVP
- Concrete acceptance criteria for MVP completion (from PRD)

## Dependency Graph Requirements

### Phase-Level Dependencies

Include ASCII diagram showing:
- Which phases block others
- Parallel paths through the plan
- Early-start opportunities

### Task-Level Dependencies

Every task must specify:
- `deps: none` - Can start immediately
- `deps: 1.2.3` - Single dependency
- `deps: 1.2.3, 1.2.4` - Multiple dependencies
- `parallel: 1.2.3, 1.2.4` - Can work concurrently

## Constraints

1. **No Code Writing** - This skill generates plans only, not implementation
2. **Task Time Limit** - Each task should be completable in 10-15 minutes
3. **File References** - Tasks must reference affected files when known
4. **Doc References** - Tasks must reference relevant documentation
5. **Dependency Metadata** - Every task must have `deps:` field
6. **Milestone Markers** - Key tasks must have milestone markers
7. **Sequential Within Phase** - Tasks within a phase should be sequential by default
8. **Phase Dependencies** - Later phases can depend on earlier ones

## Integration with /execute

The tasks generated by `/plan` are designed to be executed with the `/execute` skill:

- Task numbering enables precise targeting (e.g., `/execute 0.1.1`)
- Phase checkpoints provide natural stopping points
- File references guide implementation
- Doc references enable quick context lookup
- Dependency metadata enables parallel execution
- Verification steps confirm completion

## Templates

Use these templates when generating output:

- Plan structure: `PLAN-TEMPLATE.md`
- Tasks structure: `TASKS-TEMPLATE.md`
- CLAUDE.md structure: `CLAUDE-TEMPLATE.md`
