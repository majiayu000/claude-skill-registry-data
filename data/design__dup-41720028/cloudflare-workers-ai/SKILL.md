---
name: cloudflare-workers-ai
description: |
  Run LLMs and AI models on Cloudflare's global GPU network with Workers AI. Includes Llama 4, Gemma 3, Mistral 3.1,
  Flux image generation, BGE embeddings (2x faster, 2025), streaming support, and AI Gateway for cost tracking.

  Use when: implementing LLM inference, generating images, building RAG with embeddings, streaming AI responses,
  using AI Gateway, troubleshooting max_tokens defaults (breaking change 2025), BGE pooling parameter (not backwards
  compatible), or handling AI_ERROR, rate limits, model deprecations, token limits.

  Keywords: workers ai, cloudflare ai, ai bindings, llm workers, @cf/meta/llama-4-scout, @cf/google/gemma-3-12b-it,
  @cf/mistralai/mistral-small-3.1-24b-instruct, @cf/openai/gpt-oss-120b, workers ai models, ai inference,
  cloudflare llm, ai streaming, text generation ai, ai embeddings, bge pooling cls mean, image generation ai,
  workers ai rag, ai gateway, llama workers, flux image generation, deepgram aura, leonardo image generation,
  vision models ai, ai chat completion, AI_ERROR, rate limit ai, model not found, max_tokens breaking change,
  bge pooling backwards compatibility, model deprecations october 2025, token limit exceeded, neurons exceeded,
  workers ai hono, ai gateway workers, vercel ai sdk workers, openai compatible workers, workers ai vectorize,
  workers-ai-provider v2, ai sdk v5, lora adapters rank 32
---

# Cloudflare Workers AI

**Status**: Production Ready ✅
**Last Updated**: 2025-11-25
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.50.0, @cloudflare/workers-types@4.20251125.0

**Recent Updates (2025)**:
- **April 2025 - Performance**: Llama 3.3 70B 2-4x faster (speculative decoding, prefix caching), BGE embeddings 2x faster
- **April 2025 - Breaking Changes**: max_tokens now correctly defaults to 256 (was not respected), BGE pooling parameter (cls NOT backwards compatible with mean)
- **2025 - New Models (14)**: Mistral 3.1 24B (vision+tools), Gemma 3 12B (128K context), EmbeddingGemma 300M, Llama 4 Scout, GPT-OSS 120B/20B, Qwen models (QwQ 32B, Coder 32B), Leonardo image gen, Deepgram Aura 2, Whisper v3 Turbo, IBM Granite, Nova 3
- **2025 - Platform**: Context windows API change (tokens not chars), unit-based pricing with per-model granularity, workers-ai-provider v2.0.0 (AI SDK v5), LoRA rank up to 32 (was 8), 100 adapters per account
- **October 2025**: Model deprecations (use Llama 4, GPT-OSS instead)

---

## Quick Start (5 Minutes)

```typescript
// 1. Add AI binding to wrangler.jsonc
{ "ai": { "binding": "AI" } }

// 2. Run model with streaming (recommended)
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const stream = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
      messages: [{ role: 'user', content: 'Tell me a story' }],
      stream: true, // Always stream for text generation!
    });

    return new Response(stream, {
      headers: { 'content-type': 'text/event-stream' },
    });
  },
};
```

**Why streaming?** Prevents buffering in memory, faster time-to-first-token, avoids Worker timeout issues.

---

## API Reference

```typescript
env.AI.run(
  model: string,
  inputs: ModelInputs,
  options?: { gateway?: { id: string; skipCache?: boolean } }
): Promise<ModelOutput | ReadableStream>
```

---

## Model Selection Guide (Updated 2025)

### Text Generation (LLMs)

