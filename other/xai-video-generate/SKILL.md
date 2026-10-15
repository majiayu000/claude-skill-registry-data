---
name: xai_video_generate
description: Use when the user asks to generate video, Grok Imagine video, text-to-video, image-to-video, or xAI video through a Grok-connected xAI video generation tool.
---

# xAI Video Generate

Use this skill for Grok Imagine video generation through the Grok-connected xAI video-generation tool.

## Preferred Grok Tool Flow

1. Use `search_tool` to discover the available tool schema first:

```json
{
  "query": "xai video generate"
}
```

2. Call the returned xAI video-generation MCP tool with the schema it reports.

Text-to-video example:

```json
{
  "prompt": "A serene mountain lake at sunrise with slow camera pan, cinematic lighting"
}
```

Image-to-video example:

```json
{
  "prompt": "Animate this image with a slow camera push-in",
  "image_url": "https://example.com/start-frame.jpg"
}
```

Reference-image example:

```json
{
  "prompt": "Create a short cinematic shot using these reference images for style consistency",
  "reference_image_urls": [
    "https://example.com/reference-1.jpg",
    "https://example.com/reference-2.jpg"
  ]
}
```

## Options

- `prompt`: required video prompt.
- `image_url`: optional starting image for image-to-video.
- `reference_image_urls`: optional reference images, when supported by the tool schema.

Return generated video artifact paths, URLs, or IDs exactly as provided by the tool.

## Credential Safety

Use existing Grok/xAI credentials exposed by the host or MCP server. Never print, quote, summarize, or store OAuth tokens, refresh tokens, bearer tokens, or API keys.
