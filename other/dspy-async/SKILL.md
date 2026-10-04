---
name: dspy-async
description: Use when you need to run DSPy modules asynchronously — FastAPI endpoints, concurrent LM calls, non-blocking execution, or integrating DSPy into async web frameworks. Common scenarios - serving DSPy behind FastAPI or Starlette, running multiple LM calls concurrently with asyncio.gather, non-blocking batch processing, combining async with streaming, or building async agent loops. Related - ai-serving-apis, dspy-parallel, dspy-streaming, dspy-utils. Also used for aforward, acall, async DSPy, await dspy, FastAPI with DSPy async, concurrent DSPy calls, asyncio with DSPy, non-blocking DSPy, async batch processing, semaphore concurrency limit, asyncio.gather DSPy, async web framework DSPy, Starlette DSPy, aiohttp DSPy.
---

# Run DSPy Modules Asynchronously

Guide the user through running DSPy modules with async/await for non-blocking execution in web frameworks, concurrent processing, and high-throughput applications.

## What is async in DSPy

Every DSPy module supports async execution via `aforward()` and `acall()`. These return awaitable coroutines instead of blocking the event loop, making DSPy compatible with async web frameworks (FastAPI, Starlette, aiohttp) and enabling concurrent LM calls with `asyncio.gather()`.

## When to use async

| Use async when... | Use sync when... |
|-------------------|-----------------|
| Serving DSPy behind FastAPI/Starlette | Running scripts or notebooks |
| Making concurrent LM calls | Processing one input at a time |
| Building real-time APIs | Running optimization/evaluation |
| Combining with async streaming | Simple CLI tools |
| Integrating with async databases/caches | No event loop in your application |

## Step 1: Basic async execution

Every DSPy module has an async variant:

```python
import asyncio
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

qa = dspy.ChainOfThought("question -> answer")

async def ask(question: str):
    # aforward() is the async version of forward()
    result = await qa.aforward(question=question)
    return result.answer

# Run it
answer = asyncio.run(ask("What is DSPy?"))
print(answer)
```

**Two async methods:**
- `module.aforward(**kwargs)` -- async version of `module.forward()`
- `module.acall(**kwargs)` -- async version of `module(**kwargs)` (same thing, convenience alias)

## Step 2: Concurrent calls with asyncio.gather

Run multiple independent LM calls concurrently:

```python
import asyncio
import dspy

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

summarizer = dspy.ChainOfThought("text -> summary")

async def summarize_batch(texts: list[str]):
    # Launch all summarizations concurrently
    tasks = [
        summarizer.aforward(text=text)
        for text in texts
    ]
    results = await asyncio.gather(*tasks)
    return [r.summary for r in results]

texts = ["Article 1...", "Article 2...", "Article 3..."]
summaries = asyncio.run(summarize_batch(texts))
```

This is significantly faster than sequential processing because LM calls are I/O-bound -- the network round-trip dominates.

## Step 3: FastAPI endpoint

```python
from fastapi import FastAPI
import dspy

app = FastAPI()

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

classifier = dspy.Predict("text -> label, confidence: float")

@app.post("/classify")
async def classify(text: str):
    # Non-blocking -- does not hold up other requests
    result = await classifier.aforward(text=text)
    return {"label": result.label, "confidence": result.confidence}
```

**Why this matters:** Without async, each request blocks the FastAPI worker thread. With `aforward()`, the worker is free to handle other requests while waiting for the LM response.

## Step 4: Semaphore-based concurrency limiting

Prevent overwhelming the LM provider with too many concurrent requests:

```python
import asyncio
import dspy

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

processor = dspy.ChainOfThought("input -> output")

# Limit to 10 concurrent LM calls
semaphore = asyncio.Semaphore(10)

async def process_one(input_text: str):
    async with semaphore:
        return await processor.aforward(input=input_text)

async def process_batch(inputs: list[str]):
    tasks = [process_one(text) for text in inputs]
    return await asyncio.gather(*tasks)

# Even with 1000 inputs, only 10 run concurrently
results = asyncio.run(process_batch(["input"] * 1000))
```

## Step 5: Async with streaming

Combine async execution with streaming output:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import dspy
from dspy.streaming import streamify, StreamListener

app = FastAPI()

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

qa = dspy.ChainOfThought("question -> answer")
listener = StreamListener(signature_field_name="answer")
streaming_qa = streamify(qa, stream_listeners=[listener])

@app.get("/ask")
async def ask(question: str):
    async def generate():
        async for chunk in streaming_qa(question=question):
            if hasattr(chunk, "answer"):
                yield f"data: {chunk.answer}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

## Step 6: Async custom modules

When writing custom modules, implement `aforward` for async:

```python
import dspy

class AsyncPipeline(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict("text -> category")
        self.summarize = dspy.ChainOfThought("text, category -> summary")

    async def aforward(self, text):
        # Run classification (async)
        classification = await self.classify.aforward(text=text)

        # Run summarization with the category (async)
        result = await self.summarize.aforward(
            text=text,
            category=classification.category,
        )
        return dspy.Prediction(
            category=classification.category,
            summary=result.summary,
        )

# Usage
pipeline = AsyncPipeline()
result = asyncio.run(pipeline.aforward(text="..."))
```

## Step 7: Async with ReAct agents

Agents with MCP tools or async tool functions need `acall()`:

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

async def async_search(query: str) -> str:
    """Search the web asynchronously."""
    # Your async search implementation
    return "results..."

agent = dspy.ReAct("question -> answer", tools=[async_search])

async def run_agent(question: str):
    # acall() handles async tools automatically
    result = await agent.acall(question=question)
    return result.answer
```

## Gotchas

1. **Claude uses `module()` inside async functions instead of `await module.aforward()`.** Calling a module synchronously inside an async function blocks the event loop. Always use `aforward()` or `acall()` in async contexts.
2. **Claude nests `asyncio.run()` inside an existing event loop.** You cannot call `asyncio.run()` from inside an async function -- it raises `RuntimeError: This event loop is already running`. Use `await` directly instead.
3. **Claude forgets the semaphore for batch processing.** Without a concurrency limit, `asyncio.gather()` with 1000 tasks hits rate limits immediately. Always add a semaphore when processing large batches.
4. **Claude defines `forward()` but not `aforward()` in custom modules.** If your module will be called with `await`, implement `aforward()`. DSPy does not auto-wrap `forward()` into an async version.
5. **Claude mixes sync and async in the same pipeline.** If one step is async (e.g., MCP tools), the entire call chain must be async. You cannot `await` inside a sync `forward()`.

## Additional resources

- [dspy.ai/api/modules](https://dspy.ai/api/modules/) (aforward documentation)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Serving APIs** with FastAPI -- see `/ai-serving-apis`
- **Concurrent batch processing** -- see `/dspy-parallel`
- **Streaming** output with async generators -- see `/dspy-streaming`
- **MCP tools** that require async -- see `/dspy-mcp`
- **General utilities** (caching, debugging) -- see `/dspy-utils`
- **Install `/ai-do` if you do not have it** -- it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
