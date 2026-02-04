---
name: gemini-pdf
description: Process multimodal documents using Gemini CLI, leveraging Gemini's superior multimodal capabilities. Use for PDFs, scanned documents, image-heavy documents, or any file where visual understanding matters. Ideal for extracting content from complex layouts, tables, diagrams, handwritten notes, or mixed text/image documents. Triggers on PDF processing, document extraction, "use Gemini for this", or when document has visual complexity that benefits from multimodal understanding.
---

# Gemini Document Processing

Delegate document processing to Gemini CLI for superior multimodal understanding. Use when documents have visual complexity - layouts, tables, diagrams, scans, mixed content.

## Basic Usage

Reference file paths directly in your prompt - Gemini reads them via its file system tools:

```bash
gemini "Convert this to markdown: /path/to/document.pdf"

# Save output
gemini "Convert to markdown: /path/to/doc.pdf" > output.md
```

## Common Tasks

**Faithful Conversion:**
```bash
gemini "Convert this PDF to clean markdown. Preserve all content including headers, lists, tables. Output only markdown, no commentary: /path/to/document.pdf"
```

**Table Extraction:**
```bash
gemini "Extract all tables as markdown tables: /path/to/document.pdf"
```

**Structured Extraction:**
```bash
gemini "Extract and structure as markdown:
- [list the fields you want]
- [be specific about format]
File: /path/to/document.pdf"
```

**Diagram/Image Description:**
```bash
gemini "Describe the diagrams and figures in this document: /path/to/document.pdf"
```

## When to Use Gemini vs Other Tools

**Use Gemini:**
- Scanned documents / OCR needed
- Complex layouts (multi-column, mixed content)
- Tables, diagrams, charts
- Handwritten content
- Image-heavy documents

**Use pypdf/pdfplumber:**
- Simple text-only PDFs
- Programmatic batch processing
- When you need raw text extraction without interpretation
