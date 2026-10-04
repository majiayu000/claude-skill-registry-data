---
name: epub-export
description: >-
  Convert markdown or PDF content to EPUB and deliver to USB/MTP-connected ereaders (Tolino, Kobo, etc.). Covers the full pipeline including PDF extraction, artifact cleaning, CSS optimization, cover generation, and MTP deployment.
version: 2.0.0
author: Yuno
license: MIT
skill_type: class
lane: worker-flash
reasoning_effort: high
agent: Writer
routing_hint: |
  **Agent-Scope:** Long-form content, docs, proposals, copy. Off-scope: code, design, data modeling — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# epub-export

Export content to EPUB ebooks (from PDF or markdown), optimize for e-reader screens, then copy to an MTP-connected device. Used when the user wants a reading-ready document on their physical ereader (Tolino Vision 6, Kobo, PocketBook, etc.).

## Prerequisites

| Tool | Check | Purpose |
|------|-------|---------|
| `pandoc` | `which pandoc` | Markdown → EPUB conversion |
| `gio` / `gvfs` | `gio mount -l` | MTP mount/access to ereader |
| `pymupdf4llm` | `uv pip list \| grep pymupdf4llm` | PDF → Markdown extraction |

`pandoc` and `gio` are pre-installed on Ubuntu / Zorin OS. `pymupdf4llm` may need installing: `uv pip install pymupdf pymupdf4llm` (use `uv` on PEP 668 systems).

## Full Pipeline: PDF → EPUB → E-Reader

```

set -euo pipefail
PDF → pymupdf4llm → Raw Markdown → Clean → pandoc → EPUB → gio copy → E-Reader
```

### 1. Extract PDF to Markdown

```bash

set -euo pipefail
uv run python3 -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('input.pdf')
with open('/tmp/input.md', 'w') as f:
    f.write(md)
print(f'{len(md)} chars extracted')
"
```

### 2. Clean Markdown (remove PDF artifacts)

PDF-generated markdown contains layout debris: page numbers, running headers/footers, bold-from-asterisks on headings, and chapter-marker lines.

```python
import re

def clean_pdf_md(md: str) -> str:
    lines = md.split("\n")
    cleaned = []
    
    for line in lines:
        stripped = line.strip()
        
        # Remove "Seite X" / "Page X" standalone lines
        if re.match(r'^Seite \d+$', stripped):
            continue
        if re.match(r'^Page \d+$', stripped, re.IGNORECASE):
            continue
        
        # Remove running book-title footers ("**DMZ x GreyHack — E-Book Edition**")
        if re.match(r'^\*\*DMZ x GreyHack', stripped):
            continue
        
        # Remove repetitive "E-Book-freundliche" ad-style footer blocks
        if 'E-Book-freundliche Ausgabe' in stripped and 'ruhigerem Lesefluss' in stripped:
            continue
        
        # Remove standalone "**KAPITEL N**" / "**Kapitel N**" markers
        if re.match(r'^\*\*(?:KAPITEL|Kapitel)\s+\d+\*\*$', stripped):
            continue
        
        # Remove Placeholder for table of contents
        if stripped == '## Placeholder for table of contents':
            continue
        
        # Remove "Lesefunktion dieses Kapitels" heading + following content line
        if re.match(r'^## \*\*Lesefunktion dieses Kapitels\*\*', stripped):
            continue  # skip the heading; the next content line is redundant too
        
        # Clean bold-from-asterisks in headings: "## **Heading**" → "## Heading"
        h_match = re.match(r'^(#{1,6})\s+\*\*(.+?)\*\*\s*$', line)
        if h_match:
            level = h_match.group(1)
            text = h_match.group(2).strip()
            cleaned.append(f"{level} {text}")
            continue
        
        cleaned.append(line)
    
    # Collapse excessive blank lines
    text = "\n".join(cleaned)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text
```

set -euo pipefail
Also fix common PDF extraction typos with `.replace()` (e.g., `"Handbuc h" → "Handbuch"`).

### 3. Build Optimized EPUB with pandoc

