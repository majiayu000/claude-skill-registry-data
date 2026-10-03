---
name: pdf
description: Read, extract, create, merge, split, and manipulate PDF files. Use whenever a .pdf file is involved — extracting text or tables from a PDF, creating a new PDF from content or data, merging multiple PDFs, splitting a PDF into pages, rotating pages, adding watermarks, filling PDF forms, encrypting or decrypting PDFs, extracting images, or running OCR on scanned PDFs. Trigger when the user mentions a .pdf file or asks to produce a PDF output.
---

# PDF Processing

PDF is the universal document format. It is also one of the most annoying formats to work with programmatically. This skill handles the full range of PDF tasks — reading, creating, editing, merging, splitting, and extracting — using the right tool for each job.

| Task | Best tool |
|---|---|
| Extract text (digital PDF) | `pdfplumber` or `pdftotext` |
| Extract tables | `pdfplumber` |
| Create PDF from content | `reportlab` |
| Merge / split / rotate | `pypdf` or `qpdf` |
| Fill PDF forms | `pypdf` or `pdf-lib` (JS) |
| OCR scanned PDFs | `pytesseract` + `pdf2image` |
| Password protect / decrypt | `pypdf` or `qpdf` |
| Extract images | `pdfimages` (poppler) |

> `pypdf`, `pdfplumber`, and `reportlab` are typically pre-installed. Import directly. Only run `pip install` if an import fails.

---

## Reading & Extracting Content

### Extract All Text

```python
# pdfplumber — preserves layout better than pypdf
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    print(f"Pages: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if text:
            print(f"\n--- Page {i} ---")
            print(text)
```

```bash
# Command line — fastest for quick extraction
pdftotext document.pdf output.txt         # basic
pdftotext -layout document.pdf output.txt # preserve column layout
pdftotext -f 1 -l 5 document.pdf -        # pages 1–5, stdout
```

### Extract Specific Pages

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")

# Single page
text = reader.pages[0].extract_text()

# Page range (0-indexed)
for page in reader.pages[2:7]:  # pages 3–7
    print(page.extract_text())
```

### Extract Tables

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("report.pdf") as pdf:
    all_tables = []

    for page_num, page in enumerate(pdf.pages, 1):
        tables = page.extract_tables()

        for table_num, table in enumerate(tables, 1):
            if not table or not table[0]:
                continue

            print(f"Page {page_num}, Table {table_num}: {len(table)} rows")

            # Convert to DataFrame — first row as headers
            df = pd.DataFrame(table[1:], columns=table[0])

            # Clean: strip whitespace, drop empty rows
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df = df.dropna(how="all")

            all_tables.append(df)

# Combine and export
if all_tables:
    combined = pd.concat(all_tables, ignore_index=True)
    combined.to_excel("extracted_tables.xlsx", index=False)
    combined.to_csv("extracted_tables.csv", index=False)
    print(f"Extracted {len(combined)} rows across {len(all_tables)} tables")
```

### Extract Metadata

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
meta = reader.metadata

