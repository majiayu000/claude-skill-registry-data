---
name: ai-sdk-core
description: |
  Build backend AI with Vercel AI SDK v5/v6. v6 stable introduces Output API (Output.object/array/choice
  replace deprecated generateObject/streamObject), plus speech synthesis, transcription, image generation,
  embeddings, reranking, MCP tools, and middleware. Covers v4→v5 migration, latest models (GPT-5.2,
  Claude 4.x, Gemini 2.5), Workers startup fix, and 12 error solutions.

  Use when: implementing AI SDK v5/v6, using Output API, speech/transcription/image features, embeddings,
  MCP tools, migrating v4→v5, troubleshooting errors, or fixing Workers startup issues.
---

# AI SDK Core

Backend AI with Vercel AI SDK v5 and v6.

**Installation:**
```bash
npm install ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google zod
```

---

## AI SDK 6 (Stable - January 2026)

**Status:** Stable
**Latest:** ai@6.1.0 (Jan 2026)

### BREAKING: Output API Replaces generateObject/streamObject

⚠️ **CRITICAL**: `generateObject()` and `streamObject()` are **DEPRECATED** and will be removed in a future version. Use the new Output API instead.

**Before (v5 - DEPRECATED):**
```typescript
// ❌ DEPRECATED - will be removed
import { generateObject } from 'ai';

const result = await generateObject({
  model: openai('gpt-5'),
  schema: z.object({ name: z.string(), age: z.number() }),
  prompt: 'Generate a person',
});
```

**After (v6 - USE THIS):**
```typescript
// ✅ NEW OUTPUT API
import { generateText, Output } from 'ai';

const result = await generateText({
  model: openai('gpt-5'),
  output: Output.object({ schema: z.object({ name: z.string(), age: z.number() }) }),
  prompt: 'Generate a person',
});

// Access the typed object
console.log(result.object); // { name: "Alice", age: 30 }
```

### Output Types

```typescript
import { generateText, Output } from 'ai';

// Object with Zod schema
output: Output.object({ schema: myZodSchema })

// Array of typed objects
output: Output.array({ schema: personSchema })

// Enum/choice from options
output: Output.choice({ choices: ['positive', 'negative', 'neutral'] })

// Plain text (explicit)
output: Output.text()

// Unstructured JSON (no schema validation)
output: Output.json()
```

### Streaming with Output API

```typescript
import { streamText, Output } from 'ai';

const result = streamText({
  model: openai('gpt-5'),
  output: Output.object({ schema: personSchema }),
  prompt: 'Generate a person',
});

// Stream partial objects
for await (const partialObject of result.objectStream) {
  console.log(partialObject); // { name: "Ali..." } -> { name: "Alice", age: ... }
}

// Get final object
const finalObject = await result.object;
```

### v6 New Features

**1. Agent Abstraction**
Unified interface for building agents with `ToolLoopAgent` class:
- Full control over execution flow, tool loops, and state management
- Replaces manual tool calling orchestration

**2. Tool Execution Approval (Human-in-the-Loop)**
```typescript
tools: {
  payment: tool({
    needsApproval: true,  // Always ask
    // OR dynamic:
    needsApproval: async ({ amount }) => amount > 1000,
    inputSchema: z.object({ amount: z.number() }),
    execute: async ({ amount }) => { /* process payment */ },
  }),
}
```

**3. Reranking for RAG**
```typescript
import { rerank } from 'ai';

const result = await rerank({
  model: cohere.reranker('rerank-v3.5'),
  query: 'user question',
  documents: searchResults,
  topK: 5,
});
```

**4. MCP Tools (Model Context Protocol)**
```typescript
import { experimental_createMCPClient } from 'ai';

const mcpClient = await experimental_createMCPClient({
  transport: { type: 'stdio', command: 'npx', args: ['-y', '@modelcontextprotocol/server-filesystem'] },
});

const tools = await mcpClient.tools();

const result = await generateText({
  model: openai('gpt-5'),
  tools,
  prompt: 'List files in the current directory',
});
```

