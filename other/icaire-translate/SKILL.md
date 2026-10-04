---
name: icaire-translate
description: Translate ICAIRE material between English and Arabic across documents, decks, PDFs, PowerPoint, Word, and web pages. Use when the user asks for English-Arabic or Arabic-English translation.
---

# ICAIRE Translate

Translate ICAIRE material between English and Arabic, prioritizing
English-to-Arabic while supporting Arabic-to-English, with explicit handling
for decks, PDFs, Word files, PowerPoint files, and web-page copy.

## Contract

- Confirm language direction, audience, output format, deadline, and whether
  the output is internal draft, official draft, web copy, deck copy, or
  publication-ready material.
- Preserve meaning, names, dates, figures, titles, official entity names,
  acronyms, and source structure unless the user asks for adaptation.
- Prioritize English-to-Arabic, but support Arabic-to-English when requested.
- Treat official Arabic as review-ready draft text requiring human approval
  before external sending or publication.
- For government-machine material, prepare translation outputs or instructions
  that the user can manually transfer.
- Do not publish web-page translations or commit website changes unless the
  user explicitly asks for implementation work in the relevant repo.

## Workflow

1. Scope the translation.
   - Identify source format, language direction, target audience, tone, and
     whether the output should preserve layout or be text-first.
   - Ask whether the user wants a direct translation, polished translation,
     bilingual table, or translation with reviewer notes.
2. Extract source content.
   - For Word and PowerPoint, preserve headings, bullets, tables, slide order,
     speaker notes, and key structure where practical.
   - For PDFs, extract text and flag layout or OCR limits.
   - For web pages, treat supplied URLs, pasted copy, or repo files as source
     material and keep publish steps separate.
3. Translate.
   - Preserve terminology consistently across the artifact.
   - Flag ambiguous acronyms, official names, policy terms, and lines that need
     human judgment.
   - Keep Arabic clear, professional, and institutionally appropriate.
4. Review.
   - Check that facts, numbers, dates, names, and commitments match the source.
   - Note any formatting, OCR, or source-quality limitations.
   - For decks and documents, save a translated copy when file editing is in
     scope.

## Output

Default to this structure:

- `Translation Scope`: source, direction, audience, format, and tone.
- `Translated Output`: translated text or file path.
- `Reviewer Notes`: terminology choices, ambiguous items, and human-review
  needs.
- `Format Notes`: what structure was preserved and what was text-only.
- `Remaining Steps`: publication, government-machine transfer, or approval
  steps.

## Guardrails

- Do not change policy meaning, legal meaning, financial figures, dates, names,
  or commitments without flagging the change.
- Do not silently omit source sections because extraction is difficult.
- Do not treat machine-readable text extraction as proof that a PDF translation
  preserved layout.
- Do not publish or deploy translated web pages unless explicitly asked.
- Do not claim official approval for translated Arabic.
