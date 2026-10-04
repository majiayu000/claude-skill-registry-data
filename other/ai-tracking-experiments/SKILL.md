---
name: ai-tracking-experiments
description: Track which optimization experiment was best. Use when you have run multiple optimization passes, need to compare experiments, want to reproduce past results, need to pick the best prompt configuration, track experiment costs, manage optimization artifacts, decide which optimized program to deploy, or justify your choice to stakeholders. Also used for MLflow prompt experiment tracking, Weights and Biases for LLM experiments, A/B testing AI prompts, compare model performance across runs, version control for prompts, prompt experiment tracking, track prompt versions, reproduce my best AI configuration, optimization history, rollback to previous prompt version, AI experiment dashboard, which optimization run was best.
---

# Track Which Optimization Experiment Was Best

Guide the user through logging, comparing, and managing optimization experiments. The pattern: run experiments systematically, log everything, compare results, promote the winner to production.

## When you do NOT need this

- **You have run only 1-2 experiments** — just compare outputs directly, no tracking infrastructure needed
- **You are still iterating on the program itself** — stabilize your module and metric first, then track experiments
- **You just want to optimize once and deploy** — use `/ai-improving-accuracy` instead

## When you need this

- You've run 5+ optimization experiments and lost track of which was best
- "The intern ran experiments, which .json file is the good one?"
- You need to justify to stakeholders why you picked a specific approach
- You want to reproduce last week's best experiment with more data
- You're comparing optimizers, models, or hyperparameters

## How it's different from improving accuracy

| | Improving accuracy (`/ai-improving-accuracy`) | Tracking experiments (this skill) |
|---|---|---|
| Focus | Running a single optimization pass | Managing the full experimental lifecycle |
| Output | An optimized program | A comparison of all runs with the winner promoted |
| Question | "How do I make this better?" | "Which of our 8 optimization runs was best?" |

## Step 1: Understand the setup

Ask the user:
1. **How many experiments have you run?** (2-3 → file-based tracking. 10+ → consider W&B Weave or LangWatch)
2. **What varied between runs?** (optimizer, model, training data, hyperparameters?)
3. **Do you have an existing tracking tool?** (W&B, MLflow, etc.)
4. **Do multiple people run experiments?** (solo → file-based. Team → shared tool)

## Step 2: Lightweight experiment tracking (no extra tools)

A JSONL file is all you need to start. Each line records one experiment run:

```python
import json
from datetime import datetime

EXPERIMENT_LOG = "experiments.jsonl"

def log_experiment(run):
    """Log a single experiment run."""
    run["timestamp"] = datetime.now().isoformat()
    with open(EXPERIMENT_LOG, "a") as f:
        f.write(json.dumps(run) + "\n")

def load_experiments(path=EXPERIMENT_LOG):
    """Load all experiment runs."""
    with open(path) as f:
        return [json.loads(line) for line in f]
```

### What to log for each run

```python
run = {
    "name": "mipro-medium-gpt4o-mini",       # Human-readable name
    "optimizer": "MIPROv2",                    # Which optimizer
    "optimizer_config": {"auto": "medium"},    # Optimizer settings
    "model": "openai/gpt-4o-mini",            # or "anthropic/claude-sonnet-4-5-20250929", etc.
    "trainset_size": 200,                      # Training examples used
    "devset_size": 50,                         # Evaluation examples
    "metric": "answer_quality",                # Which metric
    "score": 0.84,                             # Score on devset
    "baseline_score": 0.65,                    # Score before optimization
    "improvement": 0.19,                       # Delta
    "cost_usd": 4.50,                          # API cost for this run
    "duration_minutes": 12,                    # Wall clock time
    "artifact_path": "artifacts/mipro_medium_gpt4o_mini.json",  # Saved program
    "notes": "Best so far. Instruction quality seems high.",
}
log_experiment(run)
```

## Step 3: Run and log experiments systematically

Template function that runs one experiment end-to-end:

```python
import dspy
import time
from dspy.evaluate import Evaluate

def run_experiment(
    name,
    program_class,
    optimizer_class,
    optimizer_kwargs,
    trainset,
    devset,
    metric,
    model="openai/gpt-4o-mini",  # or "anthropic/claude-sonnet-4-5-20250929", etc.
    artifact_dir="artifacts",
):
    """Run one optimization experiment and log results."""
    import os
    os.makedirs(artifact_dir, exist_ok=True)

    # Configure
    lm = dspy.LM(model)  # or "anthropic/claude-sonnet-4-5-20250929", etc.
    dspy.configure(lm=lm)
    program = program_class()

    # Baseline
    evaluator = Evaluate(devset=devset, metric=metric, num_threads=4)
    baseline_score = evaluator(program)

    # Optimize
    start = time.time()
    optimizer = optimizer_class(**optimizer_kwargs)
    optimized = optimizer.compile(program, trainset=trainset)
    duration = (time.time() - start) / 60

    # Evaluate optimized
    score = evaluator(optimized)

    # Save artifact
    artifact_path = f"{artifact_dir}/{name}.json"
    optimized.save(artifact_path)

    # Log
    run = {
        "name": name,
        "optimizer": optimizer_class.__name__,
        "optimizer_config": optimizer_kwargs,
        "model": model,
        "trainset_size": len(trainset),
        "devset_size": len(devset),
        "metric": metric.__name__,
        "baseline_score": baseline_score,
        "score": score,
        "improvement": score - baseline_score,
        "duration_minutes": round(duration, 1),
        "artifact_path": artifact_path,
    }
    log_experiment(run)

    print(f"[{name}] {baseline_score:.1f}% -> {score:.1f}% (+{score - baseline_score:.1f}%)")
    return optimized, run
```

