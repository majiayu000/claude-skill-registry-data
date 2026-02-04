---
name: discovery-tree-workflow
description: Use when planning and tracking work - creates visible, emergent work breakdown using TypeScript API with just-in-time planning and hierarchical task trees
---

# Discovery Tree Workflow

## Overview

Discovery Trees make work visible through hierarchical task breakdown that emerges just-in-time. Track work programmatically with the TypeScript API, grow the tree as you discover new requirements, maintain focus by capturing distractions.

**Core principle:** Start minimal, plan just-in-time, grow through discovery, make status visible.

**Announce at start:** "I'm using the Discovery Tree workflow to track this work."

## When to Use

**Always use when:**
- Starting any non-trivial work (more than a single simple task)
- Planning features, bugs, or investigations
- Working with multiple related tasks
- Need to make progress visible
- Want to capture emergent work without losing focus

**Instead of:**
- TodoWrite for tracking progress
- Upfront detailed planning
- Hidden mental task lists
- Linear task lists that don't show relationships

## Core Philosophy

### Just-in-Time Planning
- Start with minimal detail (one task describing user value)
- Have short conversations (2-10 minutes) to break down next steps
- Don't plan everything upfront - plan what you need now
- Delays planning until the last responsible moment

### Emergent Work
- New requirements discovered during work → add to tree
- Unexpected complexity → break down further
- Distractions or ideas → capture as tasks, mark low priority
- Tree grows organically as understanding deepens

### Visual Status
- Color by status (open, in_progress, closed, blocked)
- Progress visible at a glance
- No context needed to see what's done, active, remaining
- Bottom-up view shows full context for any task

## The Discovery Tree Workflow

**API Location**: This skill includes a ready-to-use TypeScript API in `src/discovery-tree.ts` - a unified entry point that consolidates database operations and Shortcut integration.

**TypeScript Execution**: All code examples use top-level await (no async wrapper needed). Single-line imports only.

### 1. Set Workspace and Create Root Epic

Every Discovery Tree starts with setting workspace context, then creating an epic (container) and root task (actual work):

```typescript
// Import from discovery-tree-workflow skill's src directory
// IMPORTANT: Use single-line imports only
import {
  setWorkspace,
  createTask,
  addDependency,
  updateTask,
  closeTask,
  findReadyTasks,
  getEpicStatus,
  drawTree
} from '~/.claude/skills/discovery-tree-workflow/src/discovery-tree.js';

// Set workspace context
await setWorkspace({ workspacePath: '/path/to/project' });

// Create epic (container for all work)
const epic = await createTask({
  title: "Feature: User Authentication",
  type: "epic",
  priority: 1
});

// Create root task (describes the user value)
const rootTask = await createTask({
  title: "User Authentication [root]",
  type: "task",
  priority: 1
});

// Link root task to epic
await addDependency({
  taskId: rootTask.id,
  dependsOnId: epic.id,
  type: "parent-child"
});
```

**Why both epic and root task?**
- Epic: Container that tracks overall completion
- Root task: Actual work item that can have subtasks

### 2. Initial Breakdown

Have a quick conversation (2-10 minutes) to identify first level of work:

**Questions to ask:**
- "What are the main pieces of this?"
- "What do we need to understand first?"
- "What can we start with minimal detail?"

**Create tasks for what you discover:**

```typescript
// Create main tasks
const task1 = await createTask({
  title: "API endpoint for login",
  type: "task",
  priority: 1
});

const task2 = await createTask({
  title: "Password validation logic",
  type: "task",
  priority: 1
});

const task3 = await createTask({
  title: "Session management",
  type: "task",
  priority: 1
});

// Link them to root task
await addDependency({
  taskId: task1.id,
  dependsOnId: rootTask.id,
  type: "parent-child"
});

await addDependency({
  taskId: task2.id,
  dependsOnId: rootTask.id,
  type: "parent-child"
});

await addDependency({
  taskId: task3.id,
  dependsOnId: rootTask.id,
  type: "parent-child"
});
```

