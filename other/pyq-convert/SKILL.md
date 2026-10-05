---
name: pyq-convert
description: "Convert a PYQ (previous-year question) PDF — or any text-based PDF — into clean text/markdown using plain PyMuPDF (fitz). Use whenever the user gives a PYQ PDF and wants it converted, or types /pyq-convert. Fast (~0.1s for ~36 pages), zero (cid:) garbage, questions and options in correct order. Preferred over markitdown (which produces (cid:) garbage) and Docling/Marker (which are minutes-slow on CPU)."
---

# /pyq-convert

Convert a PYQ PDF to clean text/markdown with **plain PyMuPDF (`fitz`)**.

This is the user's chosen pipeline for PYQs: benchmarked head-to-head, plain
`fitz.get_text()` beat markitdown (0 vs 1,447 `(cid:)` garbage codes) and was
100× faster than `pymupdf4llm` and ~4,000× faster than Docling on CPU — while
keeping every question and all four options in correct reading order.

## When to use

- The user gives a PYQ PDF (or any text-based PDF) and wants it as text/`.md`.
- The user types `/pyq-convert <path>`.

Do NOT reach for markitdown, Docling, or Marker for this. Only fall back to
OCR tools (Docling/Marker) if the output shows `(cid:)` garbage — that means the
PDF is scanned or font-broken and genuinely needs OCR.

## Usage

The helper script lives next to this file. Run it with the PDF path:

```bash
python "<USER_HOME>/.Codex/skills/pyq-convert/convert_pyq.py" "<path-to-pdf>"
```

Output goes to the same folder as the PDF, same name with `.txt`.

Options:
- `--md`  → write `.md` instead of `.txt` (wraps each numbered question in light markdown)
- `-o <path>` → custom output path

Examples:
```bash
# default: clean .txt next to the PDF
python "<USER_HOME>/.Codex/skills/pyq-convert/convert_pyq.py" "<USER_HOME>/Downloads/2022 - PYQ.pdf"

# markdown output
python "<USER_HOME>/.Codex/skills/pyq-convert/convert_pyq.py" "<USER_HOME>/Downloads/2022 - PYQ.pdf" --md
```

For multiple PYQs, run the command once per file (or loop over a folder).

## Output style

- Plain PyMuPDF extraction → faithful reading order.
- Each MCQ option on its own line; questions kept in sequence.
- Light cleanup: fixes ligatures (`ﬁ`→`fi`, `ﬂ`→`fl`) and normalizes odd/non-breaking spaces.
- Faithful text only — no invented structure, images omitted.

## After running

- Report: page count, time, and `(cid:)` count (should be 0).
- If `(cid:)` > 0, tell the user this specific PDF is scanned/font-broken and
  would need an OCR tool (Docling/Marker, slow on CPU) — PyMuPDF can't fix it.

## Requirements

- `pip install pymupdf` (PyMuPDF). Already installed on this machine.

