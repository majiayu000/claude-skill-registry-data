---
name: pdf-design
description: Instructions and code examples for creating, editing, and designing PDFs programmatically. Use this skill to generate reports, fill forms, or design custom layouts.
license: MIT
metadata:
  category: documents
---
# PDF Creation and Design Manual

## Overview

This skill helps you create and manipulate PDF documents using Python and command-line tools. Use it to generate reports, fill forms, or customize layouts.

## Creating PDFs with ReportLab

### Basic Example

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=A4)
width, height = A4

# Draw text
c.setFont("Helvetica-Bold", 16)
c.drawString(50, height - 50, "Hello, PDF!")

# Draw rectangle
c.rect(50, height - 100, 200, 50, stroke=1, fill=0)

# Save
c.save()
```

### Multipage Report

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf")
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Report Title", styles['Title']))
story.append(Spacer(1, 12))
story.append(Paragraph("This is the report body.", styles['Normal']))
story.append(PageBreak())
story.append(Paragraph("Page 2", styles['Heading1']))
doc.build(story)
```

## Filling PDF Forms with PyPDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Update form fields
writer.update_page_form_field_values(writer.pages[0], {
    "name_field": "John Doe",
    "date_field": "2025-10-18"
})

with open("filled_form.pdf", "wb") as f_out:
    writer.write(f_out)
```

## Merging and Splitting PDFs

```python
from pypdf import PdfMerger, PdfReader, PdfWriter

# Merge
merger = PdfMerger()
for pdf_file in ["file1.pdf", "file2.pdf"]:
    merger.append(pdf_file)
merger.write("merged.pdf")
merger.close()

# Split first 5 pages
reader = PdfReader("big.pdf")
for i, page in enumerate(reader.pages[:5]):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page{i+1}.pdf", "wb") as out:
        writer.write(out)
```

## Design Tips

- Use consistent margins and spacing.
- Choose a readable font (e.g., Helvetica or Times New Roman).
- Use headers and footers for pagination and context.
- Incorporate your brand colors and logo.
- For long documents, include a table of contents with hyperlinks.

## Command-Line Tools

- `pdftotext` – Extract text: `pdftotext -layout input.pdf output.txt`.
- `qpdf` – Merge/split: `qpdf input.pdf --pages . 1-5 -- output.pdf`.
- `pdfinfo` – View metadata.

## Additional Resources

- ReportLab User Guide.
- PyPDF documentation.
- Poppler utils man pages.
