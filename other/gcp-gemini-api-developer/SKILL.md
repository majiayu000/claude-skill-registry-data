---
name: gcp-gemini-api-developer
description: "Build, integrate, and debug Gemini API applications on Google Cloud Agent Platform (formerly Vertex AI) using the unified google-genai SDK. Covers text generation, multimodal inputs, function calling, structured output, embeddings, context caching, batch prediction, streaming, Live API (bidirectional voice/video), and model tuning across Python, TypeScript/JavaScript, Go, Java, and C#. Use when building Gemini-powered applications, migrating from deprecated Vertex AI or google-generativeai SDKs, or integrating Gemini capabilities into a GCP-hosted service."
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-09"
  category: ai
---

# GCP Gemini API Developer

## IMPORTANT BRANDING NOTE

"Agent Platform" (full name: Gemini Enterprise Agent Platform) was previously named "Vertex AI". Many web resources still use "Vertex AI" branding.

## CRITICAL SDK NOTE

The following SDKs are DEPRECATED and must NOT be used:
- `google-cloud-aiplatform` (Python)
- `@google-cloud/vertexai` (Node.js)
- `google-generativeai` (Python — Gemini Developer API SDK)

Use ONLY the unified Gen AI SDK:
- Python: `google-genai` (`pip install google-genai`)
- JavaScript/TypeScript: `@google/genai` (`npm install @google/genai`)
- Go: `google.golang.org/genai` (`go get google.golang.org/genai`)
- Java: `com.google.genai:google-genai`
- C#/.NET: `Google.GenAI` (`dotnet add package Google.GenAI`)

## Authentication

```bash
# Application Default Credentials (ADC) — preferred
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='global'  # Use 'global' for automatic region routing
export GOOGLE_GENAI_USE_VERTEXAI=true
```

## Model Selection

- `gemini-3.1-pro-preview` — complex reasoning, coding, research (1M tokens)
- `gemini-3-flash-preview` — fast, balanced, multimodal (1M tokens)
- `gemini-3.1-flash-lite-preview` — high-frequency lightweight tasks
- `gemini-3-pro-image-preview` — image generation and editing
- `gemini-live-2.5-flash-native-audio` — Live Realtime API (bidirectional audio/video)
- DEPRECATED (do not use): gemini-2.0-*, gemini-1.5-*, gemini-1.0-*, gemini-pro

## Quick Start (Python)

```python
from google import genai
client = genai.Client  # picks up env vars automatically
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain transformer architecture"
)
print(response.text)
```

## Reference Directory

Load only when needed:

| Scenario | Trigger Keywords | Reference |
|---|---|---|
| Text + multimodal | chat, image, video, audio, streaming | references/text-multimodal.md |
| Function calling + tools | tool use, function call, grounding, code execution | references/tools.md |
| Structured output | JSON, schema, structured, typed response | references/structured-output.md |
| Embeddings | embedding, semantic search, vector | references/embeddings.md |
| Context caching | cache, large context, caching tokens | references/caching.md |
| Batch prediction | batch, async, large dataset | references/batch.md |
| Live API | live, realtime, voice, video streaming, bidirectional | references/live-api.md |
| Model tuning | fine-tune, SFT, preference tuning | references/tuning.md |
| Safety | safety filter, threshold, harm category | references/safety.md |
| SDK migration | migrate, deprecated, upgrade | references/migration.md |

## Core Rules

- ALWAYS use the unified `google-genai` SDK family. If user code imports `google-cloud-aiplatform`, `@google-cloud/vertexai`, or `google-generativeai`, flag it as deprecated and provide migration guidance.
- Use `location="global"` (global endpoint) by default for automatic capacity routing. Only use a specific region if the user explicitly requests it.
- Initialize the client without parameters when environment variables are set — don't hardcode project/location in code.
- `gemini-3.1-pro-preview` ≠ `gemini-3-pro-preview` — the latter does NOT exist; use the correct model IDs.
- Context caching (`CachedContent`) reduces cost for repeated large contexts (system prompts, documents) — recommend it proactively for production workloads with stable large contexts.
- For production, consult docs for stable model version aliases rather than using `-preview` models.
- Batch prediction (`BatchJob`) is for async large-dataset inference — use it instead of looping `generate_content` for bulk processing.

## Official Docs

- https://cloud.google.com/vertex-ai/generative-ai/docs/overview
- https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview
- https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview

## Security Notes

Read-only advisory. Never embed API keys or service account credentials in code examples. Use ADC and environment variables. Do not call batch jobs or fine-tuning jobs on production data without explicit user approval.
