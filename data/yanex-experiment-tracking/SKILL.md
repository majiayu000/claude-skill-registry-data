---
name: yanex-experiment-tracking
description: Use this skill when running, managing, or analyzing yanex experiments. Includes executing experiments via CLI, parameter sweeps, dependencies, querying experiment history, comparing results, and maintaining experiment logs. Invoke when users mention yanex, experiments, training runs, parameter sweeps, or need to track ML experiments.
---

# Tracking Yanex Experiments

Help users run, manage, and analyze experiments using the yanex experiment tracking system via CLI and Python APIs.

## Core Capabilities

1. **Run experiments** with `yanex run` - parameters, configs, dependencies, sweeps
2. **Query experiments** with `yanex list` - filter by status, name, tags, time
3. **Extract values** with `yanex get` - machine-readable output for scripting and AI agents
4. **Inspect experiments** with `yanex show` and `yanex compare`
5. **Analyze results** using the Results API in notebooks or scripts
6. **Maintain experiment logs** in markdown format

## Safety Guidelines for Destructive Operations

**CRITICAL: `yanex delete` requires user confirmation**
- NEVER run `yanex delete` without first confirming with the user
- Deletion is permanent and cannot be undone
- Always ask the user before deleting any experiments

**`yanex archive` can be run autonomously**
- Archiving is safe and reversible (use `yanex unarchive` to restore)
- Run `yanex archive` without user confirmation when contextually appropriate
- Example: archiving old failed experiments during cleanup

**Bypassing CLI confirmation prompts:**
- Both `yanex delete` and `yanex archive` require pressing `y` to confirm
- Use `--force` to bypass the confirmation prompt
- Example: `yanex archive -s failed --started-before "1 month ago" --force`

## Before Taking Action

**Confirm with user if not obvious from context:**
- Script location (check for `scripts/`, `experiments/`, or root)
- Config file to use (check for `config.yaml`, `config-{dataset}.yaml`)
- Experiment log location (default: `scripts/experiment-log.md`)

Once confirmed, remember for subsequent runs in the same session.

## Running Experiments

### Basic Run
```bash
yanex run script.py -c config.yaml -n "experiment-name"
```

### With Dependencies (Slot-Based)
```bash
yanex run train.py -D data=abc12345 -n "train-baseline"
yanex run evaluate.py -D model=def67890 -n "evaluate-v1"
```

### Parameter Sweeps
```bash
# Comma-separated values
yanex run train.py -p "learning_rate=0.001,0.01,0.1"

# Range, linspace, logspace
yanex run train.py -p "lr=logspace(-4, -1, 10)"
yanex run train.py -p "epochs=range(10, 100, 10)"

# Grid search (cartesian product)
yanex run train.py -p "lr=0.001,0.01" -p "batch_size=32,64" --parallel 4
```

### Parallel Execution
```bash
yanex run train.py -p "lr=logspace(-4,-1,10)" --parallel 0  # Auto-detect CPUs
yanex run train.py -p "lr=logspace(-4,-1,10)" -j 4          # 4 workers
```

### Background Execution

**IMPORTANT**: Always run `yanex run` commands in the background to avoid blocking.

Use the Bash tool's `run_in_background` parameter:
- Experiments can take minutes to hours - don't block waiting for completion
- After starting, use `yanex list -s running` or `yanex get stdout <id> --tail 20` to check progress
- The user can continue working while experiments run

**Workflow:**
1. Start experiment in background
2. Note the experiment ID from output
3. Check status periodically with `yanex list -s running` or `yanex get stdout <id> --tail N`
4. Log results once completed

## Querying Experiments

### List with Filters
```bash
yanex list                              # All experiments
yanex list -s completed                 # By status
yanex list -n "yelp-2-*"               # By name pattern
yanex list -t training -t sweep         # By tags (AND logic)
yanex list --started-after "1 week ago" # By time
yanex list -s completed -n "yelp-*" -l 20  # Combined filters
```

