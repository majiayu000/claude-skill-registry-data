---
name: dspy-phoenix
description: Use Arize Phoenix for DSPy tracing and evaluation. Use when you want to set up Phoenix, arize-phoenix, openinference, DSPyInstrumentor, open-source trace viewer, localhost:6006, or LLM evals. Also used for phoenix setup, arize phoenix, pip install arize-phoenix, phoenix local UI, phoenix evaluations, DSPy trace viewer, open-source LLM observability, phoenix vs langtrace, openinference-instrumentation-dspy, phoenix.otel register.
---

# Arize Phoenix — Open-Source LLM Observability for DSPy

Guide the user through setting up Arize Phoenix for DSPy tracing, visualization, and evaluation.

## Step 1 — Gather context

Ask the user before generating any setup code:

1. **Local or cloud?** Local mode runs the Phoenix UI at `http://localhost:6006` with no account — ideal for development. Cloud mode sends traces to the Arize platform for persistent storage and team collaboration (needs an API key).
2. **Tracing only or also evals?** Do you need just trace visualization, or also automated quality scoring with Phoenix's `llm_classify`?
3. **What is your DSPy pipeline doing?** (e.g., RAG with `dspy.Retrieve`, simple LM calls, multi-step agent) — RAG pipelines get the most value from Phoenix because retrieval and LM spans are shown side by side.

## What is Arize Phoenix

Phoenix is an open-source LLM observability platform that runs locally or in the cloud. It provides a trace viewer, evaluation tools, and dataset management — all with DSPy auto-instrumentation via the OpenInference plugin.

