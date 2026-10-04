---
name: dspy-langwatch
description: Use LangWatch for DSPy auto-tracing and real-time optimizer progress. Use when you want to set up LangWatch, langwatch.dspy.init, auto-tracing DSPy, real-time optimization dashboard, optimizer progress tracking, app.langwatch.ai, or DSPy optimizer dashboard. Also used for langwatch setup, pip install langwatch, langwatch trace, optimizer progress, real-time optimization, watch optimizer run, LangWatch self-hosted, langwatch docker, langwatch vs langtrace, langwatch autotrack_dspy.
---

# LangWatch — Auto-Tracing + Real-Time Optimizer Progress for DSPy

Guide the user through setting up LangWatch for automatic DSPy tracing and live optimizer progress tracking.

## What is LangWatch

LangWatch is an open-source LLMOps platform with **two distinct DSPy integrations**:

1. **Auto-tracing** (inference): automatically captures module inputs/outputs, LM calls, and retrieval queries
2. **Optimizer progress tracking** (unique feature): streams live step-by-step scores, predictor states, and cost as optimizers run

No other observability tool (Langtrace, Phoenix, Weave, MLflow) patches DSPy optimizers to stream live progress.

- **Cloud**: Managed at [app.langwatch.ai](https://app.langwatch.ai) (free tier available)
- **Self-hosted**: Docker Compose, Helm chart, enterprise on-prem
- **Open source**: [github.com/langwatch/langwatch](https://github.com/langwatch/langwatch)

## When to use LangWatch

Use LangWatch when:

- You run long optimization passes and want to see progress in real-time
- You want auto-tracing of DSPy inference with no manual decorators
- You want a dashboard showing optimizer scores, cost, and predictor state as they happen
- You need both inference tracing AND optimizer monitoring in one tool

Do NOT use LangWatch when:

- You only need tracing and want the simplest one-line setup — see `/dspy-langtrace`
- You want a local trace viewer with built-in evals — see `/dspy-phoenix`
- Your team already uses W&B for experiment tracking — see `/dspy-weave`
- You need a model registry and full ML lifecycle — see `/dspy-mlflow`

## Step 1 — Gather context

Before setting up, clarify:

1. **Cloud or self-hosted?** Cloud (`app.langwatch.ai`) is quickest; self-hosted (Docker Compose or Kubernetes Helm) for data sovereignty.
2. **What do you need?** Auto-tracing only, optimizer progress tracking only, or both?
3. **Which optimizers?** The optimizer tracking integration supports `BootstrapFewShot`, `BootstrapFewShotWithRandomSearch`, `COPRO`, and `MIPROv2`. Other optimizers raise `ValueError`.

## Setup

### Install

```bash
pip install langwatch
# Or pin DSPy version compatibility:
pip install langwatch[dspy]
```

### Cloud setup (quickest)

1. Sign up at [app.langwatch.ai](https://app.langwatch.ai)
2. Create a project and copy your API key
3. Set the environment variable:

```bash
export LANGWATCH_API_KEY="your-key"
```

### Self-hosted setup

#### Docker Compose

```bash
git clone https://github.com/langwatch/langwatch.git
cd langwatch
docker compose up -d
```

Then point your SDK at your local instance:

```bash
export LANGWATCH_ENDPOINT="http://localhost:5560"
```

#### Helm chart (Kubernetes)

LangWatch provides a Helm chart for production Kubernetes deployments. See the [LangWatch Helm docs](https://langwatch.ai/docs/self-hosting/deployment/kubernetes-helm) for Helm values and configuration.

## Integration 1: Auto-Tracing (Inference)

Use `@langwatch.trace()` and `autotrack_dspy()` to automatically capture all DSPy calls during inference.

### What gets traced

| Component | Details captured |
|-----------|-----------------|
| Module calls | Inputs/outputs per `dspy.Module.forward()` |
| LM calls | Model name, messages, response, token counts |
| Retrievals | Queries, retrieved passages |
| Nested spans | Full call tree with parent-child relationships |

### Basic auto-tracing

```python
import langwatch
import dspy

langwatch.setup()  # reads LANGWATCH_API_KEY from env; add endpoint_url= for self-hosted
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

@langwatch.trace()
def answer_question(question):
    langwatch.get_current_trace().autotrack_dspy()

    program = dspy.ChainOfThought("question -> answer")
    return program(question=question)

result = answer_question("What is DSPy?")
# View traces at app.langwatch.ai (or your self-hosted URL)
```

### Tracing a full pipeline

```python
import langwatch
import dspy

langwatch.setup()  # call once at startup
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

class RAGPipeline(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.answer(context=context, question=question)

pipeline = RAGPipeline()

@langwatch.trace()
def handle_query(question):
    langwatch.get_current_trace().autotrack_dspy()
    return pipeline(question=question)

result = handle_query("How do refunds work?")
# LangWatch captures:
#   - The RAGPipeline call
#   - The Retrieve call (query, passages)
#   - The ChainOfThought LM call (prompt, response, tokens)
```

### Adding metadata to traces

```python
# langwatch.setup() already called at startup

@langwatch.trace()
def handle_query(user_id, question):
    trace = langwatch.get_current_trace()
    trace.autotrack_dspy()
    trace.update(metadata={"user_id": user_id, "environment": "production"})
    return pipeline(question=question)
```

## Integration 2: Optimizer Progress Tracking (Unique Feature)

LangWatch patches DSPy optimizer classes to stream live step-by-step progress. This is LangWatch's killer feature — no other tool does this.

### What the optimizer dashboard shows

- **Live scores**: see each trial's score as it completes
- **Predictor states**: which instructions and demos the optimizer is testing
- **LM calls**: every call the optimizer makes during search
- **Cost tracking**: running cost total as the optimizer runs
- **Progress bar**: how far through the optimization you are

### Supported optimizers

| Optimizer | Supported |
|-----------|-----------|
| `dspy.BootstrapFewShot` | Yes |
| `dspy.BootstrapFewShotWithRandomSearch` | Yes |
| `dspy.COPRO` | Yes |
| `dspy.MIPROv2` | Yes |
| Others | Raises `ValueError` |

### Setup optimizer tracking

```python
import langwatch.dspy
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

trainset = [...]  # your training examples

def metric(example, prediction, trace=None):
    return prediction.answer.strip().lower() == example.answer.strip().lower()

program = dspy.ChainOfThought("question -> answer")
optimizer = dspy.MIPROv2(metric=metric, auto="medium")

# Initialize LangWatch optimizer tracking
langwatch.dspy.init(
    experiment="mipro-medium-run1",
    optimizer=optimizer,
)

# Run optimization — progress streams to the LangWatch dashboard
optimized = optimizer.compile(program, trainset=trainset)
# Watch live progress at app.langwatch.ai
```

### Tracking BootstrapFewShot

```python
import langwatch.dspy
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

program = dspy.ChainOfThought("question -> answer")
optimizer = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)

langwatch.dspy.init(
    experiment="bootstrap-4demos",
    optimizer=optimizer,
)

optimized = optimizer.compile(program, trainset=trainset)
```

### Comparing multiple optimizer runs

Run multiple experiments with different names — they appear side-by-side in the LangWatch dashboard:

```python
import langwatch.dspy
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

experiments = [
    ("bootstrap-4", dspy.BootstrapFewShot, {"metric": metric, "max_bootstrapped_demos": 4}),
    ("bootstrap-8", dspy.BootstrapFewShot, {"metric": metric, "max_bootstrapped_demos": 8}),
    ("mipro-light", dspy.MIPROv2, {"metric": metric, "auto": "light"}),
    ("mipro-medium", dspy.MIPROv2, {"metric": metric, "auto": "medium"}),
]

for name, opt_class, kwargs in experiments:
    program = dspy.ChainOfThought("question -> answer")
    optimizer = opt_class(**kwargs)
    langwatch.dspy.init(experiment=name, optimizer=optimizer)
    optimized = optimizer.compile(program, trainset=trainset)
```

## LangWatch vs Langtrace vs Phoenix vs Weave vs MLflow

| Feature | LangWatch | Langtrace | Phoenix | Weave | MLflow |
|---------|-----------|-----------|---------|-------|--------|
| DSPy auto-tracing | Yes | Yes (built-in) | Yes (plugin) | No (manual) | Yes (`autolog`) |
| **Optimizer progress** | **Yes (unique)** | No | No | No | No |
| Live scores dashboard | Yes | No | No | No | No |
| Setup effort | 2-3 lines | One line | Two lines + launch | Manual decorators | One line |
| Self-hosted | Yes (Docker, Helm) | Yes (Docker) | Yes | No (cloud only) | Yes |
| Cloud option | Yes (app.langwatch.ai) | Yes (app.langtrace.ai) | Yes (Arize) | Yes (wandb.ai) | Yes (Databricks) |
| Model registry | No | No | No | No | Yes |
| Built-in evals | Basic | Basic | Yes | Basic | Basic |

### Decision guide

```
What do you need?
|
+- Watch optimizer progress live? -> LangWatch (this skill)
+- Easiest auto-tracing setup? -> Langtrace (/dspy-langtrace)
+- Tracing + evals (local)? -> Phoenix (/dspy-phoenix)
+- Tracing + experiment tracking (cloud)? -> Weave (/dspy-weave)
+- Full ML lifecycle + model registry? -> MLflow (/dspy-mlflow)
```

## Gotchas

1. **Claude skips `langwatch.setup()` entirely.** `langwatch.setup()` must be called once at startup before any `@langwatch.trace()` or `langwatch.dspy.init()` call. It initializes the SDK, reads `LANGWATCH_API_KEY` from the environment, and (for self-hosted) configures the endpoint via `endpoint_url=` or `LANGWATCH_ENDPOINT`. Without it, traces are silently dropped. To verify setup is working, run a traced function and check [app.langwatch.ai](https://app.langwatch.ai) for a new trace — if nothing appears within 30 seconds, `LANGWATCH_API_KEY` is missing or `langwatch.setup()` was skipped.
2. **Claude forgets to call `autotrack_dspy()` inside the traced function.** The `@langwatch.trace()` decorator creates the trace context, but DSPy auto-tracking only activates when you call `langwatch.get_current_trace().autotrack_dspy()` inside the function body. Without it, you get an empty trace with no DSPy spans.
3. **Claude puts `autotrack_dspy()` outside the `@langwatch.trace()` function.** The `autotrack_dspy()` call must be inside the decorated function where a trace context exists. Calling it at module level or before the trace starts raises an error because there is no current trace.
4. **Claude calls `langwatch.dspy.init()` after `optimizer.compile()`.** The `init()` call must come before `compile()` — it patches the optimizer to stream progress. If called after, no progress data is captured. Always: create optimizer, call `langwatch.dspy.init(experiment=..., optimizer=...)`, then call `optimizer.compile()`.
5. **Claude reuses the same experiment name across runs.** Each `langwatch.dspy.init(experiment=...)` call should use a unique experiment name so runs appear as separate entries in the dashboard. Reusing names overwrites or merges data, making comparison impossible.

## Additional resources

- [LangWatch DSPy integration docs](https://langwatch.ai/docs/integration/python/integrations/dspy)
- [LangWatch self-hosting docs](https://langwatch.ai/docs/self-hosting)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Problem-first guide to watching optimization** — `/ai-watching-optimization`
- **Langtrace** (auto-instrumentation, easiest one-line setup) — `/dspy-langtrace`
- **Arize Phoenix** (open-source with evals) — `/dspy-phoenix`
- **W&B Weave** (team dashboards, experiment tracking) — `/dspy-weave`
- **MLflow** (full ML lifecycle, model registry) — `/dspy-mlflow`
- **Lightweight experiment tracking** (JSONL-based, no extra tools) — `/ai-tracking-experiments`
- **Production monitoring** — `/ai-monitoring`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