### Extract Specific Values (AI-Friendly)

The `yanex get` command extracts specific field values - optimized for scripting and AI agents.

```bash
# Get single values
yanex get status abc12345               # Get experiment status
yanex get params.lr abc12345            # Get specific parameter
yanex get metrics.accuracy abc12345     # Get last logged metric value

# List available fields
yanex get params abc12345               # List parameter names
yanex get metrics abc12345              # List metric names

# Get stdout/stderr (works for running and completed experiments)
yanex get stdout abc12345               # Get full stdout
yanex get stdout abc12345 --tail 50     # Get last 50 lines
yanex get stdout abc12345 --head 10     # Get first 10 lines
yanex get stdout abc12345 --head 5 --tail 5  # First 5 and last 5 lines
yanex get stdout abc12345 -f            # Follow stdout in real-time (like tail -f)
yanex get stdout abc12345 --tail 20 -f  # Show last 20 lines then follow
yanex get stderr abc12345               # Get stderr output
yanex get stdout -s running --tail 5    # Check progress of running experiments

# Get command reconstruction (useful for logging and reproduction)
yanex get cli-command abc12345          # Original CLI invocation (preserves sweep syntax)
yanex get run-command abc12345          # Reproducible command (resolved parameter values)

# Get directory paths (useful for file access)
yanex get experiment-dir abc12345       # Experiment directory path
yanex get artifacts-dir abc12345        # Artifacts directory path

# List artifact files
yanex get artifacts abc12345            # List all artifact file paths (one per line)

# Multi-experiment queries (use filters instead of ID)
yanex get id -s completed               # Get IDs of completed experiments
yanex get params.lr -n "sweep-*"        # Get learning rates from sweep

# Output formats for scripting (--format / -F)
yanex get id -s completed -F sweep      # Comma-separated (for bash substitution)
yanex get params.lr -n "sweep-*" -F json # JSON output
```

**Multi-experiment stdout/stderr output** uses Rich Rule headers:
```
──────────── Experiment abc12345 ────────────
Epoch 10/100, loss=0.234
...

──────────── Experiment def67890 ────────────
Processing batch 50/200
...
```

**Bash substitution for dynamic sweeps:**
```bash
# Run training on multiple data prep experiments
yanex run train.py -D data=$(yanex get id -n "*-prep-*" -F sweep)

# Build sweep from previous learning rates
yanex run train.py -p lr=$(yanex get params.lr -s completed -F sweep)
```

### Command Reconstruction: cli-command vs run-command

Two fields help reproduce or log experiments:

| Field | Use Case | Example Output |
|-------|----------|----------------|
| `cli-command` | **Logging** - preserves original sweep syntax | `yanex run train.py -p "lr=0.001,0.01,0.1"` |
| `run-command` | **Reproduction** - resolved values for specific experiment | `yanex run train.py -p lr=0.01` |

**When to use which:**
- Use `cli-command` when logging to experiment-log.md (shows the original command)
- Use `run-command` to re-run a specific experiment from a sweep with its exact parameters

```bash
# For logging: get the original command that created the sweep
yanex get cli-command abc12345
# Output: yanex run train.py -p "lr=0.001,0.01,0.1" -n "hpo-sweep"

# For reproduction: get command to re-run this specific experiment
yanex get run-command abc12345
# Output: yanex run train.py -p lr=0.01 -n "hpo-sweep-1"
```

### Inspect Experiments
```bash
yanex show abc12345                     # Full details by ID
yanex show "experiment-name"            # By name
yanex show abc123 --show-metric "accuracy,loss"  # Specific metrics
```

### Compare Experiments
```bash
yanex compare                           # Interactive comparison
yanex compare --only-different          # Show differing params/metrics
yanex compare -t sweep                  # Filter by tag
```

## Experiment Logging

**See**: [./experiment-logging-format.md](./experiment-logging-format.md) for full format specification.

