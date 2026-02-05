---
name: plan-parallel-dev
description: Skill for creating parallel development plans with multiple developers. Leverages git worktree for branch strategy, task dependency analysis, critical path calculation, developer role assignment, and timeline creation. Use for requests like "create a parallel development plan", "I want to develop with multiple people simultaneously", "divide work with worktree", or "maximize development parallelization". Also supports on-demand parallel tasks for quick fixes with requests like "fix XX in parallel", "do YY with worktree", or "add parallel task".
---

# Parallel Development Planning

Create implementation plans to maximize parallelization of feature development with multiple developers.
Also supports on-demand parallel tasks (bug fixes, feature additions) for completed projects.

## Usage Modes

This skill has two modes:

### Mode A: Initial Parallel Development (Planning Mode)

Used immediately after project initialization (right after `uv init`, `create-react-app`, etc.) when developing multiple features in parallel.

**Trigger Phrases**:

- "Create a parallel development plan"
- "I want to develop with multiple people simultaneously"
- "Divide work with worktree"
- "Maximize development parallelization"

**Workflow**: 9-step workflow (described below) to create a plan and start multiple tasks simultaneously.

### Mode B: Maintenance Parallel Development (Quick Task Mode)

Used for bug fixes and feature additions to projects with existing implementations. Start work immediately without a plan document.

**Trigger Phrases**:

- "Fix XX in parallel"
- "Handle XX in parallel"
- "Do YY with worktree"
- "Add parallel task: XX"
- "Do this with worktree: XX"

**Workflow**: See "Quick Task Workflow" section for details.

### Mode Selection Guide

| Situation                                       | Recommended Mode                           |
| ----------------------------------------------- | ------------------------------------------ |
| Right after project initialization, parallel features | A                                          |
| Single bug fix to existing project              | B (single task)                            |
| Medium-scale feature addition to existing project | B (multiple tasks + merge coordinator)     |

---

## Workflow (Mode A: Initial Parallel Development)

```
1. Understand Requirements
   └─→ Collect list of features to develop
   └─→ Confirm tech stack (BE/FE/Infrastructure, etc.)

2. Task Decomposition
   └─→ Split each feature into independent tasks
   └─→ Granularity: whichever is smaller
       ├─→ 0.5-2 days in human time
       ├─→ Within 20 files changed
       └─→ Independently testable feature unit
   └─→ ⚠️ UI specs require human approval (see below)

3. Dependency Analysis
   └─→ Identify blocking relationships between tasks
   └─→ Calculate critical path

4. Determine Parallelism
   └─→ Calculate number of Claude instances needed
   └─→ Assignment to minimize wait time

5. Branch Strategy
   └─→ Design integration branch
   └─→ Feature branch naming convention
   └─→ Determine merge order

6. Create Timeline
   └─→ Gantt-style parallel schedule

7. Create Plan and Instruction Documents
   └─→ Communicate plan content to user (present execution order, parallelism, and task content in table format)
   └─→ Create files in .parallel-dev/
       ├─→ PLAN.md (plan document)
       ├─→ README.md (overall overview and progress management)
       ├─→ merge-coordinator.md (for merge coordinator)
       ├─→ tasks/*.md (for each task)
       ├─→ signals/ (completion notification directory)
       └─→ issues/ (issue report directory)

8. Environment Setup
   └─→ Create integration branch and push to remote
   └─→ Create worktree for each task
   └─→ Install dependencies in each worktree
   └─→ Copy .env in each worktree

9. Launch merge coordinator Claude in tmux new-window
   └─→ Create new window with tmux new-window -n "coordinator" and launch claude
   └─→ Pass initial instructions to merge coordinator
```

## Quick Task Workflow (Mode B: Quick Task)

Mode for immediately starting bug fixes or feature additions to existing projects without a plan document.

**Features**:

- Start immediately without plan document
- Support multiple concurrent sessions with session files (`.parallel-dev/quick-session-{timestamp}.md`)
- Merge directly to main

→ **See [references/quick-mode-guide.md](references/quick-mode-guide.md) for details**

---

## Terminology

To avoid confusion, unify the following terms:

| Term              | Description                               | Example                                |
| ----------------- | ----------------------------------------- | -------------------------------------- |
| **Task Name**     | Identical to branch name. Work unit ID    | `skill-files-api`, `recommendation-ui` |
| **Person/Role**   | Worker identifier. Tech area + number     | `BE-1`, `FE-1`, `INFRA-1`              |
| **Integration Branch** | Target branch to merge all tasks     | `feature/multi-file-skills`            |

**Important**: Use **task name (branch name)** for completion reports and state management. Person name alone cannot identify the task when handling multiple tasks.

## Task Decomposition Rules

Task splitting principles:

1. **Single Responsibility**: 1 task = 1 feature/1 component
2. **Appropriate Granularity**: whichever is smaller
   - 0.5-2 days in human time
   - Within 20 files changed
   - Independently testable feature unit
