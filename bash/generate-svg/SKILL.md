---
name: generate-svg
description: Generate true SVG vector graphics from a text prompt (Recraft V4.1) or convert an existing raster image to SVG (Recraft vectorize) via fal.ai — logos, icons, flat illustrations, brand marks, favicons, spot art that must stay sharp at any size. Use whenever the user asks for an SVG, a vector version of an image, a scalable logo/icon, or artwork destined for Figma/Illustrator — even if they don't say "fal.ai" or name a model. Prefer it over hand-writing SVG markup for anything that should look designed (a logo, brand mark, illustration); hand-write only simple geometric shapes, UI icons or diagrams the user wants as editable code. For raster images (photos, hero shots) use generate-image instead.
compatibility: Claude Code with Bun 1.4 or later and a fal.ai API key in FAL_KEY.
---

# generate-svg

Wraps fal.ai's Recraft vector endpoints behind one CLI: `${CLAUDE_SKILL_DIR}/scripts/generate-svg.ts`.
Requires a fal.ai key in `FAL_KEY` (same key as the other generation skills) — if it's missing the
script exits with a clear error, ask the user to export it in their shell — never ask them to paste the key into the chat.

Run it with Bash, e.g.:

```
bun ${CLAUDE_SKILL_DIR}/scripts/generate-svg.ts generate --prompt "..." --output ./logo.svg
```

If the shell says `bun` isn't found, Bun isn't installed. Stop and ask the user to install it from
https://bun.com/docs/installation and restart Claude Code. Don't replace the script with other tools or
code of your own: the checks it runs before a paid call and on the result would be lost.

Output is a real SVG with editable paths and layers (not a raster in an `.svg` wrapper) — it drops
straight into HTML via `<img>`/inline `<svg>`, and into Figma or Illustrator for hand-editing.

## generate — text to SVG

```
generate-svg.ts generate --prompt "<description>" --output <path>.svg
  [--model standard|pro] [--size square_hd|square|portrait_4_3|portrait_16_9|landscape_4_3|landscape_16_9]
  [--width N --height N] [--colors "#RRGGBB,#RRGGBB,..."] [--background "#RRGGBB"]
```

| Model | Cost | Best for |
|---|---|---|
| `standard` (default, Recraft V4.1) | \$0.08/image | logos, icons, flat illustrations, favicons — nearly everything |
| `pro` (Recraft V4.1 Pro) | \$0.30/image | large-format poster art, complex multi-object scenes with fine detail |

`--colors` pins the palette to brand colors and `--background` sets the backdrop — pass the site's
actual hex values instead of describing colors in the prompt; it's far more reliable. `--width`/
`--height` take exact pixel values as the design size (the SVG itself scales freely).

Prompt for **flat, graphic** subject matter: "minimal line icon of…", "flat geometric illustration
of…", "logo mark, two colors". Photorealism prompts produce a bad fit for vector output — that's
`generate-image` territory.

## vectorize — raster image to SVG (\$0.01/image)

```
generate-svg.ts vectorize (--source <path> | --image-url <url>) --output <path>.svg
```

Converts an existing PNG/JPEG/WebP to SVG paths. Use it to make a raster logo scalable, or to turn
a `generate-image` generation into editable vector art (generate flat artwork cheaply with `gpt-image-2.5 --quality low`,
then vectorize for \$0.01 — a useful combo when `generate` above doesn't nail the composition).

**Only vectorize flat/graphic content.** Photos and smooth gradients trace into megabyte-scale SVGs
that are worse than the original raster in every way — verified: a 100KB gradient PNG came back as
a 1.5MB SVG. If the source is photographic, keep it raster.

Input limits (handled automatically for `--source`): vectorize wants each side over 256px and under
4096px, under 16MP and under 5MB. Oversized sources are downscaled/re-encoded locally before upload,
and the *final* file is checked — a very wide banner that would drop under 256px on its short side
after downscaling is rejected with an explanation (crop it first), as are sources that are simply
too small, since upscaling adds no detail. Pass exactly one of `--source` or `--image-url`.

The script checks that the download really is an SVG. If it contains scripts, event handlers or
external links it is not saved and the command fails — generate again with a different prompt.

To look at the result, or to make a PNG, favicon or social image from it, use the process-image skill:
it renders `.svg` sources (`process-image.ts resize --source logo.svg --output logo.png --width 512`).

`generate` output carries a C2PA provenance manifest in its `<metadata>` element (it marks the file as
AI-generated) that can be two thirds of a small logo's bytes. Keep it by default; when the user wants
the SVG inlined or as small as possible, removing that `<metadata>` element doesn't change the picture.

**A paid result is never lost.** As soon as fal.ai accepts a job the script prints its request ID and a ready `resume --model … --request-id … --output …` command on stderr. If the download fails or the run is interrupted, run that command — it fetches the already-paid result. Don't rerun the original command: that generates (and bills) again.


## Cost awareness

Flat per-image pricing, billed to the user's fal.ai key: `generate` \$0.08 (`--model pro` \$0.30),
`vectorize` \$0.01. Before a batch (several icons, logo variations), state the total estimate.
For a matching icon set, generate them in one style family: same prompt skeleton, same `--colors`.
