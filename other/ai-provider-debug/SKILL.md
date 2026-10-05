---
name: ai-provider-debug
description: Debug and troubleshoot AI/LLM provider integrations. Use when investigating API failures, fallback chain issues, model selection problems, embedding dimension mismatches, or cascading provider failures across 6 providers.
---

# AI Provider Debugging

## Quick Diagnostics

```bash
# Check AI provider health via main health endpoint
curl http://localhost:7500/health | jq '.services.ai_provider'

# Check all provider statuses
curl http://localhost:7500/api/v1/health/diagnostics | jq '.providers'
```

## Provider Registry

| Provider | File | Primary Use |
|---|---|---|
| OpenAI | providers/openAI.ts | Default LLM + embeddings (gpt-4o) |
| Groq | providers/groq.ts | Fast inference fallback |
| Anthropic | providers/anthropic.ts | Premium reasoning (Claude) |
| Azure OpenAI | providers/azureOpenAI.ts | Enterprise OpenAI |
| Google Vertex | providers/googleVertex.ts | Google AI models |
| Ollama | providers/ollama.ts | Local inference (llama3.2:3b) |

## Architecture

### Three-Layer Routing

**1. AIProviderFactory** (`services/aiProvider/aiProvider.ts`)
- Singleton factory, lazy-creates providers on first use
- Primary + fallback provider from config
- `getWithFallback()`: cascading fallback through all providers

**2. AIRouter** (`services/aiProvider/aiProvider.ts`)
- Request-type routing: generate | embed | speech | classify | reason | weather | disease_alerts | vision | video
- Delegates to `AIProviderFactory.getWithFallback()`

**3. Fallback Chain**
```
primary (config.ai.primary.provider)
  -> fallback (config.ai.fallback.provider)
    -> openai
      -> anthropic
        -> groq
          -> ollama
```

### Capabilities

Each provider implements `AICapability` interface:
- generateText() / streamText()
- createEmbedding() / createBatchEmbeddings()
- speechToText() / textToSpeech()
- analyzeWithReasoning()
- classify()
- analyzeImage() / analyzeVideo()
- healthCheck() / isConfigured()

## Key Files

| File | Purpose |
|---|---|
| src/backend/src/services/aiProvider/aiProvider.ts | Factory, Router, base classes |
| src/backend/src/services/aiProvider/providers/*.ts | Individual provider implementations |
| src/backend/src/config/index.ts | Provider config (primary, fallback, models) |

## Embedding Dimensions

**Critical**: All embeddings must use the same dimension. If providers use different models:
- OpenAI: 1536 (text-embedding-3-small) or 3072 (text-embedding-3-large)
- Azure OpenAI: depends on deployment
- Ollama: depends on model

**Symptom**: Vector search returns 0 results or throws dimension mismatch.
**Check**: `VectorService.search()` logs dimension mismatch warnings.

## Common Issues

### All providers failing
If "unhealthy" — no provider has a valid API key. Check `.env` for OPENAI_API_KEY, GROQ_API_KEY, etc.

### Embedding dimension mismatch
```
Vector dimension mismatch! Stored: 1536, Query: 768
```
Cause: Switched embedding models without re-indexing. Fix: re-ingest all knowledge articles.

### Fallback not kicking in
`getWithFallback()` skips unconfigured providers silently. Check logs for:
```
AI provider {type} not configured, skipping...
```

### Ollama not responding
```bash
docker compose ps ettametta-ollama
curl http://localhost:11435/api/tags
```

### API key priority
Config reads from environment variables. Check config/index.ts for exact env var names.