### Run a batch of experiments

```python
experiments = [
    {
        "name": "bootstrap-4demos",
        "optimizer_class": dspy.BootstrapFewShot,
        "optimizer_kwargs": {"metric": metric, "max_bootstrapped_demos": 4},
    },
    {
        "name": "bootstrap-8demos",
        "optimizer_class": dspy.BootstrapFewShot,
        "optimizer_kwargs": {"metric": metric, "max_bootstrapped_demos": 8},
    },
    {
        "name": "mipro-light",
        "optimizer_class": dspy.MIPROv2,
        "optimizer_kwargs": {"metric": metric, "auto": "light"},
    },
    {
        "name": "mipro-medium",
        "optimizer_class": dspy.MIPROv2,
        "optimizer_kwargs": {"metric": metric, "auto": "medium"},
    },
]

results = []
for exp in experiments:
    optimized, run = run_experiment(
        name=exp["name"],
        program_class=MyProgram,
        optimizer_class=exp["optimizer_class"],
        optimizer_kwargs=exp["optimizer_kwargs"],
        trainset=trainset,
        devset=devset,
        metric=metric,
    )
    results.append(run)
```

## Step 4: Compare experiments

### Display comparison table

```python
def compare_experiments(path=EXPERIMENT_LOG, sort_by="score"):
    """Load experiments and display a comparison table."""
    runs = load_experiments(path)
    runs.sort(key=lambda r: r.get(sort_by, 0), reverse=True)

    # Header
    print(f"{'Name':<30} {'Optimizer':<20} {'Model':<22} {'Score':>7} {'Improve':>8} {'Cost':>7}")
    print("-" * 120)

    for r in runs:
        name = r.get("name", "?")[:29]
        opt = r.get("optimizer", "?")[:19]
        model = r.get("model", "?")[:21]
        score = r.get("score", 0)
        improvement = r.get("improvement", 0)
        cost = r.get("cost_usd", 0)

        print(f"{name:<30} {opt:<20} {model:<22} {score:>6.1f}% {improvement:>+7.1f}% ${cost:>5.2f}")

compare_experiments()
# Name                           Optimizer            Model                   Score  Improve    Cost
# ------------------------------------------------------------------------------------------------------------------------
# mipro-medium                   MIPROv2              openai/gpt-4o-mini       84.0%   +19.0%  $4.50
# mipro-light                    MIPROv2              openai/gpt-4o-mini       78.0%   +13.0%  $1.20
# bootstrap-8demos               BootstrapFewShot     openai/gpt-4o-mini       74.0%    +9.0%  $0.30
# bootstrap-4demos               BootstrapFewShot     openai/gpt-4o-mini       71.0%    +6.0%  $0.15
```

### Filter experiments

```python
def filter_experiments(path=EXPERIMENT_LOG, **filters):
    """Filter experiments by any field."""
    runs = load_experiments(path)

    for key, value in filters.items():
        if key == "min_score":
            runs = [r for r in runs if r.get("score", 0) >= value]
        elif key == "optimizer":
            runs = [r for r in runs if r.get("optimizer") == value]
        elif key == "model":
            runs = [r for r in runs if r.get("model") == value]

    return runs

# Only MIPROv2 runs
mipro_runs = filter_experiments(optimizer="MIPROv2")

# Runs scoring above 80%
good_runs = filter_experiments(min_score=80.0)
```

## Step 5: Promote best experiment to production

```python
import shutil

def promote_experiment(name, production_path="production/optimized.json"):
    """Copy the winning experiment's artifact to the production path."""
    import os
    runs = load_experiments()

    run = next((r for r in runs if r["name"] == name), None)
    if not run:
        print(f"Experiment '{name}' not found")
        return

    os.makedirs(os.path.dirname(production_path), exist_ok=True)
    shutil.copy2(run["artifact_path"], production_path)

    # Log the promotion
    promotion = {
        "event": "promotion",
        "experiment_name": name,
        "score": run["score"],
        "source_artifact": run["artifact_path"],
        "production_path": production_path,
        "timestamp": datetime.now().isoformat(),
    }
    with open("promotions.jsonl", "a") as f:
        f.write(json.dumps(promotion) + "\n")

    print(f"Promoted '{name}' (score: {run['score']:.1f}%) to {production_path}")

# Promote the best experiment
promote_experiment("mipro-medium")
# Promoted 'mipro-medium' (score: 84.0%) to production/optimized.json
```

