---
name: pandoc
description: >
  Convert documents between formats using pandoc. Supports HTML, Markdown, DOCX, PDF, EPUB, LaTeX,
  ODT, RST, Org, MediaWiki, JIRA, CSV, Jupyter notebooks, and many more — any direction pandoc supports.
  Use this skill whenever the user wants to convert, transform, or export a document from one format to
  another, even if they don't mention pandoc explicitly. Triggers include: "convert this to PDF",
  "make a Word doc from this markdown", "export as EPUB", "turn this HTML into a PDF", "transform",
  "generate PDF", "render to", or any request involving document format conversion. Also use when the
  user wants to apply custom styling, add a table of contents, use a template, or set metadata during
  conversion.
metadata:
  version: 1.0.2
  author: Oliver Herklotz (oliver-hrkltz)
  homepage: https://github.com/hrkltz/pandoc-skill
compatibility: >
  Requires: pandoc (https://pandoc.org).
  Optional PDF engines: xelatex (texlive-xetex, recommended for Unicode/fonts),
  lualatex (texlive-luatex, complex typography), tectonic (self-contained TeX workflow),
  pdflatex (texlive-latex-base, fastest for ASCII), weasyprint (CSS Paged Media, Python-based),
  wkhtmltopdf (WebKit-based HTML/CSS rendering), prince (commercial HTML/CSS renderer).
---

## Setup

### Install Homebrew (macOS)

If Homebrew is not installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install dependencies

```bash
brew install jq curl git
```

This skill uses standard macOS package management. All packages are from the official Homebrew repository.

# Pandoc Document Converter

Convert documents between any formats pandoc supports, with full control over styling, templates,
table of contents, metadata, and PDF engine selection.

## Quick Start

For most conversions, use the helper script at `scripts/convert.sh`:

```bash
bash <skill-dir>/scripts/convert.sh <input-file> <output-file> [options...]
```

The script auto-detects formats from file extensions and applies sensible defaults (standalone
output, appropriate PDF engine, default LaTeX margins for LaTeX-based PDF engines). It also checks
that `pandoc`, the input file, the output directory, and any requested PDF engine are available.
Any extra arguments are passed through to pandoc.

## How Conversions Work

Pandoc reads a source format into an internal AST, then writes it out in the target format. This
means you can go from nearly any supported input to any supported output. The key decision points are:

1. **Input format** — usually auto-detected from the file extension
2. **Output format** — auto-detected from the output file extension
3. **PDF engine** — for PDF output, choose between `xelatex` (best Unicode/font support),
  `lualatex` (strong Unicode/fonts), `tectonic` (self-contained TeX), `pdflatex` (fastest,
  good for ASCII-heavy docs), or HTML/CSS engines like `weasyprint`, `wkhtmltopdf`, or `prince`
4. **Styling** — CSS for HTML-based outputs, LaTeX templates for PDF, reference docs for DOCX/ODT

## Common Conversion Patterns

### HTML → PDF
```bash
pandoc input.html -o output.pdf --pdf-engine=weasyprint -s
```
If the HTML uses external CSS, include it:
```bash
pandoc input.html -o output.pdf --pdf-engine=weasyprint -s --css=style.css
```

### Markdown → PDF
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex -s --toc --toc-depth=3
```

### Markdown → DOCX
```bash
pandoc input.md -o output.docx -s
```
To use a reference (template) document for styling:
```bash
pandoc input.md -o output.docx --reference-doc=template.docx
```

### Markdown → HTML
```bash
pandoc input.md -o output.html -s --css=style.css --toc
```

### DOCX → Markdown
```bash
pandoc input.docx -o output.md --extract-media=./media
```

### Markdown → EPUB
```bash
pandoc input.md -o output.epub -s --toc --epub-cover-image=cover.jpg
```

### LaTeX → PDF
```bash
pandoc input.tex -o output.pdf --pdf-engine=xelatex
```

### CSV → HTML table
```bash
pandoc input.csv -o output.html -s
```

## Styling and Appearance

### CSS for HTML-based outputs
Create or use a CSS file and pass it with `--css=path/to/style.css`. For PDF output via
`weasyprint`, `wkhtmltopdf`, or `prince`, CSS is respected directly. For PDF via LaTeX engines,
CSS is usually ignored — use LaTeX variables or templates instead.

A sensible default stylesheet is provided at `assets/default.css`. Use it when the user wants
a clean, readable output without specifying their own styles:
```bash
pandoc input.md -o output.html -s --css=<skill-dir>/assets/default.css
```

### LaTeX variables for PDF styling
Control margins, fonts, and paper size without a full template:
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=12pt \
  -V mainfont="DejaVu Serif" \
  -V documentclass=article
```

### Reference documents for DOCX/ODT
To match a corporate style, provide a reference document:
```bash
pandoc input.md -o output.docx --reference-doc=brand-template.docx
```

## Advanced Features

### Table of Contents
Add `--toc` and optionally `--toc-depth=N` (default 3):
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex -s --toc --toc-depth=2
```

### Metadata
Set title, author, date via YAML frontmatter in the source file or via `-M`:
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex -s \
  -M title="My Report" -M author="Jane Doe" -M date="2026-03-15"
```

### Filters and Lua filters
Pandoc supports filters that transform the AST. Lua filters are self-contained:
```bash
pandoc input.md -o output.pdf --lua-filter=my-filter.lua
```

### Multiple input files
Pandoc concatenates multiple inputs:
```bash
pandoc chapter1.md chapter2.md chapter3.md -o book.pdf --pdf-engine=xelatex -s --toc
```

### Extracting media from DOCX/EPUB
```bash
pandoc input.docx -o output.md --extract-media=./media
```

## Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| PDF has missing characters | Font doesn't support the glyphs | Use `--pdf-engine=xelatex` with `-V mainfont="DejaVu Serif"` |
| PDF conversion fails | No compatible PDF engine installed | Check `which xelatex lualatex tectonic pdflatex weasyprint wkhtmltopdf prince` and install one that matches your output needs |
| DOCX looks unstyled | No reference doc | Create a styled DOCX template and pass `--reference-doc` |
| HTML images missing | Relative paths broken | Use `--self-contained` to embed images as base64 |
| CSS has no effect on PDF | LaTeX PDF engine selected | Use `--pdf-engine=weasyprint`, `--pdf-engine=wkhtmltopdf`, or `--pdf-engine=prince` |
| Table of contents empty | No headings in source | Ensure source uses `#` headings (Markdown) or `<h1>`–`<h6>` (HTML) |

## Format Reference

For a full list of supported input and output formats, see `references/formats.md`.

## Choosing the Right Approach

When a user asks to convert a document, think about:

1. **What's the source format?** Check the file extension or ask. If it's ambiguous (e.g., a `.txt`
   that's actually Markdown), specify `-f markdown` explicitly.
2. **What's the target format?** Map the user's intent to a file extension.
3. **Does it need styling?** If the user wants it to "look nice" or "be professional," add CSS
   (for HTML) or LaTeX variables (for PDF) or a reference doc (for DOCX).
4. **Does it need structure?** TOC, numbered sections, metadata — add these when the document is
   long or formal.
5. **Are there images or media?** Use `--self-contained` for HTML, `--extract-media` when
   converting from DOCX/EPUB to text formats.

Always use the helper script `scripts/convert.sh` as the starting point — it handles the most
common gotchas automatically, picks a reasonable PDF engine, and prints recovery hints when PDF
conversion fails. Add extra pandoc flags as needed for the specific use case.
