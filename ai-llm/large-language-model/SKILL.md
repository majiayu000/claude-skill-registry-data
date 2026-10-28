---
name: large-language-model
description: Integrate Gemini 2.5 Flash multimodal LLM via gateway for text/image understanding, content generation, summarization, and multi-turn chat with SSE streaming. Use this skill whenever the user wants to add AI chat, LLM inference, image understanding, content generation, or streaming model responses to their app.
license: MIT
---

# Large Language Model (Gemini 2.5 Flash)

## Capability Overview

Call the Gemini 2.5 Flash multimodal large language model via the API Gateway. Supports text conversation and image understanding, with responses returned as an SSE stream.

- **Endpoint**: `POST https://app-dohnbj5by5mp-api-VaOwP8E7dJqa.gateway.appmedo.com/v1beta/models/gemini-2.5-flash:streamGenerateContent?alt=sse`
- **Response mode**: SSE streaming (Server-Sent Events)
- **Supported modalities**: Multi-turn text conversation, Base64 inline images, file URI images
- **First-token latency**: Up to 30 seconds; extend API timeout settings accordingly
- **Billing**: This endpoint is billed per call

### Request Body Structure (Overview)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `contents` | array | Yes | Array of conversation turns, each containing `role` and `parts` |
| `contents[].role` | string | Yes | `"user"` or `"model"` |
| `contents[].parts` | array | Yes | Message parts; each part contains one of `text`, `inlineData`, or `fileData` |

### Response Structure (SSE stream, per-frame example)

```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [{ "text": "That's easy! Each dog has 4 paws..." }]
      },
      "finishReason": "STOP",
      "index": 0,
      "safetyRatings": []
    }
  ]
}
```

> Read `references/stream-generate-api.md` for the full parameter table, response field descriptions, and complete code for both generation-time and post-generation usage.

---

## End-to-End Workflow

1. The client sends the conversation history (`contents` array) to the Edge Function.
2. The Edge Function reads `INTEGRATIONS_API_KEY` from the Deno environment, attaches the `X-Gateway-Authorization` header, and calls the upstream endpoint via POST.
3. The upstream responds with an SSE stream; the Edge Function **passes the stream through directly** without buffering.
4. The frontend consumes the stream with `ky` + `eventsource-parser` and renders Markdown with `streamdown`.

---

## Generation-Time Usage (Agent Direct Call)

See `references/stream-generate-api.md` — **Generation-Time Usage** section.

Key points: Call the gateway directly via `fetch`, inject the platform key with `X-Gateway-Authorization: Bearer ${apiKey}`, and read the SSE stream line-by-line, parsing each frame's JSON.

---

## Post-Generation Usage (In-App via Edge Function)

See `references/stream-generate-api.md` — **Post-Generation Usage** section.

Key points: The Edge Function passes through the upstream SSE stream; the frontend depends on `ky@^1.2.3`, `eventsource-parser@^3.0.3`, and optionally `streamdown@^1.1.6` for Markdown rendering.

---

## Notes

- **Key security**: `INTEGRATIONS_API_KEY` may only be read server-side in the Edge Function; never expose it to the frontend.
- **Timeout**: First token can take up to 30 seconds; extend the frontend request timeout accordingly (recommend ≥ 60s).
- **Error handling**: Always handle 429 (quota exceeded) and 402 (insufficient balance) and display friendly messages to the user.
- **Billing**: This endpoint is billed per call; avoid unnecessary repeated calls (e.g., rapid successive clicks by the user).
- **Streaming dependency**: The frontend must use `EventSource` or `eventsource-parser` to consume SSE; do not use a plain `fetch().json()`.
- **Markdown rendering**: Model responses contain Markdown formatting; it is recommended to use `streamdown@^1.1.6` for real-time rendering.
