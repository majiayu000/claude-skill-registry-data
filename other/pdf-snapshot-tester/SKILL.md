---
name: pdf-snapshot-tester
description: "Test PDF outputs by converting per-page to images (`pdftocairo` / pdf2image / Poppler) and running pixel-diff (pixelmatch / Resemble.js / Pillow `ImageChops`) against approved baselines. Per-page-range targeting, threshold tuning, font-substitution warnings, byte-stable PDF metadata stripping (CreationDate, /ID); references/ carry cross-engine HTML→PDF regression (Chromium `page.pdf()` / WeasyPrint / wkhtmltopdf per-engine baselines, engine-agreement tests, font-embedding checks, engine-version pinning). Use when a product generates invoices, contracts, or regulatory filings whose layout must not shift, when a PDF template, font pack, or generation library is about to change, or when swapping / upgrading the PDF engine."
metadata:
  keywords: "pdf-snapshot, visual-regression, pdftocairo, poppler, pixel-diff"
  version: "1.1.10"
---

# pdf-snapshot-tester

PDFs are binary documents with embedded fonts, embedded images, and
CreationDate/ID metadata. Direct binary diff is useless. The
canonical approach: render per-page to image, then pixel-diff against
approved baselines.

## When to use

- Invoice / contract / regulatory-filing PDFs where layout
  regression is unacceptable.
- Pre-deploy gate before changing PDF generation library, font
  pack, or template.
- Cross-engine verification (WeasyPrint output vs Chromium
  `page.pdf()` output) - the per-engine generation setup, agreement
  tests, and version pinning live in
  [references/cross-engine-regression.md](references/cross-engine-regression.md).

## How to use

1. Install Poppler (`pdftocairo` / `pdfinfo`) plus `pdf2image` and Pillow.
2. Generate the PDF under test and render each page to PNG at `dpi=150`
   (300 for regulatory filings).
3. On the first run, save the rendered pages as approved baselines under
   `tests/pdf-baselines/`.
4. On later runs, pixel-diff each page against its baseline and assert the
   diff ratio stays under threshold (~0.005).
5. For long PDFs, target only the changed pages with `first_page` /
   `last_page`.
6. Pin the production font pack in CI and normalize PDF metadata so
   baselines stay reproducible - see
   [references/deterministic-rendering.md](references/deterministic-rendering.md).
7. After an intentional layout change, re-run with
   `UPDATE_PDF_BASELINES=1` and commit the new baseline images.

## Step 1 - Install Poppler + pdf2image

```bash
# Linux
apt-get install -y poppler-utils

# macOS
brew install poppler

# Python wrapper
pip install pdf2image pillow
```

Poppler ships `pdftocairo` + `pdftoppm` - the workhorses for
PDF → image.

## Step 2 - Render PDF pages to images

```python
from pdf2image import convert_from_path
from pathlib import Path

pages = convert_from_path(
    "out.pdf",
    dpi=150,
    fmt="png",
    output_folder=str(Path("rendered")),
    paths_only=True,
)
```

`dpi=150` balances diff sensitivity vs file size. Increase to 300
for high-stakes documents (regulatory filings).

CLI alternative:

```bash
pdftocairo -png -r 150 out.pdf rendered/page
# produces rendered/page-1.png, rendered/page-2.png, ...
```

## Step 3 - Pixel-diff against baseline

```python
from PIL import Image, ImageChops

def pixel_diff(actual_path, baseline_path, threshold=0.001):
    a = Image.open(actual_path).convert("RGB")
    b = Image.open(baseline_path).convert("RGB")
    if a.size != b.size:
        return 1.0  # full mismatch on dimension change

    diff = ImageChops.difference(a, b)
    bbox = diff.getbbox()
    if not bbox:
        return 0.0

    diff_pixels = sum(1 for px in diff.getdata() if any(c > 5 for c in px))
    total = a.size[0] * a.size[1]
    return diff_pixels / total
```

Or use `pixelmatch` (Node) for a maintained reference impl.

## Step 4 - Per-page assertion