### Load the promoted program in production

```python
# In your production code
program = MyProgram()
program.load("production/optimized.json")
```

## Step 6: Use W&B Weave (for teams)

For teams running many experiments, W&B Weave adds visual dashboards and collaboration:

```bash
pip install weave
```

```python
import weave

weave.init("my-project")

@weave.op()
def run_optimization(optimizer_name, model, trainset, devset, metric):
    """Tracked optimization run — Weave logs inputs, outputs, and cost."""
    lm = dspy.LM(model)
    dspy.configure(lm=lm)

    program = MyProgram()
    optimizer = dspy.MIPROv2(metric=metric, auto="medium")
    optimized = optimizer.compile(program, trainset=trainset)

    evaluator = Evaluate(devset=devset, metric=metric, num_threads=4)
    score = evaluator(optimized)

    return {"score": score, "optimizer": optimizer_name, "model": model}

# Weave auto-tracks everything — view at wandb.ai
result = run_optimization("mipro-medium", "openai/gpt-4o-mini", trainset, devset, metric)
```

For in-depth Weave setup, see `/dspy-weave`. For MLflow experiment tracking, see `/dspy-mlflow`.

## Step 7: Use LangWatch (for real-time optimizer progress)

LangWatch shows optimizer progress as it runs — useful for long optimization runs:

```bash
pip install langwatch
```

```python
import langwatch

langwatch.init()

# LangWatch tracks DSPy optimizer steps in real-time
optimizer = dspy.MIPROv2(metric=metric, auto="heavy")
optimized = optimizer.compile(program, trainset=trainset)
# Watch progress at app.langwatch.ai
```

For the full LangWatch guide (auto-tracing, optimizer dashboard, self-hosted), see `/dspy-langwatch`.

## Gotchas

- **GEPA takes metric in the constructor, not compile().** Unlike BootstrapFewShot and MIPROv2, GEPA accepts `metric` only as a constructor parameter. Passing `metric=metric` to `compile()` raises a TypeError. Always pass metric when instantiating: `dspy.GEPA(metric=metric, auto="light")`.
- **Comparing scores across different devsets is meaningless.** Claude sometimes generates experiments that evaluate on different subsets. All experiments being compared must use the exact same devset, loaded once and passed to every run. If devset changes, scores are not comparable.
- **Forgetting to save the artifact path makes experiments irreproducible.** Claude logs the score but skips `optimized.save()`. Without the saved .json artifact, you cannot reload or deploy the winning experiment. Always call `optimized.save(path)` and log the path.
- **MIPROv2 auto default is "light", not "medium".** Claude often writes `dspy.MIPROv2(metric=metric)` assuming medium optimization. The default `auto="light"` runs fewer trials. Explicitly set `auto="medium"` or `auto="heavy"` when you want more thorough optimization.
- **Logging cost requires manual tracking — DSPy does not auto-report it.** Claude sometimes writes `run["cost"] = optimizer.cost` as if DSPy tracks API costs. It does not. Track cost via your LM provider dashboard or by wrapping calls with a cost-tracking callback.

## Key patterns

- **Log from day one**: even if you only have 2 experiments now, you'll have 20 next month
- **Log the artifact path**: an experiment without a saved .json file is useless
- **Compare on the same devset**: scores from different devsets aren't comparable
- **Track cost**: "20% better accuracy for 10x the cost" is a real tradeoff
- **Promote explicitly**: don't just copy files — log which experiment is in production
- **Start file-based, upgrade later**: JSONL tracking works fine until you have a team

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Run optimization passes** — see `/ai-improving-accuracy`
- **Compare the same optimizer across models** — see `/ai-switching-models`
- **Reduce experiment costs** — see `/ai-cutting-costs`
- **Monitor promoted experiments in production** — see `/ai-monitoring`
- **W&B Weave setup** (team dashboards, run comparison) — see `/dspy-weave`
- **MLflow setup** (experiment tracking, model registry) — see `/dspy-mlflow`
- **LangWatch setup** (real-time optimizer progress) — see `/dspy-langwatch`
- **MIPROv2 optimizer** — see `/dspy-miprov2`
- **BootstrapFewShot optimizer** — see `/dspy-bootstrap-few-shot`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples, see [examples.md](examples.md)
- For API signatures (Evaluate, BootstrapFewShot, MIPROv2, save/load), see [reference.md](reference.md)
