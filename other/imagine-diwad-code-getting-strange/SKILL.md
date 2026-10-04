---
name: imagine
description: Generate or edit images with Codex. Use this skill whenever the user says "imagine ...", asks to create an image from a text description, transform or restyle an existing image, produce artwork / illustrations / logos / concept art, make image variations, or asks for any kind of AI image generation or image-to-image editing. All outputs are saved inside the current project's `./images/` folder by default.
argument-hint: "[--prompt <text>] [--n 1-8] [--size 1024x1024|1024x1536|1536x1024] [--quality low|medium|high] [--format png|jpeg|webp]"
---

# imagine

Text→image and image→image generation using Codex. Results are saved inside the current project.

## Where results go

By default every generated file lands in **`./images/`**, resolved against the working directory you launched the skill from. The folder is created automatically on first run.

You can override per-run with `--out-dir <path>` (generate) or `--out <path>` (edit).

## Before the first run

Confirm the user has completed one-time setup: Node.js ≥ 18 and a Codex login (`npx @openai/codex login`). If either is missing, point them to `reference/installation.md` — do **not** attempt to install or log in on their behalf.

## Parameter cheat sheet

Use these enum values exactly — anything else will be rejected.

- **Count (`--n`)**: `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` (default `1`)
  - User says "3장" / "three variations" → `--n 3`.
- **Size + aspect ratio (`--size`)**: pick one of three enums.
  | Enum | Ratio | Use for |
  |------|-------|---------|
  | `1024x1024` | 1:1 square | avatars, icons, logos, social posts |
  | `1024x1536` | 2:3 portrait | posters, character art, phone wallpapers (default) |
  | `1536x1024` | 3:2 landscape | banners, wide scenes, desktop wallpapers |
- **Quality (`--quality`)**: `low` | `medium` | `high` (default `medium`)
  - `low`: drafts, throwaway ideation.
  - `medium`: normal use.
  - `high`: only when the user says "high quality", "detailed", "polished", "hero shot".
- **Format (`--format`)**: `png` | `jpeg` | `webp` (default `png`)

## Usage

Run the scripts from the **project root** so `./images` resolves to the intended folder. The skill lives under `<skill-root>/scripts/` (commonly `.claude/skills/imagine/` in Claude Code).

### Generate from text

```bash
node <skill-root>/scripts/generate.js \
  --prompt "a cyberpunk city at night, neon reflections on wet streets" \
  --quality high \
  --size 1024x1024 \
  --n 2
```

| Flag | Required | Values | Default |
|------|----------|--------|---------|
| `--prompt` | yes | free text | — |
| `--n` | no | `1` \| `2` \| `3` \| `4` \| `5` \| `6` \| `7` \| `8` | `1` |
| `--size` | no | `1024x1024` (1:1) \| `1024x1536` (2:3) \| `1536x1024` (3:2) | `1024x1536` |
| `--quality` | no | `low` \| `medium` \| `high` | `medium` |
| `--format` | no | `png` \| `jpeg` \| `webp` | `png` |
| `--out-dir` | no | any path | `./images` |

### Edit / restyle an existing image

```bash
node <skill-root>/scripts/edit.js \
  --input ./photo.png \
  --prompt "turn into a watercolor painting, soft pastels" \
  --quality high \
  --out ./images/photo-watercolor.png
```

Required: `--input`, `--prompt`, `--out`. Optional: `--quality`, `--size`, `--format`.
`edit.js` preserves composition and subject pose while applying the described transform.

### Verify a PNG (optional)

```bash
node <skill-root>/scripts/verify.js --input ./images/result.png
```

Useful when debugging truncated outputs. `generate.js` and `edit.js` already call this automatically and print ✅/❌ in their output.

## Prompt crafting

Pass the user's wording through largely as-is. The scripts already append quality boosters and negative prompts — don't double-wrap.

## After a run

1. Report the saved path(s) exactly as the script prints them (e.g. `./images/gpt-img2_<ts>_0.png`).
2. If any file prints `❌ Verification failed`, re-run that single prompt once. If it fails again, surface the error rather than silently retrying.
3. Do **not** edit the image directly or pipe it through other tools unless the user asked.

## Failure handling

If the script exits with one of these, stop and point the user at `reference/installation.md`:

- `No OAuth session found` → they need to authenticate.
- `Proxy did not respond` / `OAuth proxy failed to start` → missing dependency or port conflict.
- `401` / `403` → expired token, re-login required.
- `Rate limit` → they've hit their tier cap; suggest a retry window.

These are all user-side credential or quota issues; resolving them requires the user's own terminal.

## Layout

```
imagine/
├── SKILL.md            ← this file
├── config.json         ← defaults (quality / size / format / output_dir)
├── reference/
│   └── installation.md ← setup, config reference, troubleshooting
└── scripts/
    ├── generate.js     ← text → image
    ├── edit.js         ← image → image
    └── verify.js       ← PNG sanity check
```
