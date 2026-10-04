---
name: dspy-mlflow
description: Use MLflow for DSPy tracing, experiment tracking, and model registry. Use when you want to set up MLflow, mlflow.dspy.autolog, MLflow Tracing, MLflow experiment tracking, MLflow model registry, or full ML lifecycle management. Also used for mlflow setup, pip install mlflow, mlflow.set_experiment, mlflow UI, mlflow model versioning, mlflow OpenTelemetry, mlflow vs wandb, mlflow tracing DSPy, register DSPy model.
---

# MLflow — Full ML Lifecycle for DSPy

Guide the user through using MLflow for DSPy auto-tracing, experiment tracking, model registry, and production deployment.

## Step 1 — Clarify setup goals

Before writing integration code, ask:

1. **What is your primary goal?** Tracing only (debug prompts and latency), experiment tracking (compare optimizer runs), model registry (version and promote optimized programs), or all three?
2. **Local or hosted?** Local MLflow server (`mlflow ui`) or a hosted instance (Databricks, AWS, GCP)?
3. **Existing project?** Adding MLflow to an existing DSPy pipeline, or starting fresh?
4. **Team size?** Solo (local server is fine) or collaborative (needs remote tracking server and auth)?

## What is MLflow

MLflow is an open-source platform for the complete ML lifecycle. Its DSPy integration provides:

- **Auto-tracing**: `mlflow.dspy.autolog()` traces all DSPy calls via OpenTelemetry
- **Experiment tracking**: log parameters, metrics, and artifacts for optimization runs
- **Model registry**: version and stage optimized DSPy programs
- **MLflow UI**: local web UI for viewing traces, comparing experiments, and managing models

### Key difference from Langtrace/Phoenix/Weave

MLflow covers the **full ML lifecycle** — tracing, experiment tracking, model versioning, AND deployment. The others focus primarily on observability. If you need a model registry or artifact management alongside tracing, MLflow is the right choice.

## When to use MLflow

Use MLflow when:

- You need auto-tracing with experiment tracking in one tool
- You want a model registry to version optimized DSPy programs
- Your team already uses MLflow for other ML projects
- You want to manage the full lifecycle: train → track → register → deploy

Do NOT use MLflow when:

- You only need tracing and want the simplest setup — see `/dspy-langtrace`
- You want a local trace viewer with built-in evals — see `/dspy-phoenix`
- Your team already uses W&B and wants cloud dashboards — see `/dspy-weave`

## Setup

### Install

```bash
pip install mlflow
```

### Auto-tracing (quickest start)

```python
import mlflow

mlflow.dspy.autolog()  # auto-traces all DSPy calls

import dspy
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

program = dspy.ChainOfThought("question -> answer")
result = program(question="What is DSPy?")
# View traces in MLflow UI: mlflow ui
```

### Launch the MLflow UI

```bash
mlflow ui  # Opens at http://localhost:5000
```

The UI shows:

- **Traces**: every DSPy call with prompts, responses, tokens, latency
- **Experiments**: logged parameters, metrics, and artifacts
- **Model registry**: versioned models with stage transitions

## Auto-tracing with mlflow.dspy.autolog()

One line traces everything DSPy does:

```python
import mlflow

mlflow.dspy.autolog()

import dspy
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

class RAGPipeline(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.answer(context=context, question=question)

pipeline = RAGPipeline()
result = pipeline(question="How do refunds work?")
# MLflow captures:
#   - RAGPipeline call (input/output, latency)
#   - Retrieve call (query, passages)
#   - ChainOfThought LM call (prompt, response, token counts)
```

### What autolog captures

| Component | Details |
|-----------|---------|
| LM calls | Full prompt, response, token counts, latency |
| Retrievals | Query, passages, scores |
| Module steps | Input/output per module in the pipeline |
| Cost | Token-based cost estimates |
| Errors | Stack traces for failed calls |

## Experiment tracking

Track optimization runs with parameters, metrics, and artifacts:

```python
import mlflow
import dspy
from dspy.evaluate import Evaluate

mlflow.dspy.autolog()
mlflow.set_experiment("dspy-optimization")

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

trainset = [...]  # your training examples
devset = [...]    # your dev examples

def metric(example, prediction, trace=None):
    return prediction.answer.strip().lower() == example.answer.strip().lower()

# Each run is a separate experiment
with mlflow.start_run(run_name="mipro-light"):
    mlflow.log_param("optimizer", "MIPROv2")
    mlflow.log_param("auto", "light")
    mlflow.log_param("model", "openai/gpt-4o-mini")
    mlflow.log_param("trainset_size", len(trainset))

    program = dspy.ChainOfThought("question -> answer")
    optimizer = dspy.MIPROv2(metric=metric, auto="light")
    optimized = optimizer.compile(program, trainset=trainset)

    evaluator = Evaluate(devset=devset, metric=metric, num_threads=4)
    score = evaluator(optimized)

    mlflow.log_metric("dev_score", score)

    # Save the optimized program as an artifact
    optimized.save("optimized_program.json")
    mlflow.log_artifact("optimized_program.json")
```

