---
name: pixazo-media
description: Generate images, videos, TTS, and music through Pixazo (one API key, 80+ models). Use when Decisions has a Pixazo key or the pixazo MCP is connected.
---

# Pixazo media

Unified image, video, and audio generation via [Pixazo](https://www.pixazo.ai/models).

## When to use

- User wants **image**, **video**, **TTS**, or **music** and Pixazo is configured (Settings → API Keys → Pixazo).
- Prefer **native tools** in the Decisions agent: `image_generator`, `video_generator`.
- In Cursor/Codex, use the **pixazo** MCP (`https://gateway.pixazo.ai/pixazo/mcp`) for umbrella routing, or per-model MCPs from [pixazo.ai/models/mcp](https://www.pixazo.ai/models/mcp).

## Settings

1. API key: [api-console.pixazo.ai/api_keys](https://api-console.pixazo.ai/api_keys) (`sk_live_…`)
2. Enable + Validate in Decisions **API Keys** (auto-saves).
3. **LLMs** tab:
   - **Image LLM** → Provider **Pixazo**, pick model (e.g. `flux-pro`, `sdxl-turbo`).
   - **Video generation** → Provider **Pixazo**, pick model (e.g. `seedance-2`, `veo-3.1`).

## REST pattern (for scripts)

1. `POST` model endpoint or `POST https://gateway.pixazo.ai/v1/generate` with `{ "model": "…", "prompt": "…" }`
2. Headers: `Ocp-Apim-Subscription-Key` and/or `Authorization: Bearer <key>`
3. Poll `GET https://gateway.pixazo.ai/v2/requests/status/{request_id}` until `COMPLETED`
4. Download from `output.media_url[]`

## MCP umbrella tools

`pixazoGenerateImage`, `pixazoGenerateVideo`, `pixazoTextToSpeech`, etc. — optional `model` parameter to target Flux, Seedance, ElevenLabs, etc.

## Related

- **fal-ai-media** — alternative media MCP when `FAL_KEY` is set.
- **content-engine** / **remotion-video-creation** — edit and compose finished videos after generation.
