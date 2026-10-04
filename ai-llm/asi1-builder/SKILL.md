---
name: asi1-builder
description: Complete reference and build guide for ASI:One (ASI1) — the AI platform by Fetch.ai built for agentic, Web3-native applications. Use this skill IMMEDIATELY and ALWAYS when the user mentions ASI1, ASI:One, Fetch.ai AI API, building with ASI1, integrating ASI:One, asking about ASI1 models, tool calling with ASI1, ASI1 image generation, ASI1 agentic LLM, Agentverse, uagents, Agent Chat Protocol, structured output with ASI1, or OpenAI-compatible wrappers for ASI1. Also trigger when the user says things like "use ASI1 instead of OpenAI", "build an app with ASI:One", "ASI1 API", or references docs.asi1.ai. This skill covers everything needed to build production apps - setup, all models, all API features, tool calling, image gen, agentic orchestration, structured data, session management, streaming, LangChain integration, uagents / Agent Chat Protocol, and TypeScript/Node.js patterns.
---

# ASI:One (ASI1) Builder Skill

**ASI:One** is an intelligent AI platform by [Fetch.ai](https://fetch.ai/) that unifies LLM inference, agentic orchestration (via the [Agentverse marketplace](https://agentverse.ai/)), image generation, tool calling, and Web3-native features behind a single OpenAI-compatible API.

Base URL: `https://api.asi1.ai/v1`
API Key header: `Authorization: Bearer $ASI_ONE_API_KEY`
Docs: https://docs.asi1.ai

---

## Models

ASI1 uses **one model string** that auto-activates capabilities based on context and parameters:

| Model String | Use When |
|---|---|
| `asi1` | Default — full agentic orchestration, Agentverse discovery, all capabilities |
| `asi1-mini` | Tool calling, image gen, lower latency general use |
| `asi1-fast` | Tool calling, lowest latency, real-time applications |
| `asi1-extended` | Tool calling, deep reasoning, complex analysis |

**Key specs:**
- Context window: up to **128,000 tokens**
- Streaming: supported on all models
- OpenAI SDK: fully compatible (swap `base_url` only)

### Auto-Activated Capabilities (asi1)

| Capability | What it does |
|---|---|
| Agentic Reasoning | Discovers & orchestrates agents from Agentverse marketplace |
| Extended Reasoning | Multi-step analysis, chain-of-thought |
| Fast Inference | Low-latency path for simple tasks |
| Tool Calling | External function/API integration |
| Visualization | Charts & graphs from data |
| Web3 Native | Smart contracts, tokenomics, on-chain reasoning |

---

## Quick Start

### cURL
```bash
curl -X POST https://api.asi1.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ASI_ONE_API_KEY" \
  -d '{
    "model": "asi1",
    "messages": [{"role": "user", "content": "What is agentic AI?"}]
  }'
```

### TypeScript / Node.js (OpenAI SDK)
```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.ASI_ONE_API_KEY!,
  baseURL: 'https://api.asi1.ai/v1',
});

const response = await client.chat.completions.create({
  model: 'asi1',
  messages: [
    { role: 'system', content: 'Be precise and concise.' },
    { role: 'user', content: 'Explain agentic AI.' },
  ],
  temperature: 0.7,
  max_tokens: 1000,
});

console.log(response.choices[0].message.content);
```

### Python (OpenAI SDK)
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_ASI_ONE_API_KEY",
    base_url="https://api.asi1.ai/v1"
)

