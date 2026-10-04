---
name: dspy-langfuse
description: LLM observability for DSPy with Langfuse -- auto-trace every LM call, attach scores and evaluations, run annotation queues for human review, and track experiments across prompt versions. Use when you want to set up Langfuse, langfuse.com, openinference-instrumentation-dspy, DSPyInstrumentor, trace DSPy calls, LLM observability with scores, annotation queues, or experiment tracking. Also used for langfuse setup, pip install langfuse, DSPy trace viewer, langfuse vs phoenix, langfuse vs langtrace, observe decorator with DSPy, self-hosted tracing with evaluation, production LLM monitoring with scoring.
---

# Langfuse -- LLM Observability and Evaluation for DSPy

## Step 1: Understand the setup

Before writing code, clarify:

1. **Cloud or self-hosted?** Langfuse Cloud (managed) or self-hosted (Docker)?
2. **What do you need beyond tracing?** Scores/evals, annotation queues, experiment tracking, or just traces?
3. **Do you need custom metadata on traces?** User IDs, session IDs, tags for filtering?
4. **Short-lived or long-running?** Scripts need `langfuse.flush()`; servers do not.

## What is Langfuse

Langfuse is an open-source LLM observability platform with auto-instrumentation for DSPy via the OpenInference plugin. It traces every LM call, retrieval, and module execution, then adds evaluation, scoring, and annotation on top.

### What gets traced

| Component | Details captured |
|-----------|-----------------|
| LM calls | Prompts, responses, token counts, latency, cost |
| Retrievals | Queries, passages, relevance |
| Module executions | Input/output per module step |
| Full pipeline | Nested spans showing the complete call tree |

### What Langfuse adds beyond tracing

| Feature | What it does |
|---------|-------------|
| **Scores** | Attach numeric, boolean, categorical, or text scores to any trace |
| **Annotation queues** | Structured human review workflows for building ground truth |
| **Experiments** | Compare prompt versions, measure score changes across runs |
| **Sessions** | Group multi-turn traces (chatbots, agents) |
| **Environments** | Separate dev/staging/prod traces |

## When to use Langfuse

Use Langfuse when:

- You want tracing plus built-in evaluation and scoring
- You need annotation queues for human review
- You want experiment tracking to compare prompt versions
- You need session grouping for multi-turn applications

Do NOT use Langfuse when:

- You want the easiest one-line setup with no evaluation needs -- see `/dspy-langtrace`
- You want a purely local trace viewer with no cloud -- see `/dspy-phoenix`
- Your team already uses W&B -- see `/dspy-weave`
- You need the full ML lifecycle (model registry, deployment) -- see `/dspy-mlflow`

## Setup

### Install

```bash
pip install langfuse dspy openinference-instrumentation-dspy -U
```

### Environment variables

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_BASE_URL="https://cloud.langfuse.com"  # US: us.cloud.langfuse.com | EU: cloud.langfuse.com | JP: jp.cloud.langfuse.com | HIPAA: hipaa.cloud.langfuse.com
```

### Quickstart

```python
import dspy
from langfuse import get_client
from openinference.instrumentation.dspy import DSPyInstrumentor

# 1. Verify Langfuse credentials
langfuse = get_client()
langfuse.auth_check()

# 2. Auto-instrument DSPy (one line)
DSPyInstrumentor().instrument()

# 3. Configure DSPy
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# 4. Use DSPy normally -- all calls are traced
program = dspy.ChainOfThought("question -> answer")
result = program(question="What is DSPy?")
# View traces at https://cloud.langfuse.com
```

## Adding metadata to traces

Use `@observe()` and `propagate_attributes()` to enrich auto-captured traces with user IDs, session IDs, tags, and custom metadata:

```python
from langfuse import observe, propagate_attributes

@observe()
def answer_question(question: str):
    with propagate_attributes(
        user_id="user_123",
        session_id="session_abc",
        tags=["production", "qa-pipeline"],
        metadata={"pipeline_version": "2.1"},
        version="2.1",
    ):
        program = dspy.ChainOfThought("question -> answer")
        return program(question=question)

result = answer_question("How do refunds work?")
```

### Context manager alternative

For non-decorator workflows (batch jobs, scripts):

```python
from langfuse import get_client, propagate_attributes

langfuse = get_client()

with langfuse.start_as_current_observation(as_type="span", name="batch-qa"):
    with propagate_attributes(
        user_id="batch_user",
        session_id="batch_001",
        metadata={"batch_size": 100},
    ):
        program = dspy.ChainOfThought("question -> answer")
        result = program(question="What is DSPy?")

langfuse.flush()  # Required for short-lived scripts
# Use langfuse.shutdown() instead if the process is exiting (also terminates background threads)
```

### Controlling I/O capture

DSPy prompts can contain sensitive data or be very large. Disable input/output capture on specific observations:

```python
@observe(capture_input=False, capture_output=False)
def process_pii_data(user_data: str):
    # Traces timing and structure but not the actual data
    return program(question=user_data)
```

Or disable globally via environment variable:

```bash
export LANGFUSE_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED=false
```

## Scoring traces

Langfuse scores attach evaluation results to traces. Score types: `NUMERIC`, `CATEGORICAL`, `BOOLEAN`, `TEXT`.

```python
from langfuse import get_client

langfuse = get_client()

