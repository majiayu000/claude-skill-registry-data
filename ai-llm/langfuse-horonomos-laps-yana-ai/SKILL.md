---
name: langfuse
description: LLM observability with Langfuse — tracing, evals, prompt management, cost tracking
triggers:
  - langfuse
  - llm observability
  - llm tracing
  - prompt management langfuse
  - trace llm calls
  - langfuse eval
  - llm cost tracking
  - langfuse sdk
  - observe decorator
  - langfuse dataset
do_not_use_for:
  - generic logging — use structlog/loguru
  - application monitoring — use OpenTelemetry
  - model benchmarks — use ragas/deepeval
see_also:
  - ragas
  - deepeval
  - litellm
  - pydantic-ai
---

# Langfuse — LLM Observability

## Core: Trace + Span

```python
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    host="https://cloud.langfuse.com",  # or self-hosted
)

@observe()  # auto-creates trace + span
def process_document(doc: str) -> str:
    result = call_llm(doc)
    langfuse_context.update_current_observation(
        input=doc,
        output=result,
        metadata={"doc_length": len(doc)},
    )
    return result

@observe(name="pipeline")
def run_pipeline(user_input: str) -> dict:
    langfuse_context.update_current_trace(
        user_id="user-123",
        session_id="session-456",
        tags=["production", "v2"],
    )
    extracted = extract(user_input)      # auto-nested span
    summarized = summarize(extracted)    # auto-nested span
    return {"result": summarized}
```

## Manual Tracing (SDK)

```python
trace = langfuse.trace(
    name="rag-query",
    user_id="user-123",
    input={"query": user_query},
)

retrieval = trace.span(
    name="retrieval",
    input={"query": user_query},
)
docs = vector_store.search(user_query)
retrieval.end(output={"doc_count": len(docs)})

generation = trace.generation(
    name="llm-call",
    model="claude-sonnet-4-6",
    input=[{"role": "user", "content": prompt}],
    model_parameters={"temperature": 0.7},
)
response = call_claude(prompt)
generation.end(
    output=response,
    usage={"input": 500, "output": 200, "unit": "TOKENS"},
)

trace.update(output={"answer": response})
langfuse.flush()  # ensure all events sent before process exit
```

## Prompt Management

```python
# Fetch versioned prompt from Langfuse UI
prompt_obj = langfuse.get_prompt("rag-system-prompt", version=3)
compiled = prompt_obj.compile(
    context="{{context}}",
    question="{{question}}",
)

# Use in generation — links prompt version to trace
generation = trace.generation(
    name="llm-call",
    prompt=prompt_obj,  # links version automatically
    input=compiled,
)
```

## Evals (Scores)

```python
# Manual score after human review
langfuse.score(
    trace_id=trace.id,
    name="faithfulness",
    value=0.92,                         # 0.0–1.0
    comment="All claims backed by docs",
)

# LLM-as-judge eval
from langfuse.model_based_eval import evaluate_with_llm

score = evaluate_with_llm(
    trace_id=trace.id,
    evaluator="hallucination",          # built-in evaluator
)

# Python callback for custom eval
def score_relevance(trace_id: str, input: str, output: str) -> float:
    prompt = f"Rate relevance 0-1: Q={input} A={output}"
    return float(call_llm(prompt))
```

## Datasets & Experiments

```python
# Create dataset
dataset = langfuse.create_dataset(name="rag-test-set")
langfuse.create_dataset_item(
    dataset_name="rag-test-set",
    input={"query": "What is RAG?"},
    expected_output={"answer": "Retrieval-Augmented Generation..."},
)

# Run experiment over dataset
items = langfuse.get_dataset("rag-test-set").items
for item in items:
    with item.observe(run_name="v2-experiment") as trace:
        output = my_pipeline(item.input["query"])
        trace.score(name="correctness", value=score(output, item.expected_output))
```

## LangChain / LlamaIndex Integration

```python
# LangChain — one-line integration
from langfuse.callback import CallbackHandler

handler = CallbackHandler(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    session_id="session-123",
)
chain.invoke({"input": query}, config={"callbacks": [handler]})

# LlamaIndex
from llama_index.callbacks.langfuse import LangfuseCallbackHandler
import llama_index

llama_index.global_handler = LangfuseCallbackHandler()
```

## Cost Tracking

```python
# Costs are auto-computed from usage + model pricing
generation.end(
    output=response_text,
    usage={
        "input": prompt_tokens,
        "output": completion_tokens,
        "unit": "TOKENS",           # or CHARACTERS, MILLISECONDS
        "input_cost": 0.003,        # override if custom model
        "output_cost": 0.015,
    },
)
# View totals in Langfuse dashboard: /dashboard/cost
```

## Anti-Fake-Pass Checks

- `langfuse.flush()` before process exit — otherwise buffered events lost
- `@observe()` requires `LANGFUSE_PUBLIC_KEY` + `LANGFUSE_SECRET_KEY` env vars or explicit init
- Trace IDs are UUIDs — store them to link scores back later
- `prompt_obj.compile()` raises `KeyError` if template variable missing from kwargs
- `get_dataset().items` is paginated — iterate with `while True` + `next_page` for large sets
