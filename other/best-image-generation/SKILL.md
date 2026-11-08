---
name: best-image-generation
description: Best quality AI image generation (~$0.12-0.20/image). Text-to-image, image-to-image, and image editing via the EvoLink API.
homepage: https://evolink.ai
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["EVOLINK_API_KEY"]}, "primaryEnv": "EVOLINK_API_KEY"}}
---

# EvoLink Best Image

Generate and edit images via the EvoLink Nano Banana Pro (gemini-3-pro-image-preview) API.

## API Endpoint

- Base: `https://api.evolink.ai/v1`
- Submit: `POST /images/generations`
- Poll: `GET /tasks/{id}`

## Step 1 — Submit Task

### Text-to-image

```json
{
  "model": "gemini-3-pro-image-preview",
  "prompt": "<USER_PROMPT>",
  "size": "<SIZE>",
  "quality": "<QUALITY>"
}
```

### Image-to-image / editing

```json
{
  "model": "gemini-3-pro-image-preview",
  "prompt": "<USER_PROMPT>",
  "size": "<SIZE>",
  "quality": "<QUALITY>",
  "image_urls": ["<URL1>", "<URL2>"]
}
```

| Parameter | Values |
|---|---|
| size | auto, 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| quality | 1K, 2K (default), 4K (extra cost) |
| image_urls | up to 10 URLs (each ≤10MB, formats: jpeg/jpg/png/webp) |

## Step 2 — Poll for Result

`GET /tasks/{id}` — poll every 10 s, up to 72 retries (~12 min).

Wait until `status` is `completed` or `failed`.

## Step 3 — Download & Output

Download the URL from `results[0]`. Auto-detect format from URL (png/jpg/webp). Save as `evolink-<TIMESTAMP>.<ext>`.

**CRITICAL SECURITY:** Before passing `<OUTPUT_FILE>` to shell commands, sanitize it:
- Strip all shell metacharacters: `tr -cd 'A-Za-z0-9._-'`
- Ensure valid extension (`.png`, `.jpg`, `.jpeg`, `.webp`)
- Fallback to `evolink-<timestamp>.png` if empty

Print `MEDIA:<absolute_path>` for OC auto-attach.

## Reference Implementations

| Platform | File |
|---|---|
| Python (all platforms, zero deps) | `{baseDir}/references/python.md` |
| PowerShell 5.1+ (Windows) | `{baseDir}/references/powershell.md` |
| curl + bash (Unix/macOS) | `{baseDir}/references/curl_heredoc.md` |

## API Key

- `EVOLINK_API_KEY` env var (required)
- Get key: https://evolink.ai

## Triggers

- Chinese: "高质量生图：xxx" / "编辑图片：xxx"
- English: "best image: xxx" / "edit image: xxx"

Treat the text after the colon as `prompt`, use default size `auto` and quality `2K`, generate immediately.

For image-to-image or editing, the user provides image URLs alongside the prompt.

## Notes

- Print `MEDIA:<path>` for OC auto-attach — no extra delivery logic needed.
- Image saved locally (format auto-detected from URL: png/jpg/webp). URL expires ~24h but local file persists.
- `quality: 4K` incurs additional charges.
- `image_urls` accepts up to 10 URLs (each ≤10MB, formats: jpeg/jpg/png/webp).