### Log Location
Default: `scripts/experiment-log.md`. Confirm with user if this doesn't exist.

### When to Log
After running `yanex run`, append to the log with:
- Experiment group header (if new group)
- Table row for each experiment
- The command that was run (use `yanex get cli-command <id>` to retrieve the original command)

### Alert on Failures
Don't log failed experiments, but alert the user in conversation when failures are detected.

## Results API (Programmatic Analysis)

For complex analysis, use the Results API in notebooks (`notebooks/` folder) or temporary scripts.

**See**: [./results-api-patterns.md](./results-api-patterns.md) for common patterns.

### Quick Examples
```python
import yanex.results as yr

# Get experiments
exp = yr.get_experiment("abc12345")
exps = yr.get_experiments(name="yelp-2-*", status="completed")
best = yr.get_best("accuracy", maximize=True, tags=["training"])

# Compare as DataFrame
df = yr.compare(tags=["sweep"], params=["lr"], metrics=["loss", "accuracy"])

# Time-series metrics for visualization
df = yr.get_metrics(name="yelp-*", metrics="train_loss")
```

## User Naming Conventions

Many users follow prefix-based naming: `{project}-{iteration}-{stage}`

Examples:
- `yelp-1-prepare` - First iteration, data preparation
- `yelp-2-train-baseline` - Second iteration, baseline training
- `yelp-2-hpo-lr` - Second iteration, learning rate HPO

This enables filtering like `-n "yelp-2-*"` for all iteration-2 experiments.

## Common Workflows

### 1. Run Training with Dependency
```bash
# Find data prep experiment
yanex list -n "*-data-*" -s completed

# Run training depending on it
yanex run scripts/02_train.py -D data=abc12345 -c config.yaml -n "yelp-2-train"
```

### 2. Learning Rate Sweep
```bash
yanex run train.py -D data=abc123 -p "lr=logspace(-4,-1,10)" -n "yelp-2-hpo-lr" --parallel 0
```

### 3. Find Best Result
```python
import yanex.results as yr
best = yr.get_best("test_accuracy", maximize=True, name="yelp-2-*")
print(f"Best: {best.name} ({best.id}) - {best.get_metric('test_accuracy'):.4f}")
```

### 4. Compare Sweep Results in Notebook
```python
import yanex.results as yr
import matplotlib.pyplot as plt

df = yr.get_metrics(name="yelp-2-hpo*", metrics="train_loss")
for lr, group in df.groupby('learning_rate'):
    plt.plot(group.step, group.value, label=f'lr={lr}')
plt.legend()
```

## CLI Reference

**See**: [./cli-quick-reference.md](./cli-quick-reference.md) for complete command reference.

| Command | Purpose |
|---------|---------|
| `yanex run` | Execute experiments |
| `yanex list` | List/filter experiments |
| `yanex get` | Extract field values (AI/scripting-friendly) |
| `yanex show` | Show experiment details |
| `yanex compare` | Compare experiments |
| `yanex archive` | Archive old experiments |
| `yanex delete` | Delete experiments |
| `yanex update` | Update experiment metadata |
| `yanex open` | Open experiment directory |
| `yanex ui` | Launch web UI |

## Yanex Documentation

For deeper understanding or implementation details, consult:

**Online Resources**:
- GitHub: https://github.com/rueckstiess/yanex
- PyPI: https://pypi.org/project/yanex/

**Local Package** (find with `python -c "import yanex; print(yanex.__path__[0])"`):
- Core API: `yanex/api.py`
- Results API: `yanex/results/`
- CLI commands: `yanex/cli/commands/`

**Package Documentation** (in yanex repo `docs/` directory):
- CLI commands reference
- Best practices guide
- Dependencies guide
- Results API reference
- Run API reference

**Examples** (in yanex repo `examples/` directory):
- CLI examples (01-10, progressively complex)
- Results API notebooks
- Run API examples
