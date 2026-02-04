---
name: cloudflare-workers-ai
description: >
  Cloudflare Workers AI essentials - text generation, embeddings, image generation, streaming.
  Trigger: When working with Workers AI, LLMs, text generation, embeddings, image generation.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Critical Patterns

### Setup Binding

```toml
# wrangler.toml
[ai]
binding = "AI"
```

```typescript
export interface Env {
  AI: Ai
}
```

### Text Generation

```typescript
import { createWorkersAI } from "workers-ai-provider"
import { generateText } from "ai"

type Env = { AI: Ai }

export default {
  async fetch(req: Request, env: Env) {
    const workersai = createWorkersAI({ binding: env.AI })
    
    const { text } = await generateText({
      model: workersai("@cf/meta/llama-3.3-70b-instruct-fp8-fast"),
      prompt: "Write a short poem about clouds"
    })
    
    return Response.json({ generatedText: text })
  }
}
```

**Popular models:**
- `@cf/meta/llama-3.3-70b-instruct-fp8-fast` - Llama 3.3 (large, fast)
- `@cf/meta/llama-2-7b-chat-int8` - Llama 2 (smaller)
- `@cf/mistral/mistral-7b-instruct-v0.1` - Mistral 7B

### Streaming Text

```typescript
import { streamText } from "ai"
import { Hono } from "hono"

const app = new Hono<{ Bindings: Env }>()

app.post("/chat", async (c) => {
  const { messages } = await c.req.json()
  const workersai = createWorkersAI({ binding: c.env.AI })
  
  const result = await streamText({
    model: workersai("@cf/meta/llama-3.3-70b-instruct-fp8-fast"),
    messages
  })
  
  return result.toTextStreamResponse({
    headers: {
      "Content-Type": "text/x-unknown",
      "content-encoding": "identity",
      "transfer-encoding": "chunked"
    }
  })
})

export default { fetch: app.fetch }
```

### Chat with System Prompt

```typescript
const systemPrompt = `You are a helpful financial advisor.
Provide accurate, concise advice about personal finance.`

const result = await streamText({
  model: workersai("@cf/meta/llama-3.3-70b-instruct-fp8-fast"),
  messages: [
    { role: "system", content: systemPrompt },
    { role: "user", content: userMessage }
  ],
  maxTokens: 1000,
  temperature: 0.7
})
```

### Text Embeddings

```typescript
import { embed } from "ai"

const workersai = createWorkersAI({ binding: env.AI })

const { embedding } = await embed({
  model: workersai.textEmbedding("@cf/baai/bge-base-en-v1.5"),
  value: "Search engines use embeddings for semantic understanding"
})

// embedding is array of numbers [0.123, -0.456, ...]
console.log(embedding.length) // 768 dimensions
```

**Popular embedding models:**
- `@cf/baai/bge-base-en-v1.5` - 768 dimensions (recommended)
- `@cf/baai/bge-small-en-v1.5` - 384 dimensions (faster)
- `@cf/baai/bge-large-en-v1.5` - 1024 dimensions (more accurate)

### Batch Embeddings

```typescript
import { embedMany } from "ai"

const { embeddings } = await embedMany({
  model: workersai.textEmbedding("@cf/baai/bge-base-en-v1.5"),
  values: [
    "First document",
    "Second document",
    "Third document"
  ]
})

// embeddings is array of arrays
console.log(embeddings.length) // 3
console.log(embeddings[0].length) // 768
```

### Image Generation

```typescript
import { generateImage } from "ai"

const workersai = createWorkersAI({ binding: env.AI })

const { image } = await generateImage({
  model: workersai.image("@cf/black-forest-labs/flux-1-schnell"),
  prompt: "A serene mountain landscape at sunset",
  size: "1024x1024"
})

return new Response(image, {
  headers: { "Content-Type": "image/png" }
})
```

**Popular image models:**
- `@cf/black-forest-labs/flux-1-schnell` - FLUX.1 (fast, recommended)
- `@cf/stabilityai/stable-diffusion-xl-base-1.0` - SDXL
- `@cf/bytedance/stable-diffusion-xl-lightning` - SDXL Lightning

**Sizes:** `"1024x1024"`, `"1024x768"`, `"768x1024"`

## Common Patterns

### Complete Chat API

