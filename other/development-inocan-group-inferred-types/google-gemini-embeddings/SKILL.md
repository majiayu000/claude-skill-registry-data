---
name: google-gemini-embeddings
description: |
  Build RAG systems, semantic search, and document clustering with Gemini embeddings API (gemini-embedding-001). Generate 768-3072 dimension embeddings for vector search, integrate with Cloudflare Vectorize, and use 8 task types (RETRIEVAL_QUERY, RETRIEVAL_DOCUMENT, SEMANTIC_SIMILARITY) for optimized retrieval.

  Use when: implementing vector search with Google embeddings, building retrieval-augmented generation systems, creating semantic search features, clustering documents by meaning, integrating embeddings with Cloudflare Vectorize, optimizing dimension sizes (128-3072), or troubleshooting dimension mismatch errors, incorrect task type selections, rate limit issues (100 RPM free tier), vector normalization mistakes, or text truncation errors (2,048 token limit).
---

# Google Gemini Embeddings

**Complete production-ready guide for Google Gemini embeddings API**

This skill provides comprehensive coverage of the `gemini-embedding-001` model for generating text embeddings, including SDK usage, REST API patterns, batch processing, RAG integration with Cloudflare Vectorize, and advanced use cases like semantic search and document clustering.

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [gemini-embedding-001 Model](#2-gemini-embedding-001-model)
3. [Basic Embeddings](#3-basic-embeddings)
4. [Batch Embeddings](#4-batch-embeddings)
5. [Task Types](#5-task-types)
6. [RAG Patterns](#6-rag-patterns)
7. [Error Handling](#7-error-handling)
8. [Best Practices](#8-best-practices)

---

## 1. Quick Start

### Installation

Install the Google Generative AI SDK:

```bash
npm install @google/genai@^1.30.0
```

For TypeScript projects:

```bash
npm install -D typescript@^5.0.0
```

### Environment Setup

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key from: https://aistudio.google.com/apikey

### First Embedding Example

```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: 'What is the meaning of life?',
  config: {
    taskType: 'RETRIEVAL_QUERY',
    outputDimensionality: 768
  }
});

console.log(response.embedding.values); // [0.012, -0.034, ...]
console.log(response.embedding.values.length); // 768
```

**Result**: A 768-dimension embedding vector representing the semantic meaning of the text.

---

## 2. gemini-embedding-001 Model

### Model Specifications

**Current Model**: `gemini-embedding-001` (stable, production-ready)
- **Status**: Stable
- **Experimental**: `gemini-embedding-exp-03-07` (deprecated October 2025, do not use)

### Dimensions

The model supports flexible output dimensionality using **Matryoshka Representation Learning**:

| Dimension | Use Case | Storage | Performance |
|-----------|----------|---------|-------------|
| **768** | Recommended for most use cases | Low | Fast |
| **1536** | Balance between accuracy and efficiency | Medium | Medium |
| **3072** | Maximum accuracy (default) | High | Slower |
| 128-3071 | Custom (any value in range) | Variable | Variable |

**Default**: 3072 dimensions
**Recommended**: 768, 1536, or 3072 for optimal performance

### Context Window

- **Input Limit**: 2,048 tokens per text
- **Input Type**: Text only (no images, audio, or video)

### Rate Limits

| Tier | RPM | TPM | RPD | Requirements |
|------|-----|-----|-----|--------------|
| **Free** | 100 | 30,000 | 1,000 | No billing account |
| **Tier 1** | 3,000 | 1,000,000 | - | Billing account linked |
| **Tier 2** | 5,000 | 5,000,000 | - | $250+ spending, 30-day wait |
| **Tier 3** | 10,000 | 10,000,000 | - | $1,000+ spending, 30-day wait |

**RPM** = Requests Per Minute
**TPM** = Tokens Per Minute
**RPD** = Requests Per Day

### Output Format

```typescript
{
  embedding: {
    values: number[] // Array of floating-point numbers
  }
}
```

---

## 3. Basic Embeddings

### SDK Approach (Node.js)

**Single text embedding**:

```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: 'The quick brown fox jumps over the lazy dog',
  config: {
    taskType: 'SEMANTIC_SIMILARITY',
    outputDimensionality: 768
  }
});

console.log(response.embedding.values);
// [0.00388, -0.00762, 0.01543, ...]
```

### Fetch Approach (Cloudflare Workers)

**For Workers/edge environments without SDK support**:

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const apiKey = env.GEMINI_API_KEY;
    const text = "What is the meaning of life?";

    const response = await fetch(
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent',
      {
        method: 'POST',
        headers: {
          'x-goog-api-key': apiKey,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          content: {
            parts: [{ text }]
          },
          taskType: 'RETRIEVAL_QUERY',
          outputDimensionality: 768
        })
      }
    );

    const data = await response.json();

    // Response format:
    // {
    //   embedding: {
    //     values: [0.012, -0.034, ...]
    //   }
    // }

    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
```

### Response Parsing

```typescript
interface EmbeddingResponse {
  embedding: {
    values: number[];
  };
}

const response: EmbeddingResponse = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: 'Sample text',
  config: { taskType: 'SEMANTIC_SIMILARITY' }
});

const embedding: number[] = response.embedding.values;
const dimensions: number = embedding.length; // 3072 by default
```

---

## 4. Batch Embeddings

### Multiple Texts in One Request (SDK)

Generate embeddings for multiple texts simultaneously:

```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const texts = [
  "What is the meaning of life?",
  "How does photosynthesis work?",
  "Tell me about the history of the internet."
];

const response = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  contents: texts, // Array of strings
  config: {
    taskType: 'RETRIEVAL_DOCUMENT',
    outputDimensionality: 768
  }
});

// Process each embedding
response.embeddings.forEach((embedding, index) => {
  console.log(`Text ${index}: ${texts[index]}`);
  console.log(`Embedding: ${embedding.values.slice(0, 5)}...`);
  console.log(`Dimensions: ${embedding.values.length}`);
});
```

### Batch REST API (fetch)

Use the `batchEmbedContents` endpoint:

```typescript
const response = await fetch(
  'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:batchEmbedContents',
  {
    method: 'POST',
    headers: {
      'x-goog-api-key': apiKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      requests: texts.map(text => ({
        model: 'models/gemini-embedding-001',
        content: {
          parts: [{ text }]
        },
        taskType: 'RETRIEVAL_DOCUMENT'
      }))
    })
  }
);

const data = await response.json();
// data.embeddings: Array of {values: number[]}
```

### Chunking for Rate Limits

When processing large datasets, chunk requests to stay within rate limits:

```typescript
async function batchEmbedWithRateLimit(
  texts: string[],
  batchSize: number = 100, // Free tier: 100 RPM
  delayMs: number = 60000 // 1 minute delay between batches
): Promise<number[][]> {
  const allEmbeddings: number[][] = [];

  for (let i = 0; i < texts.length; i += batchSize) {
    const batch = texts.slice(i, i + batchSize);

    console.log(`Processing batch ${i / batchSize + 1} (${batch.length} texts)`);

    const response = await ai.models.embedContent({
      model: 'gemini-embedding-001',
      contents: batch,
      config: {
        taskType: 'RETRIEVAL_DOCUMENT',
        outputDimensionality: 768
      }
    });

    allEmbeddings.push(...response.embeddings.map(e => e.values));

    // Wait before next batch (except last batch)
    if (i + batchSize < texts.length) {
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }

  return allEmbeddings;
}

// Usage
const embeddings = await batchEmbedWithRateLimit(documents, 100);
```

### Performance Optimization

**Tips**:
1. Use batch API when embedding multiple texts (single request vs multiple requests)
2. Choose lower dimensions (768) for faster processing and less storage
3. Implement exponential backoff for rate limit errors
4. Cache embeddings to avoid redundant API calls

---

## 5. Task Types

The `taskType` parameter optimizes embeddings for specific use cases. **Always specify a task type for best results.**

### Available Task Types (8 total)

| Task Type | Use Case | Example |
|-----------|----------|---------|
| **RETRIEVAL_QUERY** | User search queries | "How do I fix a flat tire?" |
| **RETRIEVAL_DOCUMENT** | Documents to be indexed/searched | Product descriptions, articles |
| **SEMANTIC_SIMILARITY** | Comparing text similarity | Duplicate detection, clustering |
| **CLASSIFICATION** | Categorizing texts | Spam detection, sentiment analysis |
| **CLUSTERING** | Grouping similar texts | Topic modeling, content organization |
| **CODE_RETRIEVAL_QUERY** | Code search queries | "function to sort array" |
| **QUESTION_ANSWERING** | Questions seeking answers | FAQ matching |
| **FACT_VERIFICATION** | Verifying claims with evidence | Fact-checking systems |

### When to Use Which

**RAG Systems** (Retrieval Augmented Generation):
```typescript
// When embedding user queries
const queryEmbedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: userQuery,
  config: { taskType: 'RETRIEVAL_QUERY' } // ← Use RETRIEVAL_QUERY
});

