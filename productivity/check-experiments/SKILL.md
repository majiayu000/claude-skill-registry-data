---
name: check-experiments
description: Standardized tmux experiment monitoring with progress parsing, CSV log reading, and status reporting
tags: [Experiment, Monitoring, tmux, ML]
---

# Check Experiments

Standardized workflow for checking all running ML experiments via tmux sessions.

## When to Use

- Checking experiment progress across multiple GPU runs
- Resuming a session and needing status of long-running experiments
- Monitoring hyperparameter sweeps or ablation studies
- Before starting new experiments (check resource availability)

## Workflow

### Step 1: List All tmux Sessions

```bash
tmux ls
```

Report each session: name, creation time, attached/detached status.

### Step 2: Capture Recent Output

For each session, capture the last 30-50 lines:

```bash
tmux capture-pane -t <session-name> -p | tail -50
```

### Step 3: Parse Progress

Look for common progress indicators in the output:
- **Epoch progress**: `Epoch X/Y` or `epoch: X`
- **Step progress**: `Step X/Y` or `X/Y iterations`
- **Percentage**: `XX.X%`
- **Loss values**: `loss: X.XXXX`, `val_loss: X.XXXX`
- **Metrics**: `accuracy`, `f1`, `auc`
- **ETA**: estimated time remaining

### Step 4: Check CSV/Log Files

If experiments write to CSV logs, read the latest entries:

```bash
# Find recent CSV logs
find . -name "*.csv" -newer <start-time> -type f

# Read last few rows
tail -5 <log-file.csv>
```

### Step 5: Check for Errors

Scan output for common failure patterns:
- `CUDA out of memory`
- `RuntimeError`
- `Traceback`
- `Error`
- `Killed` or `OOM`
- Stalled output (no new lines for extended period)

### Step 6: Generate Status Report

Output a structured report:

```
## Experiment Status Report

| Session | Status | Progress | Metric | ETA |
|---------|--------|----------|--------|-----|
| sweep-lr | Running | 45/100 epochs | loss: 0.234 | ~2h |
| ablation-1 | Running | 78% | acc: 0.891 | ~30min |
| baseline | Completed | 100/100 | loss: 0.198 | - |
| sweep-wd | Error | 23/100 | CUDA OOM | - |
```

### Step 7: Update experiments.md (if exists)

If `experiments.md` exists in the project, update it with:
- Current timestamp
- Status of each experiment
- Key metrics snapshot

## Important Rules

- **Report only** --- do NOT restart, modify, or stop any experiments
- **Do NOT create new tmux sessions** during status checks
- If an experiment has errored, report the error but do not attempt fixes unless asked
- Keep the report concise and actionable

## Integration

- Triggered by `/check-experiments` command
- `experiment-monitor.js` hook shows brief summary at session start
- `stop-summary.js` hook shows running session count at session end
