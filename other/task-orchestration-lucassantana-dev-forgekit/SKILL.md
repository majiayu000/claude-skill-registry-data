---
name: task-orchestration
description: >-
  You have 5 projects, each with a session. You open each one, paste "continue
  with next priorities", wait, switch, repeat. You're acting as a human cron
  job.
---
# Task Orchestration

> Stop being the scheduler. Define the work, let the machine manage the queue.

## The Problem

You have 5 projects, each with a session. You open each one, paste "continue with next priorities", wait, switch, repeat. You're acting as a human cron job.

## The Pattern

Separate **planning** from **execution**:

1. **Plan once** — Analyze all projects, identify highest-value work, create a prioritized backlog
2. **Dispatch automatically** — A background process picks the next task, creates a session, sends the prompt
3. **Monitor completion** — When a session goes idle with all tasks done, mark complete and dispatch next
4. **Chain work** — Sequential tasks promote automatically when predecessors complete

### Task Lifecycle

```
backlog → ready → in_progress → done
                       ↓
                    blocked
```

- **backlog**: Planned but waiting (dependencies, sequencing)
- **ready**: Can be dispatched immediately
- **in_progress**: Assigned to a session, agent is working
- **done**: Work complete, verified
- **blocked**: Something went wrong, needs human attention

### Task Schema (Tool-Agnostic)

```json
{
  "id": "unique-id",
  "title": "Short description",
  "description": "Detailed instructions for the agent",
  "directory": "/path/to/project",
  "priority": "critical | high | medium | low",
  "status": "backlog | ready | in_progress | done | blocked",
  "tags": ["security", "api", "frontend"],
  "dependsOn": ["other-task-id"],
  "createdAt": 1710000000000,
  "updatedAt": 1710000000000
}
```

### Good Task Descriptions

**Bad**: "Fix the auth bug"

**Good**:
```
Fix the session timeout race condition in auth/middleware.ts.

The bug: when two requests arrive within 50ms of session expiry,
both pass the `isValid()` check but the first one triggers a refresh
that invalidates the second.

Fix: add a mutex around the refresh logic, or use optimistic locking
on the session version field.

Test: the existing test in auth/middleware.test.ts covers the happy
path but not the race. Add a concurrent request test.
```

### Task Sizing

Break work into **5-20 minute tasks**. This:
- Gives the agent a clear finish line
- Produces frequent commits (rollback points)
- Enables parallel execution across sessions
- Makes progress visible

### Concurrency Control

Run at most 2-3 tasks simultaneously:
- More than that and you can't review the output
- Context switches between reviewing too many sessions is worse than serial execution
- Machine resources (CPU, API rate limits) become bottlenecks

## How to Plan

### Automated Planning

The agent itself is the best planner. Give it access to:
- Git status and recent log
- Open PRs and issues
- CHANGELOG.md (what's released vs unreleased)
- CLAUDE.md / AGENTS.md (project conventions)

Then ask: "What are the highest-value tasks right now?"

### Priority Framework

| Priority | Criteria | Examples |
|----------|----------|---------|
| Critical | Blocks other work or users | Broken CI, security vulnerability |
| High | High user/business value, ready to ship | Feature completion, bug fix |
| Medium | Improves quality or DX | Refactoring, test coverage, docs |
| Low | Nice to have | Code cleanup, dependency updates |

## Implementation

### Any Tool

The pattern works with any task tracking:
- **JSON file** on disk (simplest)
- **GitHub Issues** as backlog (collaborative)
- **Linear/Jira** (team scale)

The dispatch mechanism varies by tool:
- **OpenCode**: Plugin with `session.create` + `session.promptAsync`
- **Claude Code**: Shell script that launches `claude --session-id`
- **Cursor**: Workspace automation with tasks.json
- **Manual**: A checklist you work through (still better than ad-hoc)

### Reference Implementation

See: [`packages/core/implementations/opencode/plugin/orchestrator.ts`](../packages/core/implementations/opencode/plugin/orchestrator.ts)

## OMC-Inspired Orchestration Patterns

Patterns derived from [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) — a multi-agent orchestration framework built on Claude Code.

### 3-Layer Composition

```
ultrawork → ralph → autopilot
```

| Layer | Role | When to use |
|-------|------|-------------|
| `ultrawork` | Parallel execution engine with model tier routing | Multiple independent tasks, cost optimization |
| `ralph` | PRD-driven persistence loop, story-by-story | Single cohesive feature with explicit acceptance criteria |
| `autopilot` | Lightweight sequential runner | Simple chained tasks with no branching |

Use the layers independently or compose them. Example: `ultrawork` dispatches parallel stories, each story runs `ralph` internally.

### Model Tier Routing (Ultrawork Pattern)

Route subagents to the cheapest model that can do the job:

| Tier | Model | Task Types |
|------|-------|-----------|
| Haiku | Fast/cheap | Trivial fixes, config edits, lookups, spec review (mechanical) |
| Sonnet | Default | Standard implementation, bug fixes, test writing, code quality review |
| Opus | Slow/expensive | Architecture decisions, cross-repo analysis, ambiguous requirements |

**Routing heuristics:**
- Lines changed < 20 → Haiku; 20–200 → Sonnet; >200 or architectural → Opus
- Single file → Haiku; multi-file → Sonnet; cross-repo → Opus

### Ralph — PRD-Driven Persistence

The `ralph` pattern prevents agents from hallucinating completion. Key properties:

1. **Explicit acceptance criteria** — defined in `prd.json` before execution starts
2. **Story-by-story iteration** — one story at a time, not all at once
3. **Reviewer sign-off required** — a fresh subagent must return `APPROVED` before marking a story done
4. **Persistent state** — `prd.json` story statuses survive context resets

```json
{
  "feature": "feature name",
  "stories": [
    {
      "id": "S1",
      "title": "story title",
      "acceptance_criteria": ["criterion 1", "criterion 2"],
      "status": "pending | in_progress | done | blocked"
    }
  ],
  "done_criteria": ["CI passing", "CHANGELOG.md updated"]
}
```

### Preemptive Compaction

For local models with small context windows, track tokens cumulatively (O(1) per iteration) and compact before the context fills:

```python
# Instead of re-summing all messages each iteration:
cumulative_tokens = 0  # running total

# On each new message added:
cumulative_tokens += len(str(new_content)) // 4

# Compact at ~44% of context window to leave room for tool outputs:
if cumulative_tokens > COMPACT_THRESHOLD:
    messages = compact_messages(messages)
    cumulative_tokens = estimate_tokens(messages)  # reset to actual
```

For Claude Code (200K context), compact at 70% threshold. For local 16K models, compact at 44%.

### Verify-Deliverables Hook

After each subagent completes, verify it actually produced output before the parent continues. Prevents "I would implement..." responses from being treated as completions:

**Checklist before accepting subagent output:**
1. Did the subagent write or modify at least one file?
2. Do tests pass?
3. Does the output match the task spec (not just "here's how I would do it")?

If any check fails: re-dispatch the subagent with explicit instructions to execute, not describe.