**Don't over-plan:** Stop when you have enough to start. More detail emerges as you work.

### 3. Start Working

Pick a task and claim it:

```typescript
// Find what's ready to work on
const readyTasks = await findReadyTasks({ limit: 10 });

// Claim the first ready task
await updateTask({
  taskId: readyTasks[0].id,
  status: "in_progress"
});
```

**As you work:**
- Discover subtasks needed? Create and link them
- Find blocking issues? Create with `blocked` status
- Get distracted by ideas? Create low-priority task to bookmark

```typescript
// Discovered more work
const subtask = await createTask({
  title: "Validate email format",
  type: "task",
  priority: 1
});

await addDependency({
  taskId: subtask.id,
  dependsOnId: task1.id,
  type: "parent-child"
});

// Found blocker
const blocker = await createTask({
  title: "Database schema needs user table",
  type: "task",
  priority: 0
});

await updateTask({
  taskId: task1.id,
  status: "blocked"
});
```

### 4. Complete and Continue

When task is done:

```typescript
await closeTask({
  taskId: task1.id,
  reason: "Completed"
});

// Update parent with what was accomplished
await updateTask({
  taskId: rootTask.id,
  notes: "Completed: API endpoint for login. Previously: Initial setup"
});
```

**IMPORTANT:** Update parent task with what was accomplished to keep context accurate as subtasks complete.

Check progress:

```typescript
const status = await getEpicStatus({ epicId: epic.id });
console.log(`Progress: ${status.completionPercentage}%`);
console.log(`${status.completedTasks}/${status.totalTasks} tasks complete`);

// See what's ready to work on next
const nextReady = await findReadyTasks({ limit: 5 });
```

**If more work remains:** Claim next task, repeat cycle

**If work emerges:** Add to tree, keep going

**If blocked:** Mark blocked, work on unblocked tasks

### 5. View Progress

```typescript
// Bottom-up view from any task (current → parent → grandparent → root)
const tree = await getDependencyTree({ taskId: currentTask.id });

// Visual tree (top-down view from epic)
const visualTree = await drawTree({ taskId: epic.id });
console.log(visualTree); // Display to user

// Epic completion stats
const epicStatus = await getEpicStatus({ epicId: epic.id });
```

## Integration with Skills

### With TDD
1. Create task for feature
2. TDD cycle: RED → GREEN → REFACTOR
3. If new test reveals complexity → create subtask
4. Close task when all tests pass

### With Example-Driven Design
1. Create task for user story
2. EXAMPLE phase discovers API shape → might create subtasks
3. Each phase completion → progress visible in tree
4. CHECK phase → close task or create next example task

### With Mikado Method
1. Discover prerequisite → create task with `discovered-from` dependency
2. Each prerequisite becomes subtask
3. Work on leaf tasks (no dependencies)
4. Close prerequisites, return to parent

## Quick Reference

| Action | API Function |
|--------|--------------|
| Set workspace | `setWorkspace({ workspacePath })` |
| Create epic | `createTask({ title, type: "epic", priority: 1 })` |
| Create task | `createTask({ title, type: "task", priority })` |
| Link to parent | `addDependency({ taskId, dependsOnId, type: "parent-child" })` |
| Claim task | `updateTask({ taskId, status: "in_progress" })` |
| Complete task | `closeTask({ taskId, reason })` |
| Update task | `updateTask({ taskId, notes, description, title })` |
| View tree | `getDependencyTree({ taskId })` |
| Draw visual tree | `drawTree({ taskId })` |
| Check progress | `getEpicStatus({ epicId })` |
| Find ready work | `findReadyTasks({ limit })` |
| Mark blocked | `updateTask({ taskId, status: "blocked" })` |
| Show task details | `showTask({ taskId })` |
| Append notes | `appendNotes({ taskId, notes })` |

## Common Patterns

### Capture Distractions

