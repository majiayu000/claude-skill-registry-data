---
name: temporal
description: "Manage Temporal workflows: server lifecycle, worker processes, workflow execution, monitoring, and troubleshooting for Python SDK with temporal server start-dev."
version: 1.0.1
allowed-tools: "Bash(.claude/skills/temporal/scripts/*:*), Read"
---

# Temporal Skill

Manage Temporal workflows using local development server. This skill focuses on the **execution, validation, and troubleshooting** lifecycle of workflows.

| Property | Value |
|----------|-------|
| Target SDK | Python only |
| Server Type | `temporal server start-dev` (local development) |
| gRPC Port | 7233 |

---

## Critical Concepts

Understanding how Temporal components interact is essential for troubleshooting:

### How Workers, Workflows, and Tasks Relate

```
┌─────────────────────────────────────────────────────────────────┐
│                     TEMPORAL SERVER                              │
│  Stores workflow history, manages task queues, coordinates work │
└─────────────────────────────────────────────────────────────────┘
                              │
                    Task Queue (named queue)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         WORKER                                   │
│  Long-running process that polls task queue for work            │
│  Contains: Workflow definitions + Activity implementations       │
│                                                                  │
│  When work arrives:                                              │
│    - Workflow Task → Execute workflow code decisions            │
│    - Activity Task → Execute activity code (business logic)     │
└─────────────────────────────────────────────────────────────────┘
```

**Key Insight**: The workflow code runs inside the worker. If worker code is outdated or buggy, workflow execution fails.

### Workflow Task vs Activity Task

| Task Type | What It Does | Where It Runs | On Failure |
|-----------|--------------|---------------|------------|
| **Workflow Task** | Makes workflow decisions (what to do next) | Worker | **Stalls the workflow** until fixed |
| **Activity Task** | Executes business logic | Worker | Retries per retry policy |

**CRITICAL**: Workflow Task errors are fundamentally different from Activity Task errors:
- **Workflow Task Failure** → Workflow **stops making progress entirely**
- **Activity Task Failure** → Workflow **retries the activity** (workflow still progressing)

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_TEMPORAL_LOG_DIR` | `/tmp/claude-temporal-logs` | Directory for worker log files |
| `CLAUDE_TEMPORAL_PID_DIR` | `/tmp/claude-temporal-pids` | Directory for worker PID files |
| `CLAUDE_TEMPORAL_PROJECT_DIR` | `$(pwd)` | Project root directory |
| `CLAUDE_TEMPORAL_PROJECT_NAME` | `$(basename "$PWD")` | Project name (used for log/PID naming) |
| `CLAUDE_TEMPORAL_NAMESPACE` | `default` | Temporal namespace |
| `TEMPORAL_ADDRESS` | `localhost:7233` | Temporal server gRPC address |
| `TEMPORAL_CLI` | `temporal` | Path to Temporal CLI binary |
| `TEMPORAL_WORKER_CMD` | `uv run worker` | Command to start worker |

---

## Quick Start

```bash
# 1. Start server
./scripts/ensure-server.sh

# 2. Start worker (ensures no old workers, starts fresh one)
./scripts/ensure-worker.sh

# 3. Execute workflow
uv run starter  # Capture workflow_id from output

# 4. Wait for completion
./scripts/wait-for-workflow-status.sh --workflow-id <id> --status COMPLETED

# 5. Get result (IMPORTANT: verify result is correct, not an error message)
./scripts/get-workflow-result.sh --workflow-id <id>

# 6. CLEANUP: Kill workers when done
./scripts/kill-worker.sh
```

---

## Worker Management

### The Golden Rule

**Ensure no old workers are running.** Stale workers with outdated code cause:
- Non-determinism errors (history mismatch)
- Executing old buggy code
- Confusing behavior

**Best practice**: Run only ONE worker instance with the latest code.

### Starting Workers

```bash
# PREFERRED: Smart restart (kills old, starts fresh)
./scripts/ensure-worker.sh
```

This command:
1. Finds ALL existing workers for the project
2. Kills them
3. Starts a new worker with fresh code
4. Waits for worker to be ready

### Verifying Workers

```bash
# List all running workers
./scripts/list-workers.sh

