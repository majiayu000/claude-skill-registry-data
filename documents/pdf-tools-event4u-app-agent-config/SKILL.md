---
model_tier: medium
name: pdf-tools
description: "Use when creating, merging, splitting, filling, or extracting from a PDF — library-per-task, output validated. Triggers on 'merge these PDFs', 'fill this PDF form', 'split the PDF', 'create a PDF'."
status: active
tier: senior
domain: process
compatibility: "Requires consumer-installed PDF libraries: pypdf (merge/split/rotate/encrypt/extract), reportlab (create), a form library for AcroForm fill; an OCR engine (e.g. tesseract) only for the OCR task. No LibreOffice dependency. Ships zero runtime in this package."
harness_compat: consumer-installed-deps
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# pdf-tools

Wing-1 engineering skill for **PDF write/transform** — `markitdown` reads a PDF
to Markdown; this creates, merges, fills, and extracts. Ships zero runtime: the
agent drives libraries the consumer has. Pattern re-implementation only.

## When to use

- "Merge / split / rotate / encrypt these PDFs."
- "Fill this PDF form (AcroForm) with these values."
- "Create a PDF from this content."
- "Extract the text / tables from this PDF" (structured extraction beyond `markitdown`'s Markdown).
- "OCR this scanned PDF."

Do NOT use for: PDF → Markdown ingestion (`markitdown`); Word (`docx-authoring`).

## Procedure

### 1. Library per task — do not force one tool

| Task | Library path |
|---|---|
| merge / split / rotate / encrypt | pypdf — page-level operations, no rendering |
| create from content | reportlab (canvas / platypus) |
| form-fill (AcroForm) | a form-aware library; map field name → value, then flatten if the form must not be re-editable |
| text / table extraction | a text-layer extractor; tables need a layout-aware pass, not naive text |
| OCR (scanned/image PDF) | an OCR engine over rasterized pages — ONLY when there is no text layer |

### 2. Decide flatten-or-keep on form fills

A filled AcroForm stays editable unless flattened. Flatten when the PDF is a
final artifact (an invoice, a signed form); keep fields when the recipient must
edit further. State which you chose — a silently-editable "final" form is a
correctness bug.

### 3. Validate — assert output validity, do not trust the write

1. Re-open the output with pypdf; assert `len(reader.pages)` matches the expected count (merge = sum; split = 1 per part).
2. For a form-fill: read back one field value (pre-flatten) or extract the rendered text (post-flatten) and assert the value is present.
3. For create: assert the file opens and page 1 carries expected text.

## Output format

1. The output PDF path(s).
2. Validation: page count matches expected ✅, read-back value/text present ✅.
3. For fills: flatten decision stated (flattened / kept-editable + why).

## Gotcha

**OCR is a last resort, not the default extraction path.** Running OCR over a
PDF that already has a text layer produces worse output (OCR errors) than the
existing text and burns time. Check for a text layer first; OCR only when it is
genuinely absent.

- **Editable "final" form:** a filled AcroForm left un-flattened ships as a "signed invoice" the recipient can silently alter → flatten when the artifact is final.

## Do NOT

- Do NOT bundle a Python toolkit in this package — drive the consumer's libraries (zero-runtime posture).
- Do NOT OCR a PDF that has a text layer.
- Do NOT leave a "final" filled form editable without saying so.
- Do NOT claim success on "file written"; claim it only after the re-open + page-count assertion.

## Related Skills

**WHEN to use this**

- The task creates, merges, splits, rotates, encrypts, or form-fills a PDF.
- Structured text/table extraction beyond `markitdown`'s Markdown, or OCR of a scanned PDF.

**WHEN NOT to use this**

- PDF → Markdown ingestion → [`markitdown`](../markitdown/SKILL.md).
- Word documents → [`docx-authoring`](../docx-authoring/SKILL.md); spreadsheets → [`spreadsheet-authoring`](../spreadsheet-authoring/SKILL.md).

## When the agent should load this

- "Merge / split / rotate these PDFs."
- "Fill this PDF form."
- "Create a PDF from this content."
- "Extract the tables from this PDF / OCR this scan."

## Output

1. **Output PDF(s)** — the path(s). Cite as `pdf-output`.
2. **Validation receipt** — page count matches expected ✅, read-back value/text present ✅. Cite as `pdf-validation`.
3. **Fill decision** — present on form-fills: flattened / kept-editable + why. Cite as `pdf-fill-decision`.
