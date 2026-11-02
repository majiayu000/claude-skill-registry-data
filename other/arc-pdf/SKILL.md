---
name: arc-pdf
description: Inspect, extract, merge, split, and rotate PDF files with page-order and content verification, while identifying scans and avoiding false redaction claims.
---

# PDF workflows

Start with the user's actual PDF and desired operation. Keep an original copy. Use an authorized connected computer and inspect whether the document is encrypted, contains extractable text, or is a scan before choosing a method. Do not infer missing page text from the filename or pretend extraction performs OCR.

## Inspect and transform

Check Python and `pypdf`; use a task-local environment for missing packages. Obtain [scripts/inspect_pdf.py](scripts/inspect_pdf.py) through resource tools and run `python scripts/inspect_pdf.py INPUT.pdf`. It reports page count, dimensions, rotation, and a text sample per page without modifying the source. For an encrypted file it reports the lock rather than guessing a password. Use only a password supplied or authorized by the user, and do not put passwords in logs or saved instructions.

Use `PdfReader` and `PdfWriter` for merging, selecting pages, and rotation. Translate the user's one-based page numbers to zero-based indexes explicitly. Validate the selected ranges before writing. Preserve requested order, page dimensions, and orientation; write a new file unless overwriting is intended. Check whether forms, signatures, annotations, or bookmarks require special handling. Editing invalidates existing digital signatures; do not claim they survived. Covering text with a rectangle is not secure redaction: use a dedicated redaction engine and verify the removed content when redaction is requested.

For scanned pages, inspect available local OCR tools and language support. Only claim OCR after it has actually run, and check recognized text against page images. Do not upload private documents to an external converter without authorization.

## Verify delivery

Reopen the output with the inspector. Compare expected page count, order, sizes, rotations, and representative text against the source. Render relevant pages with a local PDF renderer when available and check cropping, orientation, and content. Structural checks alone do not establish layout or OCR accuracy. Return the real saved path with precise checks and any limitation.

Reference: https://pypdf.readthedocs.io/en/stable/
