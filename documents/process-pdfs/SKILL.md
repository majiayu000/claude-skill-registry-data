---
name: process-pdfs
description: Comprehensive toolkit for PDF processing and manipulation. Process PDF files to extract text/tables, convert PDF to text, merge/combine/split PDFs, fill forms, add watermarks, rotate pages, handle passwords, OCR scanned documents. Use when you need to extract from PDF, extract data from PDF, get data from PDF, work with PDF files, PDF conversion, complex tasks, batch processing, or programmatic manipulation to read, parse, combine, or extract data from PDFs at scale.
allowed-tools: [Read, Write, Bash, mcp__ide__executeCode]
model: sonnet
tags: [pdf, documents, extraction, conversion, batch-processing]
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see [reference.md](reference.md). If you need to fill out a PDF form, read [forms.md](forms.md) and follow its instructions.

## Setup

### Python Dependencies

Install required libraries:

```bash
# Core libraries
pip install pypdf pdfplumber reportlab

# For OCR (scanned PDFs)
pip install pytesseract pdf2image

# For data export
pip install pandas openpyxl
```

### Command-Line Tools

macOS (using Homebrew):

```bash
brew install poppler qpdf tesseract
```

Linux (Debian/Ubuntu):

```bash
sudo apt-get install poppler-utils qpdf tesseract-ocr
```

### Working Directory

When using scripts from the `scripts/` directory, run them from the skill directory:

```bash
cd /Users/markayers/.claude/skills/process-pdfs
python scripts/script_name.py
```

Or use absolute paths when referencing scripts.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Check for Encryption First

**Always check if a PDF is password-protected before processing:**

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")

if reader.is_encrypted:
    print("PDF is encrypted")
    # Try to decrypt with password
    if reader.decrypt("password"):
        print("Successfully decrypted")
    else:
        print("Failed to decrypt - wrong password")
        # Option 1: Ask user for password
        # Option 2: Use qpdf to remove password (if you have it)
        # qpdf --password=yourpassword --decrypt encrypted.pdf decrypted.pdf
else:
    print("PDF is not encrypted - proceed with processing")
```

**For batch processing, skip or report encrypted files:**

```python
import os
from pypdf import PdfReader

for filename in os.listdir("pdfs/"):
    if filename.endswith(".pdf"):
        try:
            reader = PdfReader(f"pdfs/{filename}")
            if reader.is_encrypted:
                print(f"SKIP: {filename} - encrypted")
                continue
            # Process the PDF...
        except Exception as e:
            print(f"ERROR: {filename} - {e}")
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF

```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata

```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages

```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables

```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction

```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

## Command-Line Tools

### pdftotext (poppler-utils)

```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf

```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)

```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs

```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark

```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images

```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task               | Best Tool                                   | Command/Code               |
| ------------------ | ------------------------------------------- | -------------------------- |
| Merge PDFs         | pypdf                                       | `writer.add_page(page)`    |
| Split PDFs         | pypdf                                       | One page per file          |
| Extract text       | pdfplumber                                  | `page.extract_text()`      |
| Extract tables     | pdfplumber                                  | `page.extract_tables()`    |
| Create PDFs        | reportlab                                   | Canvas or Platypus         |
| Command line merge | qpdf                                        | `qpdf --empty --pages ...` |
| OCR scanned PDFs   | pytesseract                                 | Convert to image first     |
| Fill PDF forms     | pdf-lib or pypdf (see [forms.md](forms.md)) | See [forms.md](forms.md)   |

## Troubleshooting

### Corrupted or Invalid PDFs

**Symptom**: Errors like "EOF marker not found", "Invalid PDF structure", or "Cannot read PDF"

**Solution**: Use qpdf to repair the PDF first:

```bash
qpdf --check input.pdf  # Check for errors
qpdf input.pdf repaired.pdf  # Attempt repair
```

If qpdf can't repair it, try:

```bash
gs -o repaired.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress input.pdf
```

### Missing Dependencies

**Symptom**: `ModuleNotFoundError` or command not found

**Python libraries**:

```bash
pip install pypdf pdfplumber reportlab pytesseract pdf2image pandas
```

**Command-line tools** (macOS):

```bash
brew install poppler qpdf tesseract
```

**Command-line tools** (Linux):

```bash
sudo apt-get install poppler-utils qpdf tesseract-ocr
```

### Memory Issues with Large PDFs

**Symptom**: Process killed, memory errors, or system slowdown when processing PDFs >100 pages

**Solution**: Process in chunks:

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("large.pdf")
chunk_size = 50  # Process 50 pages at a time

for i in range(0, len(reader.pages), chunk_size):
    writer = PdfWriter()
    for page_num in range(i, min(i + chunk_size, len(reader.pages))):
        writer.add_page(reader.pages[page_num])

    with open(f"chunk_{i//chunk_size + 1}.pdf", "wb") as output:
        writer.write(output)
```

Or extract text page-by-page:

```python
with pdfplumber.open("large.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        # Process or save immediately
        with open(f"page_{i+1}.txt", "w") as f:
            f.write(text)
```

### Permission Errors

**Symptom**: "PermissionError" or "Access denied"

**Causes**:

1. PDF is password-protected (see "Check for Encryption First" section)
2. File is open in another application (close it)
3. Insufficient file system permissions

**Solution**:

```bash
# Check file permissions
ls -la file.pdf

# Make readable
chmod 644 file.pdf
```

### Text Extraction Returns Empty or Garbled Text

**Symptom**: `extract_text()` returns empty string or gibberish

**Causes**:

1. PDF is scanned (image-based) - use OCR
2. PDF uses non-standard fonts or encoding
3. Text is embedded as images

**Solution for scanned PDFs**:

```python
# Use pytesseract for OCR (see "Extract Text from Scanned PDFs" section)
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path('scanned.pdf')
text = pytesseract.image_to_string(images[0])
```

**Solution for non-standard encoding**:
Try pdfplumber instead of pypdf:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

Or use command-line tool:

```bash
pdftotext -layout document.pdf output.txt
```

## Next Steps

- For advanced pypdfium2 usage, see [reference.md](reference.md)
- For JavaScript libraries (pdf-lib), see [reference.md](reference.md)
- If you need to fill out a PDF form, follow the instructions in [forms.md](forms.md)
- For troubleshooting guides, see [reference.md](reference.md)
