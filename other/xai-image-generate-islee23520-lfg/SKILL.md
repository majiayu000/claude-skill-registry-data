---
name: xai_image_generate
description: Use when the user asks to generate, create, make, or save images with xAI, Grok Imagine, or a Grok-connected xAI image generation tool.
---

# xAI Image Generate

Use this skill for xAI/Grok Imagine image requests through the Grok-connected xAI image-generation tool.

## Preferred Grok Tool Flow

1. Use `search_tool` to discover the available tool schema first:

```json
{
  "query": "xai image generate"
}
```

2. Call the returned xAI image-generation MCP tool with the schema it reports. A typical payload is:

```json
{
  "prompt": "tiny minimalist blue dot icon on white background",
  "resolution": "2k",
  "artifact_dir": ".grok-xai-artifacts"
}
```

For base64 image payloads saved locally, request the response format supported by the tool schema and pass an artifact directory when available.

## Options

- `prompt`: required image prompt.
- `model`: defaults are tool-owned unless the user asks for a specific model.
- `n`: number of images.
- `resolution`: commonly `1k` or `2k` when supported.
- `response_format`: `url` or `b64_json` when supported.
- `size`: provider-specific size string.
- `artifact_dir`: local directory for saved image artifacts, when supported.

When `artifact_dir` is present, return the upstream JSON plus artifact metadata. Saved artifacts should include a local `path`, `mime_type`, `source`, and `status` when the tool provides them. If a remote URL cannot be downloaded, preserve its upstream URL instead of hiding it.

## Credential Safety

Use existing Grok/xAI credentials exposed by the host or MCP server. Never print, quote, summarize, or store OAuth tokens, refresh tokens, bearer tokens, or API keys.
