---
name: pdf
description: Use when working with PDF files. Covers text and table extraction, merging and splitting, form filling, watermarking, OCR for scanned documents, and generating PDFs.
metadata:
  category: documents
  version: 1.0.0
  tags: [pdf, extraction, ocr, forms, generation]
---

# PDF

## Purpose

Read, manipulate, and produce PDFs — including the scanned ones that contain no text at all and the ones whose tables are drawn rather than structured.

## When to Use

- Extracting text or tables from a PDF.
- Merging, splitting, or rotating pages.
- Filling a PDF form.
- OCR on a scanned document.
- Generating a PDF report or invoice.

## Capabilities

- Text extraction, with layout preservation where it matters.
- Table extraction.
- Page operations: merge, split, rotate, reorder, watermark.
- Form field reading and filling.
- OCR for scanned or image-only PDFs.
- Generation with proper typography and pagination.

## Inputs

- The source PDF, and whether it contains real text or images of text.
- The target: extracted data, a modified PDF, or a new one.

## Outputs

- Extracted text or structured tables.
- A valid modified or generated PDF.

## Workflow

1. **Determine whether it has text at all** — Extract from the first page. If nothing comes out, it is a scan, and every text-based approach will silently return nothing. That is the single most important check.
2. **Choose the extractor by the task** — Simple text extraction for prose; a layout-aware extractor for anything where column position carries meaning; a dedicated table extractor for tables.
3. **OCR only when necessary** — It is slow and imperfect. If the PDF has a text layer, use it.
4. **Preserve what matters when editing** — Merging PDFs drops bookmarks, form fields, and annotations unless you carry them across deliberately.
5. **Verify the output** — Open it. A PDF that a library writes without error can still be structurally broken.

## Best Practices

- A PDF that returns an empty string from text extraction is not empty; it is a scan. Check for this before concluding the file is corrupt.
- Tables in PDFs are usually drawn lines and positioned text, not structured tables. A general text extractor will interleave the columns into nonsense. Use a table-specific tool.
- Text extraction order follows the PDF's internal content stream, not the visual reading order. A two-column layout will frequently extract as interleaved lines.
- OCR quality depends overwhelmingly on the input image. Deskew and increase the contrast before OCR; it is worth more than any tuning of the OCR engine.
- Do not use `pypdf` for text extraction quality — it is fine for page operations and poor at text. Use `pdfplumber` or `PyMuPDF`.
- A generated PDF needs embedded fonts, or it will render differently on every machine that lacks them.

## Examples

**The check that must come first:**

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    first_page_text = pdf.pages[0].extract_text() or ""

if len(first_page_text.strip()) < 50:
    # This is a scan. Every text-based approach will return nothing, silently.
    # It is not a corrupt file and it is not an empty document.
    text = ocr_pdf("document.pdf")
else:
    text = "\n".join((p.extract_text() or "") for p in pdf.pages)
```

**Table extraction, which text extraction cannot do:**

```python
with pdfplumber.open("invoice.pdf") as pdf:
    for page in pdf.pages:
        # A general text extractor turns this into interleaved gibberish, because
        # the "table" is drawn lines and absolutely-positioned text.
        for table in page.extract_tables():
            header, *rows = table
            df = pd.DataFrame(rows, columns=[h.strip() if h else "" for h in header])
            yield df
```

**OCR with preprocessing, which matters more than the OCR settings:**

```python
import fitz            # PyMuPDF
import pytesseract
from PIL import Image, ImageOps

def ocr_pdf(path: str, dpi: int = 300) -> str:
    doc = fitz.open(path)
    pages = []

    for page in doc:
        # 300 DPI is the practical minimum for reliable OCR. 150 halves the accuracy.
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        # Preprocessing is worth more than any OCR engine parameter.
        img = ImageOps.grayscale(img)
        img = ImageOps.autocontrast(img)

        pages.append(pytesseract.image_to_string(img, config="--psm 6"))

    return "\n\n".join(pages)
```

## Notes

- `--psm 6` tells Tesseract to assume a uniform block of text, which is correct for most scanned documents and substantially more accurate than the default automatic page segmentation on a clean scan.
- PyMuPDF (`fitz`) is significantly faster than the alternatives for rendering and text extraction, and its licence (AGPL) matters for commercial use — check before adopting it.
- A PDF form's fields are named, and the names are frequently not what the visible labels say. Enumerate the fields before filling them.
