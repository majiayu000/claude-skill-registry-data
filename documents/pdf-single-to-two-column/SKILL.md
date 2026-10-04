---
name: pdf-single-to-two-column
description: Reconstruct one-column PDF files as searchable two-column PDFs, with Docling Markdown (referenced picture assets) followed by Pandoc and XeLaTeX as the default PDF-only workflow. Use for permanent layout reconstruction or batch conversion when preserving figures, reading order, originals, manifests, and visual QA matters; do not use for reader reflow, zoom, or 2-up printing.
---

# PDF Single To Two Column

## Goal and boundary

Create a new, searchable two-column PDF. Do not call reader Reflow, zoom, booklet printing, 2-up, or page slicing a reconstruction. Never overwrite the source. Work in a new run directory, keep the intermediate Markdown and picture assets, append `_2col` to the PDF name, and write `manifest.json`.

The default PDF-only backend is:

```text
Docling PDF parse (OCR off, table-structure off, picture images on)
  -> referenced Markdown + assets/
  -> Pandoc Markdown-to-LaTeX
  -> XeLaTeX classoption=twocolumn
  -> pdftotext/layout + pdftoppm visual QA
```

This is a reconstruction, not a guarantee of the source's original pagination. Figures are preserved as extracted images when Docling can identify them, but figure order, captions, formulas, title/author blocks, and page breaks remain review items.

## Backend policy

1. If an authoritative DOCX, LaTeX, or publishing source exists and must remain paper-grade, change its column setting at the source and export again.
2. For PDF-only input, use `scripts/docling_latex_backend.py` as the default and pin the tested Docling environment. Do not silently switch to Word, `pdf2docx`, or a text-only conversion after a Docling failure.
3. Use Word COM only for an actual editable DOCX. Headless Word PDF import is an explicit diagnostic experiment, not a default backend.
4. Treat `pdftotext -> Pandoc -> Word` as a lossy diagnostic baseline. It is not acceptable for a paper batch because it can scramble reading order, formulas, author blocks, and figures.
5. Scanned PDFs need an explicit OCR contract. The default Docling pipeline sets `do_ocr=False`; do not claim scanned-PDF support without recording OCR language, engine, confidence, and manual-review pages.

## Prerequisites and version contract

The validated pilot used:

- Python 3.11.15 in an isolated environment;
- Docling 2.114.0;
- Pandoc 1.19.2.1;
- XeLaTeX from TeX Live 2025;
- Poppler `pdfinfo`, `pdftotext`, and `pdftoppm`.

Check the environment before conversion:

```powershell
$skill = "C:\Users\Administrator\.codex\skills\pdf-single-to-two-column"
$py = "D:\path\to\.venvs\docling-two-column\Scripts\python.exe"
& $py "$skill\scripts\docling_latex_backend.py" doctor
```

If the doctor reports a missing dependency, install it in an isolated environment and record the actual versions. Do not silently upgrade Docling for a production batch; rerun the pilot after any version change.

## Standard workflow

### 1. Freeze a pilot

- Record the absolute source path, SHA-256, page count, page size, text extractability, and whether the source is born-digital or scanned.
- Copy 3-5 representative pages into a separate pilot input: title/author, dense body, formula/table, figure/caption, and footnote pages. Do not modify the original.
- Use the same pilot input for every backend comparison.

### 2. Run Docling reconstruction

Run one file into a fresh directory. The script writes Markdown, `assets/`, `pandoc.log`, a layout text dump, rendered PNGs, the PDF, and `manifest.json`.

```powershell
$skill = "C:\Users\Administrator\.codex\skills\pdf-single-to-two-column"
$py = "D:\path\to\.venvs\docling-two-column\Scripts\python.exe"
$input = "D:\papers\pilot\sample-pages.pdf"
$run = "D:\papers\runs\sample-docling-2col"

& $py "$skill\scripts\docling_latex_backend.py" convert `
  --input $input `
  --output-dir $run `
  --render-pages 1,2,3 `
  --cjk-font "Microsoft YaHei"
if ($LASTEXITCODE -ne 0) { throw "Docling reconstruction failed; inspect $run\manifest.json and pandoc.log" }
```

Keep `--render-pages` targeted to representative pages. Use `--no-render` only for a deliberate text-only diagnostic run. Use `--overwrite` only when the run directory is disposable and the replacement is explicit.

### 3. Apply the quality gate

Do not batch until all of these are true for the pilot:

- `manifest.json` is `status: ok`, records input/output hashes, actual versions, the Pandoc command, rendered pages, and `review_gate: pending_manual_visual_review`.
- `pdfinfo` confirms a non-empty PDF, expected page size, and a plausible page count.
- `pdftotext -layout` shows title, authors, abstract, section order, and page numbers in left-column top-to-bottom then right-column order.
- Rendered PNGs show no clipped text, overlap, black blocks, missing images, font substitution, incoherent blank regions, or cross-column mixing.
- Figures and captions are in a defensible order; formulas, tables, footnotes, and symbols are readable; text remains selectable.
- Compare the reconstructed pilot against the source page by page. A PDF being openable, searchable, or two columns wide is not sufficient.

Record a human decision beside the manifest as `pilot_passed`, `pilot_rejected`, or `needs_review`. Keep rejected outputs for diagnosis; do not feed them into the batch.

### 4. Batch only after approval

Use a new output directory and one manifest per input. Stop on the first failure or unexpected version. Example:

```powershell
$skill = "C:\Users\Administrator\.codex\skills\pdf-single-to-two-column"
$py = "D:\path\to\.venvs\docling-two-column\Scripts\python.exe"
$inputDir = "D:\papers\incoming"
$outputRoot = "D:\papers\runs\two-column"

Get-ChildItem $inputDir -Filter *.pdf | Sort-Object Name | ForEach-Object {
  $run = Join-Path $outputRoot $_.BaseName
  & $py "$skill\scripts\docling_latex_backend.py" convert `
    --input $_.FullName `
    --output-dir $run `
    --render-pages 1
  if ($LASTEXITCODE -ne 0) { throw "Batch stopped at $($_.FullName)" }
}
```

Review a sample of full-batch manifests and rendered pages again. Do not overwrite or replace the source directory.

## Failure handling

- If Docling cannot parse the PDF, preserve its manifest/log and report the exact version and error. Do not silently fall back to text-only Pandoc.
- If `assets/` is empty for a document that visibly contains figures, mark the pilot as failed and inspect Docling's picture extraction before batching.
- If title/author blocks, formulas, figure order, captions, or reading order are damaged, mark `pilot_rejected` or `needs_review`; do not describe the output as publication-ready.
- If Pandoc/XeLaTeX fails, inspect `pandoc.log`, the selected CJK font, and the Markdown/image paths. Keep the Markdown as the debugging artifact.
- If page count changes substantially or a right column is blank, treat it as a layout decision requiring review, not automatic success.
- If input is a BabelDOC-generated PDF, Docling may still parse it, but do not use it as evidence that the BabelDOC IL backend can process its own output. Keep backend experiments separate.
- For Word/MCP questions, consult `references/backends.md`. An Office MCP connection does not imply a PDF reconstruction tool.

## Bundled resources

- `scripts/docling_latex_backend.py`: deterministic single-file Docling -> Markdown/assets -> Pandoc/XeLaTeX conversion, manifest, text dump, and rendering.
- `scripts/doctor.py`: environment inventory; reports `docling-markdown-xelatex` as the recommended backend when ready.
- `references/backends.md`: tested backend comparison and evidence limits.
