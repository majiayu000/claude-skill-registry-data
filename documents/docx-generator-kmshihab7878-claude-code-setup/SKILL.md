---
name: docx-generator
description: Generate professional Word documents with structured content, tables, headers, styles, and formatting. Uses python-docx. Use when creating reports, proposals, contracts, specs, or any structured document as DOCX/Word format.
version: "1.0.0"
category: documents
---

# Word Document Generator

Generate professional DOCX files using `python-docx`.

## Rules (Mandatory)

1. **Document structure** — title page, table of contents placeholder, numbered headings, page breaks between major sections
2. **No raw text dumps** — use proper heading levels (Heading 1-4), styled paragraphs, and lists
3. **Tables for structured data** — never present tabular data as plain text
4. **Consistent styling** — fonts, colors, spacing uniform. Use document styles, not inline formatting
5. **Headers/footers** — include document title in header, page numbers in footer
6. **File output** — save to concrete path, verify file exists

## Document Sections Pattern

| Section | Style | Purpose |
|---------|-------|---------|
| Title Page | Custom | Title, subtitle, author, date, version |
| ToC Placeholder | Heading | "Table of Contents" (Word auto-generates on open) |
| Executive Summary | Heading 1 + Normal | 1-paragraph overview |
| Body Sections | Heading 1-3 + Normal | Main content with sub-sections |
| Tables/Figures | Table style + Caption | Data presentation |
| Appendix | Heading 1 + Normal | Supporting material |

## python-docx Patterns

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Title
doc.add_heading('Document Title', level=0)
doc.add_paragraph('Author: <your-name> | Date: 2026-03-23')
doc.add_page_break()

# Sections
doc.add_heading('1. Executive Summary', level=1)
doc.add_paragraph('Overview text here.')

doc.add_heading('2. Analysis', level=1)
doc.add_heading('2.1 Market Data', level=2)

# Table
table = doc.add_table(rows=3, cols=3, style='Light Grid Accent 1')
table.rows[0].cells[0].text = 'Metric'
table.rows[0].cells[1].text = 'Q3'
table.rows[0].cells[2].text = 'Q4'

# Bullet list
for item in ['Point one', 'Point two', 'Point three']:
    doc.add_paragraph(item, style='List Bullet')

# Header/Footer
section = doc.sections[0]
header = section.header
header.paragraphs[0].text = 'Document Title'
footer = section.footer
footer.paragraphs[0].text = 'Page '  # Word auto-adds number

doc.save('output.docx')
```

## Workflow

1. **Outline** — define heading structure (H1/H2/H3)
2. **Styles** — set fonts, colors, spacing
3. **Content** — add paragraphs, lists, tables
4. **Formatting** — headers, footers, page breaks
5. **Save** — write to file, verify

## Install

```bash
pip install python-docx
```
