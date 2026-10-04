---
name: spec-create
description: >
  Create a structured feature specification with self-contained task files organized into
  parallel execution batches. Use this skill when the user says "create a spec", "plan this feature",
  "write up an implementation plan", "break this into tasks", or after any planning conversation
  where the user wants to capture decisions as actionable spec files. Also use when the user
  says "/spec-create" (or their host's equivalent invocation syntax) or wants to decompose a
  feature into work items that agents can implement independently. This skill produces local
  spec files under specs/{feature}/ — no GitHub integration.
license: MIT
---

# Create Feature Specification

Transform a planning conversation into a structured spec folder that enables parallel agent implementation. The spec breaks a feature into self-contained task files — each one detailed enough that a coder agent can pick it up cold and implement it without reading anything else.

The key insight: implementation plans that live in a single file are either too large for a context window or too shallow for independent execution. By splitting into one file per task with full context in each, we enable multiple agents to work in parallel while keeping each agent's context focused.

## When to Use

- After a planning conversation where requirements and technical details have been discussed
- When the user asks to create a spec, plan a feature, or break work into tasks
- When the user wants to prepare work for parallel agent implementation

## Instructions

### Step 1: Gather Requirements

If the conversation already contains planning context (requirements discussed, technical decisions made, architecture outlined), extract all of it. Review the entire conversation to ensure nothing is lost — the spec is the single source of truth, and anything not captured here disappears.

If no planning conversation exists, interview the user:
- What does this feature do and why does it matter?
- What are the acceptance criteria?
- What technical constraints or decisions have been made?
- What files, APIs, schemas, or patterns are involved?

### Step 2: Name the Feature

Choose a kebab-case name that clearly identifies the feature (e.g., `add-user-auth`, `migrate-to-postgres`, `dashboard-redesign`). This becomes the folder name under `specs/`.

### Step 3: Decompose into Tasks

Break the implementation into atomic tasks. Each task should:
- Be completable in a single coding session by one agent
- Have a clear, specific scope (one concern per task)
- Produce working, testable code when complete
- Not overlap in files modified with other tasks in the same batch

Think carefully about granularity. Too coarse and agents can't work in parallel. Too fine and the overhead of context-switching between tasks dominates. A good task typically creates or modifies 1-5 files around a single concern.

Do NOT include testing tasks (unit tests, e2e tests) unless the user explicitly asks for them.

### Step 4: Build the Dependency Graph

For each task, identify:
- **What it depends on**: which tasks must complete before this one can start
- **What depends on it**: which tasks are blocked until this one finishes

Tasks with no dependencies form Batch 1. Tasks whose dependencies are all in Batch 1 form Batch 2. And so on. All tasks within a batch can execute in parallel.

When assigning batches, verify that tasks within the same batch do not modify overlapping files. If two tasks in the same batch would touch the same file, move one to a later batch — parallel agents on the same branch cannot safely modify the same file.

### Step 5: Create the Spec Folder

Create the following structure at `specs/{feature-name}/`:

```
specs/{feature-name}/
├── README.md
├── requirements.md
├── action-required.md
└── tasks/
    ├── task-01-{name}.md
    ├── task-02-{name}.md
    └── ...
```

Read the templates in `references/` before writing each file:
- `references/readme-template.md` — for the README (dependency graph, batch table, status tracking)
- `references/task-template.md` — for each task file (self-contained with all context)
- `references/requirements-template.md` — for the requirements document
- `references/action-required-template.md` — for manual human steps

Task files are numbered with zero-padded two-digit prefixes in topological order: Batch 1 tasks first, then Batch 2, etc. Within a batch, order is arbitrary but stable.

### Step 6: Write Self-Contained Task Files

This is the most important step. Each task file is the **only thing** a coder agent will read before implementing. It must contain everything the agent needs:

- **Description**: what to build and why it matters in context
- **Dependency context**: what prior tasks produce that this task needs (summarized in prose, not just filenames). The agent should not need to read other task files.
- **Technical details**: CLI commands, code snippets, schemas, file paths, env vars, API endpoints — every implementation-specific detail from the planning conversation
- **Files to create/modify**: explicit list with purpose for each
- **Acceptance criteria**: specific, verifiable conditions

Review each task file with fresh eyes: could an agent who has never seen the planning conversation implement this correctly using only this file? If not, add what's missing.

### Step 7: Extract Manual Actions

Identify any steps that require human action (account creation, API key setup, DNS configuration, environment variables, third-party service registration, etc.). Write these to `action-required.md` grouped by timing (Before/During/After implementation). If none exist, note "No manual steps required."

### Step 8: Report to User

After creating the spec, display:

```
Feature specification created at specs/{feature-name}/

Files created:
- README.md (dependency graph, {N} batches, {T} tasks)
- requirements.md
- action-required.md
- tasks/ ({T} task files)

Batch breakdown:
- Batch 1: {count} tasks (parallel) — {brief description}
- Batch 2: {count} tasks (parallel) — {brief description}
- ...

Next steps:
1. Review action-required.md for tasks you need to complete manually
2. Review the requirements and task files
3. Use /spec-implement to start parallel implementation
```

## Critical Rules

- Every task file must be fully self-contained — this is the entire point of the spec structure. A coder agent reading only that file must know exactly what to do.
- Capture ALL technical details from the planning conversation. The spec is the single source of truth — CLI commands, schemas, code snippets, file paths, env vars, API endpoints. Anything not captured here is lost.
- Tasks within the same batch must not modify overlapping files. Parallel agents on the same branch cannot safely touch the same files.
- Keep tasks atomic — one concern per task. If a task has more than 5-7 files to modify, consider splitting it.
- Do not create testing tasks unless the user explicitly asks for them.
- Number task files in topological order (batch 1 first, then batch 2, etc.) for easy scanning.