**5. Language Model Middleware**
```typescript
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const wrappedModel = wrapLanguageModel({
  model: anthropic('claude-sonnet-4-5-20250929'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});

// Reasoning extracted automatically from <think>...</think> tags
```

**6. Telemetry (OpenTelemetry)**
```typescript
const result = await generateText({
  model: openai('gpt-5'),
  prompt: 'Hello',
  experimental_telemetry: {
    isEnabled: true,
    functionId: 'my-chat-function',
    metadata: { userId: '123' },
    recordInputs: true,
    recordOutputs: true,
  },
});
```

**Official Docs:** https://ai-sdk.dev/docs

---

## Latest AI Models (2025-2026)

### OpenAI

**GPT-5.2** (Dec 2025):
- 400k context window, 128k output tokens
- Enhanced reasoning capabilities
- Available in API platform

**GPT-5.1** (Nov 2025):
- Improved speed and efficiency over GPT-5
- "Warmer" and more intelligent responses

**GPT-5** (Aug 2025):
- 45% less hallucination than GPT-4o
- State-of-the-art in math, coding, visual perception

**o3 Reasoning Models** (Dec 2025):
- o3, o3-pro, o3-mini - Advanced reasoning
- o4-mini - Fast reasoning

```typescript
import { openai } from '@ai-sdk/openai';
const gpt52 = openai('gpt-5.2');
const gpt51 = openai('gpt-5.1');
const gpt5 = openai('gpt-5');
const o3 = openai('o3');
const o3mini = openai('o3-mini');
```

### Anthropic

**Claude 4 Family** (May-Oct 2025):
- **Opus 4** (May 22): Best for complex reasoning, $15/$75 per million tokens
- **Sonnet 4** (May 22): Balanced performance, $3/$15 per million tokens
- **Opus 4.1** (Aug 5): Enhanced agentic tasks, real-world coding
- **Sonnet 4.5** (Sept 29): Most capable for coding, agents, computer use
- **Haiku 4.5** (Oct 15): Small, fast, low-latency model

```typescript
import { anthropic } from '@ai-sdk/anthropic';
const sonnet45 = anthropic('claude-sonnet-4-5-20250929');  // Latest
const opus41 = anthropic('claude-opus-4-1-20250805');
const haiku45 = anthropic('claude-haiku-4-5-20251015');
```

### Google

**Gemini 2.5 Family** (Mar-Sept 2025):
- **Pro** (March 2025): Most intelligent, #1 on LMArena at launch
- **Pro Deep Think** (May 2025): Enhanced reasoning mode
- **Flash** (May 2025): Fast, cost-effective
- **Flash-Lite** (Sept 2025): Updated efficiency

```typescript
import { google } from '@ai-sdk/google';
const pro = google('gemini-2.5-pro');
const flash = google('gemini-2.5-flash');
const lite = google('gemini-2.5-flash-lite');
```

---

## Core Functions

### Text Generation

**generateText()** - Text completion with tools
**streamText()** - Real-time streaming

### Structured Output (v6 Output API)

**Output.object()** - Typed objects with Zod schema (replaces generateObject)
**Output.array()** - Typed arrays
**Output.choice()** - Enum selection
**Output.json()** - Unstructured JSON

See "AI SDK 6" section above for usage examples.

### Multi-Modal Capabilities

#### Speech Synthesis (Text-to-Speech)

```typescript
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateSpeech({
  model: openai.speech('tts-1-hd'),
  voice: 'alloy',
  text: 'Hello, how can I help you today?',
});

// result.audio is an ArrayBuffer containing the audio
const audioBuffer = result.audio;
```

**Supported Providers:**
- OpenAI: tts-1, tts-1-hd, gpt-4o-mini-tts
- ElevenLabs: eleven_multilingual_v2, eleven_turbo_v2
- LMNT, Hume

#### Transcription (Speech-to-Text)

```typescript
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: audioFile, // File, Blob, ArrayBuffer, or URL
});

console.log(result.text); // Transcribed text
console.log(result.segments); // Timestamped segments
```

