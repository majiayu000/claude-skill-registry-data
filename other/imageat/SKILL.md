---
name: imageat
description: Generate AI images and videos with the imageat API. Use when the user asks to create, edit or animate images, remove a background, generate a video from text or a photo, or check their imageat balance.
---

# imageat

imageat generates images and videos from prompts and reference images. Every call is
billed to the user's imageat account, so confirm before generating many outputs or
long videos.

## Setup

- The user creates an API key at https://imageat.com/projects/keys (keys start with
  `iat_live_`). Read it from the `IMAGEAT_API_KEY` environment variable; never print it.
  If it is not set, ask the user to set it (or paste a key) before calling the API.
- Base URL: `https://imageat.com/api/v1`
- Send `Authorization: Bearer $IMAGEAT_API_KEY` and `Content-Type: application/json`.
- Send an `Idempotency-Key` header (any unique string) on POSTs you might retry.
- MCP clients can connect to https://mcp.imageat.com/mcp instead (OAuth or the same key).

## Generate an image (synchronous)

```bash
curl -X POST "https://imageat.com/api/v1/images" \
  -H "Authorization: Bearer $IMAGEAT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nano-banana-2","prompt":"A cinematic product photo on sculpted stone","aspectRatio":"1:1","resolution":"1K","numImages":1}'
```

The response contains `url` (one image) or `urls` (several), hosted on cdn.imageat.com.

Models (live list: `GET https://imageat.com/api/v1/models/images`):

- `nano-banana-pro` (Nano Banana Pro): High-fidelity generation and editing with up to 4K output. From $0.40 / image.
- `nano-banana-2.1` (Nano Banana 2.1): Google's newest Nano Banana: up to 4K, extreme 8:1 to 1:8 ratios, up to 14 references, and optional web search grounding. From $0.16 / image.
- `krea-3` (Krea 3): Krea's newest model: aesthetic generation with prompt expansion, faithful instruction edits, up to 4 references, 1K or 2K. From $0.06 / image.
- `nano-banana-2` (Nano Banana 2): Fast, cost-efficient generation for iterative creative work. From $0.16 / image.
- `gpt-image-2.5` (GPT Image 2.5): OpenAI's newest image model: five quality tiers, scoped edits, and transparent cut-outs. Add gpt-image-2.5-sunburst for the slower, finer-detail variant. From $0.02 / image.
- `midjourney-v8` (Midjourney V8): Midjourney V8.2 with stylize, chaos, weird, and style references. Every run returns 4 images; native 2K HD optional. From $0.18 / 4 images.
- `gpt-image-2` (GPT Image 2): Precise instruction following with selectable quality tiers. From $0.02 / image.
- `seedream-5.0-pro` (Seedream 5 Pro): High-fidelity ByteDance generation and reference-guided editing. From $0.14 / image.
- `nano-banana-2-lite` (Nano Banana 2 Lite): The cheapest Nano Banana, for drafts, thumbnails and bulk runs. From $0.08 / image.
- `nano-banana` (Nano Banana): The original Nano Banana (Gemini 2.5 Flash Image) for quick generation and edits. From $0.16 / image.
- `seedream-5.0-lite` (Seedream 5 Lite): Faster, cheaper Seedream 5 for generation and reference-guided edits. From $0.07 / image.
- `krea-2-large` (Krea 2 Large): Krea 2 text-to-image with up to 10 style references. One image per request. $0.13 / image.
- `krea-2-medium` (Krea 2 Medium): Lighter Krea 2 with the same style references. One image per request. $0.07 / image.

- GPT Image models accept `quality`; GPT Image 2.5 also takes `xhigh`/`max` and
  `transparentBackground` (needs png or webp output).
- Nano Banana 2.1 takes up to 14 `images`, extreme ratios (`8:1` to `1:8`, plus `auto`)
  and `enableWebSearch` for grounding in live web results.
- Krea 3 (`krea-3`) renders 1K or 2K (4K requests render at 2K) and takes up to 4 `images`;
  each reference is billed like extra output pixels, so send only the ones the edit needs.
- Midjourney V8 (`midjourney-v8`) always returns 4 images per run (read `urls`; `numImages`
  is ignored) and takes ~2 minutes. `resolution` is 1K or 2K (native HD); optional `stylize`
  (0-1000), `chaos` (0-100), `weird` (0-3000), `seed` and `styleReferenceUrl`.
- Editing / reference-guided generation: pass public URLs or base64 data URLs in `images`.
- Other fields: `aspectRatio`, `resolution` (1K, 2K, 4K), `outputFormat` (png, jpeg, webp), `numImages`.

## Edit an image

`GET https://imageat.com/api/v1/edit/features` lists the edit features (id, name, credit cost): background
removal and replacement, object eraser, inpainting, relight, virtual try-on and more.

