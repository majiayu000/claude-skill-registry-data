---
name: Conductor Methodology
description: This skill should be used when the user asks about "conductor methodology", "context-driven development", "conductor directory structure", "conductor files", "tracks.md", "plan.md", "spec.md", or when commands reference conductor concepts. Provides comprehensive understanding of the Conductor framework for Context-Driven Development.
version: 0.1.0
---

# Conductor Methodology

Conductor implements Context-Driven Development, a methodology that treats project context as a first-class artifact alongside code. This skill provides essential knowledge about the Conductor framework, directory structure, file formats, and core concepts.

## Core Philosophy

**Measure twice, code once.** Conductor enforces a strict workflow:

1. **Context**: Establish project-level context once (product vision, tech stack, workflow)
2. **Spec & Plan**: Create detailed specifications and hierarchical plans for each unit of work
3. **Implement**: Follow the plan, update status, verify at phase boundaries

This approach ensures AI agents follow consistent, high-quality development practices with proper planning and context awareness.

## Directory Structure

When Conductor is active in a project, it creates and manages this structure:

```
conductor/
├── product.md              # Product vision, users, goals
├── product-guidelines.md   # Brand voice, design principles, UX guidelines
├── tech-stack.md          # Languages, frameworks, architecture, tools
├── workflow.md            # Development methodology (TDD, commits, testing)
├── code_styleguides/      # Language-specific style guides
│   ├── general.md
│   ├── javascript.md
│   ├── typescript.md
│   ├── python.md
│   ├── go.md
│   └── html-css.md
├── tracks.md              # Master list of all tracks
└── tracks/
    └── <track_id>/
        ├── metadata.json  # Track metadata (ID, title, type, status, dates)
        ├── spec.md        # Detailed requirements and acceptance criteria
        └── plan.md        # Hierarchical implementation plan
```

## Key Concepts

### Tracks

A **track** is a logical unit of work - a feature, bug fix, or chore. Each track has:
- Unique ID (timestamp-based: `track_20231215_143022`)
- Type: feature, bug, or chore
- Status: pending, in-progress, completed, or blocked
- Dedicated directory with spec and plan

### Specifications (spec.md)

Detailed requirements document for a track, including:
- Overview and context
- Functional requirements
- Non-functional requirements (performance, security, etc.)
- Acceptance criteria (definition of done)
- Out of scope (what this does NOT include)

### Plans (plan.md)

Hierarchical implementation plan with three levels:

1. **Phases**: Major stages of work (e.g., "Backend API", "Frontend UI")
2. **Tasks**: Specific actions within phases (e.g., "Create user model")
3. **Sub-tasks**: Detailed steps within tasks (e.g., "Add email field")

Each item has a status marker:
- `[ ]` - Pending (not started)
- `[~]` - In Progress (currently working)
- `[x]` - Completed (done)
- `[!]` - Blocked (cannot proceed)

### Workflow Methodology

The `workflow.md` file defines the development process, including:
- **Development methodology**: TDD, BDD, or standard
- **Commit strategy**: Conventional commits, descriptive messages
- **Testing requirements**: Unit, integration, E2E
- **Code review**: Required, optional, pair programming
- **Phase completion protocol**: Verification steps at phase boundaries

## File Formats

### tracks.md Format

Master list of all tracks:

```markdown
# Conductor Tracks

## Active Tracks

### [ ] Track: Add user authentication
- **ID**: track_20231215_143022
- **Type**: Feature
- **Status**: In Progress
- **Created**: 2023-12-15

### [ ] Track: Fix login redirect bug
- **ID**: track_20231215_150033
- **Type**: Bug
- **Status**: Pending
- **Created**: 2023-12-15

## Completed Tracks

### [x] Track: Setup project infrastructure
- **ID**: track_20231214_120000
- **Type**: Chore
- **Status**: Completed
- **Created**: 2023-12-14
- **Completed**: 2023-12-15
```

### metadata.json Format

Track metadata in JSON:

```json
{
  "track_id": "track_20231215_143022",
  "title": "Add user authentication",
  "type": "feature",
  "status": "in-progress",
  "created_at": "2023-12-15T14:30:22Z",
  "updated_at": "2023-12-15T16:45:00Z"
}
```

### plan.md Format

Hierarchical plan with status markers:

```markdown
# Implementation Plan: Add User Authentication

## Phase 1: Backend API

### [ ] Task: Create user model
- [ ] Sub-task: Define user schema
- [ ] Sub-task: Add email and password fields
- [ ] Sub-task: Add timestamps

### [~] Task: Implement authentication endpoints
- [x] Sub-task: Create /register endpoint
- [~] Sub-task: Create /login endpoint
- [ ] Sub-task: Create /logout endpoint

### [ ] Task: Conductor - User Manual Verification 'Backend API' (Protocol in workflow.md)

## Phase 2: Frontend UI

### [ ] Task: Create login form
- [ ] Sub-task: Design form layout
- [ ] Sub-task: Add form validation
- [ ] Sub-task: Connect to API

### [ ] Task: Conductor - User Manual Verification 'Frontend UI' (Protocol in workflow.md)
```

## Project Maturity Types

### Brownfield Projects

Existing projects with code, dependencies, or version control. Conductor analyzes:
- Programming languages and frameworks
- Architecture patterns
- Project goals from README or manifests
- Existing conventions and patterns

Pre-populates context files based on analysis.

### Greenfield Projects

New projects starting from scratch. Conductor guides through:
- Defining product vision
- Selecting tech stack
- Establishing workflow
- Creating initial structure

## Context Files

### product.md

Defines product vision and goals:
- Target users and their needs
- Core features and capabilities
- Product goals and success metrics
- Constraints and assumptions

### product-guidelines.md

Establishes brand and design standards:
- Brand voice and tone
- Design principles
- UX guidelines
- Content guidelines

### tech-stack.md

Documents technical decisions:
- Programming languages
- Frontend and backend frameworks
- Database and storage
- Architecture patterns
- Development tools

### workflow.md

Defines development process:
- Methodology (TDD, BDD, standard)
- Commit conventions
- Testing strategy
- Code review process
- Phase completion verification

## Status Markers

Use consistent markers throughout plans:

| Marker | Status | Meaning |
|--------|--------|---------|
| `[ ]` | Pending | Not started |
| `[~]` | In Progress | Currently working |
| `[x]` | Completed | Done |
| `[!]` | Blocked | Cannot proceed |

## Phase Completion Verification

If workflow.md defines a "Phase Completion Verification and Checkpointing Protocol", each phase must include a final verification task:

```markdown
### [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)
```

This ensures quality gates at phase boundaries.

## Commands Overview

Conductor provides five commands:

1. **setup**: Initialize conductor environment (run once per project)
2. **newTrack**: Create new track with spec and plan
3. **implement**: Execute tasks from plan
4. **status**: Display progress overview
5. **revert**: Git-aware revert of tracks/phases/tasks

## Best Practices

### When Creating Specs

- Be specific about requirements
- Include acceptance criteria
- Define what's out of scope
- Reference product.md for context
- Consider non-functional requirements

### When Creating Plans

- Break work into phases (major stages)
- Define tasks within phases (specific actions)
- Add sub-tasks for detailed steps
- Follow workflow methodology (e.g., TDD tasks)
- Include phase completion verification tasks
- Keep tasks atomic and testable

### When Implementing

- Load all context files before starting
- Follow the plan sequentially
- Update status markers in real-time
- Commit frequently (per task or phase)
- Run automated checks at phase boundaries
- Verify completion before moving to next phase

### When Updating Context

- Keep context files synchronized with reality
- Update tech-stack.md when adding new technologies
- Update workflow.md when process changes
- Update product.md when goals evolve
- Commit context changes separately

## Integration with Git

Conductor is Git-aware:
- Tracks commits associated with tasks
- Records commit SHAs in plan.md
- Enables intelligent revert of logical units
- Handles non-linear history (rebases, squashes)

## Additional Resources

For detailed patterns and advanced techniques, consult:
- **`references/brownfield-analysis.md`** - Brownfield project analysis patterns
- **`references/plan-generation.md`** - Plan generation strategies
- **`examples/sample-track/`** - Complete example track

## Common Patterns

### Starting a New Project

1. Run `/claude-conductor:setup`
2. Answer questions about product, tech stack, workflow
3. Review generated context files
4. Create first track with `/claude-conductor:newTrack`

### Working on a Feature

1. Create track: `/claude-conductor:newTrack "Feature description"`
2. Review and approve spec
3. Review and approve plan
4. Implement: `/claude-conductor:implement`
5. Verify at phase boundaries
6. Complete track

### Checking Progress

1. Run `/claude-conductor:status`
2. Review active tracks
3. Check completion percentages
4. Identify blockers

### Reverting Work

1. Run `/claude-conductor:revert`
2. Select track/phase/task to revert
3. Review Git commits to be reverted
4. Confirm and execute

## Tips for Commands

When commands reference conductor concepts, use this skill to understand:
- File formats and structure
- Status marker meanings
- Phase completion requirements
- Context file purposes
- Track lifecycle

This knowledge enables accurate implementation of conductor workflows and proper maintenance of conductor artifacts.
