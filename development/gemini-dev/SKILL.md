---
name: gemini-dev
description: "Google Gemini API development with google-genai SDK. Use for prompting, multimodal inputs, structured outputs, and agentic workflows."
---

# Gemini API Development

> **Source:** https://ai.google.dev/gemini-api/docs

Default to the official Google GenAI SDK (`google-genai`) for all prompting, streaming, batching, multimodal, and structured outputs. Use LangGraph/LangChain only for agentic workflows (multi-step + tools). Prefer async (`await client.aio...`) for all SDK calls.

## Quick Reference

### Model Selection

| Model | Use Case | Cost/Speed |
|-------|----------|------------|
| `gemini-2.5-flash-lite` | High-volume, simple tasks | Fastest, cheapest |
| `gemini-2.5-flash` | Default for most tasks | Balanced |
| `gemini-2.5-pro` | Complex reasoning, STEM | Premium |
| `gemini-3-pro-preview` | Best quality, agentic | Highest quality |

### Basic Prompting (async)

```python
from google import genai

client = genai.Client()

resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents="Summarize this document in 3 bullets."
)
print(resp.text)
```

### Streaming

```python
stream = await client.aio.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Draft a concise abstract."
)
async for chunk in stream:
    print(chunk.text, end="", flush=True)
```

### Batch Prompting

```python
import asyncio
from google import genai

client = genai.Client()
prompts = ["Summarize claim 1", "Summarize claim 2", "Summarize claim 3"]

async def run(prompt: str):
    resp = await client.aio.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )
    return resp.text

summaries = await asyncio.gather(*(run(p) for p in prompts))
```

## Multimodal Inputs

### Images

```python
from google.genai import types

with open("image.jpg", "rb") as f:
    img_bytes = f.read()

resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
        "Describe this image.",
    ],
)
```

**Supported formats:** PNG, JPEG, WEBP, HEIC, HEIF

### Documents (PDFs)

```python
import httpx
from google.genai import types

doc_bytes = httpx.get("https://example.com/document.pdf").content

resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(data=doc_bytes, mime_type="application/pdf"),
        "Summarize key points in 5 bullets.",
    ],
)
```

**Limits:** 50MB or 1000 pages max. Each page ≈ 258 tokens.

### Audio

```python
from google.genai import types

with open("audio.mp3", "rb") as f:
    audio_bytes = f.read()

resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(data=audio_bytes, mime_type="audio/mp3"),
        "Transcribe and summarize this audio.",
    ],
)
```

**Supported formats:** WAV, MP3, AIFF, AAC, OGG, FLAC
**Token rate:** 32 tokens/second

### Video

```python
# For large videos, use Files API
myfile = await client.aio.files.upload(file="video.mp4")

resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents=[myfile, "What happens at 01:30?"],
)
```

**Supported formats:** MP4, MPEG, MOV, AVI, FLV, WebM, WMV, 3GPP
**Token rate:** ~300 tokens/second

## Structured Outputs

Use JSON schema + `response_mime_type="application/json"` for guaranteed parseable responses.

```python
from google import genai
from pydantic import BaseModel, Field
from typing import List

class Analysis(BaseModel):
    summary: str = Field(description="Brief summary")
    key_points: List[str] = Field(description="Main points")
    confidence: float = Field(description="Confidence score 0-1")

client = genai.Client()
resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents="Analyze this contract for key terms.",
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Analysis.model_json_schema(),
    },
)
result = Analysis.model_validate_json(resp.text)
```

## Function Calling

Define tools for the model to invoke:

```python
from google import genai
from google.genai import types

def get_weather(location: str) -> dict:
    """Get current weather for a location.

    Args:
        location: City and state, e.g. "San Francisco, CA"

    Returns:
        Weather data dictionary.
    """
    return {"temperature": 72, "condition": "sunny"}

client = genai.Client()
config = types.GenerateContentConfig(tools=[get_weather])

resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents="What's the weather in Boston?",
    config=config,
)
# SDK handles function call automatically in Python
print(resp.text)
```

### Function Calling Modes

- **AUTO** (default): Model decides between text or function call
- **ANY**: Force function call (guarantees schema adherence)
- **NONE**: Disable function calling

```python
tool_config = types.ToolConfig(
    function_calling_config=types.FunctionCallingConfig(
        mode="ANY",
        allowed_function_names=["get_weather"]
    )
)
```