| Model | Best For | Rate Limit | Size | Notes |
|-------|----------|------------|------|-------|
| **2025 Models** |
| `@cf/meta/llama-4-scout-17b-16e-instruct` | Latest Llama, general purpose | 300/min | 17B | NEW 2025 |
| `@cf/openai/gpt-oss-120b` | Largest open-source GPT | 300/min | 120B | NEW 2025 |
| `@cf/openai/gpt-oss-20b` | Smaller open-source GPT | 300/min | 20B | NEW 2025 |
| `@cf/google/gemma-3-12b-it` | 128K context, 140+ languages | 300/min | 12B | NEW 2025, vision |
| `@cf/mistralai/mistral-small-3.1-24b-instruct` | Vision + tool calling | 300/min | 24B | NEW 2025 |
| `@cf/qwen/qwq-32b` | Reasoning, complex tasks | 300/min | 32B | NEW 2025 |
| `@cf/qwen/qwen2.5-coder-32b-instruct` | Coding specialist | 300/min | 32B | NEW 2025 |
| `@cf/qwen/qwen3-30b-a3b-fp8` | Fast quantized | 300/min | 30B | NEW 2025 |
| `@cf/ibm-granite/granite-4.0-h-micro` | Small, efficient | 300/min | Micro | NEW 2025 |
| **Performance (2025)** |
| `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | 2-4x faster (2025 update) | 300/min | 70B | Speculative decoding |
| `@cf/meta/llama-3.1-8b-instruct-fp8-fast` | Fast 8B variant | 300/min | 8B | - |
| **Standard Models** |
| `@cf/meta/llama-3.1-8b-instruct` | General purpose | 300/min | 8B | - |
| `@cf/meta/llama-3.2-1b-instruct` | Ultra-fast, simple tasks | 300/min | 1B | - |
| `@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` | Coding, technical | 300/min | 32B | - |

### Text Embeddings (2x Faster - 2025)

| Model | Dimensions | Best For | Rate Limit | Notes |
|-------|-----------|----------|------------|-------|
| `@cf/google/embeddinggemma-300m` | 768 | Best-in-class RAG | 3000/min | **NEW 2025** |
| `@cf/baai/bge-base-en-v1.5` | 768 | General RAG (2x faster) | 3000/min | **pooling: "cls"** recommended |
| `@cf/baai/bge-large-en-v1.5` | 1024 | High accuracy (2x faster) | 1500/min | **pooling: "cls"** recommended |
| `@cf/baai/bge-small-en-v1.5` | 384 | Fast, low storage (2x faster) | 3000/min | **pooling: "cls"** recommended |
| `@cf/qwen/qwen3-embedding-0.6b` | 768 | Qwen embeddings | 3000/min | NEW 2025 |

**CRITICAL (2025)**: BGE models now support `pooling: "cls"` parameter (recommended) but NOT backwards compatible with `pooling: "mean"` (default).

### Image Generation

| Model | Best For | Rate Limit | Notes |
|-------|----------|------------|-------|
| `@cf/black-forest-labs/flux-1-schnell` | High quality, photorealistic | 720/min | - |
| `@cf/leonardo/lucid-origin` | Leonardo AI style | 720/min | NEW 2025 |
| `@cf/leonardo/phoenix-1.0` | Leonardo AI variant | 720/min | NEW 2025 |
| `@cf/stabilityai/stable-diffusion-xl-base-1.0` | General purpose | 720/min | - |

### Vision Models

| Model | Best For | Rate Limit | Notes |
|-------|----------|------------|-------|
| `@cf/meta/llama-3.2-11b-vision-instruct` | Image understanding | 720/min | - |
| `@cf/google/gemma-3-12b-it` | Vision + text (128K context) | 300/min | NEW 2025 |

### Audio Models (2025)

| Model | Type | Rate Limit | Notes |
|-------|------|------------|-------|
| `@cf/deepgram/aura-2-en` | Text-to-speech (English) | 720/min | NEW 2025 |
| `@cf/deepgram/aura-2-es` | Text-to-speech (Spanish) | 720/min | NEW 2025 |
| `@cf/deepgram/nova-3` | Speech-to-text (+ WebSocket) | 720/min | NEW 2025 |
| `@cf/openai/whisper-large-v3-turbo` | Speech-to-text (faster) | 720/min | NEW 2025 |

---

## Common Patterns

### RAG (Retrieval Augmented Generation)

```typescript
// 1. Generate embeddings
const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: [userQuery] });

// 2. Search Vectorize
const matches = await env.VECTORIZE.query(embeddings.data[0], { topK: 3 });
const context = matches.matches.map((m) => m.metadata.text).join('\n\n');

// 3. Generate with context
const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [
    { role: 'system', content: `Answer using this context:\n${context}` },
    { role: 'user', content: userQuery },
  ],
  stream: true,
});
```

---

### Structured Output with Zod

```typescript
import { z } from 'zod';

const Schema = z.object({ name: z.string(), items: z.array(z.string()) });

const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{
    role: 'user',
    content: `Generate JSON matching: ${JSON.stringify(Schema.shape)}`
  }],
});

const validated = Schema.parse(JSON.parse(response.response));
```

---

## AI Gateway Integration

Provides caching, logging, cost tracking, and analytics for AI requests.

```typescript
const response = await env.AI.run(
  '@cf/meta/llama-3.1-8b-instruct',
  { prompt: 'Hello' },
  { gateway: { id: 'my-gateway', skipCache: false } }
);

