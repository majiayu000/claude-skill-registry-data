---
name: openai-responses
description: |
  Build agentic AI applications with OpenAI's Responses API - the stateful successor to Chat Completions. Preserves reasoning across turns for 5% better multi-turn performance and 40-80% improved cache utilization.

  Use when: building AI agents with persistent reasoning, integrating MCP servers for external tools, using built-in Code Interpreter/File Search/Web Search, managing stateful conversations, implementing background processing for long tasks, or migrating from Chat Completions to gain polymorphic outputs and server-side tools.
---

# OpenAI Responses API

**Status**: Production Ready
**Last Updated**: 2025-11-27
**API Launch**: March 2025
**Dependencies**: openai@6.9.1 (Node.js) or fetch API (Cloudflare Workers)

---

## What Is the Responses API?

OpenAI's unified interface for agentic applications, launched **March 2025**. Provides **stateful conversations** with **preserved reasoning state** across turns.

**Key Innovation:** Unlike Chat Completions (reasoning discarded between turns), Responses **preserves the model's reasoning notebook**, improving performance by **5% on TAUBench** and enabling better multi-turn interactions.

**vs Chat Completions:**

| Feature | Chat Completions | Responses API |
|---------|-----------------|---------------|
| State | Manual history tracking | Automatic (conversation IDs) |
| Reasoning | Dropped between turns | Preserved across turns (+5% TAUBench) |
| Tools | Client-side round trips | Server-side hosted |
| Output | Single message | Polymorphic (8 types) |
| Cache | Baseline | **40-80% better utilization** |
| MCP | Manual | Built-in |

---

## Quick Start

```bash
npm install openai@6.9.1
```

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'What are the 5 Ds of dodgeball?',
});

console.log(response.output_text);
```

**Key differences from Chat Completions:**
- Endpoint: `/v1/responses` (not `/v1/chat/completions`)
- Parameter: `input` (not `messages`)
- Role: `developer` (not `system`)
- Output: `response.output_text` (not `choices[0].message.content`)

---

## When to Use Responses vs Chat Completions

**Use Responses:**
- Agentic applications (reasoning + actions)
- Multi-turn conversations (preserved reasoning = +5% TAUBench)
- Built-in tools (Code Interpreter, File Search, Web Search, MCP)
- Background processing (60s standard, 10min extended timeout)

**Use Chat Completions:**
- Simple one-off generation
- Fully stateless interactions
- Legacy integrations

---

## Stateful Conversations

**Automatic State Management** using conversation IDs:

```typescript
// Create conversation
const conv = await openai.conversations.create({
  metadata: { user_id: 'user_123' },
});

// First turn
const response1 = await openai.responses.create({
  model: 'gpt-5',
  conversation: conv.id,
  input: 'What are the 5 Ds of dodgeball?',
});

// Second turn - model remembers context + reasoning
const response2 = await openai.responses.create({
  model: 'gpt-5',
  conversation: conv.id,
  input: 'Tell me more about the first one',
});
```

**Benefits:** No manual history tracking, reasoning preserved, 40-80% better cache utilization

**Conversation Limits:** 90-day expiration

---

## Built-in Tools (Server-Side)

**Server-side hosted tools** eliminate backend round trips:

| Tool | Purpose | Notes |
|------|---------|-------|
| `code_interpreter` | Execute Python code | Sandboxed, 30s timeout (use `background: true` for longer) |
| `file_search` | RAG without vector stores | Max 512MB per file, supports PDF/Word/Markdown/HTML/code |
| `web_search` | Real-time web information | Automatic source citations |
| `image_generation` | DALL-E integration | DALL-E 3 default |
| `mcp` | Connect external tools | OAuth supported, tokens NOT stored |

**Usage:**
```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Calculate mean of: 10, 20, 30, 40, 50',
  tools: [{ type: 'code_interpreter' }],
});
```

---

## MCP Server Integration

Built-in support for **Model Context Protocol (MCP)** servers to connect external tools (Stripe, databases, custom APIs).

**Basic MCP:**
```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Roll 2d6 dice',
  tools: [{
    type: 'mcp',
    server_label: 'dice',
    server_url: 'https://example.com/mcp',
    authorization: process.env.TOKEN, // ⚠️ NOT stored, required each request
  }],
});
```

**MCP Output Types:**
- `mcp_list_tools` - Tools discovered on server
- `mcp_call` - Tool invocation + result
- `message` - Final response

---

## Reasoning Preservation

**Key Innovation:** Model's internal reasoning state survives across turns (unlike Chat Completions which discards it).

**Visual Analogy:**
- Chat Completions: Model tears out scratchpad page before responding
- Responses API: Scratchpad stays open for next turn

**Performance:** +5% on TAUBench (GPT-5) purely from preserved reasoning

**Reasoning Summaries** (free):
```typescript
response.output.forEach(item => {
  if (item.type === 'reasoning') console.log(item.summary[0].text);
  if (item.type === 'message') console.log(item.content[0].text);
});
```

---

## Background Mode

For long-running tasks, use `background: true`:

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Analyze 500-page document',
  background: true,
  tools: [{ type: 'file_search', file_ids: [fileId] }],
});

// Poll for completion (check every 5s)
const result = await openai.responses.retrieve(response.id);
if (result.status === 'completed') console.log(result.output_text);
```

