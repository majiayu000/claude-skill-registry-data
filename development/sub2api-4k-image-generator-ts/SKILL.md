---
name: sub2api-4k-image-generator-ts
description: TypeScript-only skill for generating and debugging high-resolution AI images through sub2api OpenAI-compatible APIs. Use this whenever the user wants a TS/Node sub2api image generator, 4K image generation, stream=true /v1/images/generations or /v1/responses image generation, Cloudflare 524 timeout avoidance, partial image capture, or SUB2API_BASE_URL/SUB2API_API_KEY based image generation.
---

# sub2api 4K Image Generator TS

Use this skill when the user wants TypeScript/Node image generation through sub2api rather than Codex's built-in image tool.

## Workflow

1. Work from the skill root that contains this `SKILL.md`.
2. Ensure `.env` or the process environment provides:

```env
SUB2API_BASE_URL=https://your-sub2api.example.com
SUB2API_API_KEY=sk-...
```

3. Prefer the compiled JS entrypoint for normal use:

```powershell
node .\dist\openai_4k_image_generator.js `
  "剑仙，云海，发光长剑，无文字无水印" `
  --size 3840x2160 `
  --quality high `
  --output-dir output
```

4. For development, run the TypeScript source:

```powershell
npx tsx .\scripts\openai_4k_image_generator.ts "test prompt" --dry-run
```

5. If Node/TypeScript is inconvenient, use the bundled Python request script:

```powershell
python .\openai_4k_image_request.py "test prompt" --dry-run
```

Install `python-dotenv` first if Python reports that `dotenv` is missing.

6. Report final image paths, partial image paths, and any Cloudflare/SSE diagnostic in plain language. Never print full API keys.

## Notes

- Replace `SUB2API_BASE_URL` with the user's own deployed sub2api domain.
- Treat 4K as explicit pixel sizes: `3840x2160` or `2160x3840`.
- Streaming is enabled by default to avoid Cloudflare 524 during slow 4K generation.
- `*-partial-XX.png` files are diagnostics only; final images are saved as `<prefix>-XX.png`.
- `openai_4k_image_request.py` is a standalone Python fallback that supports `/v1/images/generations`, `/v1/responses`, `--input-image`, streaming SSE, and `--dry-run`.
- Run `npm test` after editing the skill.
- The bundled `dist/` directory is enough for normal use; use `scripts/` only for development or debugging.