print(f"Title:    {meta.title}")
print(f"Author:   {meta.author}")
print(f"Subject:  {meta.subject}")
print(f"Creator:  {meta.creator}")
print(f"Producer: {meta.producer}")
print(f"Created:  {meta.creation_date}")
print(f"Pages:    {len(reader.pages)}")
print(f"Encrypted:{reader.is_encrypted}")
```

---

## Creating PDFs

### Simple PDF with reportlab

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, HRFlowable
)

doc = SimpleDocTemplate(
    "report.pdf",
    pagesize=letter,
    rightMargin=inch,
    leftMargin=inch,
    topMargin=inch,
    bottomMargin=inch,
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=24,
    spaceAfter=12,
    textColor=colors.HexColor("#1A1A2E"),
)

heading_style = ParagraphStyle(
    "CustomHeading",
    parent=styles["Heading1"],
    fontSize=16,
    spaceBefore=16,
    spaceAfter=8,
    textColor=colors.HexColor("#2563EB"),
)

body_style = ParagraphStyle(
    "CustomBody",
    parent=styles["Normal"],
    fontSize=11,
    leading=16,  # line height
    spaceAfter=8,
)

story = []

# Title
story.append(Paragraph("Q3 2025 Engineering Report", title_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E5E7EB")))
story.append(Spacer(1, 12))

# Section heading + body
story.append(Paragraph("Executive Summary", heading_style))
story.append(Paragraph(
    "This quarter the engineering team shipped 12 features, resolved 47 bugs, "
    "and improved API response time by 34% across all endpoints.",
    body_style
))
story.append(Spacer(1, 8))

# Table
table_data = [
    ["Metric", "Q2 2025", "Q3 2025", "Change"],
    ["Features shipped", "8", "12", "+50%"],
    ["Bugs resolved", "31", "47", "+52%"],
    ["API P95 latency", "420ms", "278ms", "-34%"],
    ["Test coverage", "71%", "81%", "+10pp"],
]

table = Table(table_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.1*inch])
table.setStyle(TableStyle([
    # Header row
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A1A2E")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",   (0, 0), (-1, 0), 11),
    ("ALIGN",      (0, 0), (-1, 0), "CENTER"),
    # Data rows
    ("FONTNAME",   (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",   (0, 1), (-1, -1), 10),
    ("ALIGN",      (1, 1), (-1, -1), "CENTER"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
    # Borders
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
    ("BOX",  (0, 0), (-1, -1), 1,   colors.HexColor("#D1D5DB")),
    # Padding
    ("TOPPADDING",    (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
]))

story.append(table)
story.append(PageBreak())
story.append(Paragraph("Appendix", heading_style))

doc.build(story)
print("Created report.pdf")
```

### Important: Subscripts and Superscripts

**Never use Unicode subscript/superscript characters in reportlab** — they render as solid black boxes in built-in fonts.

```python
# ❌ WRONG — renders as black boxes
story.append(Paragraph("H₂O", styles["Normal"]))
story.append(Paragraph("x²", styles["Normal"]))

# ✅ CORRECT — use XML sub/sup tags in Paragraph text
story.append(Paragraph("H<sub>2</sub>O", styles["Normal"]))
story.append(Paragraph("x<sup>2</sup> + y<sup>2</sup>", styles["Normal"]))
```

---

## Merging PDFs

```python
from pypdf import PdfWriter, PdfReader

def merge_pdfs(input_files: list[str], output_file: str):
    writer = PdfWriter()

    for pdf_file in input_files:
        reader = PdfReader(pdf_file)
        print(f"Adding {pdf_file}: {len(reader.pages)} pages")
        for page in reader.pages:
            writer.add_page(page)

    with open(output_file, "wb") as f:
        writer.write(f)
    print(f"Merged {len(input_files)} files → {output_file}")

merge_pdfs(["intro.pdf", "chapter1.pdf", "chapter2.pdf", "appendix.pdf"], "complete.pdf")
```

```bash
# Command line — faster for large files
qpdf --empty --pages intro.pdf chapter1.pdf chapter2.pdf -- merged.pdf

# With page ranges
qpdf --empty --pages file1.pdf 1-5 file2.pdf 3-7 -- merged.pdf
```

---

## Splitting PDFs

```python
from pypdf import PdfReader, PdfWriter
import os

def split_pdf(input_file: str, output_dir: str = "."):
    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(input_file)

    for i, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        output_path = os.path.join(output_dir, f"page_{i:03d}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
    print(f"Split {len(reader.pages)} pages → {output_dir}/")

# Split by page range
def extract_pages(input_file: str, start: int, end: int, output_file: str):
    """Extract pages start..end (1-indexed, inclusive)"""
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages[start-1:end]:
        writer.add_page(page)
    with open(output_file, "wb") as f:
        writer.write(f)
```

```bash
# Command line
qpdf input.pdf --pages . 1-10 -- part1.pdf
qpdf input.pdf --pages . 11-20 -- part2.pdf
```

---

## Rotating Pages

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
writer = PdfWriter()

for i, page in enumerate(reader.pages):
    if i in [0, 2]:        # rotate specific pages
        page.rotate(90)    # 90, 180, or 270 degrees clockwise
    writer.add_page(page)

with open("rotated.pdf", "wb") as f:
    writer.write(f)
```

---

## Watermarking

```python
from pypdf import PdfReader, PdfWriter

