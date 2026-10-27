---
name: ralph-session-ops-reference
description: Ralph-v2 session operations reference for schema validation, timeout recovery, and timestamp commands. Use when validating Ralph session artifacts, reconstructing malformed state, enforcing retry timing, or generating Ralph session timestamps.
---

# Ralph Session Operations Reference

Use this skill when a Ralph-v2 agent needs deterministic session-level reference material instead of improvising it from memory.

## Use Cases

- Validate `metadata.yaml` or `iterations/<N>/progress.md`
- Repair malformed Ralph session state
- Apply the standard subagent timeout recovery ladder
- Generate Ralph session IDs or ISO8601 timestamps

## Schema Validation Rules

### `iterations/<N>/progress.md` must include

- `# Progress`
- `## Legend` with `[ ]`, `[/]`, `[P]`, `[x]`, `[F]`, `[C]`
- `## Planning Progress (Iteration N)`
- `## Implementation Progress (Iteration N)`

### `metadata.yaml` must include

- `version`, `session_id`, `created_at`, `updated_at`, `iteration`
- `orchestrator.state`
- `tasks.total`, `tasks.completed`, `tasks.failed`, `tasks.pending`
- `session_review.cycle`
- `session_review.issue_severity_threshold`
- `session_review.max_critique_cycles`

## Timeout Recovery Policy

Apply this to any Ralph-v2 subagent call that times out or fails unexpectedly.

1. Retry the same single-mode invocation immediately.
2. Retry after 30 seconds.
3. Retry after 60 seconds.
4. Retry after another 60 seconds.
5. If still failing:
   - If `TASK_ID` exists, invoke Planner with `MODE: SPLIT_TASK` and continue with the replacement tasks.
   - If no `TASK_ID` exists, stop and ask for a narrower scope.

### Sleep Commands

- Windows PowerShell: `Start-Sleep -Seconds 30` or `Start-Sleep -Seconds 60`
- Linux/WSL: `sleep 30` or `sleep 60`

## Local Timestamp Commands

### Session ID format `<YYMMDD>-<hhmmss>`

- Windows PowerShell: `Get-Date -Format "yyMMdd-HHmmss"`
- Linux/WSL: `TZ=Asia/Ho_Chi_Minh date +"%y%m%d-%H%M%S"`

### ISO8601 local timestamp

- Windows PowerShell: `Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"`
- Linux/WSL: `TZ=Asia/Ho_Chi_Minh date +"%Y-%m-%dT%H:%M:%S%z"`