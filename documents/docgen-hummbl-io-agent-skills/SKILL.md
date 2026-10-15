---
name: docgen
description: Generate documents (docx, pptx, xlsx, pdf) via Python tooling.
version: 0.1.0
execution-mode: advisory
argument-hint: "<format> \"<title>\" [options]"
category: dev-tools
status: candidate
---
# Document Generator

Generate professional documents from structured content. All generation uses Python stdlib where possible, with lightweight helpers for office formats.

## Usage

```bash
[docgen] pdf "Q1 Board Report"              # Generate PDF
[docgen] docx "Technical Proposal"          # Generate DOCX
[docgen] pptx "Product Roadmap" 10          # Generate PPTX, ~10 slides
[docgen] xlsx "Budget Tracker"              # Generate XLSX
[docgen] md "Architecture Decision Record"  # Generate Markdown (always available)
```

## Task

Format: `$ARGUMENTS`

## Supported Formats

| Format | Method | Dependencies |
|--------|--------|-------------|
| **md** | Direct write | None (always available) |
| **pdf** | `fpdf2` or HTML-to-PDF via `weasyprint` | Check availability first |
| **docx** | `python-docx` | Check availability first |
| **pptx** | `python-pptx` | Check availability first |
| **xlsx** | `openpyxl` | Check availability first |

## Execution

### 1. Check tooling availability
```bash
python3 -c "import fpdf" 2>/dev/null && echo "fpdf2: available" || echo "fpdf2: missing"
python3 -c "import docx" 2>/dev/null && echo "python-docx: available" || echo "python-docx: missing"
python3 -c "import pptx" 2>/dev/null && echo "python-pptx: available" || echo "python-pptx: missing"
python3 -c "import openpyxl" 2>/dev/null && echo "openpyxl: available" || echo "openpyxl: missing"
```

If the required library is missing:
- Ask the user: "Install `<package>` with `pip install <package>`?"
- If denied, fall back to Markdown output and explain

### 2. Gather content
- If a briefing, AAR, or existing file is referenced, read it first
- If generating from scratch, outline sections and confirm with user before writing
- Apply your organization brand tokens if `[brand-guidelines]` skill is loaded (see brand-guidelines skill)

### 3. Generate the document
Write a Python script to `~/Desktop/<title>.<format>` (or user-specified path).

**PDF generation pattern** (fpdf2):
```python
from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=24)
pdf.cell(text="Title", new_x="LMARGIN", new_y="NEXT")
# ... content
pdf.output("$HOME/Desktop/<filename>.pdf")
```

**DOCX generation pattern** (python-docx):
```python
from docx import Document
doc = Document()
doc.add_heading("Title", level=0)
doc.add_paragraph("Content...")
doc.save("$HOME/Desktop/<filename>.docx")
```

**PPTX generation pattern** (python-pptx):
```python
from pptx import Presentation
from pptx.util import Inches, Pt
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Title"
prs.save("$HOME/Desktop/<filename>.pptx")
```

**XLSX generation pattern** (openpyxl):
```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.title = "Sheet1"
ws.append(["Column A", "Column B"])
wb.save("$HOME/Desktop/<filename>.xlsx")
```

### 4. Report
- Print the output path
- Print file size
- Open with `open <path>` if on macOS (ask first)

## Constraints

- Output to `~/Desktop/` by default unless user specifies otherwise
- Do NOT install packages without asking first
- If your project has a stdlib-only rule, keep to it in the main codebase -- doc generation scripts are standalone utilities, not part of the package
- Apply your organization brand styling when the content is your organization-related
- Always UTF-8 encoding