// When embedding documents for indexing
const docEmbedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: documentText,
  config: { taskType: 'RETRIEVAL_DOCUMENT' } // ← Use RETRIEVAL_DOCUMENT
});
```

**Semantic Search**:
```typescript
const embedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text,
  config: { taskType: 'SEMANTIC_SIMILARITY' }
});
```

**Document Clustering**:
```typescript
const embedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text,
  config: { taskType: 'CLUSTERING' }
});
```

### Impact on Quality

Using the correct task type **significantly improves** retrieval quality:

```typescript
// ❌ BAD: No task type specified
const embedding1 = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: userQuery
});

// ✅ GOOD: Task type specified
const embedding2 = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: userQuery,
  config: { taskType: 'RETRIEVAL_QUERY' }
});
```

**Result**: Using the right task type can improve search relevance by 10-30%.

---

## 6. RAG Patterns

**RAG** (Retrieval Augmented Generation) combines vector search with LLM generation to create AI systems that answer questions using custom knowledge bases.

### Document Ingestion Pipeline

```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

// Generate embeddings for chunks
async function embedChunks(chunks: string[]): Promise<number[][]> {
  const response = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    contents: chunks,
    config: {
      taskType: 'RETRIEVAL_DOCUMENT', // ← Documents for indexing
      outputDimensionality: 768 // ← Match Vectorize index dimensions
    }
  });

  return response.embeddings.map(e => e.values);
}

