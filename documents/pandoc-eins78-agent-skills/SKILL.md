---
name: pandoc
description: >-
  Use when converting documents between formats — HTML, Markdown, DOCX, PDF,
  LaTeX, EPUB, reStructuredText, Org, JIRA, CSV, Jupyter notebooks, slides,
  and 60+ others. Triggers: convert file, export to PDF, make a PDF, print
  to PDF, printable PDF, A4 print, fold-to-A5 booklet, turn this into
  markdown, HTML to markdown, DOCX to markdown, markdown to DOCX, generate
  slides, create EPUB, format conversion, pandoc, document conversion.
  Always prefer pandoc over ad-hoc conversion scripts.
globs: []
compatibility: claude-code, cursor
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.4.0"
---

# Pandoc

Universal document converter. Reader → AST → Writer pipeline with 60+ input and 80+ output formats. Prefer pandoc over writing custom conversion scripts — one command replaces most python-docx, beautifulsoup4, or markdown library usage.

## Quick Reference

| Flag | Purpose |
|------|---------|
| `-f FORMAT` | Input format (auto-detected from file extension) |
| `-t FORMAT` | Output format (auto-detected from extension) |
| `-o FILE` | Output file (stdout if omitted) |
| `-s` | Standalone — complete document with header/footer |
| `--wrap=none` | Don't rewrap lines (preserve original line breaks) |
| `--extract-media=DIR` | Extract images from DOCX/EPUB/ODT |
| `--toc` | Generate table of contents |
| `--number-sections` | Number section headings |
| `--pdf-engine=ENGINE` | PDF backend (default: pdflatex) |
| `--reference-doc=FILE` | Style template for DOCX/ODT/PPTX output |
| `--template=FILE` | Custom output template |
| `--embed-resources` | Embed images/CSS inline (HTML) |
| `-V KEY=VALUE` | Set template variable |
| `-L SCRIPT` | Apply Lua filter |
| `--shift-heading-level-by=N` | Adjust heading levels |
| `--columns=N` | Line wrap width (default 72) |

## Common Recipes

### HTML → Markdown

```bash
pandoc -f html -t gfm -o output.md input.html
pandoc -f html -t gfm --wrap=none https://example.com/page  # from URL
```

### Markdown → HTML

```bash
pandoc -s -o output.html input.md                    # standalone page
pandoc -s --toc --css=style.css -o output.html input.md  # with TOC + CSS
pandoc -t html input.md                              # fragment only (no <head>)
```

### DOCX → Markdown

```bash
pandoc --extract-media=media/ --wrap=none -o output.md input.docx
```

### Markdown → DOCX

```bash
pandoc -o output.docx input.md
pandoc --reference-doc=template.docx -o output.docx input.md  # styled
```

### Markdown → PDF

Requires a LaTeX engine (or alternative). See `${CLAUDE_SKILL_DIR}/references/pandoc-install.md` for setup.

```bash
pandoc -o output.pdf input.md                           # default (pdflatex)
pandoc --pdf-engine=xelatex -o output.pdf input.md      # Unicode/custom fonts
pandoc --pdf-engine=typst -o output.pdf input.md        # lightweight, no LaTeX
pandoc --pdf-engine=weasyprint -t html -o output.pdf input.md  # via HTML/CSS
```

### Compact A4 print PDF (Marked-style, with Japanese + emoji)

For printable docs that match the look of Marked 2's GitHub/Swiss styles —
9pt body, bold heading hierarchy, tight A4 margins, full Unicode + emoji
support via Apple system font fallback. Uses pandoc → HTML → headless Chrome;
no LaTeX needed.

```bash
"${CLAUDE_SKILL_DIR}/scripts/md2pdf-print.sh" input.md output.pdf
```

The wrapper:

1. Pipes markdown through pandoc with `--embed-resources` and the bundled
   `themes/marked-print.css`.
2. Renders with `chrome --headless=new --print-to-pdf`.

Why not pandoc's own PDF engines? `xelatex`/`typst`/`weasyprint` all need
extra fonts to render Japanese + emoji together. Headless Chrome already
has Apple's full font stack and emoji color font available, so glyph
fallback "just works" for any script.

Why not Marked 2's own PDF export? On macOS 26.3.1, Marked's "Export PDF"
clips ~5–10pt off the left edge of every page in all styles. This pipeline
bypasses the underlying Quartz PDFContext bug entirely.

Trade-off: output PDFs are ~4× larger than LaTeX output because Chrome
embeds font subsets. Acceptable for one-shot print; not ideal for
distribution-sized PDFs. Page count and density match Marked 2 closely,
so it works well for booklet folding (e.g., A4 fold-to-A5).

Long lines in fenced code blocks wrap at the page edge (CSS sets
`white-space: pre-wrap; overflow-wrap: anywhere`) so they don't get
silently clipped. If you'd rather keep lines unbroken, break them in
the source.

Pandoc has no Chrome `--pdf-engine` (as of 3.9). Even if one ships
later, this wrapper still gives explicit control over headless flags
and the print stylesheet, which is the reason to keep it.

### Jupyter Notebook ↔ Markdown

```bash
pandoc -o output.md notebook.ipynb                    # notebook → markdown
pandoc -o output.ipynb input.md                       # markdown → notebook
```

### Markdown → Slides

```bash
pandoc -t revealjs -s -o slides.html input.md         # reveal.js
pandoc -o slides.pptx input.md                        # PowerPoint
pandoc -t beamer -o slides.pdf input.md               # LaTeX Beamer
```

### EPUB