```typescript
// Something came up while working
const distraction = await createTask({
  title: "Refactor utils.ts for clarity",
  type: "task",
  priority: 3
});

await addDependency({
  taskId: distraction.id,
  dependsOnId: currentParent.id,
  type: "parent-child"
});
// Now it's captured, back to current work
```

### Break Down Complex Task

```typescript
// Realized task is bigger than expected
const subtask1 = await createTask({
  title: "Part 1: Schema validation",
  type: "task",
  priority: 1
});

const subtask2 = await createTask({
  title: "Part 2: Error handling",
  type: "task",
  priority: 1
});

await addDependency({
  taskId: subtask1.id,
  dependsOnId: complexTask.id,
  type: "parent-child"
});

await addDependency({
  taskId: subtask2.id,
  dependsOnId: complexTask.id,
  type: "parent-child"
});

// Parent stays open until children done
await updateTask({
  taskId: complexTask.id,
  status: "open"
});
```

### Handle Discovered Prerequisites

```typescript
// Found something that must be done first
const prerequisite = await createTask({
  title: "Add user_id column to sessions table",
  type: "task",
  priority: 0
});

await addDependency({
  taskId: currentTask.id,
  dependsOnId: prerequisite.id,
  type: "blocks"
});

await updateTask({
  taskId: currentTask.id,
  status: "blocked"
});

await updateTask({
  taskId: prerequisite.id,
  status: "in_progress"
});
```

### Restructure Tree Based on New Learnings

```typescript
// When requirements change and tree needs reorganizing
await setWorkspace({ workspacePath });

// Create new epic/structure
const newEpic = await createTask({
  title: "Revised Approach",
  type: "epic",
  priority: 1
});

// Create tasks programmatically
const tasks = await Promise.all([
  createTask({ title: "New component A", type: "task", priority: 1 }),
  createTask({ title: "New component B", type: "task", priority: 1 }),
  createTask({ title: "Integration layer", type: "task", priority: 2 })
]);

// Link all at once
for (const task of tasks) {
  await addDependency({
    taskId: task.id,
    dependsOnId: newEpic.id,
    type: "parent-child"
  });
}

// Close obsolete tasks
await closeTask({
  taskId: oldTask.id,
  reason: "Superseded by revised approach"
});
```

## API Types

```typescript
type TaskType = "bug" | "feature" | "task" | "epic" | "chore";
type TaskStatus = "open" | "in_progress" | "blocked" | "closed";
type DependencyType = "parent-child" | "blocks" | "related" | "discovered-from";

interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: number;
  taskType: TaskType;
  createdAt: string;
  updatedAt: string;
}

interface EpicStatus {
  epicId: string;
  totalTasks: number;
  completedTasks: number;
  inProgressTasks: number;
  blockedTasks: number;
  openTasks: number;
  completionPercentage: number;
}
```

## Red Flags

**STOP if you catch yourself:**
- Planning all details upfront before starting work
- Using TodoWrite instead of discovery trees for multi-step work
- Keeping task breakdown in your head instead of API
- Not capturing emerged work because "it's small"
- Marking tasks complete without using `closeTask()`
- Closing subtasks without updating parent task with what was done
- Forgetting to check `findReadyTasks()` when looking for next work
- Creating flat task lists instead of hierarchical trees

**All of these mean: Use Discovery Trees with the TypeScript API for visible, emergent planning.**

## Why This Works

**Just-in-time planning:**
- Short conversations vs hours of upfront meetings
- Plan what you need now, defer rest
- Less waste from planning things that change

**Emergent structure:**
- Tree grows as understanding deepens
- Captures reality of software development (new discoveries)
- Makes unexpected work visible, not hidden

**Visual progress:**
- Anyone can see status without asking
- Bottom-up tree shows full context
- Epic progress shows completion percentage

**Focus maintenance:**
- Distractions captured as low-priority tasks
- Current work stays visible
- Easy to return to main path