3. **Clear Deliverables**: Each task has concrete deliverables like API/component/file
4. **Testable**: Unit that can be independently tested and reviewed
5. **Minimize Conflicts**: Minimize file edit overlaps, consolidate common file changes (routing, type definitions, etc.) into one task

Branch naming:

```
feature/recommendation-api  # Feature name based
feature/notification-api
feature/project-card-enhance
```

Role (person) naming:

```
BE-1, BE-2, ...    # Backend
FE-1, FE-2, ...    # Frontend
INFRA-1, ...       # Infrastructure
```

## Dependency Analysis

Dependency types:

| Dependency Type | Symbol | Description           |
| --------------- | ------ | --------------------- |
| Blocking        | `→`    | Must complete         |
| Parallel        | `//`   | Can proceed independently |
| Waiting for integration | `↓` | Start after merge |

Critical path calculation:

```
Longest path = max(total effort of each path)
Optimal number of people = ceil(total effort / critical path)
```

Create dependency matrix:

```
         BE-01  BE-02  FE-01  FE-02
BE-01      -      //     ↓      //
BE-02     //       -     //      ↓
FE-01    Wait     //      -      //
FE-02     //     Wait    //       -
```

## Developer Role Assignment

Role definition template:

| Role | Assigned Branch | Required Skills   |
| ---- | --------------- | ----------------- |
| BE-1 | feature/xxx-api | Python, FastAPI   |
| FE-1 | feature/xxx-ui  | React, TypeScript |

Principles for minimizing wait time:

1. Assign dependent tasks to the dependency source worker
2. Fill wait time with independent tasks
3. Utilize idle time for review and support

## Branch Strategy with Worktree

Git worktree basics for parallel development:

```
main
└── feature/integration (integration branch)
    ├── feature/xxx-api     → worktree/xxx-api/
    ├── feature/yyy-api     → worktree/yyy-api/
    └── feature/xxx-ui      → worktree/xxx-ui/
```

→ **See [references/worktree-guide.md](references/worktree-guide.md) for details**

## Agent Instruction Files

For parallel development with Claude, place instruction documents for each Claude in `.parallel-dev/`.

**Directory Structure**:

| Directory/File                       | Purpose                  |
| ------------------------------------ | ------------------------ |
| `.parallel-dev/`                     | Parallel dev management (git-managed) |
| `.parallel-dev/PLAN.md`              | Plan document            |
| `.parallel-dev/merge-coordinator.md` | For merge coordinator    |
| `.parallel-dev/tasks/*.md`           | Instruction docs per task |
| `.parallel-dev-signals/`             | Completion notifications (.gitignore) |
| `.parallel-dev-issues/`              | Issue reports (.gitignore) |

**Templates**:

- [references/templates/parallel-dev-readme.md](references/templates/parallel-dev-readme.md)
- [references/templates/merge-coordinator.md](references/templates/merge-coordinator.md)
- [references/templates/task-instruction.md](references/templates/task-instruction.md)

## Task Completion Flow

**Role Division**:

- **Worker Claude**: Code implementation → Create `.done` file (don't commit)
- **Merge Coordinator**: Commit → Test → Merge → Push

**Design Philosophy**: Worker Claude focuses on writing code. Only merge coordinator manages merge order.

→ **See [references/worktree-guide.md](references/worktree-guide.md) for details**

## Rules (Common to all Claude)

### Worker Claude Rules

- **Don't commit**: Just write code. Merge coordinator does commits
- **Don't push**: Merge coordinator handles remote pushes
- **Report completion with .done file**: Describe implementation and changed files
- **UI specs require human approval**: Submit confirmation request to issues/, implement after approval

### Merge Coordinator Rules

- **Launch worker Claude with `tmux new-window -n "{task-name}"`** (don't use Task tool)
- **Always pass initial instructions as argument when launching claude**:
  ```bash
  tmux new-window -n "{task-name}" "cd worktree/{task-name} && PROJECT_ROOT=$PROJECT_ROOT claude 'Please read ../../.parallel-dev/tasks/{task-name}.md and implement. Create \$PROJECT_ROOT/.parallel-dev-signals/{task-name}.done when complete (create in parent project, not in worktree).'"
  ```
- **Terminate worker Claude after successful merge**: `tmux send-keys -t "{task-name}" C-c C-c`
- **Always merge with `--no-ff`**
- **Conflict resolution**: Merge coordinator resolves (don't delegate to worker Claude)

### Dependency Rules

- Don't launch dependent tasks until dependency tasks are **merged into integration branch**

→ **See [references/worktree-guide.md](references/worktree-guide.md) for details**

## Additional Guides

- [references/worktree-guide.md](references/worktree-guide.md) - Worktree operations, workflows, detailed rules
- [references/quick-mode-guide.md](references/quick-mode-guide.md) - Quick task mode operations
- [references/testing-guide.md](references/testing-guide.md) - Testing policy (production-equivalent tests, E2E visual checks)
- [references/ui-approval-guide.md](references/ui-approval-guide.md) - Human approval flow for UI specs
- [references/advanced-features.md](references/advanced-features.md) - Phase separation, timeline visualization, plan templates
