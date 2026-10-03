---
name: dark-pdf-studio
description: Convert PDFs, document files, or images into dark-background reading PDFs with a compact input-to-output workflow. Use when Codex needs to dark-theme a PDF, normalize docs or images into a dark PDF, build or refine a tiny dark-mode export utility, or troubleshoot a dark PDF conversion flow with downloadable output.
---

# Dark PDF Studio

Use this skill when the user wants a simple dark-PDF workflow: one input file, one output file, dark background, downloadable result.

## Quick Start

1. Prefer PDF input for layout fidelity.
2. Run `bash scripts/run_dark_pdf_studio.sh doctor`.
3. Run `bash scripts/run_dark_pdf_studio.sh inspect`.
4. Use `bash scripts/run_dark_pdf_studio.sh convert --input input.pdf --output output-dark.pdf`.
5. Use `--theme graphite`, `--theme midnight`, or `--theme navy` for the background tone.
6. For document inputs such as `.docx` or `.rtf`, let the script normalize them through `textutil` first on macOS, or LibreOffice when needed.
7. Use `bash scripts/run_dark_pdf_studio.sh validate` after edits to confirm the converter still compiles and exposes its CLI.
8. If the user wants a small app, keep the UI compact:
   - choose or drop one file
   - pick one dark theme
   - export
   - open or reveal output only after export exists

## Workflow

### Input Rules

- Best input: PDF
- Also supported:
  - `.doc`
  - `.docx`
  - `.rtf`
  - `.odt`
  - `.txt`
  - `.md`
  - `.html`
  - `.htm`
  - common images including `.png`, `.jpg`, `.webp`, `.gif`, `.heic`
- Prefer converting non-PDF documents into PDF before dark processing so the export contract stays consistent.

### Output Rules

- Default output is a dark-background PDF.
- Keep the surface simple:
  - one input
  - one output
  - one theme choice
- Prefer an essentials-only utility surface:
  - compact header
  - source picker / drop target
  - theme picker
  - export button
  - open / reveal only when there is output
- Treat “downloadable” as a local exported file path that can be opened or shared immediately.

### Editing Guidance

- Use `scripts/run_dark_pdf_studio.sh` for the normal doctor, inspect, convert, and validate flow.
- Use `scripts/dark_pdf.py` for the actual conversion path when you need the lower-level CLI directly.
- Keep the conversion deterministic and easy to explain.
- If a document backend is missing, fail with a clear dependency message instead of pretending the conversion succeeded.
- Prefer `textutil` on macOS for document-to-text normalization before falling back to LibreOffice.
- Prefer readable high-contrast results over preserving every original page color exactly.

### Validation

- Run `bash scripts/run_dark_pdf_studio.sh validate` after edits.
- If you need to prove end-to-end conversion, smoke-test one real PDF through the runner and confirm the output file exists.
- Run `python3 scripts/dark_pdf.py --help` only as a fallback when debugging the wrapper itself.
- If the user provides a real file, smoke-test one conversion and confirm the output path exists.

## Resources

- `scripts/run_dark_pdf_studio.sh`: repo-native doctor, inspect, convert, and validate helper for the dark PDF workflow.
- `scripts/dark_pdf.py`: CLI converter for PDF, doc, and image inputs into dark-background PDF output.
- `references/workflow-map.md`: input contract, backend expectations, and output behavior.
