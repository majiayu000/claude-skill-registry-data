---
name: tokenhop
description: Entry point for tokenhop — local/remote AI gateway with OpenAI-compatible REST for chat, image, TTS, embeddings, web search, web fetch. Use when the user mentions tokenhop, TOKENHOP_URL, or wants AI without writing provider boilerplate. This skill covers setup + indexes capability skills; fetch the relevant capability SKILL.md from the URLs below when needed.
---

# tokenhop

Local/remote AI gateway exposing OpenAI-compatible REST. One key, many providers, auto-fallback.

## Setup

```bash
export TOKENHOP_URL="http://localhost:20128"      # or VPS / tunnel URL
export TOKENHOP_KEY="sk-..."                      # from Dashboard → Keys (only if requireApiKey=true)
```

Older setups may only have the legacy names. When `TOKENHOP_URL` / `TOKENHOP_KEY` are unset, fall back to them:

```bash
export TOKENHOP_URL="${TOKENHOP_URL:-$NINEROUTER_URL}"   # legacy(9router): remove in v2
export TOKENHOP_KEY="${TOKENHOP_KEY:-$NINEROUTER_KEY}"   # legacy(9router): remove in v2
```

All requests: `${TOKENHOP_URL}/v1/...` with header `Authorization: Bearer ${TOKENHOP_KEY}` (omit if auth disabled).

Verify: `curl $TOKENHOP_URL/api/health` → `{"ok":true}`

## Discover models

```bash
curl $TOKENHOP_URL/v1/models                  # chat/LLM (default)
curl $TOKENHOP_URL/v1/models/image            # image-gen
curl $TOKENHOP_URL/v1/models/tts              # text-to-speech
curl $TOKENHOP_URL/v1/models/embedding        # embeddings
curl $TOKENHOP_URL/v1/models/web              # web search + fetch (entries have `kind` field)
curl $TOKENHOP_URL/v1/models/stt              # speech-to-text
curl $TOKENHOP_URL/v1/models/image-to-text    # vision
```

Use `data[].id` as `model` field in requests. Combos appear with `owned_by:"combo"`.

Response shape:

```json
{
  "object": "list",
  "data": [
    { "id": "openai/gpt-5", "object": "model", "owned_by": "openai", "created": 1735000000 },
    {
      "id": "tavily/search",
      "object": "model",
      "kind": "webSearch",
      "owned_by": "tavily",
      "created": 1735000000
    }
  ]
}
```

## Capability skills

When the user needs a specific capability, fetch that skill's `SKILL.md` from the
same gateway base you were given this file from (`<same-base>/skills/<id>/SKILL.md`):

| Capability                 | Path                                   |
| -------------------------- | -------------------------------------- |
| Chat / code-gen            | `/skills/tokenhop-chat/SKILL.md`       |
| Image generation           | `/skills/tokenhop-image/SKILL.md`      |
| Video generation           | `/skills/tokenhop-video/SKILL.md`      |
| Text-to-speech             | `/skills/tokenhop-tts/SKILL.md`        |
| Speech-to-text             | `/skills/tokenhop-stt/SKILL.md`        |
| Embeddings                 | `/skills/tokenhop-embeddings/SKILL.md` |
| Web search                 | `/skills/tokenhop-web-search/SKILL.md` |
| Web fetch (URL → markdown) | `/skills/tokenhop-web-fetch/SKILL.md`  |

## Errors

- 401 → set/refresh `TOKENHOP_KEY` (Dashboard → Keys)
- 400 `Invalid model format` → check `model` exists in `/v1/models/<kind>`
- 503 `All accounts unavailable` → wait `retry-after` or add another provider account
