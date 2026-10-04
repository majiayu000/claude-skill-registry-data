---
title: Xiaomi MiMo Free AI API
name: xiaomi-mimo-api
description: Call Xiaomi MiMo via the free-ai bootstrap + chat endpoints. Covers auth flow, headers, model IDs, streaming, and known failure modes.
---

# Xiaomi MiMo Free AI API

Use this workflow whenever a task calls Xiaomi MiMo through `api.xiaomimimo.com`.

## Preconditions

- The target environment allows outbound HTTPS to `api.xiaomimimo.com`.
- The provider must be invoked with the free-ai bootstrap flow; standard `Authorization: Bearer sk-...` or `tp-...` keys are invalid here.

## Core workflow

1. Bootstrap a session JWT:

```bash
curl -s -X POST 'https://api.xiaomimimo.com/api/free-ai/bootstrap' \
  -H 'Content-Type: application/json' \
  -d '{"client":"haha"}'
```

- Parse JSON and read `jwt`.
- The returned `jwt` is short-lived; bootstrap once per logical session.

2. Call chat:

```bash
curl -X POST 'https://api.xiaomimimo.com/api/free-ai/openai/chat' \
  -H "Authorization: Bearer *** \
  -H 'X-Mimo-Source: mimocode-cli-free' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "mimo-auto",
    "messages": [{"role":"user","content":"..."}],
    "max_tokens": 128000,
    "stream": true,
    "temperature": 1.0
  }'
```

## Response shape

Returns OpenAI-compatible SSE chunks.

- `model` is always reported as `mimo-auto`.
- Each chunk may contain `reasoning_content`, then `content`.
- Final chunk may contain `usage` when `stream=true`.

A representative successful body:

```json
{
  "id": "...",
  "object": "chat.completion.chunk",
  "model": "mimo-auto",
  "choices": [
    {
      "delta": {
        "reasoning_content": "用户要求我只回复...",
        "content": "我是MiMo，由小米大模型Core团队开发的智能助手！"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## Pitfalls

- Wrong endpoint: `/v1/chat/completions` returns 401 even with bootstrap JWT.
- Missing header: omit `X-Mimo-Source: mimocode-cli-free` and the call will reject.
- Model ID: docs mention `mimo-v2.5-pro-ultraspeed`, but the working free-ai endpoint uses `mimo-auto`.
- Key reuse: do not reuse prior `sk-...` or `tp-...` credentials with this endpoint.

## Verification

After bootstrap, a minimal successful call is:

- `model` in response: `mimo-auto`
- First non-empty assistant output in `content`
- `finish_reason`: `stop`

If bootstrap succeeds but chat returns 401, the issue is headers/model or the JWT expired.
