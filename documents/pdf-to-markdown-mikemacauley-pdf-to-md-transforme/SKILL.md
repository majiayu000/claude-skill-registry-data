---
name: pdf-to-markdown
description: Convert PDF files to clean Markdown offline and deterministically, with tables (ruled and borderless/booktabs) and sidebars placed inline and PDF metadata stripped. Use whenever the user wants a PDF turned into Markdown or text, wants a paper/report/scan extracted, asks what is in a PDF, or mentions pdf2md or pdf-to-md-transformer. Handles scanned PDFs via Tesseract OCR.
---

# PDF to Markdown

Converts PDFs to GitHub-flavoured Markdown with no network calls and no
randomness — the same file and version always produce byte-identical output.
Document metadata (Info dictionary, XMP, producer strings) is never emitted.

## Check the tool is installed

```bash
pdf2md --version || pip install /path/to/pdf_to_md_transformer
```

If the `pdf2md` MCP server is registered, use its `pdf_info`, `convert_pdf`,
and `convert_file` tools instead of the shell — same engine, same results.

## Workflow

1. **Inspect first** on an unfamiliar PDF:

   ```bash
   python3 -c "
   import json, pdfplumber
   from pdf_to_md.ocr import ocr_available, page_needs_ocr
   with pdfplumber.open('paper.pdf') as p:
       scanned = [i + 1 for i, pg in enumerate(p.pages) if page_needs_ocr(pg)]
   print(json.dumps({'pages_needing_ocr': scanned, 'ocr': ocr_available()}))"
   ```

   (Or the `pdf_info` MCP tool, which does exactly this.)

2. **Convert.** Write to a file unless the document is short:

   ```bash
   pdf2md paper.pdf -o out/ --json     # JSON report on stdout
   pdf2md paper.pdf --stdout           # Markdown on stdout (short docs)
   pdf2md paper.pdf -o out/ --extract-images   # figures as PNGs too
   ```

   Batch: pass several paths; exit code is 1 if any file failed, and the
   per-file outcome is in the `--json` report.

3. **Read back** only the section you need (`grep`, `sed -n`) rather than
   pulling a whole book into context.

## Reporting results honestly

- Scanned pages with **no OCR engine available** are skipped and replaced by an
  explanatory HTML comment. Say so; don't report a clean conversion. Fix with
  `brew install tesseract` / `apt install tesseract-ocr`, or point
  `PDF2MD_TESSERACT` at a binary.
- OCR'd pages carry a provenance comment (engine version, psm, dpi, language)
  and, where anything looked doubtful, a list of numeric tokens to check
  against the source. Pass that list on to the user — don't strip it. An
  unflagged number is likely right, not certainly right.
- For a non-English scan pass `--ocr-lang` (e.g. `deu`, `fra+eng`); the default
  `eng` silently degrades other languages.
- Figures are anchored in place with their captions, but the images themselves
  are only written out with `--extract-images` (into `<name>_assets/`). Without
  it the Markdown carries `<!-- figure: … image not extracted -->` markers — say
  so rather than implying the figures are in the output.
- Equations are either reconstructed LaTeX in a `$$` block (inferred from glyph
  geometry — tell the user it should be checked) or a ```` ```equation ```` block
  holding the raw glyph run, which the parser refused to interpret. Never retype
  a raw block as LaTeX yourself. Inline maths inside a paragraph is still
  garbled and unmarked.
- Re-running never changes the output — if it is wrong, the input or the tool
  needs attention, not another attempt.

Full interface reference: [AGENTS.md](../../../AGENTS.md).
