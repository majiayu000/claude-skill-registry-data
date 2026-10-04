---
name: dspy-streaming
description: Use when you need to stream LM output tokens to a frontend in real time — progressive responses, typing indicators, server-sent events, or WebSocket feeds. Common scenarios - streaming DSPy responses to a React UI, FastAPI SSE endpoint with DSPy, showing AI typing in a chat interface, streaming multi-field outputs, streaming ReAct agent loop progress, or handling duplicate fields with predict_name. Related - ai-serving-apis, ai-building-chatbots, dspy-react, dspy-utils. Also used for dspy.streamify, dspy.streaming, StreamListener, StreamResponse, StatusMessage, stream tokens from DSPy, real-time AI output, server-sent events with DSPy, progressive response, show AI typing, streaming DSPy to frontend, async streaming generator, sync streaming fallback, multi-field streaming, allow_reuse streaming, predict_name streaming, streaming ReAct agent, FastAPI SSE DSPy.
---

# Stream LM Output with dspy.streamify and StreamListener

Guide the user through streaming DSPy module outputs token-by-token to frontends, APIs, or CLI interfaces using `dspy.streamify()` and `StreamListener`.

## What is streaming in DSPy

`dspy.streamify()` wraps any DSPy module and returns an async (or sync) generator that yields chunks as the LM produces tokens. `StreamListener` lets you target specific output fields. The stream yields three chunk types -- `StreamResponse` (partial tokens), `StatusMessage` (progress updates), and `Prediction` (final result).

## When to stream

| Stream when... | Do NOT stream when... |
|----------------|----------------------|
| Building a chat UI that shows typing | Batch processing many inputs |
| SSE/WebSocket endpoint for real-time display | Running optimization or evaluation |
| Long-form generation where users wait | Output is short (< 50 tokens) |
| ReAct agent loop where you show each step | Pipeline stages that feed into each other |

## Step 1: Basic streaming setup

```python
import dspy
from dspy.streaming import streamify, StreamListener

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# Your existing module
qa = dspy.ChainOfThought("question -> answer")

# Create a listener for a specific output field
answer_listener = StreamListener(signature_field_name="answer")

# Wrap the module for streaming
streaming_qa = streamify(
    qa,
    stream_listeners=[answer_listener],
)

# Consume the async generator
async for chunk in streaming_qa(question="What is DSPy?"):
    if hasattr(chunk, "answer"):
        print(chunk.answer, end="", flush=True)
```

## Step 2: Understanding chunk types

The stream yields three distinct types:

```python
async for chunk in streaming_qa(question="..."):
    if isinstance(chunk, dspy.streaming.StreamResponse):
        # Partial tokens for a field -- the main content you display
        print(chunk.answer, end="", flush=True)

    elif isinstance(chunk, dspy.streaming.StatusMessage):
        # Progress updates -- useful for UI status indicators
        print(f"[Status: {chunk.message}]")

    elif isinstance(chunk, dspy.Prediction):
        # Final complete result -- same as non-streaming output
        final_answer = chunk.answer
```

**Key behavior:**
- `StreamResponse` chunks contain partial text for the field(s) you are listening to
- `StatusMessage` appears during tool calls, retries, or multi-step processing
- The final `Prediction` appears last (unless `include_final_prediction_in_output_stream=False`)

## Step 3: Multi-field streaming

Stream multiple output fields simultaneously:

```python
class Summarize(dspy.Signature):
    """Summarize the document and extract key points."""
    document: str = dspy.InputField()
    summary: str = dspy.OutputField()
    key_points: str = dspy.OutputField()

summarizer = dspy.Predict(Summarize)

# Listen to both fields
summary_listener = StreamListener(signature_field_name="summary")
points_listener = StreamListener(signature_field_name="key_points")

streaming_summarizer = streamify(
    summarizer,
    stream_listeners=[summary_listener, points_listener],
)

async for chunk in streaming_summarizer(document="..."):
    if hasattr(chunk, "summary"):
        # Tokens for the summary field
        display_summary(chunk.summary)
    elif hasattr(chunk, "key_points"):
        # Tokens for the key_points field
        display_points(chunk.key_points)
```

**Note:** Fields stream sequentially in declaration order. The LM generates `summary` fully before starting `key_points`.

## Step 4: Streaming ReAct agent loops

