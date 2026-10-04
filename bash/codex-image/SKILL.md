---
name: codex-image
description: Generate or edit raster images (photos, illustrations, mockups, hero images, product shots, bitmap icons, transparent cutouts) with OpenAI GPT Image 2 by triggering the local Codex CLI, billed to the user's ChatGPT subscription — no API key needed. Use when the user says "generate an image", "make a picture/illustration/mockup", "use codex / gpt image / gpt-image-2", "edit this image", "remove the background", or a project needs a bitmap asset. Not for video, SVG, or graphics better built in code.
---

# codex-image

Runs Codex CLI non-interactively. Codex calls its built-in `image_gen` tool (GPT Image 2) and the
script copies the result to the path you choose. Each call takes roughly 30–90 seconds.

The script is `gen.sh` in this skill's base directory (shown when the skill loads), referred to below as `<skill-dir>`.

## Command

```bash
<skill-dir>/gen.sh -o <out.png> [options] "<prompt>"
```

| Option | Meaning |
|---|---|
| `-o PATH` | Output file (required). Put project assets inside the project; otherwise use a temp/scratch folder. |
| `-n N` | 1–4 variants → `out-1.png`, `out-2.png`, … |
| `-r FILE` | Reference image for style/composition (repeatable) |
| `-e FILE` | Image to edit — only what the prompt asks changes |
| `-t` | Transparent background |
| `-a square\|portrait\|landscape` | Aspect ratio |

Prints the saved absolute path(s). Never overwrites: an existing name gets a time suffix.
Give the Bash call a timeout of at least 300000 ms (600000 for `-n 3` or `-n 4`). For several different
images, run separate commands in parallel instead of describing them all in one prompt — parallel runs are safe.

## Workflow

1. Turn the request into a clear prompt: subject, style/medium, composition, lighting, palette,
   exact text in quotes, and what to avoid. Keep the user's specifics; add detail only when the ask is vague.
2. Run `gen.sh`.
3. **Look at the output image** and check it matches (subject, spelling of any text, framing). If it's off,
   rerun with one targeted prompt change, or use `-e` on the result for a small fix.
4. Report the saved path(s) and the final prompt. If the image is for a project, reference it from the code.

## Troubleshooting

- `codex CLI not found` → the user needs `npm i -g @openai/codex`.
- `Codex is not logged in` → the user runs `codex login` and signs in with ChatGPT.
- `No image was generated` → the ChatGPT plan's image limit may be used up, or the prompt was refused.
  Say so; don't retry in a loop.
- `-t` output can have semi-transparent blotches. Check it; if dirty, regenerate on a plain white background
  without `-t` and remove the background separately.
