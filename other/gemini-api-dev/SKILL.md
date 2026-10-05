---
name: gemini-api-dev
description: Use when build applications using Google Gemini API. Handle chat completions,
  multimodal inputs, function calling, streaming, and grounding with Google Search.
  Use when building applications using google gemini api. handle chat completions,
  multimodal.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- ai
- gemini
- google
- llm
- multimodal
- api
version: 1.0.0
category: core
---


# Gemini Api Dev

## When to Use

**Trigger phrases:**
- "gemini api dev"
- "When building apps powered by Google Gemini models"
- "When processing multimodal inputs (text + images + audio + video)"
- "When implementing function calling or tool use with Gemini"


- When building apps powered by Google Gemini models
- When processing multimodal inputs (text + images + audio + video)
- When implementing function calling or tool use with Gemini
- When using Gemini for grounding with Google Search

## When NOT to Use

- For OpenAI-compatible APIs (use OpenAI skills)
- For local model inference (use Ollama skills)
- For fine-tuning (use Vertex AI training skills)

## Overview

The Google Gemini API provides access to Google's most capable AI models — Gemini 2.5 Pro, 2.5 Flash, and Gemini Nano — through a unified SDK. It supports text generation, multimodal understanding (images, audio, video, PDFs), function calling, and grounding with Google Search. The API is available via the `google-genai` Python SDK and `@google/genai` TypeScript SDK, both providing first-class async support, streaming generators, and type-safe response handling.

Gemini 2.5 Pro excels at complex reasoning, code generation, and multi-turn conversations with a 1-million-token context window. Gemini 2.5 Flash is optimized for speed and cost-efficiency while maintaining strong reasoning capabilities, making it suitable for high-volume production workloads. Nano models run on-device for Android and Chrome, handling summarization, smart reply, and text classification without network calls.

The API architecture follows a content-based message model: each request sends `contents` arrays with `role` (user or model) and `parts` — which can be text, inline_data (base64-encoded images/audio), file_data (PDFs, videos), function_call, or function_response. Configuration options include `systemInstruction` for persona setting, `temperature` (0.0–2.0), `topP`, `topK`, `maxOutputTokens`, `stopSequences`, and `safetySettings` for content filtering.

Grounding with Google Search enables responses that reference real-time information, making Gemini suitable for news analysis, fact-checking, and research tasks. Enabled via `googleSearch` grounding in the generation config, it returns `groundingMetadata` with source URLs, supporting citations alongside generated text. This feature is especially valuable for applications requiring current, verifiable information.

Streaming is a first-class pattern across both SDKs — `generateContentStream` returns async generators that yield chunks as they become available, enabling responsive UI updates, early processing of partial results, and progressive rendering of long outputs without buffering.

## Workflow

1. **Set up SDK** — Install `google-genai` (Python) or `@google/genai` (TypeScript). Configure API key from Google AI Studio or service account for Vertex AI. Load from `GEMINI_API_KEY` environment variable.
2. **Configure auth** — API key for Google AI Studio, service account for Vertex AI. For production, use service account with workload identity federation to avoid hardcoded keys.
3. **Define system instruction** — Set model persona, output format constraints, tone, and domain expertise via `systemInstruction` in generation config. System instructions are treated as developer messages and significantly improve output consistency.
4. **Prepare contents** — Build message history with alternating user/model roles. Include multimodal parts: `inline_data` for base64 images/audio, `file_data` for PDFs/videos uploaded via File API, or text blocks. Use `role: "user"` for input and `role: "model"` for prior assistant turns.
5. **Configure generation parameters** — Set `temperature` (0.0–2.0), `top_p`, `top_k`, `max_output_tokens`, `stop_sequences`, and `safety_settings` per request. For deterministic output, set a `seed` parameter (available in Pro models).
6. **Handle responses** — Stream via `generateContentStream` async generator for real-time output. Handle `function_call` parts by executing tools and resuming with `function_response` parts. Process grounded responses that include `groundingMetadata` with source citations and `groundingChunks`.
7. **Error handling** — Catch `ClientError` (4xx) and `ServerError` (5xx). Implement exponential backoff with jitter for `429 RESOURCE_EXHAUSTED` rate limits. Fallback between Pro and Flash models on quota exhaustion per region.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will just use curl" | SDK handles retries, streaming, auth, and type safety |
| "Gemini is just for text" | Gemini 2.5 processes images, audio, video, and PDFs natively |
| "One prompt fits all" | System instructions and grounding dramatically improve accuracy |
| "Temperature 0 is deterministic" | Even at 0, sampling can produce different outputs; use seed parameter for reproducibility with Pro models |
| "I don't need streaming for short responses" | Streaming is the only way to get real-time function call progress and partial safety assessments |
| "Safety settings can stay default" | Default blocks are conservative — tune per use case or responses may be silently blocked

## Code Example (TypeScript)

```typescript
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.generateContentStream({
  model: 'gemini-2.5-pro',
  contents: [{ role: 'user', parts: [{ text: 'Analyze this chart' }] }],
  config: {
    systemInstruction: 'You are a data analyst. Be precise and cite numbers.',
    temperature: 0.3,
  }
});

for await (const chunk of response) {
  process.stdout.write(chunk.text);
}
```

## Code Example (Python)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

# Basic text generation
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how RAG works in two sentences.",
)
print(response.text)

