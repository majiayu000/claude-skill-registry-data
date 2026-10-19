---
name: pdf-processing
description: >
  Extract text, parse structured tables, manipulate pages, fill form fields,
  and generate PDF documents programmatically. Use when extracting text or tables
  from PDFs with pypdf/pdfplumber, merging or rotating pages, handling scanned
  vs native digital documents, performing OCR with ocrmypdf/tesseract, handling
  encrypted or untrusted PDFs safely, or verifying rendered PDF visual layouts.
  Do not use for Word or Excel files, for true redaction of sensitive content without
  following the redaction rules below, or for legal e-signature workflows.
compatibility: >
  Agent Skills-compatible coding agents operating with Python PDF libraries
  (pypdf 6.x, pdfplumber, reportlab 4/5, pypdfium2) or poppler utilities. API names
  checked against PyPI releases in October 2026; run `pip show <lib>` to confirm
  the installed version.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "pdf, pdfplumber, pypdf, ocr, reportlab, document-processing"
  topics: "office, documentation, devtools"
---

# Programmatic PDF Processing and Verification

PDF (Portable Document Format) is a fixed-layout presentation format. Because PDFs store characters and drawing primitives at arbitrary Cartesian coordinates rather than semantic markup, processing PDFs reliably requires choosing the right tool for each task: distinguishing native digital text from scanned images, preserving tabular structures, and visually verifying outputs.

Detailed reference guides:
- [PDF Tools & Libraries Comparison](references/pdf-tools-guide.md)
- [PDF Quality & Extraction Verification Checklist](references/verification-checklist.md)
- [Untrusted PDFs, redaction, encryption, forms, licensing](references/untrusted-and-sensitive-pdfs.md)

---

## Core Rules

1. **Distinguish native text from scanned images first**: Attempt digital text extraction before invoking heavy OCR pipelines. Scanned PDFs require OCR; native PDFs do not.
2. **Never treat PDFs as plain text streams**: Text extraction must account for reading order, multi-column layouts, font encodings, and ligatures.
3. **Use specialized table extraction tools**: Do not rely on plain regex on extracted strings to parse tables. Use coordinate-aware libraries like `pdfplumber`.
4. **Preserve original documents**: Always write modified or merged PDFs to new destination files; never overwrite source inputs in place.
5. **Treat input PDFs as untrusted**: parsers have had denial-of-service bugs (huge or malformed objects, deep recursion). Cap file size and page count, set a timeout, run batch jobs in a sandbox or separate process, and keep libraries updated.
6. **Covering text is not redacting it**: a black rectangle drawn over text leaves the text in the file. Use a tool that removes the underlying content and verify by extracting text afterward (see reference).
7. **Verify visual rendering**: When generating PDFs (e.g. invoices or reports), convert the first page to PNG via `pdftoppm` or `pypdfium2` and verify margins, text wrapping, and alignment.

---

## 1. Quick Triaging: Scanned vs Native PDF

Before attempting extraction, determine if the document has native digital text:

```python
from pypdf import PdfReader

def is_scanned_pdf(file_path: str) -> bool:
    reader = PdfReader(file_path)
    total_text = ""
    # Sample up to first 3 pages
    for page in reader.pages[:3]:
        total_text += (page.extract_text() or "").strip()

    # If fewer than 50 characters extracted across 3 pages, document is likely scanned
    return len(total_text) < 50
```

---

## 2. Text and Metadata Extraction

### Native Digital Text with `pypdf`
Fast, lightweight, pure-Python:

```python
from pypdf import PdfReader

reader = PdfReader("annual_report.pdf")
print(f"Total Pages: {len(reader.pages)}")

# Extract metadata
meta = reader.metadata
if meta:
    print(f"Title: {meta.title}, Author: {meta.author}")

# Extract text with line preservation
for page_num, page in enumerate(reader.pages, start=1):
    text = page.extract_text(extraction_mode="layout") # Preserves visual layout
    print(f"--- Page {page_num} ---")
    print(text[:300]) # Print first 300 chars
```

---

## 3. Extracting Structured Tables with `pdfplumber`

`pdfplumber` inspects vector lines and character bounding boxes to extract tables into structured 2D lists:

```python
import pdfplumber
import csv

with pdfplumber.open("financial_statement.pdf") as pdf:
    first_page = pdf.pages[0]

    # Extract table using visual borders
    table = first_page.extract_table(table_settings={
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
    })

    if table:
        with open("table_output.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(table)
        print("Table successfully exported to table_output.csv")
```

