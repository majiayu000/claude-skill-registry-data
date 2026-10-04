---
name: ai-gateway
description: "Reference for the studio/ai-gateway service — the single shared entry point every other service uses to reach Claude, Gemini, and MiniMax. Use this when any service needs a new AI capability, when adding/editing system prompts or tool definitions, or when changing which provider handles which task."
---

# AI Gateway — Reference

## Purpose

One internal service that all other services call for any AI capability. No service (store, bots, dubbing) holds an AI provider API key or calls Claude/Gemini/MiniMax directly. This is what makes "swap providers" or "add logging" a one-place change instead of a three-place change.

## Endpoints

### `POST /ai/chat`
```json
{
  "context": "store-chat | store-admin | telegram-fb-ig-dm | fb-ig-comment",
  "message": "user's message",
  "history": [ /* prior turns, optional */ ]
}
```
- `context` selects the system prompt AND, for `store-admin`, the available tools (see `medusa-store` skill for the tool list)
- Routes to Claude (this is the default chat/agent provider)
- Returns `{ reply, tool_calls?: [...] }`

### `POST /ai/translate`
```json
{
  "context": "dubbing-sorani-to-iraqi",
  "text": "chunk text",
  "duration_seconds": 3.2
}
```
- Routes to MiniMax (see `video-dubbing` skill for the prompt spec)

### `POST /ai/transcribe`
```json
{ "audio_url": "...", "language_hint": "ku" }
```
- Routes to Gemini for Sorani ASR
- Returns `{ chunks: [{ text, start_time, end_time }] }`

### `POST /ai/tts`
```json
{ "text": "...", "voice": "iraqi-arabic-default", "provider": "minimax | chatterbox" }
```
- `provider` defaults to `minimax`; switch to `chatterbox` once self-hosted (see `video-dubbing` skill)

## System Prompt Registry

Each `context` value maps to one system prompt, stored as a separate file under `studio/ai-gateway/prompts/<context>.md` — never inline in code, so non-developers (and other agents) can review/edit prompts without touching application code.

| Context | Used by | Contains |
|---|---|---|
| `store-chat` | Store widget | Product catalog, FAQ, store policies (Arabic) |
| `store-admin` | Store admin agent | Tool definitions + Arabic admin persona |
| `telegram-fb-ig-dm` | Bot Bridge | Store knowledge + conversational DM persona |
| `fb-ig-comment` | Comment Bot | Shorter, public brand-voice persona |
| `dubbing-sorani-to-iraqi` | Dubbing, step 2 | Dialect/register translation spec |

## Cost Logging (mandatory)

Every request to this service writes one row to the `ai_requests` or `ai_usage_logs` table (Supabase): `{ timestamp, context, provider, model, input_tokens, output_tokens, estimated_cost }`. This is the FIRST place the `debugger` agent should look for any AI-related issue — it shows exactly what was sent/received and what it cost, across every service.

## Adding a New AI Capability

1. Does an existing endpoint cover it? (most "new AI features" are just a new `context` value on `/ai/chat`)
2. If genuinely new, add an endpoint here — never let another service call a provider directly, even "just this once"
3. Add the system prompt file under `studio/ai-gateway/prompts/`
4. Add cost logging for the new call path
5. Update the table above