// Store in Cloudflare Vectorize
async function storeInVectorize(
  env: Env,
  chunks: string[],
  embeddings: number[][]
) {
  const vectors = chunks.map((chunk, i) => ({
    id: `doc-${Date.now()}-${i}`,
    values: embeddings[i],
    metadata: { text: chunk }
  }));

  await env.VECTORIZE.insert(vectors);
}
```

### Query Flow (Retrieve + Generate)

```typescript
async function ragQuery(env: Env, userQuery: string): Promise<string> {
  // 1. Embed user query
  const queryResponse = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    content: userQuery,
    config: {
      taskType: 'RETRIEVAL_QUERY', // ← Query, not document
      outputDimensionality: 768
    }
  });

  const queryEmbedding = queryResponse.embedding.values;

  // 2. Search Vectorize for similar documents
  const results = await env.VECTORIZE.query(queryEmbedding, {
    topK: 5,
    returnMetadata: true
  });

  // 3. Extract context from top results
  const context = results.matches
    .map(match => match.metadata.text)
    .join('\n\n');

  // 4. Generate response with context
  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash',
    contents: `Context:\n${context}\n\nQuestion: ${userQuery}\n\nAnswer based on the context above:`
  });

  return response.text;
}
```

### Integration with Cloudflare Vectorize

**Create Vectorize Index** (768 dimensions for Gemini):

```bash
npx wrangler vectorize create gemini-embeddings --dimensions 768 --metric cosine
```

**Bind in wrangler.jsonc**:

```jsonc
{
  "name": "my-rag-app",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-25",
  "vectorize": {
    "bindings": [
      {
        "binding": "VECTORIZE",
        "index_name": "gemini-embeddings"
      }
    ]
  }
}
```

**Complete RAG Worker**:

See `templates/rag-with-vectorize.ts` for full implementation.

---

## 7. Error Handling

### Common Errors

**1. API Key Missing or Invalid**

```typescript
// ❌ Error: API key not set
const ai = new GoogleGenAI({});

// ✅ Correct
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

if (!process.env.GEMINI_API_KEY) {
  throw new Error('GEMINI_API_KEY environment variable not set');
}
```

**2. Dimension Mismatch**

```typescript
// ❌ Error: Embedding has 3072 dims, Vectorize expects 768
const embedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text
  // No outputDimensionality specified → defaults to 3072
});

await env.VECTORIZE.insert([{
  id: '1',
  values: embedding.embedding.values // 3072 dims, but index is 768!
}]);

// ✅ Correct: Match dimensions
const embedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text,
  config: { outputDimensionality: 768 } // ← Match index dimensions
});
```

**3. Rate Limiting**

```typescript
// ❌ Error: 429 Too Many Requests
for (let i = 0; i < 1000; i++) {
  await ai.models.embedContent({ /* ... */ }); // Exceeds 100 RPM on free tier
}