**Timeout Limits:**
- Standard: 60 seconds
- Background: 10 minutes

---

## Polymorphic Outputs

Returns **8 output types** instead of single message:

| Type | Example |
|------|---------|
| `message` | Final answer, explanation |
| `reasoning` | Step-by-step thought process (free!) |
| `code_interpreter_call` | Python code + results |
| `mcp_call` | Tool name, args, output |
| `mcp_list_tools` | Tool definitions from MCP server |
| `file_search_call` | Matched chunks, citations |
| `web_search_call` | URLs, snippets |
| `image_generation_call` | Image URL |

**Processing:**
```typescript
response.output.forEach(item => {
  if (item.type === 'reasoning') console.log(item.summary[0].text);
  if (item.type === 'web_search_call') console.log(item.results);
  if (item.type === 'message') console.log(item.content[0].text);
});

// Or use helper for text-only
console.log(response.output_text);
```

---

## Migration from Chat Completions

**Breaking Changes:**

| Feature | Chat Completions | Responses API |
|---------|-----------------|---------------|
| Endpoint | `/v1/chat/completions` | `/v1/responses` |
| Parameter | `messages` | `input` |
| Role | `system` | `developer` |
| Output | `choices[0].message.content` | `output_text` |
| State | Manual array | Automatic (conversation ID) |
| Streaming | `data: {"choices":[...]}` | SSE with 8 item types |

**Example:**
```typescript
// Before
const response = await openai.chat.completions.create({
  model: 'gpt-5',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' },
  ],
});
console.log(response.choices[0].message.content);

// After
const response = await openai.responses.create({
  model: 'gpt-5',
  input: [
    { role: 'developer', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' },
  ],
});
console.log(response.output_text);
```

---

## Error Handling

**8 Common Errors:**

**1. Session State Not Persisting**
- Cause: Not using conversation IDs or using different IDs per turn
- Fix: Create conversation once (`const conv = await openai.conversations.create()`), reuse `conv.id` for all turns

**2. MCP Server Connection Failed** (`mcp_connection_error`)
- Causes: Invalid URL, missing/expired auth token, server down
- Fix: Verify URL is correct, test manually with `fetch()`, check token expiration

**3. Code Interpreter Timeout** (`code_interpreter_timeout`)
- Cause: Code runs longer than 30 seconds
- Fix: Use `background: true` for extended timeout (up to 10 min)

**4. Image Generation Rate Limit** (`rate_limit_error`)
- Cause: Too many DALL-E requests
- Fix: Implement exponential backoff retry (1s, 2s, 3s delays)

**5. File Search Relevance Issues**
- Cause: Vague queries return irrelevant results
- Fix: Use specific queries ("pricing in Q4 2024" not "find pricing"), filter by `chunk.score > 0.7`

**6. Cost Tracking Confusion**
- Cause: Responses bills for input + output + tools + stored conversations (vs Chat Completions: input + output only)
- Fix: Set `store: false` if not needed, monitor `response.usage.tool_tokens`

**7. Conversation Not Found** (`invalid_request_error`)
- Causes: ID typo, conversation deleted, or expired (90-day limit)
- Fix: Verify exists with `openai.conversations.list()` before using

**8. Tool Output Parsing Failed**
- Cause: Accessing wrong output structure
- Fix: Use `response.output_text` helper or iterate `response.output.forEach(item => ...)` checking `item.type`

---

## Critical Patterns

**✅ Always:**
- Use conversation IDs for multi-turn (40-80% better cache)
- Handle all 8 output types in polymorphic responses
- Use `background: true` for tasks >30s
- Provide MCP `authorization` tokens (NOT stored, required each request)
- Monitor `response.usage.total_tokens` for cost control

**❌ Never:**
- Expose API keys in client-side code
- Assume single message output (use `response.output_text` helper)
- Reuse conversation IDs across users (security risk)
- Ignore error types (handle `rate_limit_error`, `mcp_connection_error` specifically)
- Poll faster than 1s for background tasks (use 5s intervals)

---

## References

**Official Docs:**
- Responses API Guide: https://platform.openai.com/docs/guides/responses
- API Reference: https://platform.openai.com/docs/api-reference/responses
- MCP Integration: https://platform.openai.com/docs/guides/tools-connectors-mcp
- Blog Post: https://developers.openai.com/blog/responses-api/
- Starter App: https://github.com/openai/openai-responses-starter-app

**Skill Resources:** `templates/`, `references/responses-vs-chat-completions.md`, `references/mcp-integration-guide.md`, `references/built-in-tools-guide.md`, `references/migration-guide.md`, `references/top-errors.md`