# Check specific worker health
./scripts/monitor-worker-health.sh

# View worker logs
tail -f $CLAUDE_TEMPORAL_LOG_DIR/worker-$(basename "$(pwd)").log
```

**What to look for in logs**:
- `Worker started, listening on task queue: ...` → Worker is ready
- `Worker process died during startup` → Startup failure, check logs for error

### Cleanup (REQUIRED)

**Always kill workers when done.** Don't leave workers running.

```bash
# Kill current project's worker
./scripts/kill-worker.sh

# Kill ALL workers (full cleanup)
./scripts/kill-all-workers.sh

# Kill all workers AND server
./scripts/kill-all-workers.sh --include-server
```

---

## Workflow Execution

### Starting Workflows

```bash
# Execute workflow via starter script
uv run starter
```

**CRITICAL**: Capture the Workflow ID from output. You need it for all monitoring/troubleshooting.

### Checking Status

```bash
# Get workflow status
temporal workflow describe --workflow-id <id>

# Wait for specific status
./scripts/wait-for-workflow-status.sh \
  --workflow-id <id> \
  --status COMPLETED \
  --timeout 60
```

### Workflow Status Reference

| Status | Meaning | Action |
|--------|---------|--------|
| `RUNNING` | Workflow in progress | Wait, or check if stalled |
| `COMPLETED` | Successfully finished | Get result, verify correctness |
| `FAILED` | Error during execution | Analyze error |
| `CANCELED` | Explicitly canceled | Review reason |
| `TERMINATED` | Force-stopped | Review reason |
| `TIMED_OUT` | Exceeded timeout | Increase timeout |

### Getting Results

```bash
./scripts/get-workflow-result.sh --workflow-id <id>
```

**IMPORTANT - False Positive Detection**:

Workflows may `COMPLETE` but return undesired results (e.g., error messages in the result payload).

```json
// This workflow COMPLETED but the result is an ERROR!
{"status": "error", "message": "Failed to process request"}
```

**Always verify the result content is correct**, not just that the status is COMPLETED.

---

## Troubleshooting

### Step 1: Identify the Problem

```bash
# Check workflow status
temporal workflow describe --workflow-id <id>

# Check for stalled workflows (workflows stuck in RUNNING)
./scripts/find-stalled-workflows.sh

# Analyze specific workflow errors
./scripts/analyze-workflow-error.sh --workflow-id <id>
```

### Step 2: Diagnose Using This Decision Tree

```
Workflow not behaving as expected?
│
├── Status: RUNNING but no progress (STALLED)
│   │
│   ├── Is it an interactive workflow waiting for signal/update?
│   │   └── YES → Send the required interaction
│   │
│   └── NO → Run: ./scripts/find-stalled-workflows.sh
│       │
│       ├── WorkflowTaskFailed detected
│       │   │
│       │   ├── Non-determinism error (history mismatch)?
│       │   │   └── See: "Fixing Non-Determinism Errors" below
│       │   │
│       │   └── Other workflow task error (code bug, missing registration)?
│       │       └── See: "Fixing Other Workflow Task Errors" below
│       │
│       └── ActivityTaskFailed (excessive retries)
│           └── Activity is retrying. Fix activity code, restart worker.
│               Workflow will auto-retry with new code.
│
├── Status: COMPLETED but wrong result
│   └── Check result: ./scripts/get-workflow-result.sh --workflow-id <id>
│       Is result an error message? → Fix workflow/activity logic
│
├── Status: FAILED
│   └── Run: ./scripts/analyze-workflow-error.sh --workflow-id <id>
│       Fix code → ./scripts/ensure-worker.sh → Start NEW workflow
│
├── Status: TIMED_OUT
│   └── Increase timeouts → ./scripts/ensure-worker.sh → Start NEW workflow
│
└── Workflow never starts
    └── Check: Worker running? Task queue matches? Workflow registered?
