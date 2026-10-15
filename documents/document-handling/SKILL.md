---
name: document-handling
description: Use when reading/writing docx/pdf/pptx/xlsx files. Prefer programmatic libs over shelling out.
---

# Handling Office and PDF documents

`.docx`, `.xlsx`, `.pptx`, and `.pdf` are binary container formats. `Read` will not show you their text directly, and shelling out to `cat` returns garbage. Always use a programmatic library through a short Python (or Node) script.

## When to trigger
- The user asks to read, extract, modify, or generate any of: `.docx`, `.xlsx`, `.xls`, `.pptx`, `.pdf`.
- A workflow expects "the spreadsheet" or "the slides" as input.
- You see a binary Office/PDF path passed as a path parameter.

## Library selection

Pick the smallest library that does the job. Python is usually the right host because the libraries are mature and well-documented.

### `.docx` (Word)

- **Read + write**: `python-docx`. Stable, handles paragraphs, tables, styles, headers.
- Node alternatives (`docx`, `mammoth`) exist but are weaker for round-tripping. Use `python-docx` unless you are already deep in a Node project.
- For complex layout or comments preservation, consider exporting to markdown via `pandoc` first.

### `.xlsx` / `.xls` (Excel)

- **Read + write**: `openpyxl` (xlsx only). Cell-level access, formulas, styles.
- **Bulk read**: `pandas.read_excel` with the `openpyxl` engine. Fastest path when you only need data, not formatting.
- **`.xls` legacy**: `xlrd` (read only, version 1.2.0).
- **Node**: `exceljs` is the closest equivalent to openpyxl.

### `.pdf`

- **Read text**: `pdfplumber` (best layout fidelity) or `pypdf` (simpler, faster for plain text).
- **Read tables**: `pdfplumber.extract_tables()` or `camelot` for harder cases.
- **Write**: `reportlab` (full control, verbose) or `fpdf2` (simpler API). For modifying an existing PDF, use `pypdf` to merge/split and overlay with `reportlab`.
- **OCR fallback**: if the PDF is scanned images, no text library will help. Use `pytesseract` after rendering pages with `pdf2image`.

### `.pptx` (PowerPoint)

- **Read + write**: `python-pptx`. The only mature option. Handles slides, shapes, text frames, tables.

## Workflow

1. **Check what you actually have.** Run `Read` on the file. If it returns clean text (because the file was already converted to markdown or txt), you are done - work with that.
2. **Otherwise, treat it as binary.** Write a short Python script that opens the file with the right library, extracts only what you need, and prints structured output.
3. **Invoke via PowerShell.** Call `python script.py <args>` from the terminal. Capture stdout.
4. **For writing**: build the output file in Python, save it, then verify with a second small read pass.

Example skeleton (read a docx):

```python
# read_docx.py
import sys
from docx import Document

doc = Document(sys.argv[1])
for p in doc.paragraphs:
    print(p.text)
```

```powershell
python read_docx.py "C:\path\to\file.docx"
```

## Large files

- Do not load a multi-megabyte spreadsheet into memory just to read column A. Use `openpyxl` with `read_only=True` and iterate.
- For PDFs over ~50 pages, extract one page at a time. `pdfplumber.open(path).pages[i]` is lazy.
- For DOCX with embedded images, skip the image parts unless asked - they bloat memory.
- Stream output to disk instead of accumulating in a Python list when extracting thousands of rows.

## Generating files

When asked to generate a docx/xlsx/pdf/pptx:

1. Confirm the target structure first (sections, sheets, slides) - do not guess.
2. Build a minimal version, save, and open in the host app once if possible to verify rendering.
3. Keep styles simple. Office formats are forgiving about content but unforgiving about malformed style definitions.

## Encoding gotchas on Windows

- PowerShell 5.1 writes UTF-16 LE by default. If you pipe Python output to a file via `>`, you will corrupt it for downstream readers. Either redirect inside Python (`open(..., encoding="utf-8")`) or use `| Out-File -Encoding utf8`.
- Paths with spaces must be double-quoted when passed to `python`.

## Red flags

- Running `Get-Content` or `cat` on a `.docx`/`.xlsx`/`.pptx`/`.pdf`. You will see XML soup or binary garbage and waste context.
- Trying to regex-parse the raw zip contents of an Office file. Use the library.
- Building a PDF parser from scratch. The libraries are good enough.
- Loading a 100 MB spreadsheet just to count rows. Use `read_only=True` mode.
- Shelling out to LibreOffice or Word headlessly when a Python library would do. Reserve that for format conversion the libraries cannot perform.
- Generating a `.docx` by writing a `.txt` and renaming it. The file will not open.

## References

- `python-docx`: https://python-docx.readthedocs.io
- `openpyxl`: https://openpyxl.readthedocs.io
- `pdfplumber`: https://github.com/jsvine/pdfplumber
- `python-pptx`: https://python-pptx.readthedocs.io
- `lean-context` skill - do not dump entire extracted documents into chat; summarize.
