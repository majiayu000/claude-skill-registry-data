---
name: compare
description: Same-epoch comparison and analysis of training runs across wandb, neptune, tensorboard, mlflow, or local result files. Aligns runs at the student's current step (never current-vs-final-of-baseline) and separates proxy metrics from downstream targets. Also writes run summaries and experiment reports, analyzes ablations, and monitors training. Use when the user asks to compare runs, check if a run is improving, track lag against a baseline, rank experiments, evaluate run-vs-run performance, analyze results, write a training report or experiment summary, summarize training results, monitor training, or asks which run is best.
---

# Compare: same-epoch run comparison across trackers

The most common comparison error is reporting "run A is 4 percentage points behind baseline" when run A is at epoch 11 of 100 and the baseline number is from epoch 100. The student is _still training_; the comparison is meaningless. This skill enforces same-epoch alignment.

The agentic Stop hook routes here from `reason` when an assistant reports a delta without aligning the runs.

If the question is "why did X fail / diverge / underperform", go to `/labrat:debug` first.

## Auto-detect the tracker

Check in this order:

1. `WANDB_API_KEY` env var set, or `wandb` imports or a `*.yaml` config with wandb keys in the project → **wandb**
2. `NEPTUNE_API_TOKEN` env var set, or a `*.yaml` config with neptune keys → **neptune**
3. `MLFLOW_TRACKING_URI` env var set, or `mlruns/` dir present → **mlflow**
4. `runs/` or `lightning_logs/` dir present → **tensorboard**
5. `*results*.json` / `*meta*.json` / `eval*.csv` files in run dirs → **local file format**: read one sample file and write the analysis code for that format, not a hardcoded script

If none, ask the user where metrics live before guessing.

## The protocol

### 1. Identify the runs

Get full names (no shortcodes). If the user says "run-b vs the baseline", clarify:

- which `run-b` run (project + entity + run-id)
- which baseline (full run name; baselines often have several variants)

### 2. Fetch metric history (not just final value)

You need the full curve, not the last reported value. Final-value-only comparisons hide convergence dynamics.

For wandb:

```python
import wandb
api = wandb.Api()
run = api.run("entity/project/run-id")
history = run.history(samples=10000)  # full history, not just summary
```

For tensorboard, parse the event files (`tensorboard.backend.event_processing.event_accumulator.EventAccumulator`).

For neptune / mlflow, use their respective APIs.

### 3. Find the student's current step

The student is the run still in progress (or the one being evaluated). Get its current epoch / step from the latest history row.

### 4. Slice the baseline at the same step

This is the critical step. The baseline went all the way to (say) epoch 100. The student is at epoch 11. Pull the baseline's metrics _at epoch 11_, not at epoch 100.

```python
student_step = student_history['epoch'].max()
baseline_at_same_step = baseline_history[baseline_history['epoch'] == student_step]
```

If the baseline doesn't have an exactly-matching step, interpolate or pick the nearest. State which.

### 5. Separate proxy metrics from downstream

Most ML pipelines have a _proxy metric_ (cheap, computed during training, kNN accuracy on features, loss, perplexity) and a _target downstream metric_ (expensive, computed periodically or only at the end, finetuned linear probe accuracy, downstream task F1).

The proxy is for tracking convergence; the target is what the project is actually optimizing. Reporting only the proxy can mislead, a run that lags on kNN may close the gap on downstream finetune. Report both, separately:

```
                        | student (ep 11) | baseline (ep 11) | delta |
| proxy (kNN top-1)     | 36.4%           | 38.9%            | -2.5  |
| downstream (linear)   | not yet         | 42.1%            | n/a   |
```

If the user only has proxy data, say so explicitly. Never declare a winner from proxy alone.

### 6. Run names in output

In every line of the report, use full run names. Never `run-a vs run-b`; always `imagenet-resnet50-baseline-bs256 vs imagenet-resnet50-distill-from-vit-l`. Future-you reading this will not remember the shortcode.

## Anti-patterns

- "X is behind baseline by 4pp": without saying _at what step_. Almost always wrong.
- "X has converged": without showing the last 5 epochs of the curve.
- "Best run is Y": based on a metric that was logged differently across runs (different reduction, different eval set).
- Single-seed comparison treated as definitive. Note variance if known; otherwise label as single-seed.

## Output

Compact comparison table per metric pair (proxy + downstream). Each row aligned at the student's current step. Each cell traceable to a specific tracker run-id and step. End with one or two sentences interpreting the comparison, `student is on track to catch up at step N, projected from current slope` is a useful framing; `student is winning / losing` is rarely warranted before convergence.

## Beyond two runs: ranking, reports, ablations, monitoring

### Ranking many runs

Compare runs across more than the primary metric:

- Primary metrics (accuracy, F1, loss)
- Training dynamics (convergence speed, stability)
- Resource usage (GPU hours, memory, cost)
- Hyperparameter differences

Put them in the Results Table of the experiment report below, and identify:

- Best overall run
- Best run per metric
- Most efficient run (best metric per GPU hour)
- Runs that crashed or had anomalies

### Ablation analysis

1. Identify the baseline run
2. For each ablation, compute the delta from baseline
3. Rank by impact magnitude
4. Check for interaction effects (A+B != A + B individually)
5. To choose which ablations go in the paper, hand these deltas to Ablation Selection in `/labrat:rebuttal`

### Experiment report

When the user asks for a report or summary:

```
## Experiment Report

### Overview
- Total runs: N
- Date range: start to end
- Best result: [metric] = [value] (run [name])

### Results Table
| Run | Step | Config Diff | Proxy | Downstream | GPU Hours | Status |
|-----|------|-------------|-------|------------|-----------|--------|

### Key Findings
1. [Finding with evidence]
2. [Finding with evidence]

### Recommendations
1. [Next experiment to try, with justification]
```

Align every Results Table row at the same step and keep proxy and downstream apart, as in Output above.

### Training monitoring

Set up periodic monitoring:

- Check if training is still running (GPU utilization, log freshness)
- Track metric progression
- Alert on anomalies (loss spike, NaN, OOM)
- Notify when training completes

Create a CronCreate job on `*/10 * * * *` that pipes a `{"title", "message"}` JSON object to the plugin notifier, which forwards it to whatever `/labrat:setup` configured (ntfy, Slack or email):

```bash
echo "{\"title\": \"Training check\", \"message\": \"GPU util: $(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader)\"}" | ${CLAUDE_PLUGIN_ROOT}/scripts/notify.sh
```