```

---

## Fixing Workflow Task Errors

**Workflow task errors STALL the workflow** - it stops making progress entirely until the issue is fixed.

### Fixing Non-Determinism Errors

Non-determinism occurs when workflow code changes while a workflow is running, causing history mismatch.

**Symptoms**:
- `WorkflowTaskFailed` events in history
- "Non-deterministic error" or "history mismatch" in logs

**Fix procedure**:
```bash
# 1. TERMINATE affected workflows (they cannot recover)
temporal workflow terminate --workflow-id <id>

# 2. Kill existing workers
./scripts/kill-worker.sh

# 3. Fix the workflow code if needed

# 4. Restart worker with corrected code
./scripts/ensure-worker.sh

# 5. Verify workflow logic is correct

# 6. Start NEW workflow execution
uv run starter
```

**Key point**: Non-determinism corrupts the workflow. You MUST terminate and start fresh.

### Fixing Other Workflow Task Errors

For workflow task errors that are NOT non-determinism (code bugs, missing registration, etc.):

**Symptoms**:
- `WorkflowTaskFailed` events
- Error is NOT "history mismatch" or "non-deterministic"

**Fix procedure**:
```bash
# 1. Identify the error
./scripts/analyze-workflow-error.sh --workflow-id <id>

# 2. Fix the root cause (code bug, worker config, etc.)

# 3. Kill and restart worker with fixed code
./scripts/ensure-worker.sh

# 4. NO NEED TO TERMINATE - the workflow will automatically resume
#    The new worker picks up where it left off and continues execution
```

**Key point**: Unlike non-determinism, the workflow can recover once you fix the code.

---

## Fixing Activity Task Errors

**Activity task errors cause retries**, not immediate workflow failure.

### Workflow Stalling Due to Retries

Workflows can appear stalled because an activity keeps failing and retrying.

**Diagnosis**:
```bash
# Check for excessive activity retries
./scripts/find-stalled-workflows.sh

# Look for ActivityTaskFailed count
# Check worker logs for retry messages
tail -100 $CLAUDE_TEMPORAL_LOG_DIR/worker-$(basename "$(pwd)").log
```

**Fix procedure**:
```bash
# 1. Fix the activity code

# 2. Restart worker with fixed code
./scripts/ensure-worker.sh

# 3. Worker auto-retries with new code
#    No need to terminate or restart workflow
```

### Activity Failure (Retries Exhausted)

When all retries are exhausted, the activity fails permanently.

**Fix procedure**:
```bash
# 1. Analyze the error
./scripts/analyze-workflow-error.sh --workflow-id <id>

# 2. Fix activity code

# 3. Restart worker
./scripts/ensure-worker.sh

# 4. Start NEW workflow (old one has failed)
uv run starter
```

---

## Common Error Types Reference

| Error Type | Where to Find | What Happened | Recovery |
|------------|---------------|---------------|----------|
| **Non-determinism** | `WorkflowTaskFailed` in history | Code changed during execution | Terminate workflow → Fix → Restart worker → NEW workflow |
| **Workflow code bug** | `WorkflowTaskFailed` in history | Bug in workflow logic | Fix code → Restart worker → Workflow auto-resumes |
| **Missing workflow** | Worker logs | Workflow not registered | Add to worker.py → Restart worker |
| **Missing activity** | Worker logs | Activity not registered | Add to worker.py → Restart worker |
| **Activity bug** | `ActivityTaskFailed` in history | Bug in activity code | Fix code → Restart worker → Auto-retries |
| **Activity retries** | `ActivityTaskFailed` (count >2) | Repeated failures | Fix code → Restart worker → Auto-retries |
| **Sandbox violation** | Worker logs | Bad imports in workflow | Fix workflow.py imports → Restart worker |
| **Task queue mismatch** | Workflow never starts | Different queues in starter/worker | Align task queue names |
| **Timeout** | Status = TIMED_OUT | Operation too slow | Increase timeout config |

---

## Interactive Workflows

Interactive workflows pause and wait for external input (signals or updates).

### Signals

```bash
# Send signal to workflow
temporal workflow signal \
  --workflow-id <id> \
  --name "signal_name" \
  --input '{"key": "value"}'

