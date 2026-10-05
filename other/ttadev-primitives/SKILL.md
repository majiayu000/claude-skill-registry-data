---
name: ttadev-primitives
description: 'Teaches TTA.dev primitive composition patterns so an AI agent can compose a working workflow in 1-2 turns. Use when the user wants to compose a workflow, use TTA.dev primitives, add a retry primitive, use workflow context, build a pipeline, or wire up any primitive (LambdaPrimitive, RetryPrimitive, TimeoutPrimitive, CachePrimitive, CircuitBreakerPrimitive, FallbackPrimitive, SequentialPrimitive, ParallelPrimitive). Covers the >> composition operator, WorkflowContext state passing, import paths, anti-patterns, and end-to-end workflow execution.'
---

# TTA.dev Primitive Composition

TTA.dev workflows are built by composing **typed primitives** — each a subclass of `WorkflowPrimitive[Input, Output]`. All primitives share a single execute interface and compose with `>>` (sequential) or `|` (parallel).

## When to Use This Skill

- Composing a new TTA.dev workflow from scratch
- Wrapping an existing function in retry, timeout, or cache logic
- Adding a circuit breaker to an external service call
- Building a parallel fan-out or sequential pipeline
- Passing state between steps with `WorkflowContext`

## Prerequisites

```bash
uv sync            # installs ttadev and all extras
```

All primitives live in `ttadev.primitives`:

```python
from ttadev.primitives import (
    WorkflowPrimitive, WorkflowContext, LambdaPrimitive,
    SequentialPrimitive, ParallelPrimitive,
    RetryPrimitive, TimeoutPrimitive, CachePrimitive,
    FallbackPrimitive,
)
from ttadev.primitives.recovery import CircuitBreakerPrimitive
```

## Core Primitive Types

| Primitive | Import path | When to use |
|-----------|-------------|-------------|
| `LambdaPrimitive` | `ttadev.primitives` | Wrap any function/async fn |
| `SequentialPrimitive` | `ttadev.primitives` | Run steps in order; output feeds next |
| `ParallelPrimitive` | `ttadev.primitives` | Fan-out — same input, results list |
| `RetryPrimitive` | `ttadev.primitives` | Transient failures, exponential back-off |
| `TimeoutPrimitive` | `ttadev.primitives` | Cap wall-clock time |
| `CachePrimitive` | `ttadev.primitives` | Memoize expensive calls |
| `FallbackPrimitive` | `ttadev.primitives` | Try primary, then secondary |
| `CircuitBreakerPrimitive` | `ttadev.primitives.recovery` | Stop hammering a broken service |

## The `>>` Composition Operator

`>>` creates a `SequentialPrimitive` inline. The **output** of the left primitive becomes the **input** of the right primitive.

```python
pipeline = step_a >> step_b >> step_c
result = await pipeline.execute(initial_input, ctx)
```

`|` creates a `ParallelPrimitive` — both sides receive the same input and run concurrently, returning `list[Output]`.

```python
fan_out = classifier | summariser
results = await fan_out.execute(text, ctx)   # [class_result, summary_result]
```

## WorkflowContext — Passing State

`WorkflowContext` flows through every `.execute()` call. Use `ctx.state` to share values across steps without changing function signatures.

```python
import asyncio
from ttadev.primitives import WorkflowContext, LambdaPrimitive

# Root context — starts a fresh workflow
ctx = WorkflowContext.root("my-pipeline")

# Write state in one step …
store = LambdaPrimitive(lambda data, c: (c.state.update({"key": data}), data)[1])

# … read it in another
read  = LambdaPrimitive(lambda _, c: c.state["key"].upper())

pipeline = store >> read
result = asyncio.run(pipeline.execute("hello", ctx))  # "HELLO"
```

**Child contexts** inherit state while keeping a new span ID:

```python
child_ctx = WorkflowContext.child(ctx, step_name="validate-input")
```

## Minimal Working Example

```python
import asyncio
from ttadev.primitives import (
    LambdaPrimitive, RetryPrimitive, TimeoutPrimitive, WorkflowContext,
)

async def fetch(url: str, ctx: WorkflowContext) -> str:
    # … real HTTP call here
    return f"data from {url}"

fetcher = LambdaPrimitive(fetch)
resilient = TimeoutPrimitive(
    RetryPrimitive(fetcher, max_retries=3),
    timeout_seconds=10.0,
)

ctx = WorkflowContext.root("fetch-pipeline")
result = asyncio.run(resilient.execute("https://api.example.com/data", ctx))
print(result)
```

## Recovery Primitives — Quick Reference

```python
from ttadev.primitives import RetryPrimitive, TimeoutPrimitive, FallbackPrimitive
from ttadev.primitives.recovery import CircuitBreakerPrimitive, CircuitBreakerConfig

# Retry with exponential back-off
safe = RetryPrimitive(my_prim, max_retries=3, backoff_base=2.0)

# Hard wall-clock timeout
timed = TimeoutPrimitive(my_prim, timeout_seconds=5.0)

# Primary → fallback chain
resilient = FallbackPrimitive(primary_prim, fallback_prim)

# Circuit breaker — opens after 5 failures, retries after 60 s
cb = CircuitBreakerPrimitive(
    my_prim,
    config=CircuitBreakerConfig(failure_threshold=5, recovery_timeout=60.0),
)
```

## Anti-Patterns

| ❌ Never do this | ✅ Use this instead |
|-----------------|---------------------|
| `for attempt in range(3): try/except` | `RetryPrimitive(prim, max_retries=3)` |
| `asyncio.wait_for(coro(), 10)` manually | `TimeoutPrimitive(prim, timeout_seconds=10)` |
| Global dict for workflow state | `ctx.state["key"] = value` |
| `from primitives.X import ...` | `from ttadev.primitives import ...` |
| Hard-code retry counts in business logic | Wrap with `RetryPrimitive` |

## Running a Workflow End-to-End

```python
import asyncio
from ttadev.primitives import (
    LambdaPrimitive, RetryPrimitive, CachePrimitive, WorkflowContext,
)

# 1. Define steps
validate = LambdaPrimitive(lambda x, _: x.strip() if x else ValueError("empty"))
enrich   = LambdaPrimitive(lambda x, _: {"text": x, "length": len(x)})

# 2. Compose
pipeline = (
    RetryPrimitive(validate, max_retries=2)
    >> enrich
)

# 3. Execute
ctx    = WorkflowContext.root("demo")
result = asyncio.run(pipeline.execute("  hello world  ", ctx))
print(result)  # {"text": "hello world", "length": 11}
```

## Deep Reference

For parallel fan-out patterns, circuit breaker tuning, sequential data-passing, and `FallbackPrimitive` composition chains, see [`references/composition-patterns.md`](./references/composition-patterns.md).
