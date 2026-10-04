---
name: ai-watching-optimization
description: See what is happening during optimizer.compile() instead of waiting blind. Use when you want to watch optimization progress, see scores as they come in, know if your optimizer is working, check if optimization is stuck, understand why optimization is taking too long, get live progress during compile, monitor convergence, detect overfitting during optimization, interpret optimization results, or pick the right tool for watching optimization. Also used for optimizer progress bar, is my optimizer doing anything, optimization seems stuck, how long will optimization take, watch GEPA run, watch MIPROv2 run, live optimization dashboard, optimizer not improving, scores not going up, optimization taking forever, see what optimizer is doing, debug slow optimization, optimization visibility, optimizer metrics, track compile progress, optimization observability.
---

# Watch What Happens During Optimization

Guide the user through monitoring their `optimizer.compile()` runs so they can see progress, catch problems early, and know when to stop.

## The problem

You run `optimizer.compile(program, trainset=trainset)` and wait. Minutes pass. Sometimes hours. You have no idea if scores are improving, if the optimizer is stuck, or if you should stop and try something different.

This skill helps you pick the right monitoring approach and interpret what you see.

## What you can observe

| Observable | Why it matters | Tools that show it |
|-----------|---------------|-------------------|
| Scores over time | Are they improving? Plateauing? Dropping? | All tools below |
| Instructions evolving | What is the optimizer changing in your prompts? | GEPA logger (prompt diffs), LangWatch (predictor states) |
| Cost accumulating | How much are you spending? Worth continuing? | LangWatch, MLflow |
| Convergence pattern | Should you stop early or keep going? | All tools below (scores over time) |
| LM calls | Is the optimizer calling the right model? | inspect_history, LangWatch, MLflow |
| Acceptance decisions | Why did the optimizer accept/reject a candidate? | GEPA logger (event log), BaseCallback |

## Pick your tool

### Decision tree

1. **Using GEPA?**
   - Want a web dashboard? -> dspy-gepa-logger (Option 2)
   - Just want basic stats? -> `track_stats=True` (Option 1)
2. **Using MIPROv2, BFS, BRS, or COPRO?**
   - Want a cloud dashboard with live scores? -> LangWatch (Option 3)
   - Want a local dashboard? -> MLflow (Option 4)
   - Just want console output? -> `MIPROv2(verbose=True)` or BaseCallback (Option 1)
3. **Any optimizer, post-hoc?**
   - `inspect_history()` always works (Option 1)

### Comparison

| Tool | Optimizers | Setup | Dashboard | Local/Cloud |
|------|-----------|-------|-----------|-------------|
| `MIPROv2(verbose=True)` | MIPROv2 only | One flag | No (console) | Local |
| Built-in (`track_stats`) | GEPA only | One flag | No (dict after compile) | Local |
| Built-in (`BaseCallback`) | All | ~20 lines | No (console) | Local |
| `inspect_history(n)` | All (post-hoc) | Zero setup | No (console) | Local |
| dspy-gepa-logger | GEPA only | `pip install` | Yes (web) | Local |
| LangWatch | BFS/BRS/COPRO/MIPROv2 | `pip install` + API key | Yes (cloud) | Cloud |
| MLflow | All (via autolog) | `pip install` | Yes (local) | Local |

## Option 1 - Built-in (zero dependencies)

### Always do this - baseline evaluation

Run `dspy.Evaluate` before AND after optimization. Without a baseline, you cannot tell if optimization helped.

```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(devset=devset, metric=your_metric, num_threads=8)

# Before optimization
baseline_score = evaluator(program)
print(f"Baseline: {baseline_score}")

# Run optimizer
optimized = optimizer.compile(program, trainset=trainset)

# After optimization
optimized_score = evaluator(optimized)
print(f"Optimized: {optimized_score}")
print(f"Improvement: {optimized_score - baseline_score:+.1f}")
```

### GEPA - track_stats=True

GEPA supports a built-in stats flag that records detailed results per iteration.

```python
# GEPA has no task_lm constructor param -- set the task LM via dspy.configure(lm=task_lm) before this
optimizer = dspy.GEPA(
    metric=your_metric,
    reflection_lm=reflection_lm,
    track_stats=True,  # Enable tracking (defaults to False in GEPA)
)

optimized = optimizer.compile(program, trainset=trainset)

# Inspect results after compilation -- detailed_results is on the compiled program
stats = optimized.detailed_results
for iteration, result in enumerate(stats):
    print(f"Iteration {iteration}: score={result['score']:.3f}")
```

