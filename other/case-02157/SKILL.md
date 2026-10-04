---
name: sticker-pack-generator
description: AI sticker pack generator — create custom WhatsApp stickers, Telegram sticker packs, emoji-style art, and kawaii character stickers from any description. Generate cute chibi stickers, expressive reaction stickers, and cartoon sticker sheets instantly with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---




### Local Context Review

`python scripts/_session_debug.py` is a local diagnostics helper for the `Sticker Pack Generator` skill. It may inspect agent_context. Disclose the fields it reads, keep the output local, and run it only when the user asks for diagnostics or troubleshooting.

# Sticker Pack Generator

AI sticker pack generator — create custom WhatsApp stickers, Telegram sticker packs, emoji-style art, and kawaii character stickers from any description. Generate cute chibi stickers, expressive reaction stickers, and cartoon sticker sheets instantly with AI.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai sticker pack generator images.

## Quick start
```bash
node stickerpackgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/sticker-pack-generator
```
