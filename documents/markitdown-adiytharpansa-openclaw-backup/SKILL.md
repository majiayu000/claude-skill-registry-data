---
name: markitdown
description: Convert documents and files to Markdown using the markitdown CLI (Microsoft's markitdown v0.1.5). Supports PDF, DOCX, XLSX, XLS, PPTX, HTML, CSV, JSON, XML, EPUB, images (EXIF/OCR), audio (metadata/transcription), Outlook MSG, Jupyter notebooks (.ipynb), RSS/Atom feeds, ZIP archives, YouTube URLs, Wikipedia URLs, and plain text. Use when the user wants to extract text or convert a file to Markdown, parse document contents, read spreadsheet data as a table, extract text from a presentation, or convert any supported file type into readable Markdown. Also use when needing to read/parse files that the agent cannot natively open (e.g., .docx, .pptx, .xlsx, .epub, .msg).
---

# MarkItDown

Convert files and URLs to Markdown via the `markitdown` CLI.

## Usage

```bash
# File to stdout
markitdown <file>

# File to output file
markitdown <file> -o output.md

# Stdin with extension hint
cat file.pdf | markitdown -x .pdf

# With MIME type hint
markitdown <file> -m application/pdf
```

## Supported Formats

| Format | Extensions | Notes |
|---|---|---|
| PDF | .pdf | Text extraction with layout preservation |
| Word | .docx | Full formatting, tables, images |
| Excel | .xlsx, .xls | Each sheet as a Markdown table |
| PowerPoint | .pptx | Slides with text and notes |
| HTML | .html, .htm | Converts to clean Markdown |
| CSV | .csv | Renders as Markdown table |
| JSON/XML | .json, .xml | Structured text extraction |
| EPUB | .epub | E-book to Markdown |
| Images | .jpg, .png, .gif, etc. | EXIF metadata extraction |
| Outlook | .msg | Email headers, body, attachments |
| Jupyter | .ipynb | Cells rendered as Markdown + code blocks |
| RSS/Atom | feeds | Feed entries with titles, links, content |
| ZIP | .zip | Recursively converts contained files |
| YouTube | URL | Transcript extraction |
| Wikipedia | URL | Article content |
| Plain text | .txt, .md, .py, etc. | Pass-through with charset handling |

## Key Options

- `-o FILE` — Write output to file instead of stdout
- `-x EXT` — Hint file extension (for stdin: `-x .pdf`)
- `-m MIME` — Hint MIME type
- `-c CHARSET` — Hint charset (e.g., UTF-8)

## Tips

- Redirect stderr to suppress noisy onnxruntime/pydub warnings: `markitdown file.pdf 2>/dev/null`
- For large files, pipe to `head` to preview: `markitdown big.xlsx 2>/dev/null | head -100`
- ZIP files are recursively converted — each contained file gets its own section
- Excel workbooks produce one table per sheet
- For URLs (YouTube, Wikipedia), pass the URL directly as the filename argument
