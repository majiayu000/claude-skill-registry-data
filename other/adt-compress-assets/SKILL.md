---
name: compress-assets
description: Losslessly compress PNG and SVG assets in place and generate .webp siblings for every raster image. Use when the user asks to "compress assets", "optimize images", "shrink the assets folder", or "convert to webp". Runs a deterministic pipeline via oxipng + svgo + cwebp + ImageMagick.
triggers:
  - "compress assets"
  - "optimize images"
  - "shrink the assets folder"
  - "convert to webp"
  - "optimize image sizes"
---

# compress-assets

Shrink a repo's image assets without visible quality loss and emit modern `.webp` siblings so `<picture>` tags can serve them to supporting browsers.

## When to use

- "compress the assets", "optimize images", "convert to webp", "shrink the repo"
- Before a release when the repo has grown over time
- After dropping in designer-provided PNG/SVG/JPG that weren't pre-optimized

## Pipeline

Per file, by extension:

| Source | Tool | Flags | Output |
|---|---|---|---|
| `*.png` | `oxipng` | `-o max --strip safe` | in-place (lossless, reverts if output grows) |
| `*.png` | `cwebp` | `-q 85 -m 6 -mt` | `<name>.webp` (kept only if smaller than source) |
| `*.svg` | `svgo` | `--multipass` | in-place |
| `*.jpg` / `*.jpeg` | `magick` | `-strip -interlace Plane -sampling-factor 4:2:0 -quality 85` | in-place (kept only if smaller) |
| `*.jpg` / `*.jpeg` | `cwebp` | `-q 85 -m 6 -mt` | `<name>.webp` (kept only if smaller than source) |
| `*.webp`, `*.gif`, `*.pbm` | — | kept as-is | — |
| `.DS_Store` | `rm` | — | deleted |

## Preconditions

```bash
brew install oxipng svgo pngquant webp imagemagick
```

Verify: `which oxipng svgo cwebp magick`.

## Usage

Run the bundled script (ship one copy per repo at `scripts/compress-assets.sh`):

```bash
./scripts/compress-assets.sh assets   # default dir is "assets"
```

The script prints before/after bytes per file and a summary block with per-type totals and total WEBP bytes added.

## Consuming the .webp siblings

Replace `<img src="foo.png">` with a `<picture>` fallback so PNG stays intact:

```html
<picture>
  <source srcset="assets/foo.webp" type="image/webp" />
  <img src="assets/foo.png" alt="..." width="720" />
</picture>
```

GitHub's README renderer supports this — modern browsers get webp, everyone else falls back to the already-optimized PNG.

## Don'ts

- Do **not** run `pngquant` in the default pipeline — it's lossy and not needed when oxipng gets 20–40 % for free. Only enable it if oxipng's output still exceeds a size budget.
- Do **not** delete original PNG/JPG files when emitting webp — keep both so `<picture>` fallback works.
- Do **not** recompress animated GIFs with this pipeline; they need `gif2webp` or `ffmpeg` instead.
- Do **not** run on `node_modules/`, build output, or committed binary bitmaps (`.pbm`) meant for pipelines.

## Expected gains (indicative)

- PNG: 20–45 % size reduction (oxipng strip + max level)
- SVG: 5–30 % (whitespace + default plugins)
- JPG: 25–50 % when source was saved unoptimized
- WEBP siblings: 60–90 % smaller than source PNG/JPG

## Related

- `optimize-context` — unrelated, for token budget not byte budget
- `dev-assets-sync` — syncs Claude config assets, not repo images
