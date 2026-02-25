---
name: gemini-guide
description: "Look up Gemini API documentation, SDK patterns, and current best practices when building with Google Gemini. Maps topics to local cached docs and live sources, provides correct @google/genai patterns, and highlights deprecated vs current API usage. Trigger with 'gemini docs', 'gemini guide', 'how to use gemini', 'gemini SDK', '@google/genai', or when building code that imports from @google/genai or google-genai."
compatibility: claude-code-only
---

# Gemini Guide

Look up Gemini API documentation and SDK patterns when building with Google Gemini. This skill brings Gemini docs TO Claude — it does not call Gemini.

| Skill | Direction | Tool |
|-------|-----------|------|
| **gemini-guide** (this) | Gemini docs -> Claude | Local docs, WebFetch |
| gemini-peer-review | Code -> Gemini | gemini-coach CLI |

## Documentation Sources

Check in this priority order:

| Priority | Source | Best For |
|----------|--------|----------|
| 1 | Local cached docs (`~/Documents/google-gemini-context/`) | Most topics — 24 JS, 24 Python, 7 common topics |
| 2 | GitHub codegen_instructions | Always-current SDK patterns — fetch `https://raw.githubusercontent.com/googleapis/js-genai/refs/heads/main/codegen_instructions.md` |
| 3 | Google AI docs via WebFetch | When local docs don't cover it — `https://ai.google.dev/gemini-api/docs/{topic}` |

## Lookup Workflow

When the user asks about a Gemini topic:

1. **Check corrections first**: Read [references/deprecated-patterns.md](references/deprecated-patterns.md) — know what NOT to suggest before writing any code
2. **Map the query to a topic**: Read [references/topic-index.md](references/topic-index.md) to find the right local doc file
3. **Read the local doc**: The file path will be `~/Documents/google-gemini-context/{path from topic index}`
4. **If local doc seems stale**: Fetch the GitHub codegen_instructions.md for latest SDK patterns
5. **Synthesise**: Combine the documentation into a clear answer with working code examples. Always use the CORRECT patterns from step 1.

## Quick Corrections

These are the most common mistakes. Apply these even without reading the full references:

| Claude Might Suggest | Correct |
|---------------------|---------|
| `@google/generative-ai` | `@google/genai` |
| `google-generativeai` (Python) | `google-genai` |
| `GoogleGenerativeAI` | `GoogleGenAI` |
| `genAI.getGenerativeModel()` | `ai.models.generateContent()` |
| `model.startChat()` / `chat.sendMessage()` | `ai.chats.create()` / `chat.send()` |
| `generationConfig` | `config` |
| `stream=True` (method param) | `config={"stream": True}` |
| `gemini-pro` | `gemini-2.5-flash` |
| `gemini-pro-vision` | `gemini-2.5-flash` (unified multimodal) |
| 4 safety categories | 5 categories (include `HARM_CATEGORY_CIVIC_INTEGRITY`) |
| `HARM_CATEGORY_DANGEROUS_CONTENT` | `HARM_CATEGORY_DANGEROUS` (no `_CONTENT`) |
| `X-Goog-Api-Key` (capitalised) | `x-goog-api-key` (lowercase) |
| Daily rate limits | No daily limits — only per-minute (RPM, TPM) |

### Correct Initialisation (JS)

```javascript
import { GoogleGenAI } from "@google/genai";
const ai = new GoogleGenAI({});  // auto-reads GEMINI_API_KEY env var
const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: "Your prompt"
});
```

### Correct Initialisation (Python)

```python
from google import genai
client = genai.Client()  # auto-reads GEMINI_API_KEY env var
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt"
)
```

## Local Docs Structure

All at `~/Documents/google-gemini-context/`:

| Directory | Contents |
|-----------|----------|
| `javascript/` | 24 topic files — quickstart, function-calling, streaming, structured-output, etc. |
| `python/` | 24 topic files — same topics as JavaScript |
| `common/` | 7 cross-language files — safety, pricing, rate-limits, errors, auth, regions, openai-compat |
| `rest-api/` | REST endpoint docs |
| `MODELS.md` | Current model IDs, capabilities, token limits, rate limits |
| `CLAUDE.md` | Full correction reference (source for deprecated-patterns.md) |
| `googlegenai-gemini-api.md` | Comprehensive SDK guide (608 lines, JS + Python) |
| `INDEX.md` | Keyword index mapping topics to files |

## Current Models

| Model | ID | Best For |
|-------|-----|----------|
| Gemini 2.5 Pro | `gemini-2.5-pro` | Complex reasoning, advanced coding |
| Gemini 2.5 Flash | `gemini-2.5-flash` | Most tasks (recommended default) |
| Gemini 2.5 Flash-Lite | `gemini-2.5-flash-lite-preview-06-17` | Budget, low latency |
| Gemini 2.0 Flash | `gemini-2.0-flash` | Fast inference |
| Text Embedding | `text-embedding-004` | Semantic search, RAG (768 dims) |

For full model details including token limits and rate limits, read `~/Documents/google-gemini-context/MODELS.md`.

## Maintenance

The local docs at `~/Documents/google-gemini-context/` were curated in January 2025. When information seems wrong or outdated:

1. Check the GitHub codegen_instructions.md (always current)
2. Verify model IDs against `https://ai.google.dev/gemini-api/docs/models`
3. Flag stale docs to the user

## Reference Files

| When | Read |
|------|------|
| Mapping a query to a documentation file | [references/topic-index.md](references/topic-index.md) |
| Checking for deprecated patterns before writing code | [references/deprecated-patterns.md](references/deprecated-patterns.md) |
