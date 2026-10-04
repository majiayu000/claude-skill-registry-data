---
name: task-history
description: Reads and displays task execution history from crew-history.json with filtering by type, agent, cost, and configurable limits.
---

# Task History - Execution History Viewer

Displays past task executions with filtering and cost analysis.

## When to Activate

- User runs `/crew history [flags]`

## Prerequisites

- `.claude/crew-history.json` must exist (created after first task execution)
- If missing: display "No history yet. Run /crew task to start."

## Process

### Step 1: Read History

Read `.claude/crew-history.json` — this is a JSON array of task entries (see execution-orchestrator for schema).

### Step 2: Apply Filters

| Flag | Filter Logic |
|------|-------------|
| `--type <type>` | Keep only entries where `type` matches (bug-fix, feature, refactor, docs, test, security, devops, review, performance) |
| `--agent <name>` | Keep only entries where `agents[]` contains an agent with matching `name` |
| `--limit <n>` | Show last N entries (default: 10) |

Filters stack: `--type bug-fix --agent debugger` shows bug-fixes that involved the debugger.

### Step 3: Display Results

**Display format**:
```
Task History ({count} tasks shown, {total} total):

  # | Timestamp           | Type       | Complexity | Agents                    | Mode    | Status
  1 | 2026-04-04 12:00   | bug-fix    | moderate   | debugger, senior-dev      | full    | SUCCESS
  2 | 2026-04-04 11:30   | docs       | trivial    | doc-writer                | lite    | SUCCESS
  3 | 2026-04-04 10:15   | feature    | complex    | vp-eng, senior-dev, test  | full    | SUCCESS
```

### Step 4: Summary Stats

After the table, show:
```
{count} tasks | Top: {type}({n}), {agent}({n}) | {percent}% success
```
