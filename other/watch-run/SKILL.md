---
name: watch-run
description: Monitor a Coval run's progress with live updates. Use when user wants to check run status or wait for completion.
argument-hint: "[run-id]"
---

# Watch Coval Run Progress

Monitor the progress of run `$ARGUMENTS`.

## Workflow

### Step 1: Identify Run

If no run ID provided, list recent runs:

```bash
coval runs list --page-size 10
```

Ask user to select a run to watch.

### Step 2: Watch Progress

```bash
coval runs watch <run_id> --interval 2
```

This displays a live progress bar showing:
- Completed / Total test cases
- Current status (PENDING, IN QUEUE, IN PROGRESS, COMPLETED, FAILED)
- Percentage complete

### Step 3: Report Results

When the run completes, summarize:

```bash
coval runs get <run_id> --format json
```

Report:
- Total simulations completed
- Pass/fail counts (if available)
- Duration
- Link to results

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--interval` | Refresh rate in seconds | 2 |

## Statuses

| Status | Meaning |
|--------|---------|
| PENDING | Run created, not yet queued |
| IN QUEUE | Waiting for capacity |
| IN PROGRESS | Simulations running |
| COMPLETED | All simulations finished |
| FAILED | Run encountered an error |
| CANCELLED | User cancelled the run |
