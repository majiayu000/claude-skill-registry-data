---
name: latex-word-roundtrip-cleaner
description: Clean manuscript text moving between LaTeX, Word, Markdown, and journal submission systems. Use for LaTeX转Word, Word转LaTeX, clean citations, fix broken symbols, table/figure reference cleanup, equation-safe editing, journal format cleanup, or when copy-paste between formats damages a manuscript.
---

# LaTeX Word Roundtrip Cleaner

## Purpose

Clean formatting damage caused by moving manuscripts among LaTeX, Word, Markdown, PDFs, and journal submission portals while protecting scientific content and references.

## Typical Inputs

- LaTeX text copied into Word or plain text.
- Word/PDF text with broken line breaks, hyphenation, symbols, or references.
- Markdown tables or figure legends needing manuscript-safe cleanup.
- Submission portal text that rejects or damages LaTeX commands.

## Core Rules

- Do not change manuscript meaning.
- Do not alter citation keys, equation labels, figure/table labels, accession IDs, gene names, drug names, P values, or statistical values.
- Do not fabricate or invent references, data, methods, or results.
- Preserve math delimiters and complex equations unless the user explicitly asks for conversion.
- Flag conversions that may require manual checking.
- Recommend final human review, especially for equations and references.

## Workflow

1. Identify source and target format:
   - LaTeX to Word/plain text
   - Word/plain text to LaTeX
   - Markdown to manuscript text
   - submission portal cleanup
2. Protect technical tokens:
   - `\cite{}`
   - `\ref{}`
   - `\label{}`
   - `$...$`, `\(...\)`, and `\[...\]`
   - gene names, units, P values, accession IDs
3. Clean formatting:
   - broken line breaks
   - hyphenation artifacts
   - double spaces
   - malformed punctuation
   - inconsistent figure/table references
4. Return the cleaned target-format text.
5. List protected items and risky conversions only when useful.

## Reference Cleanup

Normalize reference wording according to the user's target style:

- `Fig. 1`, `Figure 1`, or `Fig 1`
- `Table 1`
- `Supplementary Figure S1`

Never merge supplementary references with main-text references.

## Output Modes

Default output:

- Cleaned text only.

For risky conversions:

- Cleaned text.
- Protected items.
- Potentially unsafe conversions needing manual review.

## Quality Checklist

- Cross-references and citations are intact.
- Equations are not corrupted.
- Scientific values are unchanged.
- Formatting is cleaner but content is not rewritten.
