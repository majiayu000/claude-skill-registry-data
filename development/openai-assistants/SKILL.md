---
name: openai-assistants
description: |
  Build stateful chatbots with OpenAI Assistants API v2 - Code Interpreter, File Search (10k files), Function Calling. ⚠️ Deprecated (sunset August 26, 2026); use openai-responses for new projects.

  Use when: maintaining legacy chatbots, implementing RAG with vector stores, or troubleshooting "thread has active run", vector store delays, polling timeouts, or file upload errors.
---

# OpenAI Assistants API v2

**Status**: Production Ready (⚠️ Deprecated - Sunset August 26, 2026)
**Package**: openai@6.15.0
**Last Updated**: 2026-01-03
**v1 Deprecated**: December 18, 2024
**v2 Sunset**: August 26, 2026 (migrate to Responses API)

---

## ⚠️ Deprecation Notice

**OpenAI is deprecating Assistants API in favor of [Responses API](../openai-responses/SKILL.md).**

**Timeline**: v1 deprecated Dec 18, 2024 | v2 sunset August 26, 2026

**Use this skill if**: Maintaining legacy apps or migrating existing code (12-18 month window)
**Don't use if**: Starting new projects (use `openai-responses` skill instead)

**Migration**: See `references/migration-to-responses.md`

---

## Quick Start

```bash
npm install openai@6.15.0
```

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// 1. Create assistant
const assistant = await openai.beta.assistants.create({
  name: "Math Tutor",
  instructions: "You are a math tutor. Use code interpreter for calculations.",
  tools: [{ type: "code_interpreter" }],
  model: "gpt-4o",
});

// 2. Create thread
const thread = await openai.beta.threads.create();

// 3. Add message
await openai.beta.threads.messages.create(thread.id, {
  role: "user",
  content: "Solve: 3x + 11 = 14",
});

// 4. Run assistant
const run = await openai.beta.threads.runs.create(thread.id, {
  assistant_id: assistant.id,
});

// 5. Poll for completion
let status = await openai.beta.threads.runs.retrieve(thread.id, run.id);
while (status.status !== 'completed') {
  await new Promise(r => setTimeout(r, 1000));
  status = await openai.beta.threads.runs.retrieve(thread.id, run.id);
}

// 6. Get response
const messages = await openai.beta.threads.messages.list(thread.id);
console.log(messages.data[0].content[0].text.value);
```

---

## Core Concepts

**Four Main Objects:**

1. **Assistants**: Configured AI with instructions (max 256k chars in v2, was 32k in v1), model, tools, metadata
2. **Threads**: Conversation containers with persistent message history (max 100k messages)
3. **Messages**: User/assistant messages with optional file attachments
4. **Runs**: Async execution with states (queued, in_progress, requires_action, completed, failed, expired)

---

## Key API Patterns

### Assistants

```typescript
const assistant = await openai.beta.assistants.create({
  model: "gpt-4o",
  instructions: "System prompt (max 256k chars in v2)",
  tools: [{ type: "code_interpreter" }, { type: "file_search" }],
  tool_resources: { file_search: { vector_store_ids: ["vs_123"] } },
});
```

**Key Limits**: 256k instruction chars (v2), 128 tools max, 16 metadata pairs

### Threads & Messages

```typescript
// Create thread with messages
const thread = await openai.beta.threads.create({
  messages: [{ role: "user", content: "Hello" }],
});

// Add message with attachments
await openai.beta.threads.messages.create(thread.id, {
  role: "user",
  content: "Analyze this",
  attachments: [{ file_id: "file_123", tools: [{ type: "code_interpreter" }] }],
});

// List messages
const msgs = await openai.beta.threads.messages.list(thread.id);
```

**Key Limits**: 100k messages per thread

---

### Runs

```typescript
// Create run with optional overrides
const run = await openai.beta.threads.runs.create(thread.id, {
  assistant_id: "asst_123",
  additional_messages: [{ role: "user", content: "Question" }],
  max_prompt_tokens: 1000,
  max_completion_tokens: 500,
});

// Poll until complete
let status = await openai.beta.threads.runs.retrieve(thread.id, run.id);
while (['queued', 'in_progress'].includes(status.status)) {
  await new Promise(r => setTimeout(r, 1000));
  status = await openai.beta.threads.runs.retrieve(thread.id, run.id);
}
```

**Run States**: `queued` → `in_progress` → `requires_action` (function calling) / `completed` / `failed` / `cancelled` / `expired` (10 min max)

---

### Streaming

```typescript
const stream = await openai.beta.threads.runs.stream(thread.id, { assistant_id });

