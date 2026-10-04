---
name: chinese-document-style
description: Create, edit, review, or standardize Simplified Chinese documents using formal academic and technical writing conventions. Use when Codex needs to draft or revise Chinese Markdown, README files, reports, papers, specifications, product documentation, or other prose; correct Chinese-English spacing, full-width punctuation, numbers, units, terminology, headings, paragraphs, lists, tables, links, citations, or code formatting; remove colloquial, promotional, or AI-like wording; or enforce a consistent Chinese editorial style without changing technical meaning.
---

# Chinese Document Style

Apply formal Simplified Chinese writing and typography while preserving the document's facts, argument, citations, technical terms, and intended audience.

## Workflow

1. Identify the document type, audience, publication context, and existing style requirements.
2. Inspect the whole document before editing. Detect terminology, person, quotation marks, date format, heading hierarchy, citations, code, and generated sections that must remain stable.
3. Apply requirements in this order:
   - explicit user, institution, journal, or repository requirements;
   - laws, standards, citation styles, and official product spellings;
   - the document's declared style and terminology;
   - this skill's general rules.
4. Separate findings into correctness errors, consistency errors, readability improvements, and optional stylistic choices.
5. Revise the narrowest necessary scope. Preserve valid domain terminology, mathematical notation, code, URLs, file paths, identifiers, quotations, and references.
6. Re-read the revised document for semantic drift, unsupported claims, missing qualifiers, broken links, changed citations, and formatting regressions.
7. For repository files, inspect the diff and run the relevant Markdown, document, or project checks.

## Required Style

- Use formal, objective, evidence-oriented Chinese.
- Prefer precise claims over promotional evaluation. Replace vague phrases such as “大幅提升”“非常先进” with measurable evidence when evidence is available; otherwise remove or qualify them.
- Remove conversational filler, slogans, rhetorical questions, excessive exclamation marks, self-congratulatory language, and formulaic AI transitions.
- Do not introduce facts, citations, standards, statistics, or conclusions that are absent from the source material.
- Keep one concept under one stable term. Preserve official capitalization such as GitHub, JavaScript, MySQL, macOS, and ChatGPT.
- Prefer active and explicit sentence structures, but do not mechanically eliminate every passive construction.
- Keep each paragraph focused on one topic and split sentences that contain several independent judgments.
- Distinguish normative terms consistently: use “必须” for requirements, “推荐” or “建议” for guidance, and “可以” for options.

## Typography

- Add one half-width space between Chinese and adjacent Latin text or Arabic numerals.
- Add one half-width space between a number and most units: `10 GB`, `8 km`.
- Do not add a space before `%`, `°`, or `°C`: `15%`, `90°`, `37°C`.
- Use full-width Chinese punctuation in Chinese sentences and do not place spaces around it.
- Use half-width punctuation inside complete English sentences, code, URLs, paths, identifiers, formulas, and other fixed-syntax content.
- Use `……` for a Chinese ellipsis and `——` for a Chinese em dash.
- Do not stack punctuation such as `！！！` or `？？？`.
- Keep quotation-mark and parenthesis styles consistent. Follow the target institution's style when specified.

## Structure

- Do not skip heading levels. Usually keep the hierarchy within four levels.
- Make peer headings grammatically parallel and descriptive.
- Use ordered lists only when sequence or numbering matters.
- Keep list items parallel in grammar, information granularity, and terminal punctuation.
- Give tables explicit headers and define empty values.
- Use descriptive link text rather than “这里” or raw filenames.
- Use inline code for commands, parameters, paths, filenames, fields, and identifiers.

## Academic and Technical Integrity

- Preserve citation keys, footnotes, bibliography entries, quotations, equations, table and figure numbering, and cross-references.
- Do not convert a recommendation into a mandatory statement or strengthen causal claims beyond the evidence.
- Keep limitations, assumptions, sample conditions, uncertainty, and negative results.
- If the requested publication style is unknown, retain the existing citation and numbering style instead of inventing one.
- Treat relative time words such as “目前”“近期”“最新” as unstable; replace them with concrete dates only when the source supplies or verifies the date.

## Reference Use

Read [references/chinese-style-guide.md](references/chinese-style-guide.md) when:

- performing a full-document review;
- resolving punctuation, spacing, number, unit, quotation, or structure questions;
- deciding whether a rule is mandatory, recommended, or optional;
- reviewing academic or technical prose for non-promotional language.

Read only the relevant sections for small, focused edits.

## Output

For editing tasks, provide the revised artifact and summarize material changes. For review-only tasks, report issues by severity and cite exact locations when available. State any unresolved choice that depends on an institution, journal, or team style guide.
