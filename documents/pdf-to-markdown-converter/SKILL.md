---
name: pdf-to-markdown-converter
description: Converts PDF files to Markdown format using PyMuPDF, extracting text content and embedded images. Fast and lightweight. Automatically fixes LaTeX umlauts (¨a → ä, etc.) and converts ß to ss (Swiss German). Use when converting PDFs to Markdown, extracting document content, or processing PDF files for text analysis. Generates one .md file and 0..n .png files for images.
---

# PDF to Markdown Converter

## Overview

This skill converts PDF files to Markdown format using the PyMuPDF (fitz) library. It extracts text content and saves embedded images as separate PNG files. This is a fast and lightweight alternative to Docling.

**Special Features:**
- ✅ Automatically fixes LaTeX-style umlauts (¨a, ¨o, ¨u → ä, ö, ü)
- ✅ Converts ß to ss (Swiss German style)
- ✅ Corrects common LaTeX encoding issues
- ✅ Preserves text layout
- ✅ Extracts all images as PNG files

## Prerequisites

Ensure PyMuPDF is installed (installs in ~10-20 seconds):
```bash
pip install PyMuPDF --break-system-packages
```

Optional for better image format support:
```bash
pip install Pillow --break-system-packages
```

## Usage Workflow

1. **Receive PDF file**: User provides the PDF file path
2. **Validate input**: Check that the file exists and is a valid PDF
3. **Run conversion**: Execute [pdf_converter.py](scripts/pdf_converter.py) with the PDF path
4. **Output organization**:
   - Markdown file: `<original_name>.md`
   - Images folder: `<original_name>_images/` containing PNG files
   - Images are referenced in the Markdown with relative paths

## Conversion Command

```bash
python scripts/pdf_converter.py <input.pdf> [output_dir]
```

Parameters:
- `input.pdf`: Path to the source PDF file
- `output_dir`: (Optional) Output directory. Defaults to current directory

## Output Structure

```
output_dir/
├── document.md              # Converted markdown content
└── document_images/         # Extracted images (if any)
    ├── image_001.png
    ├── image_002.png
    └── ...
```

## Error Handling

If conversion fails:
- Check PDF is not corrupted or password-protected
- Verify Docling installation
- Ensure sufficient disk space for image extraction
- Review console output for specific error messages

## Best Practices

- Large PDFs may take time to process - inform user
- Preview the first page for complex documents to verify quality
- For batch processing, process files sequentially to avoid memory issues
- Preserve original PDF files - never overwrite source documents