### Comparing experiments in the UI

1. Run `mlflow ui` and open `http://localhost:5000`
2. Click the "dspy-optimization" experiment
3. You'll see all runs with their parameters and metrics
4. Click "Compare" to view runs side-by-side
5. Sort by `dev_score` to find the best run

Typical score progression: Predict baseline ~55-65% → BootstrapFewShot ~68-75% → MIPROv2 light ~75-82% → MIPROv2 medium ~80-88%. Exact numbers depend on task difficulty and data quality, but the UI makes it easy to see which optimizer wins on your data.

## Model registry

Version and manage optimized DSPy programs:

```python
import mlflow

# Register the best run's model
with mlflow.start_run(run_name="best-model"):
    program = dspy.ChainOfThought("question -> answer")
    optimizer = dspy.MIPROv2(metric=metric, auto="medium")
    optimized = optimizer.compile(program, trainset=trainset)

    # Log as an MLflow model (use name= keyword, not positional)
    mlflow.dspy.log_model(optimized, name="qa-model")

    # Register in the model registry
    mlflow.register_model(
        f"runs:/{mlflow.active_run().info.run_id}/qa-model",
        "production-qa"
    )
```

### Loading a registered model

```python
import mlflow

# Load the latest version — returns the native dspy.Module
model = mlflow.dspy.load_model("models:/production-qa/latest")
result = model(question="What is your return policy?")

# Load a specific version
model_v2 = mlflow.dspy.load_model("models:/production-qa/2")
```

> `mlflow.dspy.load_model()` returns the native `dspy.Module`. Use `mlflow.pyfunc.load_model()` if you need the PyFunc-wrapped version for REST serving via `mlflow models serve`.

### Model aliases

Use aliases (like `champion`) to tag which version serves production traffic. Reassign the alias to promote a new version — no downtime, instant rollback:

```python
from mlflow import MlflowClient

client = MlflowClient()

# Set the champion alias to version 2
client.set_registered_model_alias("production-qa", "champion", version=2)

# Load by alias in production code
model = mlflow.dspy.load_model("models:/production-qa@champion")
```

## MLflow vs Langtrace vs W&B Weave

| Feature | MLflow | Langtrace | W&B Weave |
|---------|--------|-----------|-----------|
| Auto-tracing | Yes (`autolog()`) | Yes (one line) | No (manual `@weave.op()`) |
| Experiment tracking | Yes (built-in) | No | Yes (via decorators) |
| Model registry | Yes | No | No |
| Local UI | Yes (`mlflow ui`) | Yes (Docker) | No (cloud only) |
| Cloud option | Yes (Databricks) | Yes (app.langtrace.ai) | Yes (wandb.ai) |
| Open source | Yes | Yes | No |
| Team collaboration | Basic | Basic | Yes (built-in) |
| Best for | Full ML lifecycle | DSPy-first auto-tracing | Teams on W&B |

### Decision guide

```
What do you need?
|
+- Just tracing (easiest setup)? -> Langtrace (/dspy-langtrace)
+- Tracing + evals (local)? -> Phoenix (/dspy-phoenix)
+- Tracing + experiment tracking (cloud)? -> Weave (/dspy-weave)
+- Tracing + experiments + model registry? -> MLflow
+- Already on Databricks? -> MLflow (native integration)
```

## Gotchas

1. **Claude uses `transition_model_version_stage()` which is deprecated.** MLflow replaced model stages with model aliases. Use `client.set_registered_model_alias("model-name", "champion", version=N)` and load with `mlflow.dspy.load_model("models:/model-name@champion")`.
2. **Claude calls `mlflow.dspy.autolog()` after importing and configuring DSPy.** Autolog must be called before any DSPy code executes — it patches DSPy modules at import time. Call `mlflow.dspy.autolog()` as the first line after `import mlflow`.
3. **Claude forgets to set `mlflow.set_experiment()` before `start_run()`.** Without it, all runs go to the "Default" experiment, making it impossible to compare related optimization runs. Always set an experiment name before starting runs.
4. **Claude does not log the LM configuration as a parameter.** The model name and provider are critical for reproducing results. Always `mlflow.log_param("model", "openai/gpt-4o-mini")` inside the run so you can filter and compare across models later.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Langtrace** (auto-instrumentation, easiest setup) — `/dspy-langtrace`
- **Arize Phoenix** (open-source with evals) — `/dspy-phoenix`
- **W&B Weave** (team dashboards) — `/dspy-weave`
- **Serving APIs** (deploy your registered model) — `/ai-serving-apis`
- **Experiment tracking patterns** (JSONL-based, lightweight) — `/ai-tracking-experiments`
- **Production monitoring** — `/ai-monitoring`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [MLflow DSPy integration docs](https://mlflow.org/docs/latest/genai/flavors/dspy/index.html)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)