**Supported Providers:**
- OpenAI: whisper-1
- ElevenLabs, Deepgram, AssemblyAI, Groq, Rev.ai

#### Image Generation

```typescript
import { generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'A futuristic city at sunset',
  size: '1024x1024',
  n: 1,
});

// result.images is an array of generated images
const imageUrl = result.images[0].url;
const imageBase64 = result.images[0].base64;
```

**Supported Providers:**
- OpenAI: dall-e-2, dall-e-3
- Google: imagen-3.0
- Fal AI, Black Forest Labs (Flux), Luma AI, Replicate

#### Embeddings

```typescript
import { embed, embedMany, cosineSimilarity } from 'ai';
import { openai } from '@ai-sdk/openai';

// Single embedding
const result = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'Hello world',
});
console.log(result.embedding); // number[]

// Multiple embeddings (parallel processing)
const results = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: ['Hello', 'World', 'AI'],
  maxParallelCalls: 5, // Parallel processing
});

// Compare similarity
const similarity = cosineSimilarity(
  results.embeddings[0],
  results.embeddings[1]
);
console.log(`Similarity: ${similarity}`); // 0.0 to 1.0
```

**Supported Providers:**
- OpenAI: text-embedding-3-small, text-embedding-3-large
- Google: text-embedding-004
- Cohere, Voyage AI, Mistral, Amazon Bedrock

#### Multi-Modal Prompts (Files, Images, PDFs)

```typescript
import { generateText } from 'ai';
import { google } from '@ai-sdk/google';

const result = await generateText({
  model: google('gemini-2.5-pro'),
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Summarize this document' },
      { type: 'file', data: pdfBuffer, mimeType: 'application/pdf' },
    ],
  }],
});

// Or with images
const result = await generateText({
  model: openai('gpt-5'),
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'What is in this image?' },
      { type: 'image', image: imageBuffer },
    ],
  }],
});
```

See official docs for full API: https://ai-sdk.dev/docs/ai-sdk-core

---

## v5 Stream Response Methods

When returning streaming responses from an API, use the correct method:

| Method | Output Format | Use Case |
|--------|---------------|----------|
| `toTextStreamResponse()` | Plain text chunks | Simple text streaming |
| `toUIMessageStreamResponse()` | SSE with JSON events | **Chat UIs** (text-start, text-delta, text-end, finish) |

**For chat widgets and UIs, always use `toUIMessageStreamResponse()`:**

```typescript
const result = streamText({
  model: workersai('@cf/qwen/qwen3-30b-a3b-fp8'),
  messages,
  system: 'You are helpful.',
});

// ✅ For chat UIs - returns SSE with JSON events
return result.toUIMessageStreamResponse({
  headers: { 'Access-Control-Allow-Origin': '*' },
});

// ❌ For simple text - returns plain text chunks only
return result.toTextStreamResponse();
```

**Note:** `toDataStreamResponse()` does NOT exist in AI SDK v5 (common misconception).

---

## workers-ai-provider Version Compatibility

**IMPORTANT:** `workers-ai-provider@2.x` requires AI SDK v5, NOT v4.

```bash
# ✅ Correct - AI SDK v5 with workers-ai-provider v2
npm install ai@^5.0.0 workers-ai-provider@^2.0.0 zod@^3.25.0

# ❌ Wrong - AI SDK v4 causes error
npm install ai@^4.0.0 workers-ai-provider@^2.0.0
# Error: "AI SDK 4 only supports models that implement specification version v1"
```

**Zod Version:** AI SDK v5 requires `zod@^3.25.0` or later for `zod/v3` and `zod/v4` exports. Older versions (3.22.x) cause build errors: "Could not resolve zod/v4".

---

## Cloudflare Workers Startup Fix

**Problem:** AI SDK v5 + Zod causes >270ms startup time (exceeds Workers 400ms limit).

