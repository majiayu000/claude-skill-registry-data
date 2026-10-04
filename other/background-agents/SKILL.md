---
name: background-agents
description: |
  This skill should be used when the user asks about "parallel agents", "background
  tasks", "run_in_background", "non-blocking agents", "check agent progress",
  "TaskOutput", "retrieve agent results", or discusses running multiple agents
  concurrently. Covers patterns for launching agents in background, monitoring
  progress, and retrieving results.
version: 1.0.0
---

# Background Agents - Non-Blocking Parallel Execution

Background agents let you continue working while long-running tasks execute.
Use `run_in_background: true` to launch agents that run without blocking.

## When to Use Background Agents

- Research phases with multiple independent agents
- Pre-commit reviews (code-simplifier + kieran reviewer)
- Any Task that takes >30 seconds and doesn't gate your immediate next step

## Launching Background Agents

Add `run_in_background: true` to Task calls:

```
Task(
  subagent_type="compound-engineering:review:kieran-typescript-reviewer",
  prompt="Review the changes in this PR",
  max_turns: 20,
  run_in_background: true
)
```

### Parallel Launch Pattern

Launch multiple agents in ONE message for true parallelism:

```
# Single message with multiple Task calls
Task 1: subagent_type="pr-review-toolkit:code-simplifier" (max_turns: 15, run_in_background: true)
Task 2: subagent_type="compound-engineering:review:kieran-typescript-reviewer" (max_turns: 20, run_in_background: true)
```

## Monitoring Progress

### Check All Tasks

- `/tasks` - List all background tasks with status
- `Ctrl+T` - Toggle task list view in terminal

### Check Specific Task

```
TaskOutput(task_id="task-abc123", block=false)
```

Returns current output without waiting for completion.

## Retrieving Results

### Wait for Completion

```
TaskOutput(task_id="task-abc123", block=true)
```

Blocks until agent completes, returns full output.

### Read Output File

Background agents write to output files. The path is returned when you launch:

```
Task returned: { task_id: "abc123", output_file: "/path/to/output.txt" }
```

Use `Read` tool on output_file path to check progress or results.

## Common Patterns

### Pre-Commit Reviews

```
# Launch both reviewers in parallel
Task(subagent_type="pr-review-toolkit:code-simplifier", run_in_background: true)
Task(subagent_type="compound-engineering:review:kieran-typescript-reviewer", run_in_background: true)

# Continue polishing code while they run...

# Check progress
/tasks

# Retrieve results when ready
TaskOutput(task_id="...", block=true)
```

### Research Phase

```
# Launch all research agents
Task(subagent_type="somto-dev-toolkit:prd-codebase-researcher", run_in_background: true)
Task(subagent_type="compound-engineering:research:git-history-analyzer", run_in_background: true)
Task(subagent_type="somto-dev-toolkit:prd-external-researcher", run_in_background: true)

# Continue interview prep while research runs...

# Retrieve all results
TaskOutput(task_id="task-1", block=true)
TaskOutput(task_id="task-2", block=true)
TaskOutput(task_id="task-3", block=true)
```

## When NOT to Background

- **Complexity estimator** (Phase 5.5) - Need result immediately for next phase
- **Any agent whose output gates the next step** - Must wait for result
- **Quick agents** (<10 seconds) - Overhead not worth it

## Kieran Reviewers by Language

| Language | Agent |
|----------|-------|
| TypeScript/JavaScript | `compound-engineering:review:kieran-typescript-reviewer` |
| Python | `compound-engineering:review:kieran-python-reviewer` |
| Ruby/Rails | `compound-engineering:review:kieran-rails-reviewer` |

### Domain-Specific Reviewers

| Domain | Agent |
|--------|-------|
| Database/migrations | `compound-engineering:review:data-integrity-guardian` |
| Frontend races | `compound-engineering:review:julik-frontend-races-reviewer` |
