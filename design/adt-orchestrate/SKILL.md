---
name: orchestrate
description: Coordinate multiple subagents/worktrees for parallel workstreams. Decomposes larger tasks into independent sub-tasks, dispatches each to a dedicated agent.
triggers:
  - "orchestrate parallel work"
  - "coordinate subagents"
  - "multi-agent task"
  - "parallel workstreams"
---

# Orchestrate

Coordinate multiple subagents/worktrees for parallel workstreams. Decomposes a larger task into independent sub-tasks, dispatches each to a dedicated agent in its own worktree, awaits completion, integrates results.

## Purpose

Break large tasks into parallel tracks. Use when a single agent working linearly would be too slow or when domain separation improves clarity (e.g., frontend + backend + infra as separate workstreams).

## When to use

- "Split this full-stack feature across 3 agents: frontend, API, database"
- "I need 4 concurrent code reviews on different modules"
- "Deploy 5 microservices in parallel, each with its own setup"

## Workflow

1. **Decompose** — Parse task, identify independent sub-tasks with clear boundaries.
2. **Spawn agents** — Create 1 worktree per sub-task; seed each with context + instructions.
3. **Dispatch** — Send each sub-task to a dedicated agent (up to 5 parallel, staggered start to avoid resource contention).
4. **Monitor** — Poll each agent for completion; log progress.
5. **Integrate** — Merge sub-task results (code, configs, docs) into main branch; resolve conflicts if any.

## Example Workflow

```
User: "Orchestrate: Add OAuth2 to the monorepo (frontend, API, database)"

Decompose:
  - Sub-task 1: Frontend OAuth UI + login flow
  - Sub-task 2: API endpoint + JWT validation
  - Sub-task 3: Database user/session schema

Spawn 3 worktrees, each with dedicated agent:
  - Agent A (worktree-1): frontend-oauth
  - Agent B (worktree-2): api-oauth
  - Agent C (worktree-3): db-oauth

Dispatch: "Implement OAuth login component" → Agent A
          "Add /auth/token endpoint" → Agent B
          "Create user_sessions table" → Agent C

Monitor: Poll every 30s; print status
Integrate: Merge all 3 PRs, run e2e test
```

## Safety Checks

- Each agent works in isolated worktree (no merge conflicts mid-flight).
- Central agent monitors and integrates; reports blockers immediately.
- If any sub-task fails: pause others, diagnose, offer fallback (sequential execution or help-wanted).

## References

- Git worktrees: `using-git-worktrees` skill
- Dispatcher: `dispatch` skill (single-agent routing)
- Parallel agents: `dispatching-parallel-agents` pattern