**Solution:**
```typescript
// ❌ BAD: Top-level imports cause startup overhead
import { createWorkersAI } from 'workers-ai-provider';
const workersai = createWorkersAI({ binding: env.AI });

// ✅ GOOD: Lazy initialization inside handler
app.post('/chat', async (c) => {
  const { createWorkersAI } = await import('workers-ai-provider');
  const workersai = createWorkersAI({ binding: c.env.AI });
  // ...
});
```

**Additional:**
- Minimize top-level Zod schemas
- Move complex schemas into route handlers
- Monitor startup time with Wrangler

---

## v5 Tool Calling Changes

**Breaking Changes:**
- `parameters` → `inputSchema` (Zod schema)
- Tool properties: `args` → `input`, `result` → `output`
- `ToolExecutionError` removed (now `tool-error` content parts)
- `maxSteps` parameter removed → Use `stopWhen(stepCountIs(n))`

**New in v5:**
- Dynamic tools (add tools at runtime based on context)
- Agent class (multi-step execution with tools)

---

## Critical v4→v5 Migration

AI SDK v5 introduced extensive breaking changes. If migrating from v4, follow this guide.

### Breaking Changes Overview

1. **Parameter Renames**
   - `maxTokens` → `maxOutputTokens`
   - `providerMetadata` → `providerOptions`

2. **Tool Definitions**
   - `parameters` → `inputSchema`
   - Tool properties: `args` → `input`, `result` → `output`

3. **Message Types**
   - `CoreMessage` → `ModelMessage`
   - `Message` → `UIMessage`
   - `convertToCoreMessages` → `convertToModelMessages`

4. **Tool Error Handling**
   - `ToolExecutionError` class removed
   - Now `tool-error` content parts
   - Enables automated retry

5. **Multi-Step Execution**
   - `maxSteps` → `stopWhen`
   - Use `stepCountIs()` or `hasToolCall()`

6. **Message Structure**
   - Simple `content` string → `parts` array
   - Parts: text, file, reasoning, tool-call, tool-result

7. **Streaming Architecture**
   - Single chunk → start/delta/end lifecycle
   - Unique IDs for concurrent streams

8. **Tool Streaming**
   - Enabled by default
   - `toolCallStreaming` option removed

9. **Package Reorganization**
   - `ai/rsc` → `@ai-sdk/rsc`
   - `ai/react` → `@ai-sdk/react`
   - `LangChainAdapter` → `@ai-sdk/langchain`

### Migration Examples

**Before (v4):**
```typescript
import { generateText } from 'ai';

const result = await generateText({
  model: openai.chat('gpt-4-turbo'),
  maxTokens: 500,
  providerMetadata: { openai: { user: 'user-123' } },
  tools: {
    weather: {
      description: 'Get weather',
      parameters: z.object({ location: z.string() }),
      execute: async (args) => { /* args.location */ },
    },
  },
  maxSteps: 5,
});
```

**After (v5):**
```typescript
import { generateText, tool, stopWhen, stepCountIs } from 'ai';

const result = await generateText({
  model: openai('gpt-4-turbo'),
  maxOutputTokens: 500,
  providerOptions: { openai: { user: 'user-123' } },
  tools: {
    weather: tool({
      description: 'Get weather',
      inputSchema: z.object({ location: z.string() }),
      execute: async ({ location }) => { /* input.location */ },
    }),
  },
  stopWhen: stepCountIs(5),
});
```

### Migration Checklist

- [ ] Update all `maxTokens` to `maxOutputTokens`
- [ ] Update `providerMetadata` to `providerOptions`
- [ ] Convert tool `parameters` to `inputSchema`
- [ ] Update tool execute functions: `args` → `input`
- [ ] Replace `maxSteps` with `stopWhen(stepCountIs(n))`
- [ ] Update message types: `CoreMessage` → `ModelMessage`
- [ ] Remove `ToolExecutionError` handling
- [ ] Update package imports (`ai/rsc` → `@ai-sdk/rsc`)
- [ ] Test streaming behavior (architecture changed)
- [ ] Update TypeScript types

### Automated Migration

AI SDK provides a migration tool:

```bash
npx ai migrate
```

This will update most breaking changes automatically. Review changes carefully.

**Official Migration Guide:**
https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0

