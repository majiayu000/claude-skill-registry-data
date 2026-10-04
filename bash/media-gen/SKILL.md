---
name: media-gen
description: 'Generate images and videos with AIsa. Supports Gemini, Wan, and Seedream image generation plus Wan text-to-video and image-to-video models. One API key; the bundled client routes each model to the correct endpoint automatically. Use when: you need a neutral AIsa media-generation skill that spans multiple model families without changing credentials or request flow.'
license: MIT
allowed-tools: Read Bash Grep
when_to_use: you need a neutral AIsa media-generation skill that spans multiple model families without changing credentials or request flow
---

> Release note: This package is published for Claude Code. References to OpenClaw below describe the original source workflow, a companion runtime, or compatibility guidance unless the skill is explicitly about OpenClaw itself.

# Media Gen 🎬

Generate images and videos with AIsa using one API key.

This skill covers the current image and video model families exposed by
AIsa across three different API shapes. The bundled client handles the
endpoint differences for you, so you can choose a model and keep the
same local workflow.

**Use when:** you want one neutral media-generation skill for AIsa image
and video tasks, including cases where different models use different
request schemas or response formats.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible
harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- any other harness that implements the [Agent Skills
  specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY` (available from
[aisa.one](https://aisa.one)).

## What this skill covers

### Image generation

- **Google Gemini** image generation via `generateContent`
- **Alibaba Wan 2.7** image generation via chat-completions-style
  requests
- **ByteDance Seedream** image generation via the OpenAI-compatible
  images endpoint

### Video generation

- **Wan text-to-video**
- **Wan image-to-video**
- async task creation, polling, waiting, and optional download through
  the bundled client

## Example requests

### Image — Gemini
```text
"Generate a cyberpunk-style city nightscape, neon lights, rainy night, cinematic feel"
```

### Image — Wan 2.7
```text
"Generate an ultra-detailed product shot of a red panda, studio lighting, sharp focus"
```

### Image — Seedream
```text
"Generate a 2048×2048 magazine cover: neo-noir detective portrait, film grain"
```

### Video — text-to-video
```text
"Sweeping establishing shot of a neon cyberpunk skyline at dusk, 5 seconds"
```

### Video — image-to-video
```text
"Starting from this reference image, gentle camera push-in with parallax"
```

## Supported models

### Image generation — 4 models, 3 endpoints

| Model | Developer | Endpoint | Notes |
|---|---|---|---|
| `gemini-3-pro-image-preview` | Google | `POST /v1/models/{model}:generateContent` | Images return as base64 in `candidates[].parts[].inline_data` |
| `wan2.7-image` | Alibaba | `POST /v1/chat/completions` | Images return as URL parts in `choices[].message.content[]` with `type=image`. $0.030/image |
| `wan2.7-image-pro` | Alibaba | `POST /v1/chat/completions` | Higher-fidelity variant. $0.075/image |
| `seedream-4-5-251128` | ByteDance | `POST /v1/images/generations` | OpenAI-compatible. **Minimum 3,686,400 pixels** (for example `1920x1920`). $0.040/image |

### Video generation — 4 Wan variants, 1 endpoint

| Model | Kind | Image field | Output SR |
|---|---|---|---|
| `wan2.6-t2v` | text-to-video | *none* | 1080 |
| `wan2.6-i2v` | image-to-video | `input.img_url` (string) | 720 |
| `wan2.7-t2v` | text-to-video | *none* | 720 |
| `wan2.7-i2v` | image-to-video | **`input.media`** (array) | 720 |

> **Important schema difference for `wan2.7-i2v`:** this model expects
> the reference image in `input.media` as an array of URLs, not
> `input.img_url` like `wan2.6-i2v`. If `media` is missing, the API can
> return HTTP 200 with a `task_id` and then fail downstream with
> `InvalidParameter: Field required: input.media`. The bundled client
> handles this automatically when you pass `--img-url`.

## Quick start

```bash
export AISA_API_KEY="your-key"

# Any image model — the client routes to the correct endpoint
python3 scripts/media_gen_client.py image \
  --model gemini-3-pro-image-preview \
  --prompt "A cute red panda, cinematic lighting" \
  --out out.png

python3 scripts/media_gen_client.py image \
  --model wan2.7-image-pro \
  --prompt "Ultra-detailed product shot of a red panda" \
  --out out.png

python3 scripts/media_gen_client.py image \
  --model seedream-4-5-251128 \
  --prompt "Neo-noir detective portrait, film grain" \
  --size 2048x2048 \
  --out out.png

# Video — text-to-video
python3 scripts/media_gen_client.py video-create \
  --model wan2.7-t2v \
  --prompt "Sweeping shot of a neon cyberpunk skyline"

# Video — image-to-video on wan2.7-i2v
python3 scripts/media_gen_client.py video-create \
  --model wan2.7-i2v \
  --prompt "gentle zoom with parallax" \
  --img-url "https://example.com/reference.jpg" \
  --duration 5

# Wait and download
python3 scripts/media_gen_client.py video-wait \
  --task-id <task_id> --download --out out.mp4
```

## Image generation endpoint reference

### Gemini family → `POST /v1/models/{model}:generateContent`

Documentation: [Google Gemini Chat](https://aisa.one/docs/api-reference/chat/generatecontent).

```bash
curl -X POST "https://api.aisa.one/v1/models/gemini-3-pro-image-preview:generateContent" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents":[
      {"role":"user","parts":[{"text":"A cute red panda, cinematic lighting"}]}
    ]
  }'
