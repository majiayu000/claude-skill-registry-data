---
name: evolink-video
description: AI video generation — Sora, Kling, Veo 3, Seedance, Hailuo, WAN, Grok. Text-to-video, image-to-video, video editing. 37 models, one API key.
version: 1.3.0
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    emoji: 🎬
    homepage: https://evolink.ai
---

# Evolink Video — AI Video Generation

Generate AI videos with 37 models including Sora, Kling, Veo 3, Seedance, Hailuo, WAN, and Grok. Text-to-video, image-to-video, first-last-frame, video editing, and audio generation — all through one API.

> This is the video-focused view of [evolink-media](https://clawhub.ai/EvoLinkAI/evolink-media). Install the full skill for image and music generation too.

## Setup

Get your API key at [evolink.ai](https://evolink.ai/signup?utm_source=github&utm_medium=readme&utm_campaign=video-generation-skill-for-openclaw) and set `EVOLINK_API_KEY`.

### Bridge MCP Server (recommended)

For the full tool experience, bridge the MCP server `@evolinkai/evolink-media` ([npm](https://www.npmjs.com/package/@evolinkai/evolink-media)):

**Via mcporter:**
```bash
mcporter call --stdio "npx -y @evolinkai/evolink-media@latest" list_models
```

**Or add to mcporter config:**
```json
{
  "evolink-media": {
    "transport": "stdio",
    "command": "npx",
    "args": ["-y", "@evolinkai/evolink-media@latest"],
    "env": { "EVOLINK_API_KEY": "your-key-here" }
  }
}
```

**Direct install** (Claude Code): `claude mcp add evolink-media -e EVOLINK_API_KEY=your-key -- npx -y @evolinkai/evolink-media@latest`

## MCP Tools

| Tool | Purpose |
|------|---------|
| `generate_video` | Create AI videos from text or images |
| `upload_file` | Upload local images for image-to-video generation workflows |
| `delete_file` | Remove uploaded files to free quota |
| `list_files` | View uploaded files and check storage quota |
| `check_task` | Poll generation progress and get result URLs |
| `list_models` | Browse available video models |
| `estimate_cost` | Check model pricing |

## Video Models (37)

### Top Picks

| Model | Best for | Features |
|-------|----------|----------|
| `seedance-1.5-pro` *(default)* | Image-to-video, first-last-frame | i2v, 4–12s, 1080p, audio |
| `sora-2-preview` | Cinematic preview | t2v, i2v, 1080p |
| `kling-o3-text-to-video` | Text-to-video, 1080p | t2v, 3–15s |
| `veo-3.1-generate-preview` | Google video preview | t2v, 1080p |
| `MiniMax-Hailuo-2.3` | High-quality video | t2v, 1080p |
| `wan2.6-text-to-video` | Alibaba latest t2v | t2v |
| `sora-2` [BETA] | Cinematic, prompt adherence | t2v, i2v, 1080p |
| `veo3.1-pro` [BETA] | Top quality + audio | t2v, 1080p, audio |

### All Stable Models (26)

`seedance-1.5-pro`, `seedance-2.0`, `doubao-seedance-1.0-pro-fast`, `sora-2-preview`, `kling-o3-text-to-video`, `kling-o3-image-to-video`, `kling-o3-reference-to-video`, `kling-o3-video-edit`, `kling-v3-text-to-video`, `kling-v3-image-to-video`, `kling-o1-image-to-video`, `kling-o1-video-edit`, `kling-o1-video-edit-fast`, `kling-custom-element`, `veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview`, `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-2.3-Fast`, `MiniMax-Hailuo-02`, `wan2.5-t2v-preview`, `wan2.5-i2v-preview`, `wan2.5-text-to-video`, `wan2.5-image-to-video`, `wan2.6-text-to-video`, `wan2.6-image-to-video`, `wan2.6-reference-video`

### All Beta Models (11)

`sora-2`, `sora-2-pro`, `sora-2-beta-max`, `sora-character`, `veo3.1-pro`, `veo3.1-fast`, `veo3.1-fast-extend`, `veo3`, `veo3-fast`, `grok-imagine-text-to-video`, `grok-imagine-image-to-video`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | — | Video description (required) |
| `model` | enum | `seedance-1.5-pro` | Model to use |
| `duration` | integer | model default | Duration in seconds |
| `aspect_ratio` | enum | `16:9` | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` |
| `quality` | enum | model default | `480p` / `720p` / `1080p` / `4k` |
| `image_urls` | string[] | — | Reference images for i2v |
| `generate_audio` | boolean | model default | Auto-generate audio (seedance-1.5-pro, veo3.1-pro) |

## File Upload

For image-to-video generation, upload reference images first:

1. Call `upload_file` with `file_path`, `base64_data`, or `file_url` → get `file_url` (synchronous)
2. Use that `file_url` as `image_urls` input for `generate_video`

**Supported:** Images (JPEG, PNG, GIF, WebP). Max **100MB**. Files expire after **72 hours**. Quota: 100 files (default) / 500 (VIP).

## Workflow

1. Upload reference images/video if needed (via `upload_file`)
2. Call `generate_video` → get `task_id`
3. Poll `check_task` every 10–15s until `completed`
4. Download result URLs (expire in 24h)

## Without MCP Server — Direct File Hosting

When MCP tools are not available, you can still upload files to Evolink's hosting via `curl`:

```bash
# Upload local file
curl -X POST https://files-api.evolink.ai/api/v1/files/upload/stream \
  -H "Authorization: Bearer $EVOLINK_API_KEY" \
  -F "file=@/path/to/image.jpg"

# Upload from URL
curl -X POST https://files-api.evolink.ai/api/v1/files/upload/url \
  -H "Authorization: Bearer $EVOLINK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_url": "https://example.com/image.jpg"}'
```

Response returns `file_url` (public link, expires in 72h). Supported: Images (JPEG/PNG/GIF/WebP). Max **100MB**.

> For full video generation, bridge the MCP server `@evolinkai/evolink-media` — see Setup above.
