---
name: markdown-to-pdf
description: Convert a Markdown file into a PDF for easier viewing and sharing. Use when Codex needs to render `.md` content into a presentable PDF, preserve headings and code blocks, choose an output filename, or use an available local renderer such as pandoc, weasyprint, wkhtmltopdf, or headless Chrome.
---

# Markdown To PDF

## Overview

Use this skill to turn Markdown documents into PDF files with a dependable local workflow. Prefer deterministic local renderers over ad hoc copy-paste or manual export.

When possible, use the bundled script to detect an available renderer and perform the conversion. Keep the workflow simple: source Markdown in, PDF out.

## Workflow

### 1. Confirm the input and output

Identify:

- the source Markdown file
- the desired output PDF path
- whether default styling is acceptable or whether the user wants a cleaner presentation

If the user does not specify an output path, default to the same basename as the Markdown file with a `.pdf` extension.

### 2. Use the bundled renderer script

Run:

```bash
scripts/render_markdown_pdf.sh <input.md> [output.pdf]
```

The script tries these renderers in order:

1. `pandoc`
2. `weasyprint`
3. `wkhtmltopdf`
4. Google Chrome headless

If no renderer is available, report that clearly and suggest installing one of the supported tools.

### 3. Verify the result

After rendering:

- confirm the PDF file was created
- report which renderer was used
- mention if the conversion used a fallback path

If the output looks likely to have formatting limits, say so briefly.

## Output Rules

- Prefer the bundled script instead of re-deriving renderer logic each time.
- Default to preserving headings, paragraphs, lists, and fenced code blocks.
- Do not invent rich visual styling unless the user asks for it.
- If the renderer is missing, explain the missing dependency plainly instead of pretending the conversion succeeded.

## Notes

- `pandoc` is usually the best general-purpose option when installed.
- `weasyprint` and `wkhtmltopdf` work through an intermediate HTML render.
- Headless Chrome is a useful fallback when a browser is available locally.

## Example Requests

- Convert this `threat_model.md` file to PDF.
- Turn this Markdown report into a shareable PDF.
- Render this `.md` file as a PDF with the default output name.
