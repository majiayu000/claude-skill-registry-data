---
name: canaryllm-api
description: >
  Call the CanaryLLM gateway (canaryllm.canarycoders.es) — a multi-provider LLM
  API for chat completions, image/video/audio/music/dialogue generation, vision
  (object & face detection, custom model training), conversational AI agents, and
  drop-in OpenAI/Anthropic/Responses-compatible endpoints. Use this whenever the
  user wants to hit CanaryLLM / CanaryLLM API / the canary gateway, generate media
  through it, point an existing tool or SDK at it, or write code/scripts that call
  any canaryllm.canarycoders.es endpoint — even if they don't paste the spec. Knows
  the async queue (submit → poll) workflow that the native endpoints require, the
  Bearer-token auth convention, and which endpoints are synchronous vs queued.
---

# CanaryLLM API

CanaryLLM is a self-hosted, multi-provider LLM gateway. One API fronts OpenAI,
Gemini, Vertex, Anthropic, xAI, Perplexity, LMStudio, Ollama, ElevenLabs, and
MLX Audio for text, images, video, audio, music, vision, and voice agents.

## The one thing to get right: two API surfaces

CanaryLLM has **two ways in**, and they behave differently:

1. **Native endpoints** (`/api/llm/*`, `/api/vision/*`, `/api/convagents/*`) are
   **asynchronous and queue-based**. A `POST` returns a `queueId` immediately —
   *not* the result. You then poll for the result (or stream it). Use these when
   you need media generation, vision, or fine control over CanaryLLM-specific
   options (thinking budgets, web search, caching, tags).

2. **Compatibility endpoints** (`/v1/chat/completions`, `/v1/messages`,
   `/v1/responses`) are **synchronous** — the response *is* the completion. They
   are drop-in replacements for the OpenAI / Anthropic / OpenAI-Responses APIs and
   use the `provider/model` model format (e.g. `anthropic/claude-sonnet-4-5`). Use
   these to point an existing SDK, CLI, or tool at the gateway, or for a quick
   one-shot chat where you just want text back.

**Pick the compat layer when you just want a chat answer; pick a native endpoint
when you need media, vision, agents, or CanaryLLM-only features.** Reaching for
`/api/llm/complete` and then being surprised that you got a `queueId` instead of
text is the #1 mistake — that endpoint is queued by design.

## Base URL and authentication

- **Base URL:** `https://canaryllm.canarycoders.es` (override with
  `$CANARYLLM_BASE_URL` if the user runs a local instance, e.g.
  `http://localhost:3000`).
- **Auth:** Bearer token in the `Authorization` header. The key lives in
  `~/.claude/secrets/canaryllm-api-key`; load it with
  `CANARYLLM_API_KEY=$(cat ~/.claude/secrets/canaryllm-api-key)` and do **not**
  hardcode it or print it. The shell no longer exports it.
  ```
  Authorization: Bearer $CANARYLLM_API_KEY
  ```
- **No-auth endpoints:** `/api/llm/health` and everything under `/api/public/*`
  (model & voice catalogues, the spec itself) need no token.

If that file is missing and the endpoint needs auth, say so and ask the
user for the key rather than guessing — don't invent one.

## The async queue workflow (native endpoints)

Every native generative call follows the same shape:

```
POST /api/llm/<endpoint>   →  { "success": true, "data": { "queueId": "...", "status": "queued" } }
POST /api/llm/queue/result { "queueId": "..." }
        → 202  { "success": false, "data": { "status": "processing", "position": 3 } }   ← keep polling
        → 200  { "success": true,  "data": { "status": "completed", "result": { ... } } }  ← done
```

Three ways to get the result after submitting:

- **Poll** `POST /api/llm/queue/result {queueId}` — returns **202** while still
  queued/processing, **200** with `data.result` when complete. Poll on a short
  interval (1–2s) with a sensible overall timeout. This is the default.
- **Stream** `POST /api/llm/queue/stream {queueId}` — Server-Sent Events with
  `start`, `chunk`, `done`, `error` events. Use for streaming chat output.
- **Status** `POST /api/llm/queue/status {queueId}` — lightweight check
  (`queued | processing | completed | error | cancelled | not_found`) and queue
  position, without fetching the payload.
