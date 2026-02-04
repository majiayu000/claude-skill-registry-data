---
name: pdf-reading
description: Read local PDFs to extract and verify exact numbers (counts, percentages, tables, figure captions) for papers/questions in this repository. Use this when asked to “read a PDF”, “extract results from the paper”, “verify a statistic”, or “find the exact wording in the paper”.
---

## Goal

When you need facts from a paper PDF (counts, percentages, benchmark numbers, claims, limitations), extract *verbatim* evidence from the PDF and compute derived values yourself.

This repository’s content often depends on exact values from tables/figures (not abstracts). Always bias toward **precision and traceability**.

## Process

1. **Locate the PDF**
   - Search the repo for `.pdf` files.
   - If a paper directory contains a source PDF, prefer that.
   - If the only PDF is in `tmp/` or the repo root, confirm it corresponds to the paper in question before using it.

2. **Extract text locally (no network fetches)**
   - Prefer a local text extraction flow:
     - Use `.github/skills/pdf-reading/extract_pdf_text.py` to create a plain-text copy in `tmp/`.
     - If extraction fails, try a different backend (`pypdf` vs `pdftotext`) or fall back to manual inspection.

3. **Search within the extracted text**
   - Use targeted queries first (unique phrases, table titles, “Table 2”, “Appendix”, metric names).
   - For numbers, search patterns like `n=`, `N=`, `(`, `%)`, `Table`, `Figure`.

4. **Verify statistics (repo requirement)**
   - Prefer raw counts (e.g., “31/50”) over percentages when available.
   - If the paper gives counts, compute percentages yourself: $\text{pct} = 100 \times \frac{\text{numerator}}{\text{denominator}}$.
   - If a value is ambiguous (multiple similar tables/ablations), capture the surrounding label/context.

5. **Handle common PDF pitfalls**
   - **Hyphenation and line breaks:** words may be split across lines; search both with and without hyphens.
   - **Tables:** extracted text may be messy; search by row/column headers and unique tokens.
   - **Scanned PDFs:** text extraction may fail; use manual reading if needed.

## Output expectations

- When updating a question/paper, report the exact extracted phrase/value and where it came from (section/table/figure name).
- If you cannot reliably extract the needed value, explicitly say so and propose next steps (e.g., manual verification).

## Commands

- Extract text:
   - `python3 .github/skills/pdf-reading/extract_pdf_text.py path/to/paper.pdf`

- Extract to a specific file:
   - `python3 .github/skills/pdf-reading/extract_pdf_text.py path/to/paper.pdf --out tmp/paper.txt`

## Repository conventions to respect

- Keep diffs minimal and consistent with existing patterns.
- Park derived artifacts under `tmp/` (gitignored).
- Don’t add new dependencies unless explicitly requested; prefer optional tooling or clear fallbacks.