---

## Top 12 Errors & Solutions

### 1. AI_APICallError

**Cause:** API request failed (network, auth, rate limit).

**Solution:**
```typescript
import { AI_APICallError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_APICallError) {
    console.error('API call failed:', error.message);
    console.error('Status code:', error.statusCode);
    console.error('Response:', error.responseBody);

    // Check common causes
    if (error.statusCode === 401) {
      // Invalid API key
    } else if (error.statusCode === 429) {
      // Rate limit - implement backoff
    } else if (error.statusCode >= 500) {
      // Provider issue - retry
    }
  }
}
```

**Prevention:**
- Validate API keys at startup
- Implement retry logic with exponential backoff
- Monitor rate limits
- Handle network errors gracefully

---

### 2. AI_NoObjectGeneratedError

**Cause:** Model didn't generate valid object matching schema.

**Solution:**
```typescript
import { AI_NoObjectGeneratedError } from 'ai';

try {
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: z.object({ /* complex schema */ }),
    prompt: 'Generate data',
  });
} catch (error) {
  if (error instanceof AI_NoObjectGeneratedError) {
    console.error('No valid object generated');

    // Solutions:
    // 1. Simplify schema
    // 2. Add more context to prompt
    // 3. Provide examples in prompt
    // 4. Try different model (gpt-5 or claude-sonnet-4-5 for complex objects)
  }
}
```

**Prevention:**
- Start with simple schemas, add complexity incrementally
- Include examples in prompt: "Generate a person like: { name: 'Alice', age: 30 }"
- Use GPT-4 for complex structured output
- Test schemas with sample data first

---

### 3. Worker Startup Limit (270ms+)

**Cause:** AI SDK v5 + Zod initialization overhead in Cloudflare Workers exceeds startup limits.

**Solution:**
```typescript
// BAD: Top-level imports cause startup overhead
import { createWorkersAI } from 'workers-ai-provider';
import { complexSchema } from './schemas';

const workersai = createWorkersAI({ binding: env.AI });

// GOOD: Lazy initialization inside handler
export default {
  async fetch(request, env) {
    const { createWorkersAI } = await import('workers-ai-provider');
    const workersai = createWorkersAI({ binding: env.AI });

    // Use workersai here
  }
}
```

**Prevention:**
- Move AI SDK imports inside route handlers
- Minimize top-level Zod schemas
- Monitor Worker startup time (must be <400ms)
- Use Wrangler's startup time reporting

**GitHub Issue:** Search for "Workers startup limit" in Vercel AI SDK issues

---

### 4. streamText Fails Silently

**Cause:** Stream errors can be swallowed by `createDataStreamResponse`.

**Status:** ✅ **RESOLVED** - Fixed in ai@4.1.22 (February 2025)

**Solution (Recommended):**
```typescript
// Use the onError callback (added in v4.1.22)
const stream = streamText({
  model: openai('gpt-4-turbo'),
  prompt: 'Hello',
  onError({ error }) {
    console.error('Stream error:', error);
    // Custom error logging and handling
  },
});

// Stream safely
for await (const chunk of stream.textStream) {
  process.stdout.write(chunk);
}
```

**Alternative (Manual try-catch):**
```typescript
// Fallback if not using onError callback
try {
  const stream = streamText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
  });

  for await (const chunk of stream.textStream) {
    process.stdout.write(chunk);
  }
} catch (error) {
  console.error('Stream error:', error);
}
```

**Prevention:**
- **Use `onError` callback** for proper error capture (recommended)
- Implement server-side error monitoring
- Test stream error handling explicitly
- Always log on server side in production

**GitHub Issue:** #4726 (RESOLVED)

---

### 5. AI_LoadAPIKeyError

**Cause:** Missing or invalid API key.

**Solution:**
```typescript
import { AI_LoadAPIKeyError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_LoadAPIKeyError) {
    console.error('API key error:', error.message);

    // Check:
    // 1. .env file exists and loaded
    // 2. Correct env variable name (OPENAI_API_KEY)
    // 3. Key format is valid (starts with sk-)
  }
}
```