// Access logs and send feedback
const gateway = env.AI.gateway('my-gateway');
await gateway.patchLog(env.AI.aiGatewayLogId, {
  feedback: { rating: 1, comment: 'Great response' },
});
```

**Benefits:** Cost tracking, caching (reduces duplicate inference), logging, rate limiting, analytics.

---

## Rate Limits & Pricing (Updated 2025)

### Rate Limits (per minute)

| Task Type | Default Limit | Notes |
|-----------|---------------|-------|
| **Text Generation** | 300/min | Some fast models: 400-1500/min |
| **Text Embeddings** | 3000/min | BGE-large: 1500/min |
| **Image Generation** | 720/min | All image models |
| **Vision Models** | 720/min | Image understanding |
| **Audio (TTS/STT)** | 720/min | Deepgram, Whisper |
| **Translation** | 720/min | M2M100, Opus MT |
| **Classification** | 2000/min | Text classification |

### Pricing (Unit-Based, Billed in Neurons - 2025)

**Free Tier:**
- 10,000 neurons per day
- Resets daily at 00:00 UTC

**Paid Tier ($0.011 per 1,000 neurons):**
- 10,000 neurons/day included
- Unlimited usage above free allocation

**2025 Model Costs (per 1M tokens):**

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| **2025 Models** |
| Llama 4 Scout 17B | $0.270 | $0.850 | NEW 2025 |
| GPT-OSS 120B | $0.350 | $0.750 | NEW 2025 |
| GPT-OSS 20B | $0.200 | $0.300 | NEW 2025 |
| Gemma 3 12B | $0.345 | $0.556 | NEW 2025 |
| Mistral 3.1 24B | $0.351 | $0.555 | NEW 2025 |
| Qwen QwQ 32B | $0.660 | $1.000 | NEW 2025 |
| Qwen Coder 32B | $0.660 | $1.000 | NEW 2025 |
| IBM Granite Micro | $0.017 | $0.112 | NEW 2025 |
| EmbeddingGemma 300M | $0.012 | N/A | NEW 2025 |
| Qwen3 Embedding 0.6B | $0.012 | N/A | NEW 2025 |
| **Performance (2025)** |
| Llama 3.3 70B Fast | $0.293 | $2.253 | 2-4x faster |
| Llama 3.1 8B FP8 Fast | $0.045 | $0.384 | Fast variant |
| **Standard Models** |
| Llama 3.2 1B | $0.027 | $0.201 | - |
| Llama 3.1 8B | $0.282 | $0.827 | - |
| Deepseek R1 32B | $0.497 | $4.881 | - |
| BGE-base (2x faster) | $0.067 | N/A | 2025 speedup |
| BGE-large (2x faster) | $0.204 | N/A | 2025 speedup |
| **Image Models (2025)** |
| Flux 1 Schnell | $0.0000528 per 512x512 tile | - |
| Leonardo Lucid | $0.006996 per 512x512 tile | NEW 2025 |
| Leonardo Phoenix | $0.005830 per 512x512 tile | NEW 2025 |
| **Audio Models (2025)** |
| Deepgram Aura 2 | $0.030 per 1k chars | NEW 2025 |
| Deepgram Nova 3 | $0.0052 per audio min | NEW 2025 |
| Whisper v3 Turbo | $0.0005 per audio min | NEW 2025 |

---

## Error Handling with Retry

```typescript
async function runAIWithRetry(
  env: Env,
  model: string,
  inputs: any,
  maxRetries = 3
): Promise<any> {
  let lastError: Error;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await env.AI.run(model, inputs);
    } catch (error) {
      lastError = error as Error;

      // Rate limit - retry with exponential backoff
      if (lastError.message.toLowerCase().includes('rate limit')) {
        await new Promise((resolve) => setTimeout(resolve, Math.pow(2, i) * 1000));
        continue;
      }

      throw error; // Other errors - fail immediately
    }
  }

  throw lastError!;
}
```

---

## OpenAI Compatibility

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: env.CLOUDFLARE_API_KEY,
  baseURL: `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/ai/v1`,
});

// Chat completions
await openai.chat.completions.create({
  model: '@cf/meta/llama-3.1-8b-instruct',
  messages: [{ role: 'user', content: 'Hello!' }],
});
```

**Endpoints:** `/v1/chat/completions`, `/v1/embeddings`

---

## Vercel AI SDK Integration (workers-ai-provider v2.0.0)

```typescript
import { createWorkersAI } from 'workers-ai-provider'; // v2.0.0 with AI SDK v5
import { generateText, streamText } from 'ai';

const workersai = createWorkersAI({ binding: env.AI });

// Generate or stream
await generateText({
  model: workersai('@cf/meta/llama-3.1-8b-instruct'),
  prompt: 'Write a poem',
});
```

---

## References

- [Workers AI Docs](https://developers.cloudflare.com/workers-ai/)
- [Models Catalog](https://developers.cloudflare.com/workers-ai/models/)
- [AI Gateway](https://developers.cloudflare.com/ai-gateway/)
- [Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [Changelog](https://developers.cloudflare.com/workers-ai/changelog/)
- [LoRA Adapters](https://developers.cloudflare.com/workers-ai/features/fine-tunes/loras/)
- **MCP Tool**: Use `mcp__cloudflare-docs__search_cloudflare_documentation` for latest docs
