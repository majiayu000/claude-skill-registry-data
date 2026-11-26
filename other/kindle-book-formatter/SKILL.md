---
vendored_from: https://github.com/nikmcfly/kindle-book-skill
name: kindle-book-formatter
description: >
  Convert markdown (.md) or plain text (.txt) files into Amazon KDP-ready book files:
  EPUB3 for Kindle digital publishing and a print-ready PDF for KDP paperback (6×9",
  5×8", or custom trim). Use this skill whenever the user wants to: publish a book on
  Amazon Kindle, create an ebook from markdown, generate a KDP-ready EPUB or print PDF,
  self-publish a book, convert a manuscript to Kindle format, or make digital + print
  book files. Trigger even for partial phrases like "make it a Kindle book", "publish
  this as an ebook", "KDP files", "format my book for Amazon", or "I want to sell this
  on Kindle".
triggers:
  - kindle-book-formatter
  - kindle
  - book
  - formatter

---

# Kindle Book Skill

Converts MD/TXT manuscripts → **EPUB3** (Kindle digital) + **print-ready PDF** (KDP paperback) using pandoc + XeLaTeX.

## Quick Start

1. Read the user's source file(s) from `/mnt/user-data/uploads/`
2. Extract or ask for book metadata (see Metadata section)
3. Run `scripts/build_kindle.py` with appropriate flags
4. Present both output files to the user

## Prerequisites Check

```bash
which pandoc xelatex python3
```

All three must be present. They are pre-installed in Claude's container.

---

## Step 1: Extract Metadata

Parse YAML frontmatter from the MD file if present. If missing, ask the user for:

| Field | Required | Default |
|-------|----------|---------|
| `title` | ✅ | — |
| `author` | ✅ | — |
| `language` | ✅ | `en-US` |
| `publisher` | optional | — |
| `rights` | optional | — |
| `description` | optional | — |
| `trim_size` | optional | `6x9` |
| `cover_image` | optional | none |

**Supported trim sizes**: `5x8`, `6x9` (most popular), `8.5x11`

**YAML frontmatter format** (tell user to add to top of MD file):
```yaml
---
title: "My Book Title"
author: "Author Name"
language: en-US
publisher: "Publisher Name"
rights: "© 2025 Author Name. All rights reserved."
description: "One-line book description for metadata."
trim_size: "6x9"
cover_image: "cover.jpg"   # optional, path relative to manuscript
---
```

---

## Step 2: Prepare the Manuscript

### Heading Structure (critical for chapter splitting)
- `# Title` → Book title (optional, can be in frontmatter)
- `# Chapter Name` → Each `#` heading becomes a new chapter in EPUB
- `## Section` → Sub-sections
- `### Sub-section` → Sub-sub-sections

### Markdown Features Fully Supported
- Bold `**text**`, italic `*text*`
- Block quotes `> text`
- Ordered and unordered lists
- Horizontal rules `---` (scene breaks)
- Images `![alt](path.jpg)`
- Tables

### Common Issues to Fix Before Building
- Remove any existing page numbers or headers from the source
- Ensure each chapter starts with a `#` heading (not `##`)
- Images referenced must exist relative to the source file

---

## Step 3: Build the Files

Run the build script:

```bash
python3 /path/to/skill/scripts/build_kindle.py \
  --input /mnt/user-data/uploads/manuscript.md \
  --output /mnt/user-data/outputs/ \
  --title "Book Title" \
  --author "Author Name" \
  --language en-US \
  --trim 6x9
```

**Optional flags:**
```bash
  --cover /mnt/user-data/uploads/cover.jpg   # EPUB cover image
  --publisher "Publisher Name"
  --rights "© 2025 Author"
  --description "Book tagline"
  --epub-only     # skip PDF
  --pdf-only      # skip EPUB
  --font-size 12  # body font size in pt (default: 12)
```

The script outputs:
- `<slug>_digital.epub` — upload to KDP eBook section
- `<slug>_print.pdf` — upload to KDP paperback interior section

**Print PDF overflow prevention** (built into the script):
- Long code block lines are auto-wrapped to fit the trim size
- Tables get proportional column widths via a lua filter
- Inline monospace (`code`) text can break at hyphens/slashes
- URLs break at any character via xurl
- Global `\sloppy` + `\emergencystretch` prevents text overflow

---

## Step 4: Verify Outputs

After building, tell the user:

**For digital EPUB:**
- Upload to KDP → Kindle eBooks → Manuscript upload
- KDP accepts EPUB3 directly
- Preview in KDP's online previewer before publishing

**For print PDF:**
- Upload to KDP → Paperback → Manuscript upload
- Margins are set for the selected trim size
- Page numbers are in the header (outside edge)
- Bleed is NOT included (no full-bleed images)
- Confirm page count matches KDP's estimate before ordering proof

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `lmodern.sty not found` | Script uses custom template that bypasses lmodern — use `build_kindle.py`, not raw pandoc |
| `openBinaryFile: does not exist` | YAML `cover-image:` field is empty — remove it or set a valid path |
| Chapters not splitting in EPUB | Each chapter must start with `#` (H1), not `##` |
| Images missing in EPUB | Image paths must be relative to manuscript file location |
| PDF text too small | Use `--font-size 13` or `--font-size 14` |
| KDP "text outside margins" on tables | The build script uses a lua filter to auto-assign column widths — this should be automatic. If a specific table still overflows, shorten the cell content (especially inline code) |
| KDP "text outside margins" on code blocks | The build script wraps code lines to fit the trim size. If issues persist, check for very long strings without spaces (URLs, file paths) and manually add line breaks in the markdown |
| KDP "text outside margins" on inline code | The LaTeX template allows monospace to break at hyphens. For extremely long inline code strings, break them with spaces in the markdown |
| KDP "removed non-printable markup" | Normal — KDP strips hyperlinks from print PDFs since they're not clickable on paper. No action needed |

---

## KDP Upload Checklist (tell user)

**eBook:**
- [ ] EPUB3 file uploaded
- [ ] Cover image: JPG/TIFF, 2560×1600px minimum, 1.6:1 ratio
- [ ] Preview on KDP previewer before publishing
- [ ] Set DRM preference
- [ ] Set pricing and territories

**Paperback:**
- [ ] Interior PDF uploaded (this script's output)
- [ ] Cover: use KDP Cover Calculator for spine width → upload separate PDF cover
- [ ] Select matching trim size in KDP settings
- [ ] Order a proof copy before going live

---

## References

- `references/trim-sizes.md` — KDP trim size margin specs for all sizes
- `assets/print-template.tex` — LaTeX template used for print PDF
- `assets/epub-styles.css` — CSS injected into EPUB
- `scripts/build_kindle.py` — Main build script

Read `references/trim-sizes.md` if the user requests a non-standard trim size.
