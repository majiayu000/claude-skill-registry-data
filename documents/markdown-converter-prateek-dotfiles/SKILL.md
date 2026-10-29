---
name: markdown-converter
description: Convert documents and files to Markdown using markitdown. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, remote URLs (including YouTube), or EPubs to Markdown format for LLM processing or text analysis.
disable-model-invocation: true
---

# Markdown Converter

Convert a file or URL to Markdown with `uvx markitdown`. `uvx` runs the tool
without requiring a separate installation.

## Convert a source

Choose the invocation that matches where the source comes from and where the
Markdown should go:

```bash
# Convert a local file to stdout
uvx markitdown input.pdf

# Convert a remote URL to stdout
uvx markitdown https://example.com

# Write directly to a file
uvx markitdown input.pdf -o output.md

# Redirect stdout to a file
uvx markitdown input.docx > output.md

# Read the source from stdin
cat input.pdf | uvx markitdown
```

For stdin, add a type hint when the input type cannot be inferred:

```bash
cat document | uvx markitdown -x .pdf > output.md
```

## Choose an input type

MarkItDown supports these source types:

- Documents: PDF, Word (`.docx`), PowerPoint (`.pptx`), and Excel (`.xlsx`, `.xls`)
- Web and data: HTML, CSV, JSON, and XML
- Media: images (EXIF data and OCR) and audio (EXIF data and transcription)
- Other: ZIP archives (iterates over their contents), remote HTTP/HTTPS URLs
  including YouTube, and EPub

Examples for common document types:

```bash
uvx markitdown report.docx -o report.md
uvx markitdown https://example.com/report.pdf -o report.md
uvx markitdown data.xlsx > data.md
uvx markitdown slides.pptx -o slides.md
```

## Set conversion options

Use these flags when the source needs a hint or a specific conversion service:

```text
-o OUTPUT       Write Markdown to OUTPUT
-x EXTENSION    Hint the file extension, especially for stdin
-m MIME_TYPE    Hint the MIME type
-c CHARSET      Hint the character set, such as UTF-8
-d              Use Azure Document Intelligence
-e ENDPOINT     Set the Document Intelligence endpoint
--use-plugins   Enable third-party plugins
--list-plugins  List installed plugins
```

For example, use Azure Document Intelligence when a scanned PDF or a PDF with
poor extraction needs better results. Supply the endpoint for your Azure resource:

```bash
uvx markitdown scan.pdf -d -e "https://your-resource.cognitiveservices.azure.com/"
```

## Output and first run

The Markdown output preserves document structure such as headings, tables,
lists, and links. The first run caches dependencies; later runs are faster.
