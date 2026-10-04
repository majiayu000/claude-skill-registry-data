---
name: running-workflows
description: Launches workflow engine runs in the background, monitors progress via session files, and reports status. Use when running spec-implementation workflows or any workflow engine invocation.
---

# Running Workflows

## Purpose

Standardized way to launch the workflow engine CLI, background it, and monitor progress. Keeps the main conversation available while workflows run.

## When to Use

- User asks to "run a workflow", "implement a spec", or "execute spec-implementation"
- You need to invoke the workflow engine CLI (`wrangler-workflow`)
- Monitoring a running or paused workflow

## When NOT to Use

- Implementing a single issue (use implementing-issue)
- Writing plans without execution (use writing-plans)

## 1. Launching a Workflow

### Resolve the CLI

The engine CLI lives relative to the wrangler plugin root:

```bash
# From the project root (dev checkout):
node workflows/engine/dist/cli.js

# Or via the bin wrapper:
bin/wrangler-workflow
```

If the engine is not built, build it first:

```bash
cd workflows/engine && npm run build
```

### Run Command

```bash
node workflows/engine/dist/cli.js run <spec-file> [options]
```

**Options:**
- `--dry-run` -- Analyze and plan only, do not execute or publish
- `--resume <session-id>` -- Resume a paused workflow from its last checkpoint

**Examples:**

```bash
# Full run
node workflows/engine/dist/cli.js run .wrangler/specifications/SPEC-000049-feature.md

# Dry run (plan only)
node workflows/engine/dist/cli.js run .wrangler/specifications/SPEC-000049-feature.md --dry-run

# Resume paused workflow
node workflows/engine/dist/cli.js run .wrangler/specifications/SPEC-000049-feature.md --resume wf-2026-02-16-ba6fcb97
```

### MUST Background by Default

Always launch workflows in the background using the Bash tool's `run_in_background` parameter. Workflows take 5-30 minutes. Do NOT block the conversation.

```
Bash(command: "node workflows/engine/dist/cli.js run <spec-file>", run_in_background: true, timeout: 600000)
```

After launching, immediately tell the user:
- The workflow is running in the background
- The session ID (from initial output or context.json)
- How to check status: "Ask me anytime for a progress update"

## 2. Checking Progress

### MCP Tool (Preferred)

Use the `session_status` MCP tool for a structured status report:

```
session_status({ sessionId: "wf-2026-02-16-ba6fcb97" })
```

If you omit `sessionId`, it auto-detects the most recent `wf-*` session:

```
session_status({})
```

The tool returns structured metadata including:
- `status`: running/paused/completed/failed
- `activeStep`: Current step derived from audit log (reliable, not stale context.json)
- `phasesCompleted`: Phases finished (derived from audit log)
- `tasksCompleted` / `tasksPending` / `totalTasks`: Task progress
- `duration`: Human-readable elapsed time
- `specFile`, `worktreePath`, `branchName`: Session context
- `blocker`: Details if the workflow is paused
- `checkpoint`: Resume state if available
- `lastActivity`: What happened most recently
- `auditEntryCount`: Total audit entries

### Bash Helper Script (Alternative)

For terminal use outside of Claude Code, a helper script is available:

```bash
bin/check-workflow-status <session-id>
bin/check-workflow-status              # auto-detects most recent wf-* session
```

This outputs a formatted summary including process PID and CPU/memory usage.

### Manual Status Check

If neither tool is available, check session files directly:

**Session directory:** `.wrangler/sessions/<session-id>/`

#### audit.jsonl -- Activity Log (Source of Truth)

The audit log is the most reliable source of current workflow state. Each line is a JSON object recording a step transition:

```json
{"step":"analyze","status":"started","timestamp":"2026-02-16T21:58:15.127Z"}
{"step":"analyze","status":"completed","timestamp":"2026-02-16T21:59:28.160Z","metadata":{...}}
{"step":"implement","status":"started","timestamp":"2026-02-16T22:03:48.990Z"}
```

Steps you will see: `init`, `analyze`, `plan`, `execute`, `implement` (per-task), `review` (per-task), `fix-issues` (if review found problems), `verify`, `publish`.

#### context.json -- Overall State

Contains `status`, `tasksCompleted`, `tasksPending`, `specFile`, `worktreePath`, `branchName`. Note: `currentPhase` and `phasesCompleted` may be stale -- derive these from audit.jsonl instead.

#### checkpoint.json / blocker.json

Present when the workflow paused. Checkpoint contains resume state; blocker contains the reason for pausing.

### Interpreting Progress

| Status | Meaning | Action |
|---------------------|---------|--------|
| `running` | Workflow is actively executing | Wait, check audit log for current step |
| `paused` | Hit a blocker or loop exhaustion | Read blocker, consider `--resume` |
| `completed` | All phases finished successfully | Check worktree for PR |
| `failed` | Unrecoverable error | Read audit log for error details |

### Reporting to User

When the user asks for a progress update, call `session_status({})` and report:

1. **Status**: running/paused/completed/failed
2. **Active step**: What's happening right now
3. **Progress**: X of Y tasks completed (if in execute phase)
4. **Last activity**: Most recent audit entry
5. **Duration**: How long it has been running

Example report:

```
Workflow wf-2026-02-16-ba6fcb97 is running.

Phase: execute (analyze -> plan -> [execute] -> verify -> publish)
Progress: 3/8 tasks completed
Last activity: Implementing task-004 (started 2m ago)
Running for: 12 minutes

The workflow is working in an isolated worktree at .worktrees/feature-name/.
```

## 3. Handling Completion

When the workflow finishes (check via TaskOutput or periodic polling):

**If completed:**
- Report success to user
- Show the branch name and worktree path
- Note if a PR was created
- Suggest reviewing the changes

**If paused:**
- Read blocker.json for the reason
- Report to user with context
- Offer to resume: `--resume <session-id>`

**If failed:**
- Read the last audit entries for error context
- Report the failure to user
- Suggest debugging steps

## 4. Resuming Paused Workflows

```bash
node workflows/engine/dist/cli.js run <spec-file> --resume <session-id>
```

The engine picks up from the last checkpoint, skipping completed phases and tasks.

## Workflow Phases Reference

The `spec-implementation` workflow runs these phases in order:

1. **analyze** -- Reads the spec, produces structured task breakdown
2. **plan** -- Creates MCP issues from the analysis
3. **execute** -- Implements each task (per-task loop with implement -> review -> fix cycle)
4. **verify** -- Runs full test suite, checks all requirements met
5. **publish** -- Creates GitHub PR from the completed work

Each phase produces audit entries and updates context.json.
