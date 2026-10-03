---
name: workflow-launchpad
description: >
  Set up a practical Codex workflow for a new day, project, or repo. Use when
  the user wants an amazing workflow setup, a repeatable launch checklist,
  aligned skills, project memory, low-token defaults, daemon/process control,
  multi-agent coordination, or a personal Codex operating rhythm.
---

# Workflow Launchpad

Use this to start work cleanly and avoid context drift.

## Project Bootstrap

1. Run `$repo-intelligence-brief` if the repo is unfamiliar.
2. Run `$low-token-context` to create a compact task brief.
3. Create `.codex-memory/decisions.md` only if durable decisions are expected.
4. Choose one active workflow:
   - build
   - debug
   - review
   - research
   - experiment
   - MCP integration
5. Define verification before editing.

## Control Plane Setup

Use this when the project has daemons, background workers, queues, MCP/tool
servers, release tasks, API-to-tool bridges, or parallel agents.

```md
## Control Plane
Command surface:
Runtime state:
Lifecycle owner:
Ports/namespaces:
Status/logs:
Workers/queues:
Agent scopes/leases:
Trust boundaries:
Verification:
Stop/recover:
```

- Write down the status/log/health command before starting processes.
- Keep runtime state, credentials, caches, and local databases out of source
  control.
- Assign write scopes or leases before parallel agent work.
- Run `$mcp-safety-review` before trusting side-effecting tool surfaces.
- Escalate production traces, evals, guardrails, budgets, shadow traffic, or
  release gates to `$auto-skill-build-agent-reliability-loop`.

## Daily Rhythm

```md
# Today
## Goal
## Context
## Active Files
## Commands
## Risks
## Done Criteria
```

## End-Of-Session

- Summarize decisions into memory.
- Record failed attempts only if they prevent repeated work.
- Update task brief with next action.
- Keep logs out of memory unless compacted.

Use `$codex-supercharge-router` when the next workflow is unclear.

Read `plugins/codex-supercharge/references/workflow-control-plane.md` for the
source-backed control-plane pattern.

## Skip When

- The task already has a precise plan and validation command.
- The user only wants an immediate one-off answer.

## Validation

- The active workflow, verification command, and done criteria are written down.
- Any durable decisions are placed in memory, not left only in chat.
- The chosen skill path matches the current repo/task risk.
- Daemon, worker, queue, MCP/tool, or multi-agent work has an explicit control
  plane before execution.