```typescript
import { Hono } from "hono"
import { createWorkersAI } from "workers-ai-provider"
import { streamText } from "ai"

const app = new Hono<{ Bindings: Env }>()

app.post("/api/chat", async (c) => {
  const { messages } = await c.req.json()
  
  if (!messages || !Array.isArray(messages)) {
    return c.json({ error: "Invalid messages" }, 400)
  }
  
  const workersai = createWorkersAI({ binding: c.env.AI })
  
  try {
    const result = await streamText({
      model: workersai("@cf/meta/llama-3.3-70b-instruct-fp8-fast"),
      messages,
      maxTokens: 1000,
      temperature: 0.7
    })
    
    return result.toTextStreamResponse({
      headers: {
        "Content-Type": "text/x-unknown",
        "content-encoding": "identity",
        "transfer-encoding": "chunked"
      }
    })
  } catch (error) {
    console.error("AI error:", error)
    return c.json({ error: "Failed" }, 500)
  }
})

export default { fetch: app.fetch }
```

### Semantic Search

```typescript
app.post("/search", async (c) => {
  const { query } = await c.req.json()
  const workersai = createWorkersAI({ binding: c.env.AI })
  
  // 1. Generate embedding for query
  const { embedding: queryEmbedding } = await embed({
    model: workersai.textEmbedding("@cf/baai/bge-base-en-v1.5"),
    value: query
  })
  
  // 2. Search in vector database (e.g., Vectorize)
  const results = await c.env.VECTORIZE.query(queryEmbedding, {
    topK: 10
  })
  
  return c.json({ results })
})
```

### Image Generation with Upload to R2

```typescript
app.post("/generate-image", async (c) => {
  const { prompt } = await c.req.json()
  
  if (!prompt || prompt.length < 3 || prompt.length > 1000) {
    return c.json({ error: "Invalid prompt" }, 400)
  }
  
  const workersai = createWorkersAI({ binding: c.env.AI })
  
  try {
    const { image } = await generateImage({
      model: workersai.image("@cf/black-forest-labs/flux-1-schnell"),
      prompt,
      size: "1024x1024"
    })
    
    // Upload to R2
    const key = `images/${crypto.randomUUID()}.png`
    await c.env.BUCKET.put(key, image, {
      httpMetadata: { contentType: "image/png" }
    })
    
    return c.json({ success: true, key })
  } catch (error) {
    return c.json({ error: "Generation failed" }, 500)
  }
})
```

## Performance Tips

```typescript
// ✅ Stream for long responses
const result = await streamText({...})
return result.toTextStreamResponse()

// ❌ Wait for entire response (slow)
const { text } = await generateText({...})
return Response.json({ text })

// ✅ Choose right model size
// Small tasks -> smaller models
workersai("@cf/meta/llama-2-7b-chat-int8")

// Complex reasoning -> larger models
workersai("@cf/meta/llama-3.3-70b-instruct-fp8-fast")

// ✅ Cache embeddings
const cached = await cache.get(text)
if (cached) return JSON.parse(cached)

const { embedding } = await embed({...})
await cache.put(text, JSON.stringify(embedding))

// ✅ Batch embeddings
const { embeddings } = await embedMany({
  model: workersai.textEmbedding("@cf/baai/bge-base-en-v1.5"),
  values: documents
})

// ❌ One at a time (slow)
for (const doc of documents) {
  await embed({ value: doc })
}
```

## Model Configuration

```typescript
const result = await generateText({
  model: workersai("@cf/meta/llama-3.3-70b-instruct-fp8-fast"),
  prompt: "Your prompt",
  
  maxTokens: 500,          // Max tokens to generate
  temperature: 0.7,        // Randomness (0-1)
  topP: 0.9,              // Nucleus sampling
  frequencyPenalty: 0.5,  // Reduce repetition
  presencePenalty: 0.5,   // Encourage diversity
  
  stopSequences: ["\n\n", "END"]
})
```

## Common Mistakes

❌ **Not handling errors**
```typescript
const { text } = await generateText({...}) // May throw!
```

✅ **Always use try-catch**
```typescript
try {
  const { text } = await generateText({...})
} catch (error) {
  return c.json({ error: "Failed" }, 500)
}
```

❌ **Missing streaming headers**
```typescript
return result.toTextStreamResponse()
```

✅ **Include required headers**
```typescript
return result.toTextStreamResponse({
  headers: {
    "Content-Type": "text/x-unknown",
    "content-encoding": "identity",
    "transfer-encoding": "chunked"
  }
})
```

## Commands

```bash
# List models
wrangler ai models list

# Test model
wrangler ai run @cf/meta/llama-3.3-70b-instruct-fp8-fast --prompt "Hello"

# Deploy
wrangler deploy
```

## Resources

- **Docs**: [developers.cloudflare.com/workers-ai](https://developers.cloudflare.com/workers-ai)
- **Models**: [developers.cloudflare.com/workers-ai/models](https://developers.cloudflare.com/workers-ai/models)
