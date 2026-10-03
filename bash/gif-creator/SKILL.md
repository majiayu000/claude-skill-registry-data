---
name: gif-creator
description: >-
  Generate animated GIFs with Pillow (palette, binary transparency, toss/lift
  animations, frame folders). Use when the user asks to create a GIF, animate a
  logo, convert frames to GIF, inspect a GIF, or invokes /gif-creator_*.
disable-model-invocation: true
---

### TO COPY

# gif-creator

Per-workspace registration slice. No credentials.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
```

##### END TO COPY

# gif-creator

Generate animated GIFs with **Pillow** (GIF87a/GIF89a, LZW, max 256 colors, one transparent palette index). Write and run Pillow directly — no CLI wrapper. Index: [`references/pillow-gif-guide.md`](references/pillow-gif-guide.md).

## When to use

Trigger phrases: "create a GIF", "animate this logo", "make a toss GIF", "frames to GIF", "GIF transparency", `/gif-creator_toss`, `/gif-creator_from-frames`, `/gif-creator_info`.

Library: `~/.meta-skills/skills/design/gif-creator/`. Python: `~/.meta-skills/.venv/bin/python`.

## Slash commands

Read the linked file, then write/run Pillow code.

| Slash | Do | Read |
|-------|-----|------|
| `/gif-creator_toss` | Logo rises → spins → falls (transparent GIF) | [`references/toss.md`](references/toss.md) |
| `/gif-creator_from-frames` | GIF from images in a directory (sorted by name) | [`references/pipeline.md`](references/pipeline.md) |
| `/gif-creator_info` | Print GIF metadata / frame durations | [`references/read.md`](references/read.md) |
| `/gif-creator_install-deps` | Install Pillow into the shared venv | `~/.meta-skills/install.sh pip init .` from the library dir |

## How to run

1. First run: `cd ~/.meta-skills/skills/design/gif-creator && ~/.meta-skills/install.sh pip init .`
2. Write a short Python script from the reference; run it with `~/.meta-skills/.venv/bin/python`.

## Critical GIF rules (Pillow)

- GIF has **no partial alpha** — one palette index is fully transparent.
- Save with `save_all=True`, `append_images=frames[1:]`, `loop=0`, `disposal=2`, `optimize=False` for transparent anims.
- Prefer a **solid black** shadow (size varies), not gray (looks white on dark UIs).
- Compose in `RGBA`, convert to mode `P` before save ([`references/pipeline.md`](references/pipeline.md)).
- Details: [`references/transparency.md`](references/transparency.md), [`references/save.md`](references/save.md).

## Notes

- Confirm output path with the user before overwriting an existing file.
- No credentials required for this skill.
- Prefer WebP/APNG only when the user needs true partial transparency ([`references/alternatives.md`](references/alternatives.md)).