```bash
pandoc -o book.epub chapter1.md chapter2.md metadata.yaml
```

### Markdown → Kindle EPUB

For markdown destined for an e-reader — reflowable text, adjustable font size,
and a working table of contents. Produce EPUB, not PDF: a PDF page is a fixed
canvas and only zooms/pans on a 6" screen, while Send-to-Kindle converts EPUB
into the device's own reflowable format on delivery.

```bash
"${CLAUDE_SKILL_DIR}/scripts/md2kindle-epub.sh" -o out.epub input.md
"${CLAUDE_SKILL_DIR}/scripts/md2kindle-epub.sh" -o out.epub part1.md part2.md --title "Report"
"${CLAUDE_SKILL_DIR}/scripts/md2kindle-epub.sh" -o out.epub ballot.md --raw-checkboxes
```

The wrapper sets `--toc --toc-depth=3 --split-level=2` (a real table of
contents; chapters split at each `##` so no single internal file gets huge)
and disables the `task_lists` extension by default, so GFM checkboxes stay
literal `[ ]` / `[x]` text instead of HTML `<input type="checkbox">` elements.
Plain text is guaranteed to survive a server-side ebook conversion; form
elements are not. `--raw-checkboxes` restores native task-list HTML.

Getting the file onto a device is a separate concern — see the
`send-to-kindle` skill for delivery routes, addressing, and size limits.

### Man page → Markdown

```bash
man pandoc | pandoc -f man -t gfm --wrap=none
```

### Batch conversion

```bash
for f in *.docx; do pandoc --extract-media=media/ -o "${f%.docx}.md" "$f"; done
```

## Format Detection

Pandoc auto-detects formats from file extensions. Specify `-f`/`-t` explicitly when:

- Reading from stdin or writing to stdout
- Extension is ambiguous (e.g., `.txt` → defaults to markdown)
- You need a specific variant (gfm vs markdown vs commonmark)

### Markdown Variants

| Format | Use for |
|--------|---------|
| `gfm` | GitHub — tables, task lists, strikethrough, autolinks |
| `commonmark` | Strict CommonMark spec |
| `commonmark_x` | CommonMark + pandoc extensions |
| `markdown` | Pandoc's Markdown — most features, default |
| `markdown_strict` | Original Gruber Markdown — minimal |

### Listing formats

```bash
pandoc --list-input-formats
pandoc --list-output-formats
pandoc --list-extensions=gfm          # extensions for a specific format
```

## Standalone vs Fragment

| Mode | Flag | Output | Use when |
|------|------|--------|----------|
| Fragment | (default) | Body content only | Embedding in another document |
| Standalone | `-s` | Complete document with headers | Creating a valid file (HTML, LaTeX, etc.) |

Always use `-s` for HTML files, LaTeX documents, and slide decks. DOCX/PDF/EPUB are always standalone.

## When to Use Pandoc vs Other Tools

| Task | Tool | Why |
|------|------|-----|
| Document format conversion | **pandoc** | Built for this — one command |
| Clean HTML → Markdown | **pandoc** | Handles structure well |
| Complex web scraping | Dedicated scraper | Pandoc needs clean HTML input |
| PDF text extraction | pdftotext, pdfplumber | Pandoc cannot read PDF |
| Image format conversion | ImageMagick, sips | Not pandoc's domain |
| CSV/JSON data processing | jq, csvkit, code | Pandoc reads CSV/JSON but as documents |
| Markdown rendering in terminal | glow, pandoc -t ansi | Either works |
| Office doc creation (complex) | python-docx, openpyxl | When pandoc's model is too simple |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing a Python script for DOCX → MD | Use `pandoc --extract-media=media/ -o out.md in.docx` |
| Forgetting `-s` for standalone HTML | Add `-s` when output needs `<head>` and `<body>` |
| PDF fails — no LaTeX installed | Install texlive/mactex, or use `--pdf-engine=typst` or `weasyprint` |
| Losing images from DOCX | Add `--extract-media=media/` |
| Wrong markdown flavor in output | Specify `-t gfm` or `-t commonmark` explicitly |
| Piping binary formats to stdout | Use `-o file.docx` — DOCX/PDF/EPUB must write to files |
| Line wrapping mangles output | Add `--wrap=none` to preserve original line breaks |
| Checkboxes become `<input type="checkbox">` in EPUB/HTML | Read with `-f markdown-task_lists` to keep literal `[ ]` / `[x]` text. Pre-converting to Unicode glyphs (☐/☑) does **not** help — pandoc treats those as task-list markers unconditionally, independent of the extension flag, and still emits `<input>` |

## References

Consult for deep dives — these are loaded on demand, not auto-included:

- `${CLAUDE_SKILL_DIR}/references/pandoc-manual.md` — Curated option reference, templates, extensions
- `${CLAUDE_SKILL_DIR}/references/pandoc-install.md` — Installation on macOS, Linux, Docker + PDF engines
- `${CLAUDE_SKILL_DIR}/references/pandoc-advanced.md` — Lua filters, citations, slides, custom writers, EPUB

## Bundled Assets

- `${CLAUDE_SKILL_DIR}/themes/marked-print.css` — Compact A4 print stylesheet (9pt body, GitHub-like headings, Japanese + emoji)
- `${CLAUDE_SKILL_DIR}/scripts/md2pdf-print.sh` — Markdown → A4 print PDF via pandoc + headless Chrome
- `${CLAUDE_SKILL_DIR}/scripts/md2kindle-epub.sh` — Markdown → e-reader EPUB (TOC, chapter splitting, literal checkboxes)
