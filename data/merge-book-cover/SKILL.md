---
name: merge-book-cover
description: Merge a cover image into a PDF book while preserving aspect ratio and matching width. Use when the user wants to "merge cover", "combine pdf", "fix cover size", or "add cover image".
---

# PDF Cover Merger

Merges a cover image (PNG/JPG) into an existing PDF book, ensuring the cover matches the book's page width exactly while preserving its aspect ratio.

**Why?** Solving the problem of misaligned or distorted cover pages when combining images with PDF documents programmatically.

## Quick Start

1.  Ensure `assets/cover.png` exists.
2.  Ensure `docs/Data-Science-with-Python.pdf` exists.
3.  Run the script: `python3 .agent/skills/merge-book-cover/scripts/merge_cover.py`

## Prerequisites

*   Python 3
*   Packages: `img2pdf`, `pikepdf`, `Pillow`

## Workflow Steps

### 1. Install Dependencies

Ensure the required Python packages are installed.

```bash
python3 -m pip install img2pdf pikepdf Pillow
```

### 2. Verify Files

Ensure the source files are in place:
*   Cover Image: `assets/cover.png`
*   Book PDF: `docs/Data-Science-with-Python.pdf`

### 3. Run Merge Script

Execute the script to resize the cover and merge it.

```bash
python3 .agent/skills/merge-book-cover/scripts/merge_cover.py
```

> [!TIP]
> The script automatically detects the width of the book's first page and scales the cover to match it perfectly, avoiding white margins or distortion.

### 4. Verify Output

Check the output file: `docs/Data-Science-with-Python_FINAL.pdf`.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `ModuleNotFoundError` | Missing Python packages | Run `python3 -m pip install ...` |
| `FileNotFoundError` | Missing cover or book PDF | check paths `assets/cover.png` and `docs/...` |

| Aspect Ratio issues | N/A | Script auto-calculates height based on width. |

## Quality Rules

*   **Zero Distortion**: The cover image must perfectly maintain its original aspect ratio.
*   **Exact Width Match**: The cover page width must exactly match the book's first page width (usually 612 pts for Letter).
*   **No Margins**: There should be no white bars or margins around the cover.
*   **Automation**: The process must run without manual image editing.

## Testing & Evaluation

### Manual Validation
1.  Run the script: `python3 .agent/skills/merge-book-cover/scripts/merge_cover.py`
2.  Open `docs/Data-Science-with-Python_FINAL.pdf`.
3.  **Check 1**: Is the cover (Page 1) flush with the edges? (No white border)
4.  **Check 2**: Does Page 2 (Title Page) have the exact same width as Page 1?
5.  **Check 3**: Is the cover image undistorted (circles are circular, text is proportional)?