# Score a trace after evaluation
langfuse.create_score(
    trace_id="trace-id-from-dashboard",
    name="accuracy",
    value=0.92,
    data_type="NUMERIC",
    comment="Verified against ground truth",
)
```

### Connecting DSPy metrics to Langfuse scores

After running `dspy.Evaluate`, push results to Langfuse for tracking:

```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(devset=devset, metric=metric, num_threads=4)
score = evaluator(my_program)

# Log the aggregate score
langfuse = get_client()
langfuse.create_score(
    trace_id=langfuse.get_current_trace_id(),
    name="dspy_eval_accuracy",
    value=score,
    data_type="NUMERIC",
)
langfuse.flush()
```

## Tracing a RAG pipeline

```python
from langfuse import observe, propagate_attributes
import dspy

DSPyInstrumentor().instrument()
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

class RAGPipeline(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.answer(context=context, question=question)

@observe()
def search_docs(question: str):
    with propagate_attributes(user_id="user_456", tags=["rag"]):
        pipeline = RAGPipeline()
        return pipeline(question=question)

result = search_docs("How do refunds work?")
# Trace shows: RAGPipeline -> Retrieve -> ChainOfThought (nested spans)
```

## Langfuse vs other observability tools

| Feature | Langfuse | Arize Phoenix | Langtrace | W&B Weave |
|---------|----------|---------------|-----------|-----------|
| DSPy auto-instrumentation | Yes (OpenInference plugin) | Yes (same plugin) | Yes (built-in) | Manual (`@weave.op()`) |
| Setup effort | 3 lines + env vars | 2 lines + `launch_app()` | 1 line | Decorator per function |
| Local mode (no cloud) | Yes (self-hosted Docker) | Yes (`px.launch_app()`) | Yes (Docker) | No |
| Cloud option | Yes (managed, multi-region) | Yes (Arize platform) | Yes (app.langtrace.ai) | Yes (wandb.ai) |
| Built-in scoring/evals | Yes (4 score types) | Yes (evals module) | Basic | Yes (feedback) |
| Annotation queues | Yes | No | No | No |
| Experiment tracking | Yes | Basic | No | Yes |
| Session grouping | Yes | No | No | No |
| Best for | Tracing + evaluation + human review | Local trace viewer + evals | Easiest DSPy-first setup | Teams already on W&B |

### Decision guide

```
Want DSPy observability?
|
+- Need scoring + annotation queues + experiments? -> Langfuse (/dspy-langfuse)
+- Want local-first open-source trace viewer?      -> Phoenix (/dspy-phoenix)
+- Want easiest one-line auto-instrumentation?      -> Langtrace (/dspy-langtrace)
+- Team already uses W&B?                           -> Weave (/dspy-weave)
+- Need full ML lifecycle (registry, deploy)?       -> MLflow (/dspy-mlflow)
```

## Gotchas

- **Claude forgets `langfuse.flush()` in scripts and notebooks.** Langfuse sends traces asynchronously in the background. In long-running servers this is fine, but in scripts, notebooks, and batch jobs the process exits before traces are sent. Always call `langfuse.flush()` (or `langfuse.shutdown()`) at the end of short-lived processes.
- **Claude installs `langfuse` but forgets `openinference-instrumentation-dspy`.** The DSPy auto-instrumentation lives in a separate package. Without it, `DSPyInstrumentor` is not available and no DSPy spans are captured. Install both: `pip install langfuse openinference-instrumentation-dspy`.
- **Claude calls `DSPyInstrumentor().instrument()` after `dspy.configure()` and DSPy calls.** The instrumentor must be activated before any DSPy module runs. Calls made before instrumentation are not captured. Always instrument first, then configure DSPy, then run modules.
- **Claude hardcodes `LANGFUSE_BASE_URL` to US cloud for all users.** Langfuse has region-specific endpoints: US (`us.cloud.langfuse.com`), EU (`cloud.langfuse.com`), Japan (`jp.cloud.langfuse.com`), HIPAA (`hipaa.cloud.langfuse.com`), and self-hosted URLs. Always ask the user which region or instance they use, or read it from environment variables rather than hardcoding.
- **Claude creates a new `get_client()` instance in every function.** `get_client()` returns a singleton -- calling it multiple times is safe but unnecessary clutter. Call it once at module level or in setup, then reuse the reference.
- **Claude skips debug-mode guidance when traces are missing.** When a user reports no traces appearing, Claude jumps straight to re-checking configuration rather than directing them to set `export LANGFUSE_DEBUG="True"` first. Debug mode prints every API call and error to stdout and is almost always the fastest diagnosis path — recommend it before asking users to re-audit credentials or instrumentation order.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Langtrace** (easiest DSPy auto-instrumentation) -- `/dspy-langtrace`
- **Arize Phoenix** (local trace viewer + evals) -- `/dspy-phoenix`
- **W&B Weave** (team dashboards, experiment tracking) -- `/dspy-weave`
- **MLflow** (full ML lifecycle) -- `/dspy-mlflow`
- **LangWatch** (real-time optimizer progress) -- `/dspy-langwatch`
- **Aggregate monitoring** (not per-request) -- `/ai-monitoring`
- **Per-request debugging** (inspect_history, JSONL traces) -- `/ai-tracing-requests`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [Langfuse DSPy integration docs](https://langfuse.com/docs/integrations/dspy)
- [Langfuse Python SDK docs](https://langfuse.com/docs/sdk/python/decorators)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)
