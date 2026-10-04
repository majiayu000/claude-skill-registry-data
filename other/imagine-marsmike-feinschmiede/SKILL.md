---
name: imagine
description: Generate AI images via Replicate or Gemini. Use to create illustrations, photos, or graphics from a text prompt.
---

# feinbild — AI image generation

## Quick Start

```
/imagine retro synthwave city skyline
```

See [`references/providers.md`](references/providers.md) for examples.

`feinbild` is a command on your PATH. Requires a provider key in `~/.env`
(`REPLICATE_API_KEY` or `GEMINI_API_KEY`).

```bash
feinbild imagine --prompt "a calm mountain lake at dawn" --out lake.webp
```

Options: `--provider` (`replicate`/`gemini`), `--model`, `--aspect-ratio`
(`1:1` default, `16:9`, `9:16`, `4:3`, `3:2`, …), `--out`.
Without a key the command prints a clean error and makes no paid call.

## Providers

- **Replicate** (default) — Flux models, fast, best text rendering for memes.
- **Gemini** — free tier (500/day), great general quality.

Full model list, selection guide, and examples: [`references/providers.md`](references/providers.md).

## Brand Design Systems

For images in the visual style of specific companies (Apple, Linear, Stripe,
Vercel, etc.), fetch the brand's DESIGN.md from
[awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — 76+ design
systems as plain markdown.

**URL:** `https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/designs/<brand>/DESIGN.md`

Extract the brand's color palette, typography style, and visual language, then
weave them into the `--prompt` (e.g., "clean Apple-style design with SF Pro
typography, white background, subtle shadows, #007AFF accent blue").
