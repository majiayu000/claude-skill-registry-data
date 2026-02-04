---
name: markdown-to-standalone-html
description: Convert Markdown documents (*.md files) to self-contained HTML files with embedded images. Use when you need a portable, offline-friendly single HTML file from Markdown—ideal for blog posts, essays, reports, or any content that should work without external dependencies.
---

# Markdown → Standalone HTML (Embedded Images)

## Overview

Convert any Markdown file into a **single self-contained HTML document** with all images embedded as base64 data URIs. No external hosting required—the output is a single `.html` file that works offline.

## Requirements

- `pandoc` — Markdown → HTML conversion
- `ruby` — Script execution

Both must be on your `PATH`. The script checks and exits with a clear error if missing.

## Workflow

1. **Prepare your Markdown** — Any `.md` file with images (local paths or public URLs)
2. **Run the conversion script** with the Markdown file, title, and output path
3. **Resolve images** — If images can't be found locally, you'll be prompted for a file path or URL
4. **Get your HTML** — A single `.html` file with all images embedded, ready to share

## Image Resolution

For each image in your Markdown:

1. **Relative path** — Resolved relative to the Markdown file's directory
2. **Absolute path** — Used as-is if it exists
3. **Public URL** (`http://` or `https://`) — Downloaded to temp directory, embedded, then cleaned up
4. **Unresolved** — You're prompted to provide a local file path or URL

All images in the final HTML are base64-encoded and embedded directly—no external dependencies.

## Limitations

- Only rewrites `<img src="">` tags (not CSS `background-image` URLs)
- Does not guess missing images; prompts interactively instead
- Untrusted SVG can contain scripts—review embedded SVG carefully

## Script Reference

**Script:** `scripts/markdown_to_standalone_html.rb`

**Usage:**

```bash
ruby .github/skills/markdown-to-standalone-html/scripts/markdown_to_standalone_html.rb \
  /path/to/post.md \
  --title "Your Post Title" \
  --template .github/skills/markdown-to-standalone-html/assets/template.html \
  --out /path/to/output.html
```

**Arguments:**

- `markdown` — Path to your Markdown file (required)
- `--title` — Title for the HTML document (required; displayed in browser tab and header)
- `--template` — Path to the HTML template (required; use the provided `assets/template.html`)
- `--out` — Path where the final HTML will be written (required)
