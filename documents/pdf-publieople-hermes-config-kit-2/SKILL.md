---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

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

### fpdf2 - Create PDFs with Unicode/Chinese Support

fpdf2 is a good alternative to reportlab for text-heavy documents, especially when you need Chinese/Unicode support.

#### Installation (Chinese network — use mirror)
```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple fpdf2 fonttools defusedxml
```

#### WSL: Get Chinese Fonts from Windows
```bash
# Windows fonts are mounted under /mnt/c/Windows/Fonts/
# simhei.ttf (黑体) is reliable with fpdf2
# NotoSansSC-VF.ttf is also available (variable font — test first)
# TTC files (msyh.ttc) may not be supported by fpdf2
cp /mnt/c/Windows/Fonts/simhei.ttf /tmp/SimHei.ttf
```

#### Minimal Chinese PDF
```python
from fpdf import FPDF

pdf = FPDF('P', 'mm', 'A4')
pdf.add_font('CN', '', '/tmp/SimHei.ttf')   # regular
pdf.add_font('CN', 'B', '/tmp/SimHei.ttf')   # bold (same font, fpdf2 handles it)
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

pdf.set_font('CN', 'B', 26)
pdf.cell(0, 12, '标题', new_x="LMARGIN", new_y="NEXT", align='C')

pdf.set_font('CN', '', 10)
pdf.multi_cell(0, 5, '正文内容，支持中文排版。')

pdf.output('output.pdf')
```

#### Tips
- SimHei lacks some symbols (e.g. `•` \u2022). Use `·` (\u00b7 middle dot) instead.
- For section headers with color: `pdf.set_text_color(R, G, B)` before writing.
- For horizontal rules: `pdf.set_draw_color(R, G, B)` then `pdf.line(x1, y1, x2, y2)`.
- Chinese text will auto-page-break with `multi_cell`.

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

### Extract Text When pdftotext/pypdf Return Empty (Chinese/Scanned PDFs)

When `pdftotext` produces no output or `pypdf` can't extract text (common with Chinese academic PDFs, scanned documents, or image-based PDFs), use the **pdftoppm → mmx vision** fallback chain. This avoids installing OCR packages and works with any content:

```bash
# 1. Convert PDF pages to JPEG images (one per page)
pdftoppm -jpeg -r 200 "document.pdf" /tmp/pdf_page

# 2. Read key pages with mmx vision (MiniMax VLM)
mmx vision describe --image /tmp/pdf_page-01.jpg \
  --prompt "逐字描述所有文字内容" --output json --quiet

# 3. For multi-page docs, read TOC first (usually page 3-4), then target specific pages
```

**Pitfalls:**
- `pdftoppm` is part of `poppler-utils` (usually pre-installed on Linux)
- Large PDFs (20+ pages): read the TOC/contents page first, then selectively read relevant pages
- `mmx vision describe` has a ~30s timeout; use `--quiet` to suppress progress spinners
- Chinese prompts work best: `"请逐字描述所有文字内容，不要遗漏"`

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

### weasyprint - HTML+CSS to PDF (Best for Design-Heavy Documents)

When fpdf2's layout capabilities aren't enough (resumes, reports, certificates), use weasyprint to convert HTML with CSS into a polished PDF. This gives you full control over typography, colors, spacing, multi-column layouts, and responsive design.

#### Installation
```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple weasyprint
```

#### Basic Usage
```python
from weasyprint import HTML
HTML('resume.html').write_pdf('output.pdf')
```

#### Key CSS Techniques for PDF

**A4 page setup:**
```css
@page { 
  margin: 0; 
  size: A4;
}
body {
  font-family: 'SimHei', 'Microsoft YaHei', sans-serif;
  font-size: 10pt;
}
```

**Two-column layout (resume sidebar style):**
```css
.page {
  width: 210mm; min-height: 297mm;
  display: flex;
}
.sidebar {
  width: 95mm;           /* sidebar width */
  background: #1a2332;   /* dark sidebar */
  color: #e0e0e0;
  padding: 12mm 8mm;
}
.main {
  flex: 1;
  padding: 12mm 10mm;
}
```

**Print-specific rules:**
```css
@media print {
  .no-print { display: none; }
}
```

#### Critical Pitfall: Empty PDF in WSL

**⚠️ weasyprint generates EMPTY PDFs (0 pages, no /Type /Page objects) in WSL when no Chinese fonts are registered with fontconfig.** The PDF structure validates but contains no visible content. To fix:

1. **Register a Chinese font** with fontconfig:
```bash
cp /mnt/c/Windows/Fonts/simhei.ttf ~/.local/share/fonts/
fc-cache -fv
```
Then use `font-family: 'SimHei', '黑体', sans-serif;` in CSS (no @font-face needed).

2. **Or use @font-face** (if font is not system-registered):
```css
@font-face {
  font-family: 'MyFont';
  src: url('file:///path/to/simhei.ttf') format('truetype');
}
```

3. **Or fall back to fpdf2** — it works reliably without fontconfig.

Verify PDF has content:
```python
with open('out.pdf', 'rb') as f:
    assert b'/Type /Page' in f.read(), 'PDF has no pages!'
```

#### When to Use fpdf2 vs weasyprint

| Scenario | Tool | Reason |
|----------|------|--------|
| Simple text-heavy doc with Chinese | fpdf2 | Lightweight, no HTML/CSS needed |
| Resume / report / certificate | weasyprint | CSS gives full design control |
| Dynamic page count, auto layout | weasyprint | CSS handles pagination naturally |
| Multi-column layouts | weasyprint | CSS columns/flexbox are far easier |
| Icons, images, complex formatting | weasyprint | HTML ecosystem is richer |
| Serverless / minimal dependencies | fpdf2 | Only needs fonttools |