---

## 4. Page Operations: Merging, Splitting, and Rotating

```python
from pypdf import PdfWriter, PdfReader

# Merging multiple documents
writer = PdfWriter()
for pdf_file in ["cover.pdf", "body.pdf", "appendix.pdf"]:
    writer.append(pdf_file)

with open("combined_output.pdf", "wb") as f_out:
    writer.write(f_out)

# Rotating a page (e.g. landscape table page)
reader = PdfReader("combined_output.pdf")
writer = PdfWriter()
for page in reader.pages:
    if page.mediabox.width > page.mediabox.height:
        # Page is landscape; rotate clockwise 90 degrees if portrait is desired
        page.rotate(90)
    writer.add_page(page)

with open("oriented_output.pdf", "wb") as f_out:
    writer.write(f_out)
```

---

## 5. Generating PDFs with `reportlab`

When generating pixel-perfect invoices, tickets, or reports from scratch:

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_invoice(dest_path: str):
    doc = SimpleDocTemplate(dest_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("INVOICE #2026-001", styles["Heading1"]))
    story.append(Spacer(1, 12))

    # Tabular data
    data = [
        ["Item Description", "Qty", "Unit Price", "Total"],
        ["Consulting Services (Hours)", "10", "$150.00", "$1,500.00"],
        ["Cloud Hosting Credits", "1", "$250.00", "$250.00"],
        ["", "", "Grand Total:", "$1,750.00"],
    ]
    t = Table(data, colWidths=[240, 60, 100, 100])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B4C7E")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))
    story.append(t)

    doc.build(story)
```

---

## 6. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| Running OCR on native digital PDFs | Extremely slow, introduces recognition errors, loses font fidelity | Check `extract_text()` first; OCR only if empty |
| Parsing tables with naive line regex | Breaks when columns wrap or table has empty cells | Use `pdfplumber.extract_table()` |
| Overwriting source PDF file directly | Corrupts source file if writing process is interrupted | Write to temp file, then atomically replace |
| Ignoring page rotation flags | Extracted text or rendered pages display upside down or sideways | Check `page.rotation` or orientation metadata |
| Using the old `PyPDF2` package | Unmaintained; merged back into `pypdf` | `pip install pypdf` and use `PdfReader`/`PdfWriter` |
| Drawing a black box to "redact" | Underlying text remains extractable | True redaction tool, then extract text to prove removal |
| Trusting `extract_text()` order for multi-column pages | Columns interleaved | Try `extraction_mode="layout"`, `pdfplumber` crop boxes per column, or render and read visually |
| Treating an empty extraction as "no content" | Could be scanned pages or text drawn as vector outlines | Render the page to PNG and look; use OCR if needed |
| Assuming OCR output is exact | Digits and similar glyphs misread | Spot check numbers against the rendered page; keep the confidence in mind |
| Shipping a PDF with hidden metadata | Author, software, and XMP leak | Inspect and clear metadata before sharing |

---

## 7. Troubleshooting Extraction

| Symptom | Likely cause | Action |
| :--- | :--- | :--- |
| `PdfReadError` / "EOF marker not found" | Truncated or corrupt file | Try `pdftotext`/`qpdf --check` if installed; ask for a fresh copy; do not guess content |
| `FileNotDecryptedError` or empty text | Encrypted PDF | `reader.is_encrypted`; decrypt only with a password the user supplied |
| Encrypted AES PDF fails to open | Missing crypto backend | Install `cryptography` (needed by pypdf for AES) |
| Garbled characters or `(cid:123)` | Font lacks a Unicode map | Try another extractor (`pdftotext`, `pdfplumber`) or OCR the rendered page |
| Table cells merged or shifted | No ruling lines | Switch `pdfplumber` strategies to `"text"`, tune tolerances, or define explicit column lines |
| Slow or out-of-memory on large file | Whole-document processing | Process page by page, close pages (`page.flush_cache()` in pdfplumber), set limits |

## 8. Verification Checklist

- [ ] Evaluated whether input PDF is scanned or digital.
- [ ] Table extraction preserves all column headers and numeric alignments.
- [ ] Text extraction contains expected keywords and no corrupted character encoding.
- [ ] Multi-page operations preserve metadata and links.
- [ ] Generated PDF renders cleanly in standard PDF viewers without clipped text or overflowing margins.
