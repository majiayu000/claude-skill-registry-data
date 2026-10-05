---
name: openai
description: OpenAI API integration — GPT models, embeddings, function calling, assistants, vision
layer: domain
category: ai
triggers:
  - "openai"
  - "gpt-4"
  - "chatgpt api"
  - "openai embeddings"
  - "openai assistants"
  - "openai function calling"
riskLevel: low
linksTo:
  - ai-sdk
  - rag
  - prompt-engineering
  - ai-agents
linkedFrom:
  - ai-sdk
  - rag
---

# OpenAI

> OpenAI API integration -- GPT models, embeddings, function calling, assistants, vision.

## When to Use
- Calling GPT models for chat completions or text generation
- Generating embeddings for vector search / RAG pipelines
- Building assistants with threads, runs, and tool use
- Image understanding with GPT-4o vision
- Structured JSON output or function/tool calling

## Key Patterns

### Chat Completions
- **Messages array**: `[{ role: "system" | "user" | "assistant", content }]`
- **Streaming**: Use `stream: true` and consume SSE chunks via `for await (const chunk of stream)`
- **Function calling**: Define `tools` with JSON Schema; model returns `tool_calls` to execute
- **Structured outputs**: `response_format: { type: "json_schema", json_schema: { ... } }` for guaranteed schema

### Embeddings
- `text-embedding-3-small` (1536d, cheap) or `text-embedding-3-large` (3072d, precise)
- Batch embed with `input: string[]` -- up to 2048 inputs per request
- Use cosine similarity for retrieval; same model for docs and queries

### Assistants API
- **Threads**: Persistent conversation state managed server-side
- **Runs**: Execute assistant on a thread; poll or stream for completion
- **Tools**: `code_interpreter`, `file_search`, or custom `function` tools
- **File search**: Built-in RAG with vector store attachments

### Vision
- Pass images as `content: [{ type: "image_url", image_url: { url } }]` in user messages
- Supports base64 data URIs and HTTP URLs
- Use `detail: "low" | "high" | "auto"` to control token cost

### Rate Limiting and Retries
- Respect `429` with exponential backoff (2^n seconds, jitter, max 60s)
- Track `x-ratelimit-remaining-*` headers; use `tiktoken` to count tokens before sending

### Fine-Tuning
- Prepare JSONL with `{"messages": [...]}` per line; validate token counts before submitting
- Upload file, create fine-tune job, monitor via events endpoint

## Anti-Patterns
- Ignoring token limits -- estimate usage with tiktoken before large prompts
- Hardcoding model names -- use config/env vars for easy upgrades
- Skipping error handling on streams -- network drops lose partial responses
- Mixing embedding models between docs and queries
- Polling assistant runs without backoff -- use streaming or exponential delay

## Related Skills
`ai-sdk` | `rag` | `prompt-engineering` | `ai-agents`