For agents, use `allow_reuse=True` so the listener captures output across multiple reasoning iterations:

```python
from dspy.streaming import StatusMessageProvider

agent = dspy.ReAct("question -> answer", tools=[search, lookup])

# allow_reuse=True is critical for agents -- the agent generates
# multiple "answer" attempts across iterations
answer_listener = StreamListener(
    signature_field_name="answer",
    allow_reuse=True,
)

# status_message_provider must be a StatusMessageProvider subclass
# INSTANCE that overrides status hooks -- not a lambda
class AgentStatus(StatusMessageProvider):
    def tool_start_status_message(self, instance, inputs):
        return f"Calling {instance.name}..."

streaming_agent = streamify(
    agent,
    stream_listeners=[answer_listener],
    status_message_provider=AgentStatus(),
)

async for chunk in streaming_agent(question="..."):
    if isinstance(chunk, dspy.streaming.StatusMessage):
        show_progress(chunk.message)
    elif hasattr(chunk, "answer"):
        show_answer_token(chunk.answer)
```

## Step 5: Disambiguating duplicate fields with predict_name

When a module has multiple predictors with the same output field name, use `predict_name` to target a specific one:

```python
class Pipeline(dspy.Module):
    def __init__(self):
        self.draft = dspy.ChainOfThought("topic -> answer")
        self.refine = dspy.ChainOfThought("draft_answer -> answer")

    def forward(self, topic):
        draft = self.draft(topic=topic)
        return self.refine(draft_answer=draft.answer)

pipeline = Pipeline()

# Only stream the final refinement step, not the draft
final_listener = StreamListener(
    signature_field_name="answer",
    predict_name="refine",  # matches self.refine attribute name
)

streaming_pipeline = streamify(pipeline, stream_listeners=[final_listener])
```

## Step 6: FastAPI SSE integration

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import dspy
from dspy.streaming import streamify, StreamListener

app = FastAPI()

qa = dspy.ChainOfThought("question -> answer")
answer_listener = StreamListener(signature_field_name="answer")
streaming_qa = streamify(qa, stream_listeners=[answer_listener])

@app.get("/ask")
async def ask(question: str):
    async def event_stream():
        async for chunk in streaming_qa(question=question):
            if hasattr(chunk, "answer"):
                yield f"data: {chunk.answer}\n\n"
            elif isinstance(chunk, dspy.Prediction):
                yield f"data: [DONE]\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

## Step 7: Sync streaming fallback

For non-async contexts (scripts, notebooks), set `async_streaming=False`:

```python
streaming_qa = streamify(
    qa,
    stream_listeners=[answer_listener],
    async_streaming=False,  # Returns a sync generator
)

# Use regular for loop instead of async for
for chunk in streaming_qa(question="What is DSPy?"):
    if hasattr(chunk, "answer"):
        print(chunk.answer, end="", flush=True)
```

## Gotchas

1. **Claude omits `async_streaming=False` in non-async code.** If you use a regular `for` loop with an async generator, you get `TypeError: 'async_generator' object is not iterable`. Always set `async_streaming=False` for sync contexts.
2. **The listener buffers ~10 tokens before yielding.** This is by design -- ChatAdapter needs to detect field boundary delimiters (`[[ ## field_name ## ]]`) before it can emit tokens. First chunk arrives slightly delayed.
3. **Claude forgets `allow_reuse=True` for agents.** Without it, `StreamListener` only captures the first iteration. ReAct and CodeAct agents need `allow_reuse=True` to stream across multiple reasoning cycles.
4. **`include_final_prediction_in_output_stream=True` is the default.** The last item in the stream is always a `Prediction` object unless you explicitly disable it. Check for both `StreamResponse` and `Prediction` types.
5. **Claude wraps streamify in an extra async function.** `streamify()` already returns a callable that produces a generator. Do not wrap it in another async function -- just call it directly and iterate.

## Additional resources

- [dspy.ai/api/streaming](https://dspy.ai/api/streaming/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Serving streaming endpoints** -- see `/ai-serving-apis`
- **Building chat UIs** with streaming -- see `/ai-building-chatbots`
- **ReAct agents** that benefit from streaming -- see `/dspy-react`
- **Async execution** patterns -- see `/dspy-async`
- **General DSPy utilities** (caching, debugging) -- see `/dspy-utils`
- **Install `/ai-do` if you do not have it** -- it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