### Any optimizer - custom BaseCallback

Write a callback that prints progress as the optimizer evaluates candidates.

```python
import dspy

class OptimizationProgressCallback(dspy.BaseCallback):
    def __init__(self):
        super().__init__()
        self.eval_count = 0

    def on_evaluate_end(self, instance, inputs, outputs, exception):
        self.eval_count += 1
        score = outputs.get("score", None)
        if score is not None:
            print(f"[Eval {self.eval_count}] Score: {score:.3f}")

# Register the callback
progress = OptimizationProgressCallback()
dspy.configure(callbacks=[progress])

# Now run your optimizer -- progress prints automatically
optimized = optimizer.compile(program, trainset=trainset)
```

### Post-hoc - inspect_history

After optimization completes (or if you interrupt it), inspect recent LM calls.

```python
# Show the last 5 LM calls
dspy.inspect_history(n=5)
```

This shows the full prompt and completion for each call, useful for verifying the optimizer is calling the correct model and seeing what instructions it tried.

## Option 2 - GEPA Logger (web dashboard)

A drop-in replacement for GEPA's internal logger that adds a web dashboard with real-time stats, eval tables, and prompt diffs.

```bash
pip install dspy-gepa-logger
```

```python
import dspy
from dspy_gepa_logger import GEPALogger

# Create the logger (starts web dashboard on port 3000)
logger = GEPALogger()

# GEPA has no task_lm constructor param -- set it via dspy.configure(lm=task_lm) before this
optimizer = dspy.GEPA(
    metric=your_metric,
    reflection_lm=reflection_lm,
)

# Register the logger as an observer
optimizer.register_observer(logger)

optimized = optimizer.compile(program, trainset=trainset)
```

The dashboard shows:

- **Real-time scores** as iterations progress
- **Eval tables** with per-example pass/fail
- **Prompt diffs** showing how instructions changed between iterations
- **LM call logs** with full prompts and completions
- **Event timeline** with 8 event types (SeedValidation, Reflection, ValsetEval, etc.)

The web dashboard requires Node.js and uses SQLite for storage.

For detailed GEPA usage, see `/dspy-gepa`.

## Option 3 - LangWatch (cloud dashboard)

LangWatch patches DSPy optimizers to stream live progress to a cloud dashboard. This is the only tool that shows real-time optimizer progress for non-GEPA optimizers.

```bash
pip install langwatch
```

```python
import langwatch
import dspy

langwatch.dspy.init(experiment="my-optimization-run")

optimizer = dspy.MIPROv2(metric=your_metric, auto="light")
optimized = optimizer.compile(program, trainset=trainset)
```

The LangWatch dashboard shows:

- **Live scores** updating as each candidate is evaluated
- **Cost tracking** so you know how much the optimization is spending
- **Predictor states** showing the current instructions and demos for each module
- **Run comparison** across multiple optimization experiments

**Supported optimizers:** BootstrapFewShot, BootstrapFewShotWithRandomSearch, COPRO, MIPROv2.

**Not supported:** GEPA (use dspy-gepa-logger instead).

Requires a LangWatch API key. Free tier available at app.langwatch.ai.

For detailed setup, see `/dspy-langwatch`.

## Option 4 - MLflow (local dashboard)

MLflow's DSPy autolog captures optimization as parent/child runs with traces.

```bash
pip install mlflow
```

```python
import mlflow
import dspy

mlflow.dspy.autolog(log_compiles=True)

# Set up experiment
mlflow.set_experiment("my-optimization")

with mlflow.start_run():
    optimizer = dspy.MIPROv2(metric=your_metric, auto="light")
    optimized = optimizer.compile(program, trainset=trainset)
```

```bash
# View results
mlflow ui
# Open http://localhost:5000
```

The MLflow dashboard shows:

- **Parent run** for the optimization, child runs for each candidate
- **Metrics** logged per candidate (score, parameters tried)
- **Traces tab** showing individual LM calls
- **Artifacts** including the optimized program state

Works with all optimizers via autolog.

For detailed setup, see `/dspy-mlflow`.

## Interpreting what you see

This is the most important section. Knowing which tool to use is step one. Knowing what the data means is what saves you hours.

### Converging?

