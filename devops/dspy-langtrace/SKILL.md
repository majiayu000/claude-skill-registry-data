---
name: dspy-langtrace
description: Use Langtrace for DSPy observability and tracing with langtrace.init() auto-instrumentation. Use when you want to set up Langtrace, langtrace-python-sdk, auto-instrument DSPy, trace DSPy calls, LLM observability, app.langtrace.ai, or self-hosted tracing. Also used for langtrace.init, with_langtrace_root_span, langtrace setup, langtrace API key, pip install langtrace-python-sdk, DSPy tracing, auto-instrument DSPy, langtrace self-hosted, langtrace docker, trace LM calls, langtrace vs phoenix, langtrace cloud.
---

# Langtrace — Open-Source LLM Observability for DSPy

Guide the user through setting up Langtrace for automatic DSPy tracing and observability.

## Before you start

Ask the user (skip if already clear from context):
- **Cloud or self-hosted?** Cloud (`app.langtrace.ai`) needs only an API key; self-hosted (Docker) keeps all data on your infrastructure.
- **Inference tracing only, or experiment tracking too?** Experiment tracking during optimization runs uses `inject_additional_attributes` to tag each optimizer trial.

## What is Langtrace

Langtrace is an open-source LLM observability platform with **first-class DSPy auto-instrumentation**. One line of code traces all DSPy LM calls, retrievals, module executions, token counts, and cost — no manual decorators needed.

