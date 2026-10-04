---
name: dspy-weave
description: Use W&B Weave for DSPy experiment tracking and observability. Use when you want to set up Weave, W&B, wandb, Weights & Biases, experiment dashboard, weave.op, or team collaboration for DSPy. Also used for weave setup, pip install weave, weave.init, wandb project, W&B experiment tracking, weave decorator, weave.op decorator, wandb dashboard, compare optimization runs, team experiment tracking.
---

# W&B Weave — Cloud Observability & Experiment Tracking for DSPy

Guide the user through setting up W&B Weave for tracing DSPy calls, tracking optimization experiments, and collaborating with team dashboards.

## Before you start

Ask yourself (or the user):

1. Are you already using W&B for ML experiments or do you need to create an account?
2. Do you need auto-tracing of all DSPy calls, selective tracing of specific functions, or both?
3. Is this for a team with shared dashboards, or a solo project?

## What is W&B Weave

Weave is Weights & Biases' LLM observability and experiment tracking product. It provides cloud-hosted dashboards for tracing function calls, comparing optimization runs, and sharing results across teams.

- **Cloud-hosted**: Dashboards at [wandb.ai](https://wandb.ai)
- **Dual instrumentation**: Auto-traces all DSPy calls out of the box; also supports `@weave.op()` for custom non-DSPy functions
- **Team collaboration**: shared projects, comments, and run comparisons

### Key difference from Langtrace/Phoenix

Weave auto-instruments DSPy (like Langtrace) — once you call `weave.init()`, all DSPy modules, signatures, and optimizer runs are traced automatically. Weave also supports manual `@weave.op()` decorators for tracing non-DSPy functions. The main differentiator is the W&B experiment comparison dashboard and team collaboration features.

## When to use Weave

Use Weave when:

- Your team already uses W&B for ML experiments
- You want cloud-hosted dashboards with team collaboration
- You want to track and compare optimization runs side-by-side
- You need both auto-tracing (DSPy) and selective tracing (custom functions)

Do NOT use Weave when:

- You want a free, local-only trace viewer — see `/dspy-phoenix`
- You need the full ML lifecycle (model registry, deployment) — see `/dspy-mlflow`
- You are a solo developer who does not need team features — Langtrace or Phoenix is simpler

## Setup

### Install

```bash
pip install weave
```

### Initialize (auto-tracing for DSPy)

For DSPy projects, just call `weave.init()` — all DSPy modules, signatures, and optimizer runs are traced automatically:

```python
import weave
import dspy

weave.init("my-dspy-project")  # Creates project at wandb.ai; auto-traces all DSPy calls
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-3-5-sonnet", etc.

class QABot(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.answer(context=context, question=question)

bot = QABot()
# Every DSPy call is automatically traced — no decorators needed
answer = bot(question="How do refunds work?")
```

You will be prompted to log in on first run, or set `WANDB_API_KEY` as an environment variable.

### Environment variable configuration

```bash
export WANDB_API_KEY="your-key"          # From wandb.ai/settings
export WANDB_ENTITY="your-team"          # Optional: team name
export WANDB_PROJECT="my-dspy-project"   # Optional: project name
```

## Tracing custom functions with @weave.op()

For non-DSPy code (custom preprocessing, business logic, API calls), use `@weave.op()` to add manual tracing. The decorator captures inputs, outputs, latency, and cost:

```python
@weave.op()
def handle_question(question: str) -> str:
    """Traced by Weave — includes DSPy sub-calls automatically."""
    result = bot(question=question)
    return result.answer

# Weave shows the call tree: handle_question -> QABot.forward -> ChainOfThought
answer = handle_question("How do refunds work?")
```

### Tracing multiple custom functions

```python
@weave.op()
def fetch_user_context(user_id: str) -> dict:
    return db.query("SELECT * FROM users WHERE id = ?", user_id)

@weave.op()
def handle_question(user_id: str, question: str) -> str:
    ctx = fetch_user_context(user_id)  # non-DSPy step, manually traced
    result = bot(question=question)     # DSPy step, auto-traced
    return result.answer

# Weave shows the full call tree including both custom and DSPy steps
```

## Tracking optimization experiments

Weave excels at comparing optimization runs. Wrap your optimization in `@weave.op()`:

```python
import weave
import dspy
from dspy.evaluate import Evaluate

weave.init("optimization-experiments")
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

@weave.op()
def run_optimization(optimizer_name: str, model: str, auto_setting: str):
    """Run and track an optimization experiment."""
    lm = dspy.LM(model)
    dspy.configure(lm=lm)

    program = dspy.ChainOfThought("question -> answer")

    if optimizer_name == "miprov2":
        optimizer = dspy.MIPROv2(metric=metric, auto=auto_setting)
    elif optimizer_name == "bootstrap":
        optimizer = dspy.BootstrapFewShot(metric=metric)

    optimized = optimizer.compile(program, trainset=trainset)

    evaluator = Evaluate(devset=devset, metric=metric, num_threads=4)
    score = evaluator(optimized)

    # Save the artifact
    path = f"experiments/{optimizer_name}_{model}_{auto_setting}.json"
    optimized.save(path)

    return {
        "score": score,
        "optimizer": optimizer_name,
        "model": model,
        "auto": auto_setting,
        "artifact_path": path,
    }

# Run experiments — each is tracked in Weave
run_optimization("miprov2", "openai/gpt-4o-mini", "light")
run_optimization("miprov2", "openai/gpt-4o-mini", "medium")
run_optimization("bootstrap", "openai/gpt-4o-mini", "n/a")
```

### Comparing runs in the W&B dashboard

1. Go to [wandb.ai](https://wandb.ai) and open your project
2. Click on the "Traces" tab to see all tracked calls
3. Compare inputs and outputs across runs
4. Sort by score to find the best experiment
5. Share the dashboard URL with your team

## Weave vs Langtrace vs Phoenix

| Feature | W&B Weave | Langtrace | Arize Phoenix |
|---------|-----------|-----------|---------------|
| DSPy instrumentation | Auto (`weave.init()`) | Auto (one line) | Auto (plugin) |
| Custom function tracing | Manual (`@weave.op()`) | Auto | Auto |
| Cloud dashboard | Yes (wandb.ai) | Yes (app.langtrace.ai) | Yes (Arize platform) |
| Local/self-hosted | No | Yes (Docker) | Yes (`px.launch_app()`) |
| Team collaboration | Yes (built-in) | Basic | Basic |
| Experiment comparison | Yes (side-by-side) | No | No |
| Built-in evals | Basic | Basic | Yes (evals module) |
| Cost | Free tier + paid plans | Free tier + paid | Free (open source) |
| Best for | Teams on W&B, experiment comparison | Lightweight auto-tracing | Local trace viewer + evals |

### Decision guide

```
Want DSPy observability?
|
+- Team already uses W&B or need experiment comparison? -> Weave
+- Want the simplest setup with no W&B account? -> Langtrace (/dspy-langtrace)
+- Want local-only + built-in evals? -> Phoenix (/dspy-phoenix)
+- Need full ML lifecycle (registry, deploy)? -> MLflow (/dspy-mlflow)
```

## Verifying the setup

After calling `weave.init()`, run a DSPy call and confirm it appears in the dashboard:

```python
import weave
import dspy

weave.init("smoke-test")
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

predict = dspy.Predict("question -> answer")
result = predict(question="What is 2+2?")
print(f"Check your project at https://wandb.ai — look for the Predict call in Traces")
```

If the call does not appear: check `WANDB_API_KEY` is set, confirm `weave.init()` was called before any DSPy calls, and verify network access to wandb.ai.

## Gotchas

- **Claude puts `@weave.op()` on the DSPy module class instead of the calling function.** Weave decorators trace regular functions, not DSPy module classes. Decorate the function that *calls* the module, not the module itself. `@weave.op()` goes on `handle_question()`, not on `QABot`.
- **Claude calls `weave.init()` inside a function instead of at module level.** `weave.init()` must run once at startup, before any `@weave.op()` decorated functions are called. Placing it inside a request handler creates a new project per call and fragments your traces.
- **Claude forgets to set `WANDB_API_KEY` in deployment environments.** Local development prompts for login interactively, but production (Docker, CI, serverless) needs the environment variable explicitly set. Always include `WANDB_API_KEY` in environment configuration for non-local setups.
- **Claude adds unnecessary `@weave.op()` to every DSPy module.** DSPy calls are auto-traced once `weave.init()` is called — no decorators needed on `dspy.Module` subclasses. Reserve `@weave.op()` for non-DSPy custom functions (preprocessing, database calls, business logic) that you also want in the trace tree.
- **Claude nests `@weave.op()` and DSPy decorators incorrectly.** If combining with other decorators, `@weave.op()` should be the outermost decorator so it captures the full function execution including any inner decorator behavior.

## Additional resources

- [W&B Weave docs](https://docs.wandb.ai/weave/)
- [DSPy integration guide](https://docs.wandb.ai/weave/guides/integrations/dspy)
- [Weave Python SDK reference](https://docs.wandb.ai/weave/reference/python-sdk/)
- [W&B dashboard](https://wandb.ai)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Langtrace** (auto-instrumentation, no W&B account needed) — `/dspy-langtrace`
- **Arize Phoenix** (open-source with evals) — `/dspy-phoenix`
- **MLflow** (full ML lifecycle) — `/dspy-mlflow`
- **Aggregate monitoring** — `/ai-monitoring`
- **Experiment tracking patterns** (JSONL-based, lightweight) — `/ai-tracking-experiments`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