- **Scores climbing then plateauing** -- good. The optimizer found improvements and saturated. You can stop.
- **Scores climbing steadily** -- keep going. The optimizer is still finding improvements.
- **Flat from the start** -- the optimizer is not finding better candidates. Possible causes:
  - Your metric is saturated (already near 100%)
  - Your metric is broken (always returns the same score)
  - The search space is too constrained
  - The task is too easy for optimization to help

### Overfitting?

If you have a separate validation set:

- **Train score up, val score also up** -- good. Real improvement.
- **Train score up, val score flat or dropping** -- overfitting. The optimizer is memorizing training examples.
  - Fix: use a larger, more diverse trainset
  - Fix: reduce the optimization budget (fewer iterations)
  - Fix: keep train and val sets strictly separate

```python
# Always evaluate on held-out data
eval_train = Evaluate(devset=trainset, metric=your_metric)
eval_val = Evaluate(devset=valset, metric=your_metric)

train_score = eval_train(optimized)
val_score = eval_val(optimized)
print(f"Train: {train_score}, Val: {val_score}")
if train_score - val_score > 10:
    print("Warning: possible overfitting")
```

### Stuck?

- **Same score for many iterations** -- the optimizer cannot find better candidates.
  - GEPA: check if the reflection LM is providing useful feedback. Try a stronger reflection model.
  - MIPROv2: try a heavier preset (`auto="medium"` or `auto="heavy"`).
  - BootstrapFewShot: increase `max_bootstrapped_demos` or `max_labeled_demos`.
  - Any optimizer: check if your metric has enough granularity (binary pass/fail gives less signal than a 0-1 float score).

### When to stop early?

- **Plateaued for 5+ iterations** -- diminishing returns. Stop and use the best so far.
- **Most improvement happens in the first 30-50% of budget** -- if you have seen minimal gains in the second half, further iterations are unlikely to help.
- **Cost per improvement point increasing** -- track cost alongside score. When each additional point costs 10x more than the previous, you have hit practical limits.

### Wrong model being called?

A common bug: the optimizer or your program is calling a different LM than you intended.

- **inspect_history**: look at the model name in the prompt headers
- **LangWatch dashboard**: shows which model each call uses
- **Fix**: make sure you called `dspy.configure(lm=...)` and that per-module LM assignments are correct

```python
# Check what model was actually used
dspy.inspect_history(n=1)
# Look for the model identifier in the output
```

### Cost signals

- Track total cost as optimization runs. Compare cost-per-point-of-improvement across iterations.
- If early iterations gave +5 points for $2, and recent iterations gave +0.5 points for $2, you are in diminishing returns territory.
- LangWatch shows cost natively. For other tools, estimate from token counts and model pricing.

## Gotchas

1. **`track_stats` means different things in GEPA vs MIPROv2.** In GEPA, `track_stats` defaults to `False` -- setting it to `True` populates `optimized.detailed_results` on the compiled program (not the optimizer) with per-iteration data. In MIPROv2, `track_stats=True` is already the default and controls internal bookkeeping -- it does not produce a `detailed_results` attribute you can inspect. For live MIPROv2 progress, use `verbose=True`, BaseCallback, or LangWatch.
2. **LangWatch does not support GEPA.** LangWatch patches BFS/BRS/COPRO/MIPROv2 internals. For GEPA monitoring, use dspy-gepa-logger.
3. **Always run baseline evaluation.** Without a before score, you cannot tell if optimization helped. This is the most common mistake.
4. **Flat score does not mean the optimizer is broken.** It could mean your metric is saturated, your metric is broken (always returns the same value), or the task does not benefit from optimization.
5. **`inspect_history()` is post-hoc, not live.** It shows recent LM calls from memory. It does not stream progress during optimization.

## Additional resources

- For API signatures and parameter tables, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **GEPA optimizer details** -- see `/dspy-gepa`
- **MIPROv2 optimizer details** -- see `/dspy-miprov2`
- **LangWatch setup and features** -- see `/dspy-langwatch`
- **MLflow setup and features** -- see `/dspy-mlflow`
- **Arize Phoenix tracing** -- see `/dspy-phoenix`
- **Experiment tracking** for comparing completed runs -- see `/ai-tracking-experiments`
- **Improving accuracy** for the full measure-improve-verify loop -- see `/ai-improving-accuracy`
- **Cutting costs** when optimization is too expensive -- see `/ai-cutting-costs`
- **Install `/ai-do` if you do not have it** -- it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
