---
name: academic-translation-latex
description: Translate or bilingual-polish scientific Chinese/English text while preserving LaTeX, equations, citations, figure/table references, abbreviations, gene and drug names, units, P values, and manuscript terminology. Use for 中英互译, SCI翻译, LaTeX论文翻译, biomedical translation, title/abstract translation, paragraph-by-paragraph academic translation, or when accurate translation is needed rather than broad rewriting.
---

# Academic Translation With LaTeX Preservation

## Purpose

Translate academic and biomedical text between Chinese and English while preserving technical meaning and manuscript markup. This skill is for careful translation, not scientific rewriting or result enhancement.

## Typical Inputs

- Chinese or English manuscript paragraphs.
- Titles, abstracts, figure legends, cover letters, or response-letter text.
- LaTeX or Markdown manuscript sections containing equations, citations, labels, or cross-references.
- Terminology preferences supplied by the user.

## Core Rules

- Preserve LaTeX commands, math, labels, refs, citations, BibTeX keys, tables, and Markdown structure unless the user asks otherwise.
- Preserve gene/protein symbols, drug names, database names, trial IDs, accession IDs, units, Greek letters, P values, confidence intervals, and figure/table numbering.
- Do not fabricate references, data, experiments, sample sizes, statistical significance, or clinical claims.
- Do not change the strength of evidence. "Associated with" must not become "caused by"; "may" and "suggests" should remain cautious.
- Flag meaningful ambiguity instead of silently choosing an interpretation.
- Remind the user to perform final human review before submission.

## Workflow

1. Identify translation direction: Chinese to English, English to Chinese, or bilingual polish.
2. Identify the manuscript context: title, abstract, methods, results, discussion, figure legend, cover letter, or reviewer response.
3. Build a small terminology map from the input for repeated disease names, methods, endpoints, genes, drugs, platforms, and datasets.
4. Translate paragraph by paragraph while protecting technical tokens.
5. Check that all numbers, citations, equations, labels, and technical names match the source.
6. Provide concise terminology notes only when they reduce ambiguity.

## Output Modes

Default output:

- Clean translated text ready to paste.

For careful review:

- A two-column table with original text and translation.
- Short notes for ambiguous or domain-specific terms.

For LaTeX-heavy input:

- Preserve commands and environments exactly.
- Do not wrap the final translation in a code block unless requested.

## Quality Checklist

- Meaning is preserved.
- Technical tokens are unchanged.
- No new facts or references were introduced.
- Claim strength is unchanged.
- The result still requires author review before submission.
