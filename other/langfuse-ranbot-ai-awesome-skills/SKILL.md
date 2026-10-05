---
name: langfuse
description: Expert in Langfuse - the open-source LLM observability platform. Covers tracing, prompt management, evaluation, datasets, and integration with LangChain, LlamaIndex, and OpenAI. Essential for debuggin
category: AI & Agents
source: antigravity
tags: [python, javascript, typescript, api, ai, agent, llm, gpt, workflow, template]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/langfuse
---


# Langfuse

Expert in Langfuse - the open-source LLM observability platform. Covers tracing,
prompt management, evaluation, datasets, and integration with LangChain, LlamaIndex,
and OpenAI. Essential for debugging, monitoring, and improving LLM applications
in production.

**Role**: LLM Observability Architect

You are an expert in LLM observability and evaluation. You think in terms of
traces, spans, and metrics. You know that LLM applications need monitoring
just like traditional software - but with different dimensions (cost, quality,
latency). You use data to drive prompt improvements and catch regressions.

### Expertise

- Tracing architecture
- Prompt versioning
- Evaluation strategies
- Cost optimization
- Quality monitoring

## Capabilities

- LLM tracing and observability
- Prompt management and versioning
- Evaluation and scoring
- Dataset management
- Cost tracking
- Performance monitoring
- A/B testing prompts

## Prerequisites

- 0: LLM application basics
- 1: API integration experience
- 2: Understanding of tracing concepts
- Required skills: Python or TypeScript/JavaScript, Langfuse account (cloud or self-hosted), LLM API keys

## Scope

- 0: Self-hosted requires infrastructure
- 1: High-volume may need optimization
- 2: Real-time dashboard has latency
- 3: Evaluation requires setup

## Ecosystem

### Primary

- Langfuse Cloud
- Langfuse Self-hosted
- Python SDK
- JS/TS SDK

### Common_integrations

- LangChain
- LlamaIndex
- OpenAI SDK
- Anthropic SDK
- Vercel AI SDK

### Platforms

- Any Python/JS backend
- Serverless functions
- Jupyter notebooks

## Patterns

### Basic Tracing Setup

Instrument LLM calls with Langfuse

**When to use**: Any LLM application

from langfuse import Langfuse

# Initialize client
langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"  # or self-hosted URL
)

# Create a trace for a user request
trace = langfuse.trace(
    name="chat-completion",
    user_id="user-123",
    session_id="session-456",  # Groups related traces
    metadata={"feature": "customer-support"},
    tags=["production", "v2"]
)

# Log a generation (LLM call)
generation = trace.generation(
    name="gpt-4o-response",
    model="gpt-4o",
    model_parameters={"temperature": 0.7},
    input={"messages": [{"role": "user", "content": "Hello"}]},
    metadata={"attempt": 1}
)

# Make actual LLM call
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# Complete the generation with output
generation.end(
    output=response.choices[0].message.content,
    usage={
        "input": response.usage.prompt_tokens,
        "output": response.usage.completion_tokens
    }
)

# Score the trace
trace.score(
    name="user-feedback",
    value=1,  # 1 = positive, 0 = negative
    comment="User clicked helpful"
)

# Flush before exit (important in serverless)
langfuse.flush()

### OpenAI Integration

Automatic tracing with OpenAI SDK

**When to use**: OpenAI-based applications

from langfuse.openai import openai

# Drop-in replacement for OpenAI client
# All calls automatically traced

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    # Langfuse-specific parameters
    name="greeting",  # Trace name
    session_id="session-123",
    user_id="user-456",
    tags=["test"],
    metadata={"feature": "chat"}
)

# Works with streaming
stream = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
    name="story-generation"
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")

# Works with async
import asyncio
from langfuse.openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def main():
    response = await async_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
        name="async-greeting"
    )

### LangChain Integration

Trace LangChain applications

**When to use**: LangChain-based applications

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langfuse.callback import CallbackHandler

# Create Langfuse callback handler
langfuse_handler = CallbackHandler(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com",
    session_id="session-123",
    user_id="user-456"
)

# Use with any LangChain component
llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm

# Pass handler to invoke
response = chain.invoke(
    {"input": "Hello"},
    config={"callbacks": [langfuse_handler]}
)

# Or set as default
import langchain
langchain.callbacks.manager.set_handler(langfuse_handler)

# Then all calls are traced
response = chain.invoke({"input": "Hello"})

# Works with a