**Prevention:**
- Validate API keys at application startup
- Use environment variable validation (e.g., zod)
- Provide clear error messages in development
- Document required environment variables

---

### 6. AI_InvalidArgumentError

**Cause:** Invalid parameters passed to function.

**Solution:**
```typescript
import { AI_InvalidArgumentError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    maxOutputTokens: -1,  // Invalid!
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_InvalidArgumentError) {
    console.error('Invalid argument:', error.message);
    // Check parameter types and values
  }
}
```

**Prevention:**
- Use TypeScript for type checking
- Validate inputs before calling AI SDK functions
- Read function signatures carefully
- Check official docs for parameter constraints

---

### 7. AI_NoContentGeneratedError

**Cause:** Model generated no content (safety filters, etc.).

**Solution:**
```typescript
import { AI_NoContentGeneratedError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Some prompt',
  });
} catch (error) {
  if (error instanceof AI_NoContentGeneratedError) {
    console.error('No content generated');

    // Possible causes:
    // 1. Safety filters blocked output
    // 2. Prompt triggered content policy
    // 3. Model configuration issue

    // Handle gracefully:
    return { text: 'Unable to generate response. Please try different input.' };
  }
}
```

**Prevention:**
- Sanitize user inputs
- Avoid prompts that may trigger safety filters
- Have fallback messaging
- Log occurrences for analysis

---

### 8. AI_TypeValidationError

**Cause:** Zod schema validation failed on generated output.

**Solution:**
```typescript
import { AI_TypeValidationError } from 'ai';

try {
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: z.object({
      age: z.number().min(0).max(120),  // Strict validation
    }),
    prompt: 'Generate person',
  });
} catch (error) {
  if (error instanceof AI_TypeValidationError) {
    console.error('Validation failed:', error.message);

    // Solutions:
    // 1. Relax schema constraints
    // 2. Add more guidance in prompt
    // 3. Use .optional() for unreliable fields
  }
}
```

**Prevention:**
- Start with lenient schemas, tighten gradually
- Use `.optional()` for fields that may not always be present
- Add validation hints in field descriptions
- Test with various prompts

---

### 9. AI_RetryError

**Cause:** All retry attempts failed.

**Solution:**
```typescript
import { AI_RetryError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
    maxRetries: 3,  // Default is 2
  });
} catch (error) {
  if (error instanceof AI_RetryError) {
    console.error('All retries failed');
    console.error('Last error:', error.lastError);

    // Check root cause:
    // - Persistent network issue
    // - Provider outage
    // - Invalid configuration
  }
}
```

**Prevention:**
- Investigate root cause of failures
- Adjust retry configuration if needed
- Implement circuit breaker pattern for provider outages
- Have fallback providers

---

### 10. Rate Limiting Errors

**Cause:** Exceeded provider rate limits (RPM/TPM).

**Solution:**
```typescript
// Implement exponential backoff
async function generateWithBackoff(prompt: string, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await generateText({
        model: openai('gpt-4-turbo'),
        prompt,
      });
    } catch (error) {
      if (error instanceof AI_APICallError && error.statusCode === 429) {
        const delay = Math.pow(2, i) * 1000;  // Exponential backoff
        console.log(`Rate limited, waiting ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Rate limit retries exhausted');
}
```

**Prevention:**
- Monitor rate limit headers
- Queue requests to stay under limits
- Upgrade provider tier if needed
- Implement request throttling

---

### 11. TypeScript Performance with Zod

**Cause:** Complex Zod schemas slow down TypeScript type checking.

**Solution:**
```typescript
// Instead of deeply nested schemas at top level:
// const complexSchema = z.object({ /* 100+ fields */ });

// Define inside functions or use type assertions:
function generateData() {
  const schema = z.object({ /* complex schema */ });
  return generateObject({ model: openai('gpt-4-turbo'), schema, prompt: '...' });
}