# Or via interact script (if available)
uv run interact --workflow-id <id> --signal-name "signal_name" --data '{"key": "value"}'
```

### Updates

```bash
# Send update to workflow
temporal workflow update \
  --workflow-id <id> \
  --name "update_name" \
  --input '{"approved": true}'
```

### Queries

```bash
# Query workflow state (read-only)
temporal workflow query \
  --workflow-id <id> \
  --name "get_status"
```

---

## Common Recipes

### Recipe 1: Clean Start (Fresh Environment)
```bash
./scripts/kill-all-workers.sh
./scripts/ensure-server.sh
./scripts/ensure-worker.sh
uv run starter
```

### Recipe 2: Debug Stalled Workflow
```bash
# 1. Find what's wrong
./scripts/find-stalled-workflows.sh
./scripts/analyze-workflow-error.sh --workflow-id <id>

# 2. Check worker logs
tail -100 $CLAUDE_TEMPORAL_LOG_DIR/worker-$(basename "$(pwd)").log

# 3. Fix based on error type (see decision tree above)
```

### Recipe 3: Clear Stalled Environment
```bash
./scripts/find-stalled-workflows.sh
./scripts/bulk-cancel-workflows.sh
./scripts/kill-worker.sh
./scripts/ensure-worker.sh
```

### Recipe 4: Test Interactive Workflow
```bash
./scripts/ensure-worker.sh
uv run starter  # Get workflow_id
./scripts/wait-for-workflow-status.sh --workflow-id $workflow_id --status RUNNING
uv run interact --workflow-id $workflow_id --signal-name "approval" --data '{"approved": true}'
./scripts/wait-for-workflow-status.sh --workflow-id $workflow_id --status COMPLETED
./scripts/get-workflow-result.sh --workflow-id $workflow_id
./scripts/kill-worker.sh  # CLEANUP
```

### Recipe 5: Check Recent Workflow Results
```bash
# List recent workflows
./scripts/list-recent-workflows.sh --minutes 30

# Check results (verify they're correct, not error messages!)
./scripts/get-workflow-result.sh --workflow-id <id1>
./scripts/get-workflow-result.sh --workflow-id <id2>
```

---

## Tool Reference

### Lifecycle Scripts

| Tool | Description | Key Options |
|------|-------------|-------------|
| `ensure-server.sh` | Start dev server if not running | - |
| `ensure-worker.sh` | Kill old workers, start fresh one | Uses `$TEMPORAL_WORKER_CMD` |
| `kill-worker.sh` | Kill current project's worker | - |
| `kill-all-workers.sh` | Kill all workers | `--include-server` |
| `list-workers.sh` | List running workers | - |

### Monitoring Scripts

| Tool | Description | Key Options |
|------|-------------|-------------|
| `list-recent-workflows.sh` | Show recent executions | `--minutes N` (default: 5) |
| `find-stalled-workflows.sh` | Detect stalled workflows | `--query "..."` |
| `monitor-worker-health.sh` | Check worker status | - |
| `wait-for-workflow-status.sh` | Block until status | `--workflow-id`, `--status`, `--timeout` |

### Debugging Scripts

| Tool | Description | Key Options |
|------|-------------|-------------|
| `analyze-workflow-error.sh` | Extract errors from history | `--workflow-id`, `--run-id` |
| `get-workflow-result.sh` | Get workflow output | `--workflow-id`, `--raw` |
| `bulk-cancel-workflows.sh` | Mass cancellation | `--pattern "..."` |

---

## Log Files

| Log | Location | Content |
|-----|----------|---------|
| Worker logs | `$CLAUDE_TEMPORAL_LOG_DIR/worker-{project}.log` | Worker output, activity logs, errors |

**Useful searches**:
```bash
# Find errors
grep -i "error" $CLAUDE_TEMPORAL_LOG_DIR/worker-*.log

# Check worker startup
grep -i "started" $CLAUDE_TEMPORAL_LOG_DIR/worker-*.log

# Find activity issues
grep -i "activity" $CLAUDE_TEMPORAL_LOG_DIR/worker-*.log
```
