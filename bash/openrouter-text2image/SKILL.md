---
name: openrouter-text2image
description: Generate images via OpenRouter. Default model openai/gpt-5.4-image-2; any image-modality model can be passed via --model.
---

# openrouter-text2image

Text → image via OpenRouter. Default model: `openai/gpt-5.4-image-2`.

Other supported models (override with `--model`):
- `google/gemini-3.1-flash-image-preview` (Nano Banana 2)
- any other OpenRouter image-modality model

## Usage

Resolve `TOOL_DIR` = the directory containing this `SKILL.md`. Commands below use `TOOL_DIR` as a symbolic placeholder; replace it with the resolved, quoted path before running Bash.

```bash
export OPENROUTER_API_KEY=sk-or-v1-...

python3 TOOL_DIR/scripts/generate_image.py \
  --prompt "Editorial illustration: a neon-lit skateboard at dusk, dramatic shadows" \
  --download PROJECT_DIR/assets/teaser.png
```

## Flags

| Flag | Default | Description |
|---|---|---|
| `--prompt` | required | Text prompt |
| `--download` | required | Output file path (PNG) |
| `--model` | `openai/gpt-5.4-image-2` | Override with any OpenRouter image-modality model |

## Notes

- Request uses `POST /api/v1/chat/completions` with `modalities: ["image","text"]`.
- Images are returned as base64 data URLs in the assistant message; the script decodes and writes to disk.
- For edits/inpainting, include `messages` with both text and image-URL content parts — the script currently supports text-only prompts.
