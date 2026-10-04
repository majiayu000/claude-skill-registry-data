---
name: icon
description: "Generate and convert icons. Use when creating SVGs, building sprite sheets, converting ICO/PNG/SVG, or generating favicon sets."
version: "3.4.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - icon
  - svg
  - favicon
  - sprite
  - design
---

# Icon

Generate, convert, and manage icons for web and app projects.

## Commands

### generate

Generate an SVG icon from a name and optional style parameters.

```bash
bash scripts/script.sh generate --name "arrow-right" --size 24 --color "#333" --output icons/
```

### sprite

Combine multiple SVG icons into a single SVG sprite sheet.

```bash
bash scripts/script.sh sprite --input icons/ --output sprite.svg --prefix "icon-"
```

### convert

Convert icons between ICO, PNG, and SVG formats.

```bash
bash scripts/script.sh convert --input icon.svg --format png --sizes "16,32,64"
```

### search

Search available icon names by keyword.

```bash
bash scripts/script.sh search --query "arrow" --style outline
```

### resize

Batch resize icons to specified dimensions.

```bash
bash scripts/script.sh resize --input icons/ --sizes "16,24,32,48" --output resized/
```

### favicon

Generate a full favicon set (ICO, PNG, Apple Touch, manifest) from a source image.

```bash
bash scripts/script.sh favicon --input logo.svg --output favicons/
```

## Output

- `generate`: SVG file written to output directory
- `sprite`: Single SVG sprite sheet with `<symbol>` elements
- `convert`: Converted files in target format and sizes
- `search`: List of matching icon names printed to stdout
- `resize`: Resized icon files in output directory
- `favicon`: favicon.ico, apple-touch-icon.png, android-chrome PNGs, site.webmanifest


## Requirements
- bash 4+

## Feedback

https://bytesagain.com/feedback/

---

Powered by BytesAgain | bytesagain.com