// ✅ Correct: Implement rate limiting
async function embedWithRetry(text: string, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await ai.models.embedContent({
        model: 'gemini-embedding-001',
        content: text,
        config: { taskType: 'SEMANTIC_SIMILARITY' }
      });
    } catch (error: any) {
      if (error.status === 429 && attempt < maxRetries - 1) {
        const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
}
```

See `references/top-errors.md` for all 8 documented errors with detailed solutions.

---

## 8. Best Practices

### Always Do

✅ **Specify Task Type**
```typescript
// Task type optimizes embeddings for your use case
const embedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text,
  config: { taskType: 'RETRIEVAL_QUERY' } // ← Always specify
});
```

✅ **Match Dimensions with Vectorize**
```typescript
// Ensure embeddings match your Vectorize index dimensions
const embedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text,
  config: { outputDimensionality: 768 } // ← Match index
});
```

✅ **Implement Rate Limiting**
```typescript
// Use exponential backoff for 429 errors
async function embedWithBackoff(text: string) {
  // Implementation from Error Handling section
}
```

✅ **Cache Embeddings**
```typescript
// Cache embeddings to avoid redundant API calls
const cache = new Map<string, number[]>();

async function getCachedEmbedding(text: string): Promise<number[]> {
  if (cache.has(text)) {
    return cache.get(text)!;
  }

  const response = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    content: text,
    config: { taskType: 'SEMANTIC_SIMILARITY' }
  });

  const embedding = response.embedding.values;
  cache.set(text, embedding);
  return embedding;
}
```

✅ **Use Batch API for Multiple Texts**
```typescript
// Single batch request vs multiple individual requests
const embeddings = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  contents: texts, // Array of texts
  config: { taskType: 'RETRIEVAL_DOCUMENT' }
});
```

### Never Do

❌ **Don't Skip Task Type**
```typescript
// Reduces quality by 10-30%
const embedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text
  // Missing taskType!
});
```

❌ **Don't Mix Different Dimensions**
```typescript
// Can't compare embeddings with different dimensions
const emb1 = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text1,
  config: { outputDimensionality: 768 }
});

const emb2 = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: text2,
  config: { outputDimensionality: 1536 } // Different dimensions!
});

// ❌ Can't calculate similarity between different dimensions
const similarity = cosineSimilarity(emb1.embedding.values, emb2.embedding.values);
```

❌ **Don't Use Wrong Task Type for RAG**
```typescript
// Reduces search quality
const queryEmbedding = await ai.models.embedContent({
  model: 'gemini-embedding-001',
  content: query,
  config: { taskType: 'RETRIEVAL_DOCUMENT' } // Wrong! Should be RETRIEVAL_QUERY
});
```

---

## Using Bundled Resources

### Templates (templates/)

- `package.json` - Package configuration with verified versions
- `basic-embeddings.ts` - Single text embedding with SDK
- `embeddings-fetch.ts` - Fetch-based for Cloudflare Workers
- `batch-embeddings.ts` - Batch processing with rate limiting
- `rag-with-vectorize.ts` - Complete RAG implementation with Vectorize

### References (references/)

- `model-comparison.md` - Compare Gemini vs OpenAI vs Workers AI embeddings
- `vectorize-integration.md` - Cloudflare Vectorize setup and patterns
- `rag-patterns.md` - Complete RAG implementation strategies
- `dimension-guide.md` - Choosing the right dimensions (768 vs 1536 vs 3072)
- `top-errors.md` - 8 common errors and detailed solutions

### Scripts (scripts/)

- `check-versions.sh` - Verify @google/genai package version is current

---

## Official Documentation

- **Embeddings Guide**: https://ai.google.dev/gemini-api/docs/embeddings
- **Model Spec**: https://ai.google.dev/gemini-api/docs/models/gemini#gemini-embedding-001
- **Rate Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
- **SDK Reference**: https://www.npmjs.com/package/@google/genai
- **Context7 Library ID**: `/websites/ai_google_dev_gemini-api`

---

## Related Skills

- **google-gemini-api** - Main Gemini API for text/image generation
- **cloudflare-vectorize** - Vector database for storing embeddings
- **cloudflare-workers-ai** - Workers AI embeddings (BGE models)

---

## Success Metrics

**Token Savings**: ~60% compared to manual implementation
**Errors Prevented**: 8 documented errors with solutions
**Production Tested**: ✅ Verified in RAG applications
**Package Version**: @google/genai@1.30.0
**Last Updated**: 2025-11-26

---

## License

MIT License - Free to use in personal and commercial projects.

---

**Questions or Issues?**

- GitHub: https://github.com/jezweb/claude-skills
- Email: jeremy@jezweb.net