```bash
curl -X POST "https://imageat.com/api/v1/edit" \
  -H "Authorization: Bearer $IMAGEAT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"feature":"ideogram-remove-background","imageUrl":"https://example.com/photo.jpg"}'
```

Body: `feature`, `imageUrl` (public URL or base64 data URL), plus `prompt`, `maskUrl`,
`backgroundPrompt` or `backgroundImageUrl` when the feature needs them.

## Generate a video (asynchronous)

```bash
curl -X POST "https://imageat.com/api/v1/videos" \
  -H "Authorization: Bearer $IMAGEAT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"seedance25","providerVariant":"more","prompt":"A paper airplane glides through a softly lit studio","duration":"5s","resolution":"720p","aspectRatio":"adaptive"}'
```

The response has `status: pending`, `taskId` and `generationId`. Poll every 5-10 seconds:

```bash
curl "https://imageat.com/api/v1/videos/status?taskId=TASK_ID&generationId=GENERATION_ID" \
  -H "Authorization: Bearer $IMAGEAT_API_KEY"
```

Stop when `status` is `completed` (read `url`) or `failed`. Cancel with `POST https://imageat.com/api/v1/videos/cancel` and body
`{"taskId":"TASK_ID","generationId":"GENERATION_ID"}`.

Models (live list: `GET https://imageat.com/api/v1/models/videos`):

- `wan3` (Wan 3.0): Text, image, first/last-frame or reference-image video; 2–30s · 480p/720p/1080p · audio; From $0.20.
- `minimax-h3-max` (MiniMax H3 Max): Text, image, or first/last-frame video; 5–15s · 480p/768p; From $0.25.
- `seedance25` (Seedance 2.5): Text, image, reference, or frame-controlled video; 4–30s · 480p/720p; From $0.83.
- `midjourney-v8` (Midjourney V8): Image-to-video, 4 clips per run; 4 × 5s · 480p/720p; From $0.18.
- `pixverse` (Pixverse V6): Text/image video with optional audio; 1–15s · up to 1080p; From $0.09/sec.
- `veo` (Veo 3.1 Fast): Default model. Text or image video; 4/6/8s · 720p/1080p/4K · audio; From $1.20.
- `veo-lite` (Veo 3.1 Lite): Text, image, or first/last-frame video; 4/6/8s · 720p/1080p · audio; From $0.40.
- `sora` (Sora): Text or image video; 4/8/12s · 720p/1080p; From $0.80.
- `kling` (Kling 2.6): Text or image video; 5/10s · 720p/1080p · optional audio; From $0.70.
- `kling3` (Kling 3.0): Text or image video; 3–15s · 720p/1080p/4K · optional audio; From $0.34/sec.
- `kling3-omni` (Kling 3.0 Omni): Text or image video; 3–15s · 720p/1080p/4K · optional audio; From $0.42/sec.
- `grok` (Grok Video): Text or image video; 1–15s · 480p/720p; From $0.10/sec.
- `grok-1-5` (Grok Video 1.5): Image-to-video; 1–15s · 480p/720p; From $0.17/sec.
- `seedance2` (Seedance 2.0): Text, image, or reference-image video; 4–15s · 480p/720p/1080p; From $1.08.
- `seedance2-mini` (Seedance 2.0 Mini): Text, image, or reference-image video; 5/10/15s · 480p/720p; From $0.36.
- `gemini-omni` (Gemini Omni Flash): Text or image video; 5/10s · 720p; From $2.12.
- `happyhorse` (Happy Horse 1.0): Text or image video; 5/10/15s · 720p/1080p; From $1.40.
- `happyhorse-ref` (Happy Horse 1.0 Reference): Reference-image video (referenceImageUrls); 5/10/15s · 720p/1080p; From $1.40.
- `flux3` (FLUX 3 Video): Text or image video; 5–20s · 720p/1080p; From $1.70.

- Image-to-video: pass `imageUrl` (first frame), or `firstFrameUrl` + `lastFrameUrl`.
- `midjourney-v8` is image-to-video only: `imageUrl` is required, `resolution` is 480p or 720p,
  `motion` is low or high. Each run returns 4 five-second clips in `urls`.

## Check balance

`GET https://imageat.com/api/v1/credits` returns the account's API balance in USD (and spendable web
credits, which are spent first).

## Errors

- `401`: missing or invalid key. Ask the user for a valid key.
- `402`: not enough balance (`balance` and `required` in the body). Send the user to
  https://imageat.com/api-pricing; do not retry.
- `429`: rate limited. Wait for `Retry-After` seconds, then retry.
- `500`: retry once with the same `Idempotency-Key`.

## Reference

- Full API docs (markdown): https://imageat.com/docs/api/md
- OpenAPI: https://imageat.com/openapi.yaml
- Pricing: https://imageat.com/api-pricing
