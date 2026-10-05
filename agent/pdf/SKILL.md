---
name: pdf
description: Read, extract, merge, split, rotate, watermark, create, fill forms, encrypt/decrypt, or OCR PDF files. Use whenever a `.pdf` is mentioned or a PDF is requested.
argument-hint: <pdf file or operation>
model: sonnet
effort: low
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# PDF Processing

## Gotchas
- Never use Unicode subscript/superscript characters (₁, ², etc.) in ReportLab PDFs. Built-in fonts don't include these glyphs, rendering them as solid black boxes.
- OCR requires the `tesseract` system binary, not just `pip install pytesseract`. On macOS: `brew install tesseract`.
- Watermark PDFs must have transparent backgrounds. `merge_page()` composites content — a watermark with a white background will cover the document.

## Instructions

### Step 1: Identify the Operation

Determine what the user needs: read/extract text, merge, split, rotate, create, fill forms, OCR, watermark, encrypt/decrypt, or extract images. If the task involves filling a PDF form, read `references/forms.md` and follow its instructions instead of continuing here.

### Step 2: Choose the Right Tool

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pypdf or annotations (see `references/forms.md`) | See `references/forms.md` |

### Step 3: Execute

Use the code patterns below, organized by tool/library.

#### Quick Start

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

#### pypdf - Basic Operations

**Merge PDFs:**
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

**Split PDF:**
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

**Extract Metadata:**
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

**Rotate Pages:**
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

#### pdfplumber - Text and Table Extraction

**Extract Text with Layout:**
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

**Extract Tables:**
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

**Advanced Table Extraction:**
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

#### reportlab - Create PDFs

**Basic PDF Creation:**
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

**Create PDF with Multiple Pages:**
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

**Subscripts and Superscripts:**

**IMPORTANT**: Never use Unicode subscript/superscript characters in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes. Use ReportLab's XML markup tags instead:

```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

#### Command-Line Tools

**pdftotext (poppler-utils):**
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

**qpdf:**
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

**pdftk (if available):**
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

#### Common Tasks

**Extract Text from Scanned PDFs (OCR):**
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

**Add Watermark:**
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

**Extract Images:**
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

**Password Protection:**
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

### Step 4: Verify Output

Open the output PDF and confirm the operation succeeded. For form fills, convert the filled PDF to images and visually verify text placement:
```python
from pdf2image import convert_from_path
images = convert_from_path("output.pdf")
for i, img in enumerate(images):
    img.save(f"verify_page_{i+1}.png")
```

## Examples

### Extract text from a multi-page PDF
```
User: "Extract all the text from report.pdf"
```
Use pdfplumber to extract text page by page, then combine into a single output.

### Merge three invoices into one file
```
User: "Combine invoice_jan.pdf, invoice_feb.pdf, and invoice_mar.pdf into one PDF"
```
Use pypdf's PdfWriter to iterate through all pages of each file and write to a merged output.

### Fill out a government form
```
User: "Fill out form W-9.pdf with my company info"
```
Follow `references/forms.md`: check for fillable fields, extract field info, create field values JSON, and fill using the appropriate script.

## Troubleshooting

### Encrypted PDF blocks all operations
**Solution:** Decrypt first with `qpdf --password=SECRET --decrypt encrypted.pdf decrypted.pdf`, or in Python: `reader = PdfReader("file.pdf"); reader.decrypt("password")`. If you don't have the password, the file cannot be processed.

### Text extraction returns empty strings or garbage
**Solution:** The PDF is likely scanned/image-based. Fall back to OCR: convert pages to images with `pdf2image`, then run `pytesseract.image_to_string()` on each page image.

### Missing Python dependency (pypdf, pdfplumber, reportlab, etc.)
**Solution:** Install the required package with pip: `pip install pypdf pdfplumber reportlab pdf2image pytesseract`. For command-line tools like `pdftotext` or `qpdf`, install via the system package manager (e.g., `brew install poppler qpdf` on macOS).

## Notes

- **Tool selection**: pypdf for structural operations (merge, split, rotate, encrypt), pdfplumber for text/table extraction, reportlab for creating new PDFs, pytesseract+pdf2image for OCR on scanned documents.
- **Advanced features**: See `references/reference.md` for pypdfium2, JavaScript libraries (pdf-lib, pdfjs-dist), advanced CLI usage, and performance optimization.
- **Form filling**: See `references/forms.md` for the complete form-filling workflow including fillable fields, non-fillable annotation-based filling, and validation scripts.
