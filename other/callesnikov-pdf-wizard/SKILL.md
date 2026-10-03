---
name: callesnikov-pdf-wizard
description: Local PDF manipulation and page surgery with pypdf. Use when Codex needs to split, merge, extract, delete, replace, insert, reorder, rotate, crop, stamp, watermark, encrypt, decrypt, inspect metadata, update metadata, list or fill form fields, handle attachments, reduce file size, or assemble PDFs without cloud services. Do not use for OCR, layout-aware parsing, deep text extraction, or document understanding; delegate those to a parsing/OCR skill.
---

# Callesnikov PDF Wizard

Use this skill for local PDF assembly and page-level editing. Keep source PDFs unchanged, write outputs to the current working directory by default, and treat page ranges as human-facing 1-based ranges in the user interface.

## Step Zero: Runtime Setup

This skill is GitHub-friendly and must not assume a user-specific absolute path. Run commands from the skill folder or reference scripts by relative path.

Check dependencies:

```bash
python scripts/pdf_wizard.py self-check
```

Install into the active project/venv:

```bash
python -m pip install -r scripts/requirements.txt
```

Recommended isolated setup:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r scripts/requirements.txt
.venv/Scripts/python scripts/pdf_wizard.py self-check
```

On macOS/Linux, use `.venv/bin/python` instead of `.venv/Scripts/python`.

Core dependency:

- `pypdf[crypto]` for PDF reading/writing plus encryption/decryption support.

Optional external helpers:

- a renderer such as Poppler, MuPDF, Chrome/Edge, or another local PDF preview workflow when visual verification is needed;
- `qpdf` or `pikepdf` for heavily damaged PDFs that pypdf cannot repair.

## Tool Boundary

Use this skill for:

- split, extract, delete, merge, insert, replace, reorder, rotate, crop;
- stamp or watermark using another PDF page;
- encrypt, decrypt, inspect permissions;
- read/update/remove metadata;
- list/fill AcroForm text fields;
- attach files or extract embedded files;
- reduce file size by compressing content streams and removing duplicate objects where possible.

Do not use this skill as the primary tool for:

- OCR or scanned-document reading;
- layout-aware parsing, bounding boxes, tables, screenshots, or document Q&A;
- editing text inside a PDF as if it were a Word document;
- creating polished PDFs from scratch.

For those tasks, use the dedicated parsing/OCR or document-generation skill. For content corrections, prefer replacing whole pages instead of editing PDF text internals.

## PyPDF Capability Map

Use this map when choosing the safest operation:

| Area | PyPDF idea | Skill stance |
|---|---|---|
| Document assembly | `PdfWriter.append`, `merge`, `add_page`, `insert_page` | Core workflow: merge, insert, replace, extract, delete |
| Page surgery | `PageObject.rotate`, crop boxes, transformations | Core workflow: rotate/crop; use visual QA for crop/stamp/overlay |
| Stamps and watermarks | `merge_page`, `merge_transformed_page` | Supported through `stamp`; create the stamp PDF elsewhere |
| Encryption | `PdfWriter.encrypt`, `PdfReader.decrypt` | Supported; prefer AES when `cryptography` is installed |
| Metadata | `reader.metadata`, `writer.add_metadata`, `writer.metadata`, XMP APIs | Regular metadata supported; advanced XMP edits are manual/custom |
| Forms | `get_fields`, `get_form_text_fields`, `update_page_form_field_values` | List/fill text fields; flatten when final output should not be editable |
| Attachments | `writer.add_attachment`, `reader.attachments` | Supported for attach/extract embedded files |
| Outlines/bookmarks | imported by `append`/`merge`; writer can add outline items | Preserve by default during merge; custom outline authoring is advanced |
| Page labels | `writer.set_page_label` | Know it exists; add a custom script path if the user needs labels |
| Annotations | read/add/remove annotation APIs | Treat as advanced; avoid destructive annotation work without inspection |
| Viewer preferences / JavaScript | writer APIs exist | Avoid unless the user explicitly asks; JS in PDFs can be security-sensitive |
| Text/images extraction | pypdf can extract text/images | Delegate serious parsing, OCR, tables, screenshots, and document Q&A to the parsing skill |
| File size reduction | compress content streams, duplicate object compression, image removal APIs | Use `reduce` conservatively; do not promise dramatic compression |

## Core CLI

Primary script:

```bash
python scripts/pdf_wizard.py <command> ...
```

Common commands:

```bash
python scripts/pdf_wizard.py info source.pdf
python scripts/pdf_wizard.py extract source.pdf extracted.pdf 1-5,8,10-12
python scripts/pdf_wizard.py delete source.pdf without-pages.pdf 8-10
python scripts/pdf_wizard.py merge final.pdf part1.pdf edited.pdf part2.pdf
python scripts/pdf_wizard.py replace source.pdf edited-block.pdf final.pdf 8-10
python scripts/pdf_wizard.py insert source.pdf appendix.pdf final.pdf --after 7
python scripts/pdf_wizard.py rotate source.pdf rotated.pdf 90 --pages 2,4-6
python scripts/pdf_wizard.py crop source.pdf cropped.pdf --pages 1 --left 36 --bottom 36 --right 36 --top 36
python scripts/pdf_wizard.py stamp source.pdf stamp.pdf stamped.pdf --pages all --mode over
python scripts/pdf_wizard.py encrypt source.pdf locked.pdf --password "user-password" --algorithm AES-256-R5
python scripts/pdf_wizard.py decrypt locked.pdf unlocked.pdf --password "user-password"
python scripts/pdf_wizard.py metadata source.pdf
python scripts/pdf_wizard.py set-metadata source.pdf meta.pdf --title "Title" --author "Author"
python scripts/pdf_wizard.py list-fields form.pdf
python scripts/pdf_wizard.py fill-form form.pdf filled.pdf fields.json --flatten
python scripts/pdf_wizard.py attach source.pdf with-attachment.pdf file.txt
python scripts/pdf_wizard.py extract-attachments source.pdf attachments/
python scripts/pdf_wizard.py reduce source.pdf reduced.pdf
```

Add `--force` only when overwriting an existing output is intentional.

## Page Range Rules

User-facing page ranges are 1-based:

```text
1
1-5
1,3,7-10
all
odd
even
```

Python and pypdf use 0-based page indexes internally. The script handles this conversion. When writing custom code, state the conversion explicitly before editing.

## Workflows

### Replace Pages Safely

Use this when a PDF needs a corrected block:

1. Inspect source page count with `info`.
2. Extract the block if the user needs a separate editing artifact.
3. Build or receive the replacement PDF.
4. Run `replace source.pdf replacement.pdf output.pdf 8-10`.
5. Verify expected page count:
   `new_count = old_count - replaced_count + replacement_count`.

### Delete Or Extract Pages

Use `delete` for redaction by page removal, not content redaction. Use `extract` when the user needs a smaller PDF containing selected pages.

Never delete pages from the original in place unless the user explicitly asks and `--force` is set.

### Merge Or Insert Documents

Use `merge` for simple concatenation. Use `insert` when adding an appendix, cover page, signed page, or corrected block at a specific location. When merging forms, field names may collide; group or flatten forms when necessary.

### Rotate, Crop, Stamp

Use `rotate` for multiples of 90 degrees. Prefer pypdf's page `rotate()` for orientation fixes because it keeps page boxes consistent.

Use `crop` only when the requested trim is clear. Crop values are PDF points. One inch is 72 points.

Use `stamp`/`watermark` with a one-page PDF as the overlay/underlay. If the stamp page size differs from the target page, test visually.

### Encrypt And Decrypt

Prefer AES-based algorithms. If the user does not specify an algorithm, use `AES-256-R5` as a conservative default. Never print passwords back to chat. Do not store passwords in manifests.

### Forms

Use `list-fields` first. Fill only fields named by the user or JSON file. Prefer `auto_regenerate=False`. Use `--flatten` when the final PDF should keep visual values but stop being an editable form.

### Metadata

Use `metadata` to inspect regular document info. Use `set-metadata` for `/Title`, `/Author`, `/Subject`, `/Keywords`, `/Creator`, and `/Producer`. Clearing metadata is allowed only when the user asks.

## Output And Validation

For every operation that writes a PDF:

- write to a new output path unless `--force` is set;
- create parent directories if needed;
- report input page count, output page count, and output path;
- write a small JSON manifest beside the output unless `--no-manifest` is set;
- confirm the output starts with a PDF header and can be opened by `PdfReader`.

For important PDFs, do a visual check with a local renderer or ask the user to open the output before publishing, printing, or submitting it.

## Failure Handling

If pypdf fails:

1. Check whether the file exists and has a `%PDF-` header.
2. Check encryption and ask for a password if needed.
3. Try `strict=False` reading behavior, which the script uses by default.
4. Try a smaller operation, such as `info` or extracting one page.
5. For damaged PDFs, recommend `qpdf`/`pikepdf` repair before retrying.
6. Report the exact command, error, and whether any output was written.

## Source Ideas

This skill borrows the broad capability map from public pypdf skill patterns: merge, split, rotate, watermark/stamp, metadata, forms, and encryption. The implementation is intentionally narrower and more operational: it focuses on safe local page surgery and does not compete with the separate parsing/OCR skill.