# Multimodal input with image
import httpx
img = httpx.get("https://example.com/chart.png").content
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        "Analyze this chart and summarize the trend.",
        types.Part.from_bytes(data=img, mime_type="image/png"),
    ],
)
print(response.text)

# Streaming
stream = client.models.generate_content_stream(
    model="gemini-2.5-pro",
    contents="Write a short story about AI.",
    config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=2048,
    ),
)
for chunk in stream:
    print(chunk.text, end="")

# Function calling
def get_weather(city: str) -> str:
    return f"Weather in {city}: sunny, 25\u00b0C"

tools = [
    types.Tool(function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Get current weather for a city",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"],
            },
        ),
    ]),
]

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="What's the weather in Tokyo?",
    config=types.GenerateContentConfig(tools=tools),
)

if response.candidates[0].content.parts[0].function_call:
    fc = response.candidates[0].content.parts[0].function_call
    result = get_weather(fc.args["city"])
    # Send function response back to continue conversation
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[
            "What's the weather in Tokyo?",
            types.Part.from_function_call(fc),
            types.Part.from_function_response(
                name=fc.name,
                response={"result": result},
            ),
        ],
        config=types.GenerateContentConfig(tools=tools),
    )
    print(response.text)

```

## Setup / Configuration

### Installation

**Python:**
```bash
pip install google-genai
```

**TypeScript / Node.js:**
```bash
npm install @google/genai
```

### Authentication

1. Go to [Google AI Studio](https://aistudio.google.com) and click **Get API Key**
2. Create an API key (free tier includes 60 requests per minute)
3. Set it as environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

For production deployments, use a Vertex AI service account with workload identity federation to avoid embedding API keys in application code.

### Safety Settings

Gemini safety filters operate on four categories: harassment, hate speech, sexually explicit content, and dangerous content. Each has adjustable thresholds:

| Threshold | Behavior |
|---|---|
| BLOCK_NONE | Never block |
| BLOCK_ONLY_HIGH | Block only high-confidence harmful content |
| BLOCK_MEDIUM_AND_ABOVE (default) | Block medium and high content |
| BLOCK_LOW_AND_ABOVE | Most restrictive — blocks everything |

Override via generation config:
```python
config = types.GenerateContentConfig(
    safety_settings=[
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_ONLY_HIGH",
        ),
    ],
)
```

### Model Selection Guide

| Model | Use Case | Context | Speed |
|---|---|---|---|
| gemini-2.5-pro | Complex reasoning, code, multimodal | 1M tokens | Slower |
| gemini-2.5-flash | Chat, fast responses, high volume | 1M tokens | Fast |
| gemini-2.5-flash-8b | Lightweight, specialized tasks | 1M tokens | Fastest |

## Common Issues / Troubleshooting

| Error / Symptom | Root Cause | Solution |
|---|---|---|
| `403 PERMISSION_DENIED` | Invalid or expired API key | Regenerate key in AI Studio, verify `GEMINI_API_KEY` env var |
| `429 RESOURCE_EXHAUSTED` | Rate limit exceeded (60 RPM free tier) | Implement exponential backoff, switch to Flash model, upgrade to paid tier |
| `400 INVALID_ARGUMENT` — blocked content | Safety filter triggered | Review safety settings, adjust thresholds, check input content |
| Empty or truncated responses | `max_output_tokens` too low | Increase to 8192 for complex tasks |
| Function call not triggered | Model chose not to call — vague prompt | Add explicit instruction: "Use the available functions" |
| Streaming stalls / hangs | Network issues or server timeout | Set client timeout, implement retry with `generateContent` fallback |
| `400` — invalid multimodal format | Image encoded incorrectly | Use valid base64; supported MIME: PNG, JPEG, WEBP, HEIC, HEIF |
| High latency on simple tasks | Using Pro model unnecessarily | Switch to Flash for speed, reserve Pro for reasoning-heavy work |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Gemini-powered SaaS API | 2-4 weeks | Build vertical API for content analysis, document processing, or image understanding; charge per-request or subscription |
| Chrome extension with Nano | 1-2 weeks | On-device AI extension for summarization/rewriting — zero server costs using Gemini Nano |
| Multimodal chatbot service | 2-3 weeks | Custom chatbots for businesses that analyze images, PDFs, and documents using Gemini Pro vision |
| AI content moderation API | 3-4 weeks | Wrap Gemini safety classification into a moderation SaaS for user-generated content platforms |
| Code review automation tool | 2-3 weeks | PR review assistant using Gemini 2.5 Pro code analysis — integrate with GitHub Apps marketplace |
| Educational content generator | 1-2 weeks | Generate quiz questions and study guides from lecture materials (PDFs + video transcripts) using multimodal input |

## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] API key authenticated successfully via Google AI Studio
- [ ] Chat completions return valid responses for multiple models (Pro, Flash)
- [ ] Streaming works without buffering issues or missing chunks
- [ ] Function calling triggers correctly and resumes conversation
- [ ] Safety settings block harmful content at configured thresholds
- [ ] Multimodal input (image/audio/PDF) processed without errors
- [ ] Grounding with Google Search returns citations in response
- [ ] Error handling catches rate limit (429) and permission (403) errors
- [ ] System instruction correctly influences model behavior
- [ ] Token usage tracked and within quota limits