## Notion → Resume/CV PDF (Practical Workflow)

When the user asks to generate a resume/CV PDF from their Notion page:

### 1. Find the Resume Page in Notion

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "简历"}' | python3 -c "
import json,sys; d=json.load(sys.stdin)
for r in d['results']:
  for k,v in r.get('properties',{}).items():
    if v['type']=='title':
      t=''.join([x.get('plain_text','') for x in v['title']])
      print(f'{r[\"id\"]} | {t}')
"
```

### 2. Fetch Page Content (Blocks)

Write a Python script to recursively fetch all blocks. Key types to handle: `paragraph`, `heading_1/2/3`, `bulleted_list_item`, `numbered_list_item`, `divider`, `callout`, `code`, `to_do`, `image`. Handle nested blocks via `has_children`.

### 3. Best Tool: fpdf2 (NOT weasyprint in WSL)

**⚠️ CRITICAL PITFALL**: weasyprint generates EMPTY PDFs (0 pages, no /Type /Page objects) in WSL environments when no Chinese fonts are registered with fontconfig. The PDF structure validates but contains no visible content. **Do NOT use weasyprint for Chinese PDFs in WSL unless you verify fonts are registered first.**

Use **fpdf2** for Chinese resume PDFs — it's reliable:

```bash
# Install with Tsinghua mirror (fast in CN networks)
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple fpdf2 fonttools defusedxml
```

#### WSL: Get Chinese Font from Windows

```bash
cp /mnt/c/Windows/Fonts/simhei.ttf /tmp/simhei.ttf
```

#### Two-Column Resume Layout in fpdf2

fpdf2 is top-to-bottom flow, so two-column layouts require manual Y tracking:

```python
from fpdf import FPDF

SIDEBAR_W = 85  # mm

class ResumePDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('CN', '', '/tmp/simhei.ttf')
        self.add_font('CN', 'B', '/tmp/simhei.ttf')
    
    def sidebar_bg(self):
        """Draw dark sidebar background behind left column."""
        self.set_fill_color(26, 35, 50)   # #1a2332
        self.rect(0, 0, SIDEBAR_W, 297, 'F')
    
    def sidebar_text(self, text, size=7.5, bold=False):
        style = 'B' if bold else ''
        self.set_font('CN', style, size)
        self.set_text_color(200, 200, 200)
        self.set_x(8)
        self.multi_cell(SIDEBAR_W - 16, 4.5, text)
    
    def main_section_title(self, title):
        self.set_font('CN', 'B', 12)
        self.set_text_color(26, 35, 50)
        self.set_x(90)   # main content starts at 90mm
        self.cell(self.w - 90 - 15, 7, title)
        self.set_draw_color(26, 35, 50)
        self.line(90, self.get_y(), self.w - 15, self.get_y())

pdf = ResumePDF()
pdf.add_page()
pdf.sidebar_bg()

# Sidebar content
pdf.set_y(20)
pdf.set_font('CN', 'B', 20)
pdf.set_text_color(255, 255, 255)
pdf.set_x(8)
pdf.cell(SIDEBAR_W - 16, 9, '姓名')

# Main content
pdf.set_y(20)
pdf.main_section_title('项目经历')

pdf.output('resume.pdf')
```

#### fpdf2 Quirks for Chinese

- **SimHei lacks `•` (\\u2022 bullet)** — use `·` (middle dot \\u00b7) instead
- **SimHei is one weight** — both regular and bold use the same font file; fpdf2 handles this fine
- **No auto two-column flow** — must manually set_x/set_y for sidebar vs main content
- **Draw sidebar background first** with `rect()`, then write sidebar text, then re-position Y to write main content
- **Use `multi_cell`** for wrapping Chinese text; `cell` overflows silently
- **Valid PDF check**: verify with `b'/Type /Page' in open('out.pdf','rb').read()`

### 4. Template Inspiration

For visually appealing resumes, reference templates from [visiky/resume](https://github.com/visiky/resume):
- **Template 1 (Default)**: Dark sidebar (#1a2332) + green accent (#8bc34a), avatar placeholder, contact info, skill tags on left; experience, projects, awards on right
- **Template 2 (Simple)**: Single column, minimal, clean
- **Template 3 (Simple 2)**: More compact, multi-page suitable

### 5. Deliver the PDF

Copy to Windows Downloads for easy access:

```bash
cp ~/resume.pdf "/mnt/c/Users/$(ls /mnt/c/Users/ | grep -v -E 'Public|Default|All Users|Administrator' | head -1)/Downloads/resume.pdf"
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab or fpdf2 | Canvas/Platypus or FPDF with `add_font()` |
| Create Chinese/Unicode PDFs | fpdf2 | `add_font('CN', '', font_path)` — see fpdf2 section |
| **Design-heavy PDFs** (resume/report) | **weasyprint** | HTML+CSS → PDF — see weasyprint section |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see forms.md) | See forms.md |
| **Chinese academic PDF text extraction** | **pdftoppm + mmx vision** | See "Extract Text When pdftotext Returns Empty" section |
| **GB/T 7714-2015 citation format** | See `references/gbt7714-2015.md` | Chinese national standard for bibliographic references |

## References

- `references/gbt7714-2015.md` — GB/T 7714-2015 Chinese bibliographic reference format quick reference (Books [M], Journals [J], Dissertations [D], etc.)

## Next Steps

- For advanced pypdfium2 usage, see reference.md
- For JavaScript libraries (pdf-lib), see reference.md
- If you need to fill out a PDF form, follow the instructions in forms.md
- For troubleshooting guides, see reference.md