```bash
pandoc /tmp/cleaned.md \
  --to epub3 \
  --metadata title="Book Title" \
  --metadata author="Author Name" \
  --metadata date="June 2026" \
  --metadata lang="de-DE" \
  --metadata identifier="my-book-20260623" \
  --metadata publisher="Publisher" \
  --metadata rights="CC BY-NC-SA 4.0" \
  --metadata description="Short description for library view" \
  --epub-cover-image=cover.svg \
  --css /path/to/ereader.css \
  --toc --toc-depth=2 \
  --split-level=1 \
  --number-sections \
  -o output.epub
```

set -euo pipefail
#### pandoc flag reference

| Flag | Purpose | Notes |
|------|---------|-------|
| `--to epub3` | Modern EPUB format | EPUB3 handles CSS better, reflow, metadata |
| `--css file.css` | Custom stylesheet | **NOT** `--epub-stylesheet` (removed in newer pandoc) |
| `--metadata` | Dublin Core / OPF metadata | Repeat for each key: title, author, date, lang, identifier, publisher, rights, description |
| `--epub-cover-image` | Cover image (SVG/PNG/JPG) | Path to image file for the library view |
| `--toc` | Generate NCX table of contents | |
| `--toc-depth=N` | How many heading levels in TOC | 2 is usually right (H1 + H2) |
| `--split-level=N` | Create chapter files at heading level N | 1 = per H1 (fewer, larger files), 2 = per H2 (more, smaller; better for 6" screens). Replaces deprecated `--epub-chapter-level`. |
| `--number-sections` | Auto-number headings | 1.1, 1.2, etc. |

**`--split-level` strategy for Tolino Vision 6:**
- `--split-level=1` → one HTML file per major section (H1). Works well for shorter documents (<50 pages) where chapter files are 3-8 pages each.
- `--split-level=2` → one file per H2. Produces more files, each 1-3 pages. Better for very long documents (>100 pages) where page-turn latency matters.

### 4. Generate a Cover SVG (when no image available)

Create a simple dark-theme SVG cover when the PDF has no embedded cover image:

```python
COVER_SVG = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800" width="600" height="800">
  <rect width="600" height="800" fill="#1a1a2e"/>
  <rect x="30" y="30" width="540" height="740" fill="none" stroke="#e94560" stroke-width="2" rx="5"/>
  <text x="300" y="250" text-anchor="middle" font-family="Georgia, serif" font-size="42" fill="#e94560" font-weight="bold">{TITLE}</text>
  <text x="300" y="310" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#ccc">{SUBTITLE}</text>
  <line x1="150" y1="340" x2="450" y2="340" stroke="#e94560" stroke-width="1"/>
  <text x="300" y="530" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="#888">Autor: {AUTHOR}</text>
  <text x="300" y="560" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#666">{DATE}</text>
</svg>'''
```

set -euo pipefail
Customize the fill color, stroke, font sizes, and layout per project. Save to a temp file and pass as `--epub-cover-image`.

### 5. Deploy to E-Reader via MTP / GVFS

**Preferred method — `gio copy` with MTP URI (works even when GVFS mount path is broken):**

```bash
# Find the device URI
gio mount -l | grep -i "tolino\|kobo\|ereader\|pocketbook"
# Example output: mtp:host=Rakuten_Kobo_Inc._tolino_vision_6/

# Copy the EPUB
gio copy output.epub \
  "mtp://Rakuten_Kobo_Inc._tolino_vision_6/Interner gemeinsamer Speicher/Books/YourFolder/"

# Verify
gio list "mtp://Rakuten_Kobo_Inc._tolino_vision_6/Interner gemeinsamer Speicher/Books/YourFolder/"
```

set -euo pipefail
**Alternative — GVFS filesystem path:**
```bash
MTP_MOUNT="/run/user/$(id -u)/gvfs/mtp:host=Rakuten_Kobo_Inc._tolino_vision_6"
cp output.epub "$MTP_MOUNT/Interner gemeinsamer Speicher/Books/"
```

set -euo pipefail
**Remove old files before copying fresh ones:**
```bash
gio remove "mtp://Vendor_Model/Books/old-file.epub"
```

set -euo pipefail
**Books directory names by locale:**

| Locale | Path |
|--------|------|
| German | `Interner gemeinsamer Speicher/Books/` |
| English | `Internal Storage/Books/` |
| French | `Stockage interne partagé/Books/` |
| Italian | `Memoria interna condivisa/Books/` |
| Spanish | `Almacenamiento interno compartido/Books/` |

## Tolino Vision 6 E-Reader Optimization

The Tolino Vision 6 has a 6" E-Ink Carta display at 1448×1072 (300 DPI). Key optimization points:

### CSS Principles for E-Ink

| Property | Value | Rationale |
|----------|-------|-----------|
| Font-family | Georgia, "Times New Roman", serif | Best readability on 300 DPI E-Ink |
| Line-height | 1.7 | Wide enough for screen reading |
| Hyphens | auto | Justified text needs hyphenation |
| Text-align | justify | Standard for German book typography |
| @page margins | 15-20px sides | Not too wide on a 6" screen |
| Body font-size | 1em (device default) | Let the user control with Tolino's slider |
| Code font | "Courier New", Courier, monospace | Break-long-lines by word-break |
| Code size | 0.8-0.85em | Smaller than body text for code blocks |
| Table borders | thin, clean (no background) | Readable on grayscale E-Ink |
| Body > h1:first-of-type | page-break-before: avoid | Prevents blank page before title |
| Links | color: #000, text-decoration: none | No purple visited links on E-Ink |

### Font strategy for E-Ink

- **Do NOT embed fonts** — the device's built-in font rendering is optimized for E-Ink
- **Do NOT use `@font-face`** — it slows down rendering and can cause reflow issues
- **Use `Georgia` as first choice** with `"Times New Roman", serif` fallback
- **Avoid thin/light font weights** — they wash out on E-Ink
- **Avoid colored backgrounds** — anything on non-white backgrounds looks muddy on grayscale E-Ink

### Splitting strategy

For the Tolino's 6" screen with default font size:
- **`--split-level=1`** produces chapter files of ~3-8 reader pages each — sweet spot
- **`--split-level=2`** produces files of ~1-3 pages each — fine but more navigation clicks
- Rationale: E-Ink page turns take ~0.5-1s per full redraw, so fewer turns = better UX

## Workflow: Markdown Source Only

If starting from existing markdown (not a PDF):

```bash
# Quick conversion with basic metadata
pandoc input.md --to epub3 --toc -o output.epub

# Full flags for production quality
pandoc input.md \
  --to epub3 \
  --metadata title="My Book" --metadata author="Me" \
  --css ereader.css \
  --toc --toc-depth=2 --split-level=1 \
  --number-sections \
  -o output.epub
```

## Common Sources

| Source | Command |
|--------|---------|
| PDF | pymupdf4llm → clean → pandoc (see full pipeline above) |
| MorphReader Briefing | `morphreader --no-cve-ids --days 3 \| pandoc ...` or save to file first |
| Any markdown output | Save to file → run pandoc |
| Daily briefing markdown | `~/scripts/morphreader-briefing.md` (generated by OS-cron at 7:50) |

## Pitfalls

- **`--epub-chapter-level` is deprecated** — use `--split-level` instead
- **`--epub-stylesheet` is deprecated** — use `--css` instead (newer pandoc versions removed the old flag)
- **`--epub-cover-image` cannot be an empty string** — pandoc errors with `cover-image: does not exist`. Omit the flag if no cover, or generate a simple SVG
- **MTP requires unlocked device** — the ereader must be awake and on its home screen. If copy hangs or fails, wake the device
- **E-reader library refresh is manual** — Tolino does NOT auto-scan. After copying, go to Library and pull down to refresh
- **MTP path can be fragile** — `cp` through GVFS paths sometimes hangs. Use `gio copy` with the mtp:// URI instead
- **`gio remove` is needed** — MTP doesn't support overwrite-on-copy. Delete old versions first
- **UTF-8 filenames** — MTP handles them fine, but avoid special characters (`?`, `*`, `<`, `>`) for maximum compatibility
- **Tolino uses filename as default title** — ensure `--metadata title=...` is set correctly
- **Cover thumbnail delay** — Tolino generates the cover thumbnail on first library view. Wait 5-10 seconds after opening the book

## References

- `references/tolino-vision-6.md` — Tolino-specific mount path, Books path, and quirks
- `references/tolino-vision-6-css.md` — Full CSS stylesheet optimized for Tolino Vision 6
- `templates/cover-template.svg` — Reusable SVG cover template