// Or use z.lazy() for recursive schemas:
type Category = { name: string; subcategories?: Category[] };
const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(CategorySchema).optional(),
  })
);
```

**Prevention:**
- Avoid top-level complex schemas
- Use `z.lazy()` for recursive types
- Split large schemas into smaller ones
- Use type assertions where appropriate

**Official Docs:**
https://ai-sdk.dev/docs/troubleshooting/common-issues/slow-type-checking

---

### 12. Invalid JSON Response (Provider-Specific)

**Cause:** Some models occasionally return invalid JSON.

**Solution:**
```typescript
// Use built-in retry and mode selection
const result = await generateObject({
  model: openai('gpt-4-turbo'),
  schema: mySchema,
  prompt: 'Generate data',
  mode: 'json',  // Force JSON mode (supported by GPT-4)
  maxRetries: 3,  // Retry on invalid JSON
});

// Or catch and retry manually:
try {
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: mySchema,
    prompt: 'Generate data',
  });
} catch (error) {
  // Retry with different model
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: mySchema,
    prompt: 'Generate data',
  });
}
```

**Prevention:**
- Use `mode: 'json'` when available
- Prefer GPT-4 for structured output
- Implement retry logic
- Validate responses

**GitHub Issue:** #4302 (Imagen 3.0 Invalid JSON)

---

**More Errors:** https://ai-sdk.dev/docs/reference/ai-sdk-errors (28 total)

---

## When to Use This Skill

### Use ai-sdk-core when:

- Building backend AI features (server-side text generation)
- Implementing server-side text generation (Node.js, Workers, Next.js)
- Creating structured AI outputs (JSON, forms, data extraction)
- Building AI agents with tools (multi-step workflows)
- Integrating multiple AI providers (OpenAI, Anthropic, Google, Cloudflare)
- Migrating from AI SDK v4 to v5
- Encountering AI SDK errors (AI_APICallError, AI_NoObjectGeneratedError, etc.)
- Using AI in Cloudflare Workers (with workers-ai-provider)
- Using AI in Next.js Server Components/Actions
- Need consistent API across different LLM providers

### Don't use this skill when:

- Building React chat UIs (use **ai-sdk-ui** skill instead)
- Need frontend hooks like useChat (use **ai-sdk-ui** skill instead)
- Need advanced topics like embeddings or image generation (check official docs)
- Building native Cloudflare Workers AI apps without multi-provider (use **cloudflare-workers-ai** skill instead)
- Need Generative UI / RSC (see https://ai-sdk.dev/docs/ai-sdk-rsc)

---

## Versions

**AI SDK:**
- Stable: ai@6.1.0 (Jan 2026)
- Legacy v5: ai@5.0.98 (Nov 2025)
- Zod 3.x/4.x both supported

**Latest Models (2026):**
- OpenAI: GPT-5.2, GPT-5.1, GPT-5, o3, o3-mini, o4-mini
- Anthropic: Claude Sonnet 4.5, Opus 4.1, Haiku 4.5
- Google: Gemini 2.5 Pro/Flash/Lite

**Check Latest:**
```bash
npm view ai version
npm view ai dist-tags
```

---

## Official Docs

**Core:**
- AI SDK v6: https://ai-sdk.dev/docs
- AI SDK Core: https://ai-sdk.dev/docs/ai-sdk-core/overview
- Output API: https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data
- v4→v5 Migration: https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0
- All Errors (31): https://ai-sdk.dev/docs/reference/ai-sdk-errors
- Providers (69+): https://ai-sdk.dev/providers/overview

**Multi-Modal:**
- Speech: https://ai-sdk.dev/docs/ai-sdk-core/speech
- Transcription: https://ai-sdk.dev/docs/ai-sdk-core/transcription
- Image Generation: https://ai-sdk.dev/docs/ai-sdk-core/image-generation
- Embeddings: https://ai-sdk.dev/docs/ai-sdk-core/embeddings

**GitHub:**
- Repository: https://github.com/vercel/ai
- Issues: https://github.com/vercel/ai/issues

---

**Last Updated:** 2026-01-03
**Skill Version:** 2.0.0
**AI SDK:** 6.1.0 stable
