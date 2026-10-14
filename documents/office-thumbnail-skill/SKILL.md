---
name: office-thumbnail-skill
description: >-
  Thumbnail grids and image conversion from Office files (PPTX/DOCX/XLSX) via
  LibreOffice and Poppler. Use for 'show me thumbnails' or visual review of
  document pages.
license: Apache-2.0
compatibility: opencode
category: Office Utilities
---

## What I do

I convert Office files to images for **visual analysis** — thumbnail grids, individual page images, or PDF intermediates. This is the visual-review companion to the OOXML editing and slide-generation skills.

- **Thumbnail grids** — multi-page Office files → single grid image for quick overview (`thumbnail.py`)
- **PDF conversion** — Office file → PDF via headless LibreOffice (`soffice.py`)
- **Image conversion** — PDF pages → individual JPEG/PNG images via Poppler

## When to use me

Use this skill when the user wants:
- "Show me thumbnails" / "visual analysis of this deck"
- "Convert slides to images"
- "Generate a visual grid for review"
- Any task needing to visually inspect Office document pages

Also used internally by:
- `pptx-specialist-subagent` Stage 5 (visual verification via `image-analyzer-subagent`) — renders each generated slide to PNG for vision-model sizing verification
- `code-review-subagent` / `uiux-reviewer-subagent` — visual evidence capture

## Prerequisites

- **LibreOffice** (`soffice`) — headless PDF conversion
  ```bash
  sudo apt-get install libreoffice          # Debian/Ubuntu
  winget install TheDocumentFoundation.LibreOffice   # Windows (or use WSL)
  ```
- **Poppler** (`pdftoppm`) — PDF to image conversion
  ```bash
  sudo apt-get install poppler-utils        # Debian/Ubuntu
  # Windows: use WSL, or a poppler build via your package manager
  ```
- **Python 3.9+**

## Workflow

### Thumbnail grid generation
```bash
python scripts/thumbnail.py presentation.pptx [output_prefix]
```
- Creates `thumbnails.jpg` (or `thumbnails-1.jpg`, `thumbnails-2.jpg` for large decks)
- Default: 5 columns, max 30 slides per grid (5×6)
- Custom columns: `--cols 4` (range 3-6)

### Convert to PDF (intermediate)
```bash
python scripts/soffice.py --headless --convert-to pdf presentation.pptx
```
The `soffice.py` wrapper handles the AF_UNIX socket restriction in sandboxed VMs.

### Convert PDF to images
```bash
pdftoppm -jpeg -r 150 presentation.pdf slide
```
Creates `slide-1.jpg`, `slide-2.jpg`, etc.

## Scripts

| Script | Purpose |
|--------|---------|
| `thumbnail.py` | Generate visual thumbnail grids from any Office file |
| `soffice.py` | LibreOffice wrapper — handles sandbox AF_UNIX socket restrictions |

## Use cases

- **Template analysis**: Quickly understand slide layouts and design patterns
- **Content review**: Visual overview of entire presentation
- **Quality check**: Verify all slides are properly formatted
- **Visual verification**: Render generated slides for `image-analyzer-subagent` sizing checks (BT-142 Phase 2.4b)
- **Documentation**: Include slide images in reports or PR reviews
