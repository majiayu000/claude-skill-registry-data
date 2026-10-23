---
name: image-gen
description: >-
  Generate or edit marketing images with OpenAI gpt-image-2 through a bundled stdlib-only CLI — blog covers, landing-page illustrations, ad visuals, social graphics, product mockups, inpainting and multi-image compositions — choosing quality (low / medium / high) by whether the user needs drafts or a final asset, and checking every rendered word. Use whenever someone asks to create, draw, render, edit or inpaint an image. Triggers: "generate an image", "make a cover", "illustration for the landing", "edit this picture", "inpaint".
---

# Image generation — gpt-image-2

`scripts/img.py` wraps OpenAI's image API. Python stdlib only, nothing to install. Default model `gpt-image-2`; OpenAI now recommends the GPT Image 2.5 models for new work (`--model gpt-image-2.5-flare`, or set `IMG_MODEL`) — same per-token price, plus `xhigh` and `max` quality. Try one on a draft before switching a whole project.

**Key:** `OPENAI_API_KEY`, from the environment or `~/.config/marketing-agent-kit/.env`. Setup: `connections/openai-images-api.md`, or run the `connect` skill.

```bash
IMG="python3 ${CLAUDE_SKILL_DIR}/scripts/img.py"
$IMG "a watercolor cat on a windowsill" -q low -o drafts/cat.png
$IMG edit "make it nighttime" -i photo.png -o out.png
$IMG edit "fill the masked area with sky" -i photo.png -m mask.png -o out.png
$IMG edit "compose these two into one scene" -i a.png -i b.png -o combined.png
```

`img.py <prompt>` without a subcommand means `generate`.

## Quality is the main cost lever

The default is `high`. Quality changes the price roughly 35×, so downgrade on purpose for exploration. Approximate prices for 1024×1024 (OpenAI pricing, autumn 2026; landscape 1536×1024 is slightly cheaper):

| `-q` | ~price | Use for |
|---|---|---|
| `low` | ~$0.006 | brainstorming many variants, mood boards, "show me 5 ideas" |
| `medium` | ~$0.053 | working drafts, "is this the right direction?" |
| `high` | ~$0.211 | final assets that will be published or shown (default) |

**Rule:** more than three images of one concept for the user to pick from → `low` or `medium`. Re-render the chosen one at `high`. Say it out loud: "Rendering 4 drafts at low quality — pick one and I'll re-render it at high."

## Flags

- `-o PATH` — output file (default `img-<timestamp>.png` in the current folder). With `-n > 1`: `name-1.png`, `name-2.png`, …
- `-s SIZE` — `auto` (default) | `1024x1024` | `1536x1024` (landscape) | `1024x1536` (portrait) | other sizes: edges in multiples of 16, up to 3840 px, aspect ratio up to 3:1 (above 2560×1440 is experimental).
- `-f png|jpeg|webp`, `--compression 0-100` (jpeg / webp only).
- `-n N` — variants in one call.
- `--background opaque|transparent|auto` — for a transparent PNG use a GPT Image 2.5 model: `--model gpt-image-2.5-flare --background transparent -f png`. `gpt-image-2` rejects `transparent` with HTTP 400 (tested 2026-10-01, although the API reference calls it a preview).
- `--moderation low|auto` — `low` only when the user asks and the content is benign.
- `--model` — default `gpt-image-2`; pin a dated snapshot when the user needs reproducibility.

Edits: without `-m` the whole image is rewritten from the prompt and inputs. With `-m mask.png` only the transparent area of the mask changes (the mask needs an alpha channel and the same size and format as the input, under 50 MB).

New OpenAI accounts may need **API Organization Verification** before GPT Image models work, and the lowest usage tier is limited to about 5 images per minute. Several `-i` flags compose several references into one image.

## Art direction rules for marketing images

Read `references/art-direction.md` before writing a prompt for anything that will be published. The core:

- **The picture illustrates the actual content**, literally. A generic flat-lay of blurred papers next to a list of bonuses is filler; the same documents with their real short titles on them is an illustration.
- **At most two pieces of text in an image**, short ones, and **check every letter** of every rendered word before showing it. Misspelled text in a generated image is the most common reason it gets rejected.
- **A metaphor has to be literally true** to what the copy says. If it isn't, use the product itself.

## After generating

- Print the absolute output path.
- If the project keeps images in a folder (`assets/`, `public/images/`), generate there.
- Look at the result yourself before presenting it: text spelling, extra fingers, cut-off objects, wrong brand colours.

## Adapt it

- Add your brand to `references/art-direction.md`: palette (hex codes), what your product UI looks like, two or three reference images you like and why. Prompts that quote these come out on-brand.
