---
name: gpt-image2
description: Generate and edit images with Dreamfield's OpenAI-compatible gpt-image-2 image API. Use when the user asks Codex to create, test, or save an image from a text description, make wallpaper or illustration assets, perform image-to-image generation from reference images or clipboard images, use masks/inpainting, verify Dreamfield image generation, or troubleshoot image-generation responses such as empty data, b64_json, URL output, quota errors, or content policy errors.
---

# GPT Image 2

Use Dreamfield's OpenAI-compatible image endpoints:

```text
POST https://www.dreamfield.top/v1/images/generations
POST https://www.dreamfield.top/v1/images/edits
```

Recommended environment:

- Provider: Dreamfield, https://www.dreamfield.top/
- Model: `gpt-image-2`
- API key env var: `NEW_image2_API_KEY`
- Author usage note: this skill has been tested with Dreamfield for personal use. It supports 4K output. For details, check Dreamfield for current pricing and model limits.

Use `scripts/generate_image2.py` for all calls. It handles text-to-image, image-to-image, clipboard images, input preprocessing, mask normalization/generation, manual mask drawing, mask overlay previews, conservative retry, response saving, multi-image output, target resizing, and `summary.json` indexing.

## Workflow

1. Convert the user's request to a concise English prompt. Include practical constraints such as `no text` and `no watermark`.
2. Use text-to-image when there is no usable local or clipboard image.
3. Use image-to-image when the user provides `--image`, asks to use a reference image, or asks for image-to-image.
4. Use `--clipboard-image` when the user copied an image to the OS clipboard.
5. Use mask editing only for localized edits/inpainting; otherwise omit mask parameters. Use `--mask-draw` when the user needs to manually paint or circle the edit area.
6. Prefer `response_format=b64_json` for deterministic local PNG saving.
7. Show final local image paths and summary paths.

## Common Commands

Text-to-image:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/gpt-image2"
python3 "$SKILL_DIR/scripts/generate_image2.py" \
  --prompt "A cinematic 16:9 desktop wallpaper of golden lightning over green hills at sunset, no text, no watermark." \
  --size 1792x1024
```

Image-to-image:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/gpt-image2"
python3 "$SKILL_DIR/scripts/generate_image2.py" \
  --image "/absolute/path/to/reference.png" \
  --prompt "Create a new photorealistic 16:9 wallpaper inspired by this reference image, no text, no watermark." \
  --size 1792x1024
```

Masked edit:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/gpt-image2"
python3 "$SKILL_DIR/scripts/generate_image2.py" \
  --image "/absolute/path/to/source.png" \
  --mask-auto rect \
  --mask-rect 120,80,640,360 \
  --prompt "Replace only the masked area while preserving the rest of the image. No text, no watermark." \
  --size 1792x1024
```

Manual masked edit:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/gpt-image2"
python3 "$SKILL_DIR/scripts/generate_image2.py" \
  --image "/absolute/path/to/source.png" \
  --mask-draw \
  --prompt "Replace only the painted area while preserving the rest of the image. No text, no watermark." \
  --size 1792x1024
```

Self-test:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/gpt-image2"
python3 "$SKILL_DIR/scripts/generate_image2.py" --self-test
```

## References

- Full CLI parameters: `references/cli.md`
- Mask semantics and examples: `references/mask.md`
- Self-test, retry, and troubleshooting: `references/troubleshooting.md`

Load the relevant reference file only when the user needs those details.