## Files API

For files >20MB or reused across requests:

```python
# Upload
uploaded = await client.aio.files.upload(file="large_document.pdf")

# Use in request
resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents=[uploaded, "Summarize this document."],
)

# Files auto-delete after 48 hours
# Manual delete:
await client.aio.files.delete(name=uploaded.name)
```

## Context Caching

For repeated queries over the same large context:

```python
# Create cache (min 1024 tokens for flash, 4096 for pro)
cache = await client.aio.caches.create(
    model="gemini-2.5-flash",
    system_instruction="You are a legal analyst.",
    contents=[large_document],
    ttl="3600s",  # 1 hour
)

# Use cached context
resp = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the key terms?",
    config={"cached_content": cache.name},
)
```

**Benefit:** ~4x cost reduction for repeated queries.

## Token Counting

```python
# Pre-flight count
counts = await client.aio.models.count_tokens(
    model="gemini-2.5-flash",
    contents=[prompt, image_part],
)
print(f"Input tokens: {counts.total_tokens}")

# Post-generation usage
resp = await client.aio.models.generate_content(...)
usage = resp.usage_metadata
print(f"Prompt: {usage.prompt_token_count}")
print(f"Cached: {usage.cached_content_token_count}")
print(f"Output: {usage.candidates_token_count}")
print(f"Total: {usage.total_token_count}")
```

## Best Practices Checklist

- [ ] Use `google-genai` async APIs (`client.aio.*`)
- [ ] Pick appropriate model: flash-lite → flash → pro → 3-pro-preview
- [ ] Use Files API for large/reused media (>20MB)
- [ ] Use JSON schema structured outputs (not prompt-formatted JSON)
- [ ] Front-load shared context for implicit caching
- [ ] Use explicit caching for repeated large-context queries
- [ ] Count tokens before sending large requests
- [ ] Reserve LangGraph/LangChain for multi-step tool-using agents only
- [ ] Keep temperature at 1.0 for Gemini 3 models

## Resources Index

Detailed official documentation is synced to `resources/`. Consult these when you need specifics beyond this quick reference.

### Core Capabilities

| Resource | When to Consult |
|----------|-----------------|
| [models.md](resources/models.md) | Choosing between models, checking capabilities, context limits, pricing tiers |
| [text-generation.md](resources/text-generation.md) | System instructions, temperature settings, thinking mode, multi-turn conversations |
| [structured-outputs.md](resources/structured-outputs.md) | Complex JSON schemas, nested objects, enums, validation, streaming structured output |
| [function-calling.md](resources/function-calling.md) | Tool definitions, parallel/compositional calling, MCP integration, automatic function calling |

### Multimodal Inputs

| Resource | When to Consult |
|----------|-----------------|
| [multimodal/images.md](resources/multimodal/images.md) | Image formats, object detection, segmentation, bounding boxes, token costs |
| [multimodal/documents.md](resources/multimodal/documents.md) | PDF processing limits, page handling, document vision specifics |
| [multimodal/audio.md](resources/multimodal/audio.md) | Audio formats, transcription, speaker diarization, timestamps |
| [multimodal/video.md](resources/multimodal/video.md) | Video formats, YouTube URLs, frame sampling, timestamp references |

### Infrastructure & Optimization

| Resource | When to Consult |
|----------|-----------------|
| [files-api.md](resources/files-api.md) | Uploading large files, file management, retention policies |
| [context-caching.md](resources/context-caching.md) | Explicit caching setup, TTL management, cost savings calculations |
| [token-counting.md](resources/token-counting.md) | Pre-flight token counts, usage metadata fields, multimodal token costs |
| [long-context.md](resources/long-context.md) | 1M+ token handling, query placement, many-shot learning |

### Tools & Grounding

| Resource | When to Consult |
|----------|-----------------|
| [code-execution.md](resources/code-execution.md) | Sandboxed Python execution, matplotlib, data analysis |
| [url-context.md](resources/url-context.md) | Fetching web pages as context, URL limitations |
| [search-grounding.md](resources/search-grounding.md) | Google Search integration, grounding responses with web results |

### Syncing Documentation

Resources are synced from official Google documentation. To update:

```bash
cd ~/.agents/skills/gemini-dev
~/.bun/bin/bun run scripts/sync-docs.ts
```
