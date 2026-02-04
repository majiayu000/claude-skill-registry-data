---
name: front-matter-image-converter
description: Convert local images referenced in Hugo front matter to modern formats (WebP) and update front matter using ci/convert_page_images.py.
---

# Front Matter Image Converter

## When to use this skill

Use this skill when you need to:

- Ensure images referenced in tool front matter (page bundle resources, hero images, etc.) use modern formats where possible.
- Convert legacy formats (PNG/JPEG/GIF) to WebP and update front matter paths in `index.md`.
- Normalize tool icons or other page resources so the site prefers modern image formats.

## What this does

The script `ci/convert_page_images.py` scans `index.md` front matter, finds local image paths, converts eligible files to `.webp`, updates the YAML front matter to point at the new files, and deletes the originals after successful conversion.

Supported/behavior notes:

- Converts `.png`, `.jpg`, `.jpeg`, `.gif` to `.webp`.
- Skips `.webp` inputs.
- Treats `.svg` as non-convertible (left as-is).
- `.avif` is recognized but conversion depends on Pillow build support; if conversion fails, keep the original and report the error.
- Only local file paths are processed (no URLs or data URIs).

## How to run

Process all tools under `content/` (default root):

```bash
uv run ci/convert_page_images.py
```

Process a specific subtree:

```bash
uv run ci/convert_page_images.py --root content/tools
```

Process a single page bundle index:

```bash
uv run ci/convert_page_images.py --file content/tools/html/tool-slug/index.md
```

Adjust WebP quality (1-100, default 80):

```bash
uv run ci/convert_page_images.py --quality 85
```

## Post-run checks

- Review `git status` to confirm which images were converted and removed.
- Open the updated `index.md` front matter and ensure references now point to `.webp` files.
- Verify any non-convertible images (like `.svg`) remain intact.

## Troubleshooting

- If a conversion fails for `.avif`, leave the original in place and consider keeping it (already modern) or replacing it with WebP manually.
- If front matter YAML fails to parse, fix the YAML and rerun the script.