- **Cancel** `POST /api/llm/queue/cancel {queueId}` — abort a pending task.

Worked example with `curl` — submit, then poll until the status flips to
`completed`:

```bash
# 1. Submit (returns a queueId)
curl -s "$CANARYLLM_BASE_URL/api/llm/generate-image" \
  -H "Authorization: Bearer $CANARYLLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"provider":"openai","prompt":"a red bicycle","n":1}'
# → { "success": true, "data": { "queueId": "abc123", "status": "queued" } }

# 2. Poll for the result (repeat until HTTP 200 with data.result)
curl -s "$CANARYLLM_BASE_URL/api/llm/queue/result" \
  -H "Authorization: Bearer $CANARYLLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"queueId":"abc123"}'
```

When writing application code, implement the same loop: submit, read
`data.queueId`, then poll `/api/llm/queue/result` on a short interval (1–2 s),
treating HTTP **202** as "still processing — keep going" and HTTP **200** (with
`data.status: "completed"`) as done. Add an overall timeout and stop on
`error`/`cancelled`. For streaming chat, set `"stream": true` on the request and
read the SSE events from `/api/llm/queue/stream` instead of polling.

## Common parameters on native endpoints

Most native endpoints accept two optional bookkeeping fields:
- `tag` (string, ≤100 chars) — label a request for usage tracking.
- `service` (string) — route to a named service/key configuration.

Generative requests are validated server-side (size limits, enums); a malformed
body returns `400` with `{ error, code, statusCode, message }`.

## Endpoint index → where to look

Read the matching reference file before writing a request; each has exact request
bodies, enums, limits, and worked examples. The full machine-readable spec is at
`references/openapi.yaml`.

| You want to… | Endpoint(s) | Reference |
|---|---|---|
| One-shot or streaming chat, tool calls, vision, thinking, web search, JSON output | `/api/llm/complete` (queued) | `references/chat-completions.md` |
| Point Claude Code / Codex / Cursor / an SDK at the gateway; quick sync chat | `/v1/messages`, `/v1/chat/completions`, `/v1/responses` (sync) | `references/compat-endpoints.md` |
| Generate images, video, speech (TTS), transcribe (STT), sound effects, music, multi-speaker dialogue; list voices | `/api/llm/generate-*`, `/transcribe`, `/upload-video`, `/voices` | `references/media-generation.md` |
| Object / zero-shot / face detection, auto-label, train or manage custom vision models | `/api/vision/*` | `references/vision.md` |
| Build interview/conversation voice agents, templates, sessions, signed URLs | `/api/convagents/*`, `/api/agents/signed-url` | `references/conversational-ai.md` |
| Discover providers, models, pricing, capabilities, voices, usage, concurrency, health | `/api/llm/providers,models,capabilities,usage,...`, `/api/public/*` | see below |

### Discovery & ops endpoints (GET, mostly quick)

- `GET /api/public/models` — all providers with models, pricing, capabilities (no auth). Best starting point for "what models/pricing are available?"
- `GET /api/public/voices` — all TTS voices by provider (no auth).
- `GET /api/llm/providers` — list provider names.
- `GET /api/llm/models?provider=<name>` — models for one provider.
- `GET /api/llm/voices?provider=<name>` — voices for one provider.
- `GET /api/llm/capabilities` — capability matrix (which provider does what).
- `GET /api/llm/concurrency` and `/api/llm/concurrency/{provider}` — active/queued/limit per provider.
- `GET /api/llm/usage`, `/api/llm/usage/monthly`, `/api/llm/usage/daily` — usage stats.
- `GET /api/llm/health` — health check (no auth).

## Picking a provider/model

If the user doesn't name a provider, don't guess blindly: hit
`GET /api/public/models` (no auth) or `GET /api/llm/capabilities` first to see
what's available and which providers support the capability you need, then choose.
Provider enums differ per endpoint (e.g. image gen accepts `openai, gemini,
vertex, xai, ollama`; video accepts `gemini, vertex, xai`; TTS accepts
`elevenlabs, mlxaudio`) — the reference files list the valid set for each.
