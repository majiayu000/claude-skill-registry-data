---
name: arc-docx
description: Create, edit, and inspect Word DOCX reports, letters, and proposals while preserving existing document structure and checking the delivered file.
---

# Word documents

Use the user's existing document and template when supplied. Inspect the actual headings, tables, headers, and sections before editing. Prefer a focused edit over reconstructing a document that contains fields, comments, revisions, or custom styles. `python-docx` does not provide a reliable tracked-changes editor: inspect the OOXML and choose a suitable editor when those features matter.

## Create or edit

Use an authorized connected computer with Python and `python-docx`. Check the import before installing; if required, create a task-local virtual environment and install `python-docx` there. Use `read_skill_resource` or `prepare_skill` to obtain [scripts/inspect_docx.py](scripts/inspect_docx.py). These instructions and the helper do not constitute an installed runtime.

For a new document, use `docx.Document()`, real heading styles, paragraphs, and tables. Set page size and margins explicitly. Use repeating table headers for multipage tables and keep headings with the following paragraph. Choose installed fonts with coverage for the user's language; do not assume Latin-only fonts render Chinese. Preserve source attribution and distinguish supplied facts from estimates. Save a new `.docx` under the requested output directory unless overwriting is expressly intended.

For an edit, load `Document(existing_path)` and address the actual paragraph or cell. Assigning an entire paragraph's `.text` removes run formatting and hyperlinks: edit runs when those should survive. Preserve section breaks, numbering, headers, footers, and existing styles. Do not claim unimplemented redlining.

## Verify delivery

Run `python scripts/inspect_docx.py OUTPUT.docx`. Check the reported headings, tables, section dimensions, and expected text against the request. The helper is read-only and does not paginate or certify visual layout. If an available local Word/LibreOffice renderer can export PDF, render the result and inspect every page for clipped tables, orphan headings, blank pages, and font substitution. Do not silently use a remote conversion service for private files. When rendering is unavailable, report structural verification and the missing visual check accurately.

Return the exact saved path and the checks performed. A Markdown response or a successful library import is not a delivered Word file.

Reference: https://python-docx.readthedocs.io/en/latest/