- **Local mode**: `px.launch_app()` starts a UI at `http://localhost:6006` — no account needed
- **Cloud mode**: Hosted on the [Arize platform](https://arize.com/)
- **Open source**: [github.com/Arize-ai/phoenix](https://github.com/Arize-ai/phoenix)

### What gets traced

| Component | Details captured |
|-----------|-----------------|
| LM calls | Prompts, responses, token counts, latency |
| Retrievals | Queries, passages, relevance scores |
| Module executions | Input/output per module step |
| Full pipeline | Nested spans showing the complete call tree |

## When to use Phoenix

Use Phoenix when:

- You want a local trace viewer with no cloud dependency
- You need built-in evaluation tools (evals module)
- You want an open-source solution you can self-host
- You want to visually inspect what your DSPy pipeline is doing

Do NOT use Phoenix when:

- You want the absolute easiest one-line setup — see `/dspy-langtrace`
- Your team already uses W&B — see `/dspy-weave`
- You need the full ML lifecycle (model registry, deployment) — see `/dspy-mlflow`

## Setup

### Install

```bash
pip install arize-phoenix openinference-instrumentation-dspy openinference-instrumentation-litellm
```

DSPy uses LiteLLM under the hood — install both instrumentors to get token counts and cost tracking.

### Local mode (recommended for development)

```python
import phoenix as px
from phoenix.otel import register

# Launch local UI at http://localhost:6006
px.launch_app()

# Register with auto-instrumentation (instruments DSPy + LiteLLM automatically)
tracer_provider = register(
    project_name="my-dspy-project",
    auto_instrument=True,
)

# All DSPy calls are now traced
import dspy
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or any LiteLLM-supported provider

program = dspy.ChainOfThought("question -> answer")
result = program(question="What is DSPy?")
# View traces at http://localhost:6006
```

### Cloud mode (Arize platform)

For teams that want persistent storage and collaboration:

```python
import os
from phoenix.otel import register

os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"
os.environ["PHOENIX_API_KEY"] = "your-api-key"

tracer_provider = register(
    project_name="my-dspy-project",
    auto_instrument=True,
)
```

### Adding metadata to traces

Use `using_attributes` to attach session, user, and tag metadata:

```python
from phoenix.otel import using_attributes

with using_attributes(
    session_id="session-123",
    user_id="user-456",
    metadata={"environment": "staging"},
    tags=["experiment-v2"],
):
    result = program(question="What is DSPy?")
    # This trace will carry the session/user/tag metadata in Phoenix
```

## Tracing a DSPy pipeline

```python
import phoenix as px
from phoenix.otel import register

px.launch_app()
register(project_name="rag-pipeline", auto_instrument=True)

import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or any LiteLLM-supported provider

class RAGPipeline(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.answer(context=context, question=question)

pipeline = RAGPipeline()
result = pipeline(question="How do refunds work?")
# Open http://localhost:6006 to see the trace tree:
#   RAGPipeline
#   +-- Retrieve (query, passages, latency)
#   +-- ChainOfThought (prompt, response, tokens)
```

## Evaluations with Phoenix

Phoenix includes a built-in evals module for scoring LM outputs:

```python
from phoenix.evals import llm_classify, OpenAIModel

# Define evaluation criteria
eval_model = OpenAIModel(model="gpt-4o-mini")

# Score traces against criteria
eval_results = llm_classify(
    dataframe=px.Client().get_spans_dataframe(),
    model=eval_model,
    template="Is this response helpful and accurate? {output}",
    rails=["helpful", "not helpful"],
)
```

This is useful for:

- **Automated quality checks**: score every response in a batch
- **Finding failure patterns**: filter by low-scoring traces
- **Regression testing**: compare eval scores before and after changes

## Phoenix vs Langtrace vs Jaeger

| Feature | Arize Phoenix | Langtrace | Jaeger |
|---------|---------------|-----------|--------|
| DSPy auto-instrumentation | Yes (plugin) | Yes (built-in) | Manual |
| Setup effort | Two lines + launch | One line | Docker + manual spans |
| Local mode (no cloud) | Yes (`px.launch_app()`) | Yes (Docker) | Yes (Docker) |
| Cloud option | Yes (Arize platform) | Yes (app.langtrace.ai) | No |
| Built-in evals | Yes (evals module) | Basic | No |
| Dataset management | Yes | No | No |
| LM call details | Prompts, tokens, latency | Prompts, tokens, cost | Custom attributes |
| Best for | Teams wanting evals + traces | DSPy-first teams | Teams already using Jaeger |

### Decision guide

```
Want DSPy tracing?
|
+- Need built-in evals + dataset management? -> Arize Phoenix
+- Want easiest one-line setup? -> Langtrace (/dspy-langtrace)
+- Team already uses W&B? -> W&B Weave (/dspy-weave)
+- Need full ML lifecycle (registry, deploy)? -> MLflow (/dspy-mlflow)
+- Team already uses Jaeger? -> Jaeger (see /ai-tracing-requests)
```

## Gotchas

1. **Missing LiteLLM instrumentor hides token counts.** Claude installs `openinference-instrumentation-dspy` but forgets `openinference-instrumentation-litellm`. Without it, traces show LM calls but token counts and costs are missing. Always install both.
2. **Using the old `DSPyInstrumentor().instrument()` pattern instead of `register(auto_instrument=True)`.** The `register` function from `phoenix.otel` is the current recommended approach — it auto-discovers and instruments all installed OpenInference packages. Manual `DSPyInstrumentor().instrument()` still works but misses LiteLLM spans.
3. **Forgetting `px.launch_app()` before `register()` in local mode.** Without `px.launch_app()`, there is no local collector to receive traces. Call `px.launch_app()` first, then `register()`. In cloud mode, set `PHOENIX_COLLECTOR_ENDPOINT` instead.
4. **Traces missing metadata for filtering.** Without `using_attributes`, all traces look identical in the UI. Wrap DSPy calls in `using_attributes(session_id=..., user_id=..., tags=[...])` to make traces filterable and attributable.
5. **litellm version constraint may be needed.** Phoenix DSPy integration docs pin `litellm<1.82.7` for compatibility with `openinference-instrumentation-litellm`. If Claude installs the latest litellm and token counts are missing from traces, pin the version: `pip install 'litellm<1.82.7'`.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Langtrace** (easiest DSPy auto-instrumentation) — `/dspy-langtrace`
- **W&B Weave** (team dashboards, experiment tracking) — `/dspy-weave`
- **MLflow** (full ML lifecycle) — `/dspy-mlflow`
- **Aggregate monitoring** (not per-request) — `/ai-monitoring`
- **Per-request debugging** (inspect_history, JSONL traces) — `/ai-tracing-requests`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [Phoenix DSPy integration docs](https://arize.com/docs/phoenix/integrations/python/dspy/dspy-tracing)
- [Phoenix GitHub](https://github.com/Arize-ai/phoenix)
- For complete setup options and API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)
