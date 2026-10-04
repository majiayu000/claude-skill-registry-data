---
name: gemini-api
description: Use when using the Gemini API on Agent Platform with Google Gen AI SDK.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [gemini, api, google-cloud, vertex-ai, sdk, llm, ai]
---

# Gemini API in Agent Platform

Access Google's most advanced AI models for enterprise use cases using the Gemini API in Agent Platform (formerly Vertex AI).

## SDK Installation

| Language | Package | Install Command |
|----------|---------|-----------------|
| Python | `google-genai` | `pip install google-genai` |
| JS/TS | `@google/genai` | `npm install @google/genai` |
| Go | `google.golang.org/genai` | `go get google.golang.org/genai` |
| Java | `com.google.genai:google-genai` | Add to `build.gradle` or `pom.xml` |
| C# | `Google.GenAI` | `dotnet add package Google.GenAI` |

## Authentication

```bash
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='global'
export GOOGLE_GENAI_USE_ENTERPRISE=true
```

## Code Example: Python

```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Explain quantum computing",
)
print(response.text)
```

## Code Example: JavaScript/TypeScript

```typescript
import { GoogleGenAI } from "@google/genai";
const ai = new GoogleGenAI({ enterprise: { project: "your-project-id", location: "global" } });
const response = await ai.models.generateContent({
    model: "gemini-3.6-flash",
    contents: "Explain quantum computing"
});
console.log(response.text);
```

## Recommended Models

- `gemini-3.1-pro-preview` — Complex reasoning, coding, research (1M tokens)
- `gemini-3.6-flash` — Fast, balanced performance, multimodal (1M tokens)
- `gemini-3.5-flash-lite` — High-frequency, lightweight tasks (1M tokens)

## Common Pitfalls

- **Legacy SDKs**: Do NOT use `google-cloud-aiplatform`, `@google-cloud/vertexai`, or `google-generativeai` — they are deprecated
- **Model naming**: Use correct model names (e.g., `gemini-3.6-flash`, not legacy `gemini-pro`)
- **Enterprise flag**: Set `GOOGLE_GENAI_USE_ENTERPRISE=true` for Agent Platform access

## Verification Checklist

- [ ] Gen AI SDK installed for the target language
- [ ] Environment variables configured (`GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`)
- [ ] API enabled: `gcloud services enable aiplatform.googleapis.com`
- [ ] Basic generate_content call succeeds