```python
def test_invoice_pdf_matches_baseline(tmp_path):
    actual_pdf = tmp_path / "invoice.pdf"
    generate_invoice(invoice_id="inv_001", out=actual_pdf)

    pages = convert_from_path(actual_pdf, dpi=150)
    for i, page_img in enumerate(pages, start=1):
        actual = tmp_path / f"actual-{i}.png"
        page_img.save(actual, "PNG")
        baseline = Path(f"tests/pdf-baselines/inv_001-{i}.png")
        diff_ratio = pixel_diff(actual, baseline)
        assert diff_ratio < 0.005, f"Page {i} diff ratio {diff_ratio:.4f}"
```

## Step 5 - Page-range targeting

For long PDFs (statements, prospectuses), test only changed pages:

```python
pages = convert_from_path(
    "out.pdf",
    dpi=150,
    first_page=2,
    last_page=5,
)
```

CLI:

```bash
pdftocairo -png -r 150 -f 2 -l 5 out.pdf rendered/page
```

## Step 6 - Update-baseline workflow

Add an opt-in update mode (analogous to Jest snapshots):

```python
import os

def assert_pdf_matches(actual_pdf, baseline_dir, threshold=0.005):
    update = os.environ.get("UPDATE_PDF_BASELINES") == "1"
    pages = convert_from_path(actual_pdf, dpi=150)
    for i, page_img in enumerate(pages, start=1):
        baseline = baseline_dir / f"page-{i}.png"
        if update or not baseline.exists():
            page_img.save(baseline, "PNG")
            continue
        diff = pixel_diff_img(page_img, Image.open(baseline))
        assert diff < threshold, f"Page {i} diff {diff}"
```

Run `UPDATE_PDF_BASELINES=1 pytest tests/pdf/` after intentional
changes; commit the new baseline images.

## Deterministic rendering

Non-deterministic PDF metadata (`/CreationDate`, `/ID`, `/ModDate`) and
host font substitution both invalidate baselines. Normalize metadata
with `qpdf` and detect missing fonts via Poppler stderr before diffing:
[references/deterministic-rendering.md](references/deterministic-rendering.md).

## Worked example

A billing service renders `invoice.pdf` from an HTML template; the team
is about to swap the body font and needs proof no invoice layout shifts.

1. On `main`, run the suite once with `UPDATE_PDF_BASELINES=1` to capture
   `tests/pdf-baselines/inv_001-1.png` from the current template.
2. Apply the font swap on a branch and re-run `pytest tests/pdf/`.
3. `convert_from_path("invoice.pdf", dpi=150)` renders page 1; `pixel_diff`
   compares it to the baseline and returns `0.0182`.
4. The assertion `diff_ratio < 0.005` fails with `Page 1 diff ratio 0.0182`,
   flagging that the new font reflowed the line-item table.
5. `pdfinfo -list-embedded-fonts invoice.pdf` confirms the new font is
   embedded (no substitution), so the shift is a real layout change, not a
   host-font artifact.
6. The team narrows column widths, re-runs until the diff ratio drops below
   0.005, then refreshes the baseline with `UPDATE_PDF_BASELINES=1`.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Binary diff PDFs directly | CreationDate / ID change per run | Render to image (Step 2) |
| `dpi=72` (default) | Sub-pixel changes invisible | `dpi=150` minimum (Step 2) |
| Threshold = 0 | Anti-aliasing flake | `threshold ≈ 0.005` (Step 4) |
| Skip font-pack pinning in CI | OS upgrade swaps fonts; baselines invalidate | Check fonts into repo or pin OS image (see Deterministic rendering) |
| Snapshot every page of 500-page PDF | CI time + storage explodes | Page-range targeting (Step 5) |

## Limitations

- Pixel-diff catches visual regressions but not semantic changes
  (text content swap with same layout). Pair with text-extraction
  tests if needed.
- Baselines are large binary files; use Git LFS for repos with
  many PDF baselines.
- Headless rendering may differ from production printer output; for
  print-critical work, sample real-printer output too.

## References

- Poppler utilities (`pdftocairo`, `pdftoppm`, `pdfinfo`) - packaged
  per-OS; consult system package docs for current version
- pdf2image Python wrapper - github.com/Belval/pdf2image
- pixelmatch (Node reference impl) - github.com/mapbox/pixelmatch
- [references/deterministic-rendering.md](references/deterministic-rendering.md) -
  metadata stripping + font-substitution detection
- [references/cross-engine-regression.md](references/cross-engine-regression.md) -
  cross-engine HTML→PDF generation, per-engine baselines,
  engine-agreement tests
- `print-stylesheet-tests` - 
  sister skill for pre-PDF CSS verification
