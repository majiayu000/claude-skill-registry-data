---
name: markitdown
description: "Convert any file (PDF, DOCX, XLSX, PPTX, HTML, images, audio, video, ZIP) to clean Markdown using Microsoft's markitdown CLI. Use when user wants to extract text from documents, convert files to markdown, or preprocess documents for LLM consumption. Triggers on: 'convert to markdown', 'extract text from', 'read this PDF', 'parse this document'."
---

# MarkItDown — File to Markdown Converter

Convert virtually any file format to clean, structured Markdown using the `markitdown` CLI.
Prioritizes structural fidelity (headings, tables, lists, links) over visual reproduction.

Source: [microsoft/markitdown](https://github.com/microsoft/markitdown) (118k+ stars)

## Supported Formats

| Format | Extensions |
|--------|-----------|
| PDF | `.pdf` |
| Word | `.docx` |
| Excel | `.xlsx`, `.xls` |
| PowerPoint | `.pptx` |
| HTML | `.html`, `.htm` |
| Images | `.jpg`, `.png`, `.gif` (with LLM description) |
| Audio | `.mp3`, `.wav` (with transcription) |
| Video | `.mp4` (with transcription) |
| Archives | `.zip` (extracts and converts contents) |
| Text | `.txt`, `.csv`, `.json`, `.xml`, `.yaml` |
| Code | Most programming language files |

## CLI Usage

### Convert a file
```bash
markitdown path/to/file.pdf
```

### Convert with output file
```bash
markitdown path/to/file.pdf -o output.md
```

### Convert from stdin
```bash
cat file.pdf | markitdown
```

### Convert a URL
```bash
markitdown https://example.com/page.html
```

## Workflow

1. User provides a file path or URL to convert
2. Run `markitdown <path>` via Bash tool to get markdown output
3. Present the converted content or save to a file
4. For large files, pipe through `head` or extract specific sections

## Python API (for programmatic use)

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)
```

## Notes

- For images: markitdown can optionally use an LLM to describe image contents (requires OpenAI API key via `OPENAI_API_KEY` env var)
- For audio/video: uses SpeechRecognition for transcription
- Excel files: converts each sheet to a markdown table
- PowerPoint: extracts text from all slides with slide numbers