# Assume watermark.pdf exists with the watermark on page 1
watermark_page = PdfReader("watermark.pdf").pages[0]

reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark_page)  # overlay watermark
    writer.add_page(page)

with open("watermarked.pdf", "wb") as f:
    writer.write(f)
```

---

## Password Protection

```python
from pypdf import PdfReader, PdfWriter

# Encrypt a PDF
def encrypt_pdf(input_file: str, output_file: str, password: str):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(user_password=password, owner_password=password + "_owner")
    with open(output_file, "wb") as f:
        writer.write(f)

# Decrypt a PDF
def decrypt_pdf(input_file: str, output_file: str, password: str):
    reader = PdfReader(input_file)
    if reader.is_encrypted:
        reader.decrypt(password)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    with open(output_file, "wb") as f:
        writer.write(f)
```

```bash
# Command line
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
qpdf --encrypt userpass ownerpass 256 -- plain.pdf encrypted.pdf
```

---

## OCR (Scanned PDFs)

When a PDF contains images of text (not selectable text), OCR is required:

```python
# pip install pytesseract pdf2image
# Also requires: brew install tesseract poppler (macOS)
import pytesseract
from pdf2image import convert_from_path

def ocr_pdf(input_file: str, output_file: str = None) -> str:
    # Convert PDF pages to images (300 DPI for accuracy)
    images = convert_from_path(input_file, dpi=300)
    print(f"OCR processing {len(images)} pages...")

    full_text = ""
    for i, image in enumerate(images, 1):
        page_text = pytesseract.image_to_string(image, lang="eng")
        full_text += f"\n--- Page {i} ---\n{page_text}\n"
        print(f"  Page {i}: {len(page_text)} characters")

    if output_file:
        with open(output_file, "w") as f:
            f.write(full_text)
    return full_text

text = ocr_pdf("scanned_contract.pdf", "contract_text.txt")
```

---

## Convert PDF to Other Formats

```bash
# PDF → Word (requires LibreOffice)
libreoffice --headless --convert-to docx document.pdf

# PDF → images (one image per page)
pdfimages -j document.pdf page    # → page-000.jpg, page-001.jpg...
pdftoppm -r 150 document.pdf page # → page-1.ppm (150 DPI)

# PDF → text (preserving layout)
pdftotext -layout document.pdf output.txt

# HTML/Markdown → PDF (via reportlab or weasyprint)
# pip install weasyprint
from weasyprint import HTML
HTML(filename="page.html").write_pdf("output.pdf")
```

---

## Quick Reference

| Task | Code / Command |
|---|---|
| Read text | `pdfplumber.open(f).pages[0].extract_text()` |
| Read tables | `page.extract_tables()` → `pd.DataFrame` |
| Create PDF | `reportlab` `SimpleDocTemplate` + `Paragraph` |
| Merge | `PdfWriter` + `add_page()` per file |
| Split | One `PdfWriter` per page |
| Rotate | `page.rotate(90)` |
| Watermark | `page.merge_page(watermark)` |
| Encrypt | `writer.encrypt(password)` |
| Decrypt | `reader.decrypt(password)` → new `PdfWriter` |
| OCR | `pdf2image` convert → `pytesseract.image_to_string()` |
| CLI merge | `qpdf --empty --pages f1.pdf f2.pdf -- out.pdf` |
| CLI split | `qpdf input.pdf --pages . 1-5 -- part.pdf` |

---

## Definition of Done — PDF

- [ ] Correct tool selected for the task (pdfplumber for extraction, reportlab for creation, pypdf for manipulation)
- [ ] Text extraction verified against known content — no garbled characters
- [ ] Tables exported to DataFrame and validated row/column counts match visual inspection
- [ ] Created PDFs: all text renders correctly (no black boxes from Unicode subscripts)
- [ ] Created PDFs: all pages have consistent margins and formatting
- [ ] Merged/split files: page count verified (sum of inputs = merged output)
- [ ] Encrypted files: verified password opens correctly and wrong password fails
- [ ] OCR output: spot-checked for accuracy on 3+ pages
- [ ] Output file opens without errors in PDF reader (Adobe, Preview, Chrome)
- [ ] No intermediate temp files left on disk