for await (const event of stream) {
  if (event.event === 'thread.message.delta') {
    process.stdout.write(event.data.delta.content?.[0]?.text?.value || '');
  }
}
```

**Key Events**: `thread.run.created`, `thread.message.delta` (streaming content), `thread.run.step.delta` (tool progress), `thread.run.completed`, `thread.run.requires_action` (function calling)

---

## Tools

### Code Interpreter

Runs Python code in sandbox. Generates charts, processes files (CSV, JSON, PDF, images). Max 512MB per file.

```typescript
// Attach file to message
attachments: [{ file_id: "file_123", tools: [{ type: "code_interpreter" }] }]

// Access generated files
for (const content of message.content) {
  if (content.type === 'image_file') {
    const fileContent = await openai.files.content(content.image_file.file_id);
  }
}
```

### File Search (RAG)

Semantic search with vector stores. **10,000 files max** (v2, was 20 in v1). **Pricing**: $0.10/GB/day (1GB free).

```typescript
// Create vector store
const vs = await openai.beta.vectorStores.create({ name: "Docs" });
await openai.beta.vectorStores.files.create(vs.id, { file_id: "file_123" });

// Wait for indexing
let store = await openai.beta.vectorStores.retrieve(vs.id);
while (store.status === 'in_progress') {
  await new Promise(r => setTimeout(r, 2000));
  store = await openai.beta.vectorStores.retrieve(vs.id);
}

// Use in assistant
tool_resources: { file_search: { vector_store_ids: [vs.id] } }
```

**⚠️ Wait for `status: 'completed'` before using**

### Function Calling

Submit tool outputs when run.status === 'requires_action':

```typescript
if (run.status === 'requires_action') {
  const toolCalls = run.required_action.submit_tool_outputs.tool_calls;
  const outputs = toolCalls.map(tc => ({
    tool_call_id: tc.id,
    output: JSON.stringify(yourFunction(JSON.parse(tc.function.arguments))),
  }));

  run = await openai.beta.threads.runs.submitToolOutputs(thread.id, run.id, {
    tool_outputs: outputs,
  });
}
```

## File Formats

**Code Interpreter**: .c, .cpp, .csv, .docx, .html, .java, .json, .md, .pdf, .php, .pptx, .py, .rb, .tex, .txt, .css, .jpeg, .jpg, .js, .gif, .png, .tar, .ts, .xlsx, .xml, .zip (512MB max)

**File Search**: .c, .cpp, .docx, .html, .java, .json, .md, .pdf, .php, .pptx, .py, .rb, .tex, .txt, .css, .js, .ts, .go (512MB max)

---

## Known Issues

**1. Thread Already Has Active Run**
```
Error: 400 Can't add messages to thread_xxx while a run run_xxx is active.
```
**Fix**: Cancel active run first: `await openai.beta.threads.runs.cancel(threadId, runId)`

**2. Run Polling Timeout**
Long-running tasks (Code Interpreter, File Search) may exceed polling windows.
**Fix**: Set max timeout (e.g., 5 min) and cancel if exceeded

**3. Vector Store Not Ready**
Using vector store before indexing completes.
**Fix**: Poll `vectorStores.retrieve()` until `status === 'completed'` (see File Search section)

**4. File Upload Format Issues**
Unsupported file formats cause silent failures.
**Fix**: Validate file extensions before upload (see File Formats section)

See `references/top-errors.md` for complete catalog.

## Relationship to Other Skills

**openai-api** (Chat Completions): Stateless, manual history, direct responses. Use for simple generation.

**openai-responses** (Responses API): ✅ **Recommended for new projects**. Better reasoning, modern MCP integration, active development.

**openai-assistants**: ⚠️ **Deprecated H1 2026**. Use for legacy apps only. Migration: `references/migration-to-responses.md`

---

## v1 to v2 Migration

**v1 deprecated**: Dec 18, 2024

**Key Changes**: `retrieval` → `file_search`, vector stores (10k files vs 20), 256k instructions (vs 32k), message-level file attachments

See `references/migration-from-v1.md`

---

**Templates**: `templates/basic-assistant.ts`, `code-interpreter-assistant.ts`, `file-search-assistant.ts`, `function-calling-assistant.ts`, `streaming-assistant.ts`

**References**: `references/top-errors.md`, `thread-lifecycle.md`, `vector-stores.md`, `migration-to-responses.md`, `migration-from-v1.md`

**Related Skills**: `openai-responses` (recommended), `openai-api`

---

**Last Updated**: 2025-11-27
**Package**: openai@6.9.1
**Status**: Production Ready (⚠️ Deprecated - Sunset H1 2026)
