---
name: openrouter-icu-image
description: Generate or edit images synchronously through OpenRouter ICU's OpenAI-compatible image API. Use when the user asks Codex to create an image, produce visual assets, transform or edit local/reference images, use OpenRouter ICU, call https://openrouter.icu/v1/images/generations, call https://openrouter.icu/v1/images/edits, parse streaming image responses, or save generated image files from OpenRouter ICU. Always run foreground/blocking and wait for final image files before continuing or replying.
---

# OpenRouter ICU Image

## Core Workflow

1. Check `OPENROUTER_ICU_API_KEY` before making network requests. The CLI also loads `OPENROUTER_ICU_API_KEY=...` from a private `.env` file in the skill directory. If the key is still missing, ask the user for it and do not call the API.
2. Keep API controls out of the image prompt. The prompt should describe only the visual goal: subject, scene, composition, materials, lighting, style, and explicit visual constraints.
3. Choose the endpoint:
   - Text-to-image: `/v1/images/generations`.
   - Local image editing or multi-image references: `/v1/images/edits`.
4. Set explicit request parameters. Defaults are `model=gpt-image-2`, `size=1024x1024`, `quality=medium`, `output_format=png`, `stream=true`, and `partial_images=2`.
5. Run image generation synchronously. Do not background the command, detach the process, start a separate hidden terminal, or use fire-and-forget automation.
6. Wait until the CLI process exits and the final image file is written before continuing with dependent work or sending a final response. If a terminal tool returns a live session ID, poll that session until it exits; do not start unrelated work while image generation is still running.
7. Save outputs under a user-requested path when provided; otherwise use a clear local output path such as `output/openrouter-icu/<slug>.png`.
8. After generation, verify the file exists and render or show it when useful.

## Manuscript-to-PPT Academic Figures

When this skill is used inside `manuscript-to-ppt-workflow` for a source-derived academic diagram, do not improvise the image prompt.

Require a confirmed `align/academic_figure_prompt_v*.md` with:

```yaml
stage: academic_figure_prompt
stage_status: confirmed
```

Use the confirmed English visual prompt from that artifact as the image prompt. Keep model, size, quality, output path, and other API controls outside the prompt. If no confirmed prompt artifact exists, route back to `academic-figure-prompt` and stop.

## Preferred CLI

Use `scripts/openrouter_icu_image.py` for most tasks. It uses only the Python 3 standard library, handles streaming SSE, validates core parameters, avoids accidental requests without an API key, and writes decoded images only after image payload fields are present.

For a local global install, keep a private file at `C:\Users\Administrator\.codex\skills\openrouter-icu-image\.env` with `OPENROUTER_ICU_API_KEY=...`. Do not put real keys in repo-local files, docs, examples, or chat.

On Windows, `scripts\set_openrouter_icu_key.ps1` can prompt for the key and write the private `.env` file without echoing the value.

The CLI is synchronous by default: it does not exit until the HTTP response has completed, SSE events have been parsed, and final image files have been decoded and written. Treat a nonzero exit code as a failed generation and do not claim success.

Run the script from the skill directory or pass the script path appropriate for the installed location. Use a Python 3 launcher:

- macOS/Linux: `python3 scripts/openrouter_icu_image.py`
- Windows PowerShell/CMD: `python scripts\openrouter_icu_image.py` when `python` points to Python 3
- Windows with the Python launcher: `py -3 scripts\openrouter_icu_image.py`

Examples:

```bash
python3 scripts/openrouter_icu_image.py generate \
  --prompt "A clean product photo of a white ceramic coffee mug on a wooden desk, soft natural light" \
  --output output/openrouter-icu/mug.png
```

Windows equivalent:

```powershell
python scripts\openrouter_icu_image.py generate `
  --prompt "A clean product photo of a white ceramic coffee mug on a wooden desk, soft natural light" `
  --output output\openrouter-icu\mug.png
```

```bash
python3 scripts/openrouter_icu_image.py edit \
  --image input.png \
  --prompt "Change the background to a clean modern office while preserving the subject, clothing, pose, and facial features" \
  --output output/openrouter-icu/office.png
```

```bash
python3 scripts/openrouter_icu_image.py edit \
  --image product.png \
  --image background-reference.png \
  --prompt "Create a premium product photo using the product from the first image and the environment style from the second image" \
  --size 1536x1024 \
  --quality high \
  --output output/openrouter-icu/product.png
```

Use `--dry-run` to inspect the request shape without contacting the API.

CLI flags use hyphenated names while the API payload uses snake_case. The script also accepts the snake_case aliases for API-shaped options:

| CLI flag | API payload field |
|---|---|
| `--output-format` / `--output_format` | `output_format` |
| `--output-compression` / `--output_compression` | `output_compression` |
| `--stream`, `--stream true`, `--stream false` | `stream` |
| `--no-stream` / `--no_stream` | `stream=false` |
| `--partial-images` / `--partial_images` | `partial_images` |
| `--image` / `--image-file` | multipart `image[]` |
| `--file-id` / `--file_id` | `images[].file_id` |
| `--image-url` / `--image_url` | `images[].image_url` |
| `--base-url` / `--base_url` | request base; accepts `https://openrouter.icu` or `https://openrouter.icu/v1` |

## Parameter Rules

- Always set `size`, `quality`, and `output_format` explicitly.
- Use `quality=medium` unless the user specifies otherwise.
- Use `output_format=png` unless the user asks for `jpeg` or `webp`.
- Use `stream=true` and `partial_images=2` by default for visible progress and robust final-event handling.
- When using `--stream false`, `--no-stream`, or `--no_stream`, omit `partial_images` from the API payload.
- For custom sizes, require `WIDTHxHEIGHT`, dimensions divisible by 16, aspect ratio between `1:3` and `3:1`, and no more pixels than `3840x2160`.
- Avoid sizes above `2560x1440` unless the user needs high-resolution output.

## Error Handling

- `400`: print full error JSON, fix parameters, and do not retry unchanged.
- `401`: check `OPENROUTER_ICU_API_KEY`; if absent or invalid, ask the user for a valid key.
- `403` / `404`: print full error JSON and check model, file IDs, image URLs, and permissions.
- `408` / `409` / `429` / `5xx`: retry with bounded exponential backoff when appropriate.
- Preserve debugging context: HTTP status, `x-request-id`, model, size, quality, output format, streaming mode, and last SSE event type.

## References

Read `references/api.md` when you need complete endpoint parameters, curl examples, SDK examples, SSE parsing details, or troubleshooting tables.