```

Response contains `candidates[].parts[].inline_data` with
`{mime_type, data}`, where `data` is base64 image content.

### Wan 2.7 family → `POST /v1/chat/completions`

Documentation: [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation).

**Critical rule:** `messages[].content` must be an **array of typed
parts**. A plain string returns HTTP 400 `invalid_parameter_error`.

```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.7-image",
    "messages": [
      {"role":"user","content":[
        {"type":"text","text":"A cute red panda, ultra-detailed, cinematic lighting"}
      ]}
    ],
    "n": 1
  }'
```

Images return as `{type: "image", image: "<url>"}` parts inside
`choices[].message.content[]`.

### Seedream → `POST /v1/images/generations`

Documentation: [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations).

```bash
curl -X POST "https://api.aisa.one/v1/images/generations" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedream-4-5-251128",
    "prompt": "A cute red panda, ultra-detailed, cinematic lighting",
    "n": 1,
    "size": "2048x2048"
  }'
```

Response: `data[].url` or `data[].b64_json`.

**Important:** upstream enforces a minimum of 3,686,400 pixels.
`1024x1024` and `1536x1536` are rejected. Any aspect ratio works as long
as `width × height ≥ 3,686,400`.

## Video generation endpoint reference

### Create task → `POST /apis/v1/services/aigc/video-generation/video-synthesis`

Documentation: [Create video generation task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis).
Header `X-DashScope-Async: enable` is required.

```bash
# wan2.6-t2v — text-to-video
curl -X POST "https://api.aisa.one/apis/v1/services/aigc/video-generation/video-synthesis" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model":"wan2.6-t2v",
    "input":{"prompt":"cinematic close-up, slow push-in"},
    "parameters":{"resolution":"720P","duration":5}
  }'

# wan2.7-i2v — image-to-video (uses input.media, not input.img_url)
curl -X POST "https://api.aisa.one/apis/v1/services/aigc/video-generation/video-synthesis" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model":"wan2.7-i2v",
    "input":{
      "prompt":"gentle zoom with parallax",
      "media":["https://example.com/reference.jpg"]
    },
    "parameters":{"resolution":"720P","duration":5}
  }'
```

### Poll task → `GET /apis/v1/services/aigc/tasks/{task_id}`

Documentation: [Get video generation task result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks).

> `task_id` is a **path parameter**. The query-string form
> `?task_id=...` returns HTTP 500 `unsupported uri`.

```bash
curl "https://api.aisa.one/apis/v1/services/aigc/tasks/YOUR_TASK_ID" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## Bundled Python client

The bundled client at `scripts/media_gen_client.py` auto-routes each
image model to the correct endpoint and normalizes output to saved local
files where applicable.

```bash
# Image — model selects the endpoint
python3 scripts/media_gen_client.py image \
  --model <gemini-3-pro-image-preview | wan2.7-image | wan2.7-image-pro | seedream-4-5-251128> \
  --prompt "..." \
  --out out.png

# Video — create task
python3 scripts/media_gen_client.py video-create \
  --model <wan2.6-t2v | wan2.6-i2v | wan2.7-t2v | wan2.7-i2v> \
  --prompt "..." \
  [--img-url https://... (required for -i2v models)] \
  [--duration 5|10] \
  [--resolution 720P|1080P]

# Video — poll / wait / download
python3 scripts/media_gen_client.py video-status --task-id <id>
python3 scripts/media_gen_client.py video-wait --task-id <id> --poll 10 --timeout 600
python3 scripts/media_gen_client.py video-wait --task-id <id> --download --out out.mp4
```

## API reference

This skill calls the following AIsa endpoints directly:

- [Google Gemini Chat — `generateContent`](https://aisa.one/docs/api-reference/chat/generatecontent) — Gemini image models
- [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation) — Wan 2.7 image models
- [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations) — Seedream image generation
- [Create video generation task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis) — Wan video task creation
- [Get video generation task result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks) — async polling

See the [full AIsa API Reference](https://aisa.one/docs/api-reference)
for the complete catalog.

## License

MIT — see [LICENSE](../LICENSE) at the repo root.
