---
name: orchestrating-parallel-workers
description: Fan out tasks to parallel background agents with independent context windows. Use when work can be split into independent units that benefit from isolated execution.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Agent, TaskCreate, TaskUpdate, TaskList, Read, Write
  argument-hint: <task-list-or-description>
  context: inline
  stability: development
---

# Parallel Worker Orchestration

**Target**: $ARGUMENTS

Decomposes work into independent units and dispatches them to parallel
background agents. Each agent gets its own context window, preventing
cross-contamination between unrelated tasks.

## When to Use

- Multiple independent tasks (e.g., create 3 unrelated files, research 4 topics)
- Context-heavy work that would pollute the main session
- Parallel file creation/editing in different areas of the codebase

## When NOT to Use

- Sequential dependent tasks (output of A feeds into B)
- Single-file changes or trivial edits
- Tasks requiring shared mutable state between workers
- Fewer than 2 independent units

## Workflow

### 1. Decompose

Split the user request into independent work units. Each unit must be:

- Self-contained (no dependency on other units)
- Well-scoped (clear input, clear expected output)
- Worth isolating (non-trivial enough to justify agent overhead)

### 2. Plan

For each unit, define:

| Field | Description |
|-------|-------------|
| **Name** | Short identifier (e.g., `worker-auth`, `worker-docs`) |
| **Type** | `worktree` for file changes, `shared` for read-only research |
| **Prompt** | Complete, self-contained instructions (no shared context) |
| **Output** | What the agent should produce and where |

### 3. Dispatch

Launch all agents in a **single message with multiple Agent tool calls**.
This ensures true parallel execution. Each agent prompt must include:

- Full context needed (file paths, requirements, constraints)
- Expected output format and location
- No references to other agents or their work

### 4. Track

Use TaskCreate for each dispatched unit to give the user visibility:

```text
TaskCreate: "worker-auth: implement OAuth module" — status: in_progress
TaskCreate: "worker-docs: write API reference" — status: in_progress
```

Update tasks as agents complete via TaskUpdate.

### 5. Collect

After all agents finish:

- Read each agent's output
- Validate completeness and correctness
- Synthesize a summary for the user
- Handle any git operations (worktree agents lack Bash)

## Agent Isolation Modes

| Mode | Use when | File access |
|------|----------|-------------|
| `worktree` | Agent creates/edits files | Isolated copy, lead merges |
| `shared` | Agent only reads/researches | Shared repo, no writes |

## Constraints

- **Worktree agents lack Bash** — the lead agent handles all git operations
  (commits, merges, branch management) after collecting results
- **Max ~5 parallel agents** — diminishing returns beyond this; context
  scheduling overhead increases
- **Self-contained prompts** — each agent gets a complete prompt with all
  necessary context; no shared memory between agents
- **Lead agent owns coordination** — only the lead creates, tracks, and
  collects; agents do not spawn sub-agents

## Anti-Patterns

- Dispatching a single trivial task as a "parallel" worker (just do it inline)
- Sharing mutable state between agents (they cannot see each other's changes)
- Vague prompts that require agents to ask clarifying questions
- Dispatching dependent tasks in parallel (use sequential execution instead)
- Skipping the collect phase (results must be validated and synthesized)

## Quality Check

- Each agent prompt is self-contained and actionable
- No circular or hidden dependencies between units
- All agent results collected and validated before reporting to user
- Git operations performed by lead after collection, not by workers