response = client.chat.completions.create(
    model="asi1",
    messages=[
        {"role": "system", "content": "Be precise and concise."},
        {"role": "user", "content": "What is agentic AI?"}
    ],
    temperature=0.2,
    max_tokens=1000,
)
print(response.choices[0].message.content)
```

---

## Response Structure

Standard OpenAI fields + ASI:One-specific fields:

```json
{
  "id": "...",
  "choices": [{
    "finish_reason": "stop",
    "index": 0,
    "message": {
      "content": "...",
      "role": "assistant",
      "tool_calls": null
    }
  }],
  "usage": {
    "completion_tokens": 149,
    "prompt_tokens": 2105,
    "total_tokens": 2254
  },
  "executable_data": [],    // ASI:One — agent manifests/tool calls from Agentverse
  "intermediate_steps": [], // ASI:One — multi-step reasoning traces
  "thought": [],            // ASI:One — model reasoning process
  "metadata": { "weight_version": "default" }
}
```

---

## API Parameters Reference

### Chat Completions — `POST /v1/chat/completions`

**Headers:**
- `Authorization: Bearer <api_key>` (required)
- `x-session-id: <uuid>` (required for agentic model session persistence)

**Body:**

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `model` | string | ✅ | `asi1`, `asi1-mini`, `asi1-fast`, `asi1-extended` |
| `messages` | array | ✅ | Standard chat array |
| `stream` | boolean | ❌ | SSE streaming |
| `temperature` | float | ❌ | 0–2 |
| `max_tokens` | integer | ❌ | Max response tokens |
| `top_p` | float | ❌ | Nucleus sampling |
| `frequency_penalty` | float | ❌ | -2.0 to 2.0 |
| `presence_penalty` | float | ❌ | -2.0 to 2.0 |
| `tools` | array | ❌ | Tool definitions for function calling |
| `tool_choice` | string/object | ❌ | `"auto"`, `"required"`, `"none"`, or `{type, function}` |
| `parallel_tool_calls` | boolean | ❌ | Default true |
| `response_format` | object | ❌ | For structured JSON output |
| `web_search` | boolean | ❌ | Enable built-in web search |
| `agent_address` | string | ❌ | Target specific Agentverse agent |
| `planner_mode` | boolean | ❌ | Enable ASI Planner |
| `study_mode` | boolean | ❌ | Enable study/research mode |

---

## Feature Deep-Dives

For detailed implementation docs, see the reference files:

- **`references/tool-calling.md`** — Tool definitions, execution cycle, strict mode, parallel calls
- **`references/image-generation.md`** — Image gen endpoint, sizes, prompting, batch patterns
- **`references/agentic-llm.md`** — Session management, async polling, Agentverse integration
- **`references/structured-data.md`** — JSON schema output, Pydantic/LangChain patterns
- **`references/agent-chat-protocol.md`** — uagents, Chat Protocol, inter-agent messaging (Python)
- **`references/openai-compat.md`** — Full OpenAI SDK compatibility, LangChain, streaming, web search

Read the relevant reference file(s) based on what the user needs to build.

---

## TypeScript Patterns (Quick Reference)

### Streaming
```typescript
const stream = await client.chat.completions.create({
  model: 'asi1',
  messages: [{ role: 'user', content: 'Tell me about Web3' }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? '');
}
```

### Session-based Agentic Calls
```typescript
import { v4 as uuidv4 } from 'uuid';

const sessionId = uuidv4();

const response = await client.chat.completions.create(
  {
    model: 'asi1',
    messages: [{ role: 'user', content: 'Check flight arrivals at Delhi airport' }],
    stream: true,
  },
  {
    headers: { 'x-session-id': sessionId },
  }
);
```

### Web Search Enabled
```typescript
const response = await client.chat.completions.create({
  model: 'asi1',
  messages: [{ role: 'user', content: 'Latest AI research 2025' }],
  // @ts-ignore — ASI:One-specific extra body field
  extra_body: { web_search: true },
});
```

---

## Getting an API Key

1. Sign up at https://asi1.ai/
2. Navigate to the Developer Section
3. Click **Create New** → name it → save the key

Set it as env var: `ASI_ONE_API_KEY=your_key_here`

---

## Key Gotchas

- Always use `x-session-id` header when using `asi1` model for multi-turn agentic tasks
- Tool calling is supported on `asi1-mini`, `asi1-fast`, `asi1-extended` (not base `asi1` alone)
- Image generation uses a **separate endpoint**: `POST /v1/image/generate`
- Structured output: set `strict: true` AND `additionalProperties: false` AND list all fields in `required`
- Tool result `content` must be JSON-stringified (a string, not an object)
- Preserve exact `tool_call_id` values when sending tool results back
- For async Agentverse agent tasks: poll with follow-up messages ("Any update?") until response changes
