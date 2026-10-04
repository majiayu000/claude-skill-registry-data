---
name: MXE Skill - Markdown Export Tool
description: Convert Markdown files to PDF, DOCX, or HTML with advanced features.
---

# MXE Skill - Markdown Export Tool

Convert Markdown files to PDF, DOCX, or HTML with advanced features.

## When to Use

Use MXE when the user wants to:
- Convert Markdown to PDF with nice formatting
- Export documents with Mermaid diagrams
- Generate PDFs with table of contents
- Create professional documents from Markdown
- Download web articles as Markdown

## Installation Check

```bash
which mxe || echo "Not installed"
```

If not installed:
```bash
cd /Users/tuan/.openclaw/workspace/mxe && npm run build && npm link
```

## Basic Usage

```bash
# Simple PDF conversion
mxe document.md

# With table of contents
mxe document.md --toc

# Specify output directory
mxe document.md -o ./output
```

## Font Options

```bash
# Custom body font
mxe document.md --font roboto

# Custom code font  
mxe document.md --mono-font fira-code

# Both
mxe document.md --font inter --mono-font jetbrains-mono
```

**Available body fonts:** `inter` (default), `roboto`, `lato`, `opensans`, `source-sans`, `merriweather`

**Available mono fonts:** `jetbrains-mono` (default), `fira-code`, `source-code`

## Mermaid Diagrams

```bash
# Default theme
mxe document.md

# Forest theme
mxe document.md --mermaid-theme forest

# Hand-drawn style
mxe document.md --hand-draw

# Dark theme with ELK layout
mxe document.md --mermaid-theme dark --mermaid-layout elk
```

**Themes:** `default`, `forest`, `dark`, `neutral`, `base`

## Full Example

```bash
# Professional PDF with all features
mxe report.md \
  --toc \
  --font roboto \
  --mono-font fira-code \
  --mermaid-theme forest \
  -o ./output
```

## Output Formats

```bash
mxe doc.md -f pdf      # PDF (default)
mxe doc.md -f docx     # Word document
mxe doc.md -f html     # HTML file
mxe doc.md -f clipboard # Copy to clipboard
```

## Download Web Articles

```bash
# Download and convert URL to PDF
mxe https://example.com/article

# Download as Markdown only
mxe https://example.com/article -f clipboard
```

## Tips

1. **Mermaid requires mmdc**: Install with `npm i -g @mermaid-js/mermaid-cli`
2. **Images are embedded**: Local images are base64 encoded into the PDF
3. **Custom CSS**: Use `-s style.css` for custom styling
4. **Bookmarks**: PDF bookmarks are auto-generated from headings (disable with `--no-bookmarks`)

## Location

Tool source: `/Users/tuan/.openclaw/workspace/mxe`
