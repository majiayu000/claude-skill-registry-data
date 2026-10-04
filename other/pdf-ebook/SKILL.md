---
name: pdf-ebook
description: Convert any file format (markdown, text, HTML) into a professionally styled PDF e-book using WeasyPrint. Supports single files, directories of files, and custom styling. Use when generating PDF deliverables from content files.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

Convert content files to a styled PDF e-book: $ARGUMENTS

$ARGUMENTS should specify: the source file or directory path, and optionally: title, subtitle, author, output path, or style overrides. If no arguments, ask the user.

## Before Starting

1. Identify the source: single file or directory of files
2. If a directory, determine file order (numeric prefixes, alphabetical, or custom)
3. Read source files to understand content structure (headings, tables, lists, images)
4. Check for any existing cover or metadata files

## Process

1. **Gather content** — Read all source files in order. For directories, sort by filename (numeric prefixes respected).
2. **Generate the conversion script** — Write a Python script to `/tmp/pdf_ebook_convert.py` that:
   - Reads and concatenates all markdown/text/HTML files
   - Converts markdown to HTML via the `markdown` Python library (with `tables`, `toc`, `fenced_code`, `meta` extensions)
   - Wraps in a full HTML document with embedded CSS
   - Generates PDF via WeasyPrint
3. **Run the script** — Execute with `python3 /tmp/pdf_ebook_convert.py`
4. **Report** — Show the output path and page count

## Styling Defaults

The default e-book style uses:
- **Page size:** US Letter with 1in margins
- **Body font:** Georgia, serif at 11pt / 1.6 line-height
- **Heading font:** system sans-serif stack
- **Colors:** Dark charcoal text (#1a1a1a), accent for headings (#2c3e50)
- **Tables:** Clean bordered style with subtle header background
- **Page breaks:** Before each H1; avoid breaks inside tables, figures, blockquotes
- **Header/footer:** Running title in header, page numbers in footer
- **Cover page:** First page with title, subtitle, author centered

The user may override any of these via $ARGUMENTS (e.g., "dark theme", "A4 size", "sans-serif body").

## Dependencies

Requires Python packages: `weasyprint`, `markdown`. Both should be installed. If missing, install with `pip3 install weasyprint markdown`.

## Output

Default output path: same directory as source, named `{title-slug}.pdf`. User may specify a custom output path.
