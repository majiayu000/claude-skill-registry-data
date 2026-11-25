---
name: process-image
description: Resize, convert, rotate, flip, color-adjust, or inspect a local image file (JPEG/PNG/WebP/AVIF, or an SVG rendered to pixels) and make blur-up placeholders — thumbnails, avatars, hero images, fitting an image into a layout, converting between formats, orientation fixes, brightness/saturation tweaks, checking dimensions/size. Runs entirely offline via Bun's native image API, no network call and no fal.ai credit spent. Use whenever the user wants to resize, shrink, convert, re-encode, compress, rotate, mirror, brighten/desaturate an image they already have, needs an LQIP/blur-up placeholder, or needs a PNG/favicon/preview from an SVG logo — even if they just paste a path and say "make this smaller".
compatibility: Claude Code with Bun 1.4 or later. Offline; no API key.
---

# process-image

Wraps Bun's native `Bun.Image` API (statically linked libjpeg-turbo/spng/libwebp plus OS codecs — this is the "sharp" people mean when they say Bun has it built in, not the npm `sharp` package) behind one CLI: `${CLAUDE_SKILL_DIR}/scripts/process-image.ts`. Purely local — no network, no API key, safe to run freely.

```
bun ${CLAUDE_SKILL_DIR}/scripts/process-image.ts <command> ...
```

If the shell says `bun` isn't found, Bun isn't installed. Stop and ask the user to install it from
https://bun.com/docs/installation and restart Claude Code. Don't replace the script with other tools or
code of your own: the checks it runs before a paid call and on the result would be lost.

If you're about to generate a *new* image and just want it encoded a particular way, don't chain `generate` → `process-image convert/resize` — the `generate-image generate`/`edit` commands already take `--format` / `--output-quality` / `--max-width` and do it in one step. Reach for `process-image` for images that already exist on disk.

An `.svg` source works with every command: it is rendered to pixels first (with resvg, installed by
Bun on first use). `resize` renders it straight at the target width, so
`resize --source logo.svg --output favicon-64.png --width 64` gives a sharp favicon. Render an SVG
this way to look at it before showing it to the user. A preview isn't a deliverable, so it goes in
the project's work folder: `media-generation/` inside the project's own scratch folder if it has
one (`.scratch/`, `tmp/`), otherwise `.media-generation/` holding a `.gitignore` that contains `*`,
so git never sees it. Never `/tmp` or a folder next to the project.

For `rotate`, `flip` and `adjust`, the output format is inferred from the `--output` extension
(`.jpg`/`.jpeg`, `.png`, `.webp`, `.avif`, `.heic`; anything else is rejected); `--quality 1-100` (default 85) applies to any lossy format.

## info — inspect before deciding

```
process-image.ts info --source <path>
```

Prints format, dimensions, and file size. Run this first when you don't already know the source image's size — e.g. before picking a resize width or deciding whether a convert is even needed.

## resize

```
process-image.ts resize --source <path> --output <path> --width N [--height N] [--fit inside|fill] [--quality 1-100]
```

`--fit inside` (the default) preserves aspect ratio, shrinking to fit within the given width/height. `--fit fill` stretches to the exact dimensions, distorting the aspect ratio — only use it when the caller explicitly wants an exact box (e.g. a fixed avatar frame). Omit `--height` to derive it from the width at the source's aspect ratio.

## convert

```
process-image.ts convert --source <path> --output <path> --format jpeg|png|webp|avif|heic [--quality 1-100]
```

`webp` is the safe default for anything web-bound — good size/quality, transparency, universal support. `avif` is typically another 20–30% smaller and every current browser renders it, **but Bun encodes it through the OS codec**: impossible on Linux (nothing to install), on macOS only on Apple M3 or newer, on Windows only with the AV1 Video Extension. HEIC works on macOS and on Windows with the HEIF extension, never on Linux; reading AVIF/HEIC/TIFF sources has the same limits. The script says so when the machine can't do it — then just use `webp`. `--format` must agree with the `--output` extension. `png` is lossless with transparency (large), `jpeg` is smallest for photos but has no alpha, `heic` is for Apple-ecosystem deliverables, not the web. `--quality` (default 85) affects all lossy formats.

## rotate / flip — orientation fixes

```
process-image.ts rotate --source <path> --output <path> --degrees 90|180|270
process-image.ts flip   --source <path> --output <path> [--axis horizontal|vertical]
```

`rotate` turns clockwise. `flip --axis horizontal` (the default) mirrors left↔right; `vertical` turns it upside down. Mirroring is not safe for images containing text or recognizable logos — they'll read backwards.

## adjust — brightness / saturation

```
process-image.ts adjust --source <path> --output <path> [--brightness N] [--saturation N]
```

`--brightness` and `--saturation` are multipliers (`1.0` = unchanged, `0.5` = half, `1.3` = +30%). There is no hue rotation — Bun's image API doesn't support it. Typical uses: darken a hero image so overlay text stays readable (`--brightness 0.7`), desaturate a busy background (`--saturation 0.6`). At least one flag is required.

## placeholder — blur-up LQIP

```
process-image.ts placeholder --source <path>
```

Prints a tiny blurred `data:image/png;base64,…` URI (a few hundred bytes) to stdout. Put it in the `<img>`'s CSS `background` or a low-quality `src` that swaps to the real image on load — the standard blur-up loading pattern. Nothing is written to disk.
