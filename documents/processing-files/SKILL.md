---
name: processing-files
description: Converts PDF files to markdown text. Use when the user wants to extract text from PDFs, convert PDFs to readable format, or process PDF documents.
---

# File Processing Tools

Tools for converting and processing file formats.

## PDF to Markdown

Extract text from PDF files and convert to markdown format.

### Basic usage

```python
result = await pdf_to_markdown(file_path="/path/to/document.pdf")
# Returns: {"success": True, "data": {"markdown": "# Document Title\n\nContent..."}}
```

### With page limits

```python
# Extract first 5 pages only
result = await pdf_to_markdown(
    file_path="/path/to/document.pdf",
    max_pages=5
)
```

### Response format

```json
{
  "success": true,
  "data": {
    "markdown": "extracted markdown content",
    "page_count": 10,
    "file_path": "/path/to/document.pdf"
  }
}
```

## Requirements

Requires `pymupdf` package for PDF processing.

## When to use

- Converting PDF reports to readable text
- Extracting content from PDF documents
- Processing PDF files for further analysis