- **Cloud**: Managed at [app.langtrace.ai](https://app.langtrace.ai)
- **Self-hosted**: Run your own instance with Docker
- **Open source**: [github.com/Scale3-Labs/langtrace](https://github.com/Scale3-Labs/langtrace)

### What gets traced automatically

| Component | Details captured |
|-----------|-----------------|
| LM calls | Prompts, responses, token counts, cost, latency |
| Retrievals | Queries, retrieved passages, scores |
| Module executions | Input/output per `dspy.Module.forward()` call |
| Nested pipelines | Full call tree with parent-child relationships |

## When to use Langtrace

Use Langtrace when:

- You want the easiest DSPy tracing setup (one line)
- You need auto-instrumentation without decorating every function
- You want a cloud dashboard with no infrastructure to manage
- You need self-hosted tracing for data privacy

Do NOT use Langtrace when:

- You need deep evaluation/evals features — see `/dspy-phoenix` (Phoenix has built-in evals)
- Your team is already invested in W&B for experiment tracking — see `/dspy-weave`
- You need the full ML lifecycle (model registry, deployment) — see `/dspy-mlflow`

## Setup

### Install

```bash
pip install langtrace-python-sdk
```

### Cloud setup (quickest)

1. Sign up at [app.langtrace.ai](https://app.langtrace.ai)
2. Create a project and copy your API key
3. Add two lines to your code:

```python
from langtrace_python_sdk import langtrace

langtrace.init(api_key="your-key")  # or set LANGTRACE_API_KEY env var

# That's it — all DSPy calls are now traced automatically
import dspy
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

program = dspy.ChainOfThought("question -> answer")
result = program(question="What is DSPy?")
# View traces at app.langtrace.ai
```

**Verify it works**: Open `app.langtrace.ai` (or your self-hosted URL), go to your project, and confirm a trace appeared for the call above within ~30 seconds. If no trace shows up, the most common cause is `langtrace.init()` being called after `import dspy` — see Gotcha 1.

### Self-hosted setup (Docker)

For teams that need data to stay on-premises:

```bash
# Clone and start Langtrace
git clone https://github.com/Scale3-Labs/langtrace.git
cd langtrace
docker compose up -d
```

Then point your SDK at your local instance:

```python
from langtrace_python_sdk import langtrace

langtrace.init(api_host="http://localhost:3000/api/trace")

# All traces go to your self-hosted instance
# Replace localhost:3000 with your own DNS/IP for non-local deployments
```

### Environment variable configuration

```bash
export LANGTRACE_API_KEY="your-key"           # Cloud API key
# OR
export LANGTRACE_API_HOST="http://localhost:3000/api/trace"  # Self-hosted URL
```

```python
from langtrace_python_sdk import langtrace

langtrace.init()  # Picks up from environment variables
```

## Tracing a DSPy pipeline

Langtrace auto-instruments the entire call tree. No changes to your DSPy code:

```python
from langtrace_python_sdk import langtrace

langtrace.init(api_key="your-key")

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
# Langtrace captures:
#   - The top-level RAGPipeline call
#   - The Retrieve call (query, passages, latency)
#   - The ChainOfThought LM call (prompt, response, tokens, cost)
```

## Tracing optimization runs

Langtrace traces optimizer internals too — useful for understanding what MIPROv2 or GEPA tried:

```python
from langtrace_python_sdk import langtrace

langtrace.init(api_key="your-key")

import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

trainset = [...]  # your training examples

program = dspy.ChainOfThought("question -> answer")
optimizer = dspy.MIPROv2(metric=my_metric, auto="light")
optimized = optimizer.compile(program, trainset=trainset)
# Every LM call the optimizer makes is traced — see which candidates it tried
```

## Viewing traces in the Langtrace UI

The Langtrace dashboard shows:

- **Trace timeline**: waterfall view of every step in a request
- **Token counts & cost**: per-call and aggregate
- **Latency breakdown**: which step is slowest
- **Prompt/response viewer**: full text of every LM interaction
- **Filters**: by time range, latency, status, and custom attributes

### Adding custom attributes

Tag traces with metadata for filtering. `inject_additional_attributes` is a **standalone function** (not a method on `langtrace`) that wraps a callable and attaches the attribute dict to the resulting span:

```python
from langtrace_python_sdk import langtrace, with_langtrace_root_span, inject_additional_attributes

@with_langtrace_root_span("customer-query")
def handle_query(user_id, question):
    # inject_additional_attributes wraps the call and tags the span
    return inject_additional_attributes(
        lambda: pipeline(question=question),
        {
            "user_id": user_id,
            "environment": "production",
        }
    )
```

## Langtrace vs Phoenix vs Jaeger

| Feature | Langtrace | Arize Phoenix | Jaeger |
|---------|-----------|---------------|--------|
| DSPy auto-instrumentation | Yes (built-in) | Yes (plugin) | Manual |
| Setup effort | One line | Two lines + launch | Docker + manual spans |
| Self-hosted option | Yes (Docker) | Yes | Yes |
| Cloud option | Yes (app.langtrace.ai) | Yes (Arize platform) | No |
| LM call details | Prompts, tokens, cost | Prompts, tokens | Custom attributes |
| Evals/evaluation | Basic | Built-in evals module | No |
| Best for | DSPy-first teams | Teams wanting evals + traces | Teams already using Jaeger |

### Decision guide

```
Want DSPy tracing?
|
+- Easiest setup, auto-instrument everything? -> Langtrace
+- Need built-in evaluation features? -> Arize Phoenix (/dspy-phoenix)
+- Team already uses W&B? -> W&B Weave (/dspy-weave)
+- Need full ML lifecycle (registry, deploy)? -> MLflow (/dspy-mlflow)
+- Team already uses Jaeger? -> Jaeger (see /ai-tracing-requests)
```

## Gotchas

1. **Claude calls `langtrace.init()` after importing and configuring DSPy.** Langtrace must be initialized before any DSPy imports or configuration — it patches DSPy modules at import time. Always call `langtrace.init()` as the first line after `from langtrace_python_sdk import langtrace`, before `import dspy`.
2. **Claude sees no traces and does not realize DSPy caching is the cause.** DSPy caches LM responses by default. Repeated calls with the same input return cached results and do not generate new traces. To see traces for repeated calls, either change the input or disable DSPy caching with `dspy.configure_cache(enable=False)`.
3. **Claude omits `TRACE_DSPY_CHECKPOINT=false` in production.** Checkpoint tracing is enabled by default and serializes predictor state at each step, adding latency. For production deployments, set `export TRACE_DSPY_CHECKPOINT=false` to disable it.
4. **Claude wraps every function with `@with_langtrace_root_span` when auto-instrumentation already traces everything.** The root span decorator is only needed when you want to group DSPy calls under a named parent span with custom metadata. For basic tracing, `langtrace.init()` alone is sufficient — do not add decorators unless you need metadata filtering.

## Additional resources

- [Langtrace DSPy integration docs](https://docs.langtrace.ai/supported-integrations/llm-frameworks/dspy)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Arize Phoenix** (open-source with evals) — `/dspy-phoenix`
- **W&B Weave** (team dashboards, experiment tracking) — `/dspy-weave`
- **MLflow** (full ML lifecycle) — `/dspy-mlflow`
- **Aggregate monitoring** (not per-request) — `/ai-monitoring`
- **Per-request debugging** (inspect_history, JSONL traces) — `/ai-tracing-requests`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
