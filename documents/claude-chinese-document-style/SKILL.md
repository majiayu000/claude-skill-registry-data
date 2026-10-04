---
name: claude-chinese-document-style
description: Create, edit, review, or standardize Simplified Chinese documents in Claude Code using formal academic and technical writing conventions. Use whenever Chinese Markdown, README files, reports, papers, specifications, product documentation, or prose needs correction of Chinese-English spacing, punctuation, numbers, units, terminology, headings, paragraphs, lists, tables, links, citations, or code formatting; removal of colloquial, promotional, or AI-like wording; or consistent editorial revision without changing technical meaning.
---

# Chinese Document Style for Claude Code

Apply formal Simplified Chinese writing and typography while preserving facts, argument, citations, technical terms, and intended audience.

## Workflow

1. Determine the document type, audience, publication context, and explicit style requirements.
2. Read the complete file or the complete section in scope before editing. Inspect terminology, person, quotation marks, dates, heading levels, citations, code blocks, and generated content.
3. Apply requirements in this order:
   - user, institution, journal, or repository requirements;
   - laws, standards, citation styles, and official product spellings;
   - existing document conventions;
   - this skill's general rules.
4. Classify issues as correctness, consistency, readability, or optional style. Do not present optional preferences as errors.
5. Edit the smallest necessary scope. Do not rewrite code, URLs, paths, identifiers, formulas, quotations, references, or generated files as ordinary prose.
6. Re-read the result for changed meaning, unsupported claims, lost qualifiers, damaged citations, and formatting regressions.
7. Use `git diff --check`, the repository's formatter or linter, and a focused preview or build when available.

## Required Style

- Use formal, objective, evidence-oriented Chinese.
- Remove slogans, rhetorical questions, conversational filler, excessive emotion, self-praise, and formulaic AI transitions.
- Replace promotional or vague evaluation with verifiable evidence when supplied. Do not invent evidence.
- Preserve official names and capitalization such as GitHub, JavaScript, MySQL, macOS, and ChatGPT.
- Use one stable term for one concept.
- Prefer explicit subjects and concise sentences. Split sentences containing several independent judgments.
- Use “必须” only for requirements, “推荐” or “建议” for guidance, and “可以” for options.

## Typography

- Insert one half-width space between Chinese and adjacent Latin text or Arabic numerals.
- Insert one half-width space between numbers and most units: `10 GB`, `8 km`.
- Do not insert spaces before `%`, `°`, or `°C`.
- Use full-width Chinese punctuation in Chinese sentences without surrounding spaces.
- Preserve half-width punctuation inside complete English sentences and fixed-syntax content.
- Use `……` for a Chinese ellipsis and `——` for a Chinese em dash.
- Do not repeat exclamation marks or question marks.
- Keep quotation-mark, parenthesis, date, and range styles consistent.

## Structure

- Do not skip heading levels; usually use no more than four levels.
- Keep peer headings and list items grammatically parallel.
- Use ordered lists only when order or later reference matters.
- Give tables explicit headers and define empty values.
- Use descriptive link text.
- Use inline code for commands, parameters, paths, filenames, fields, and identifiers.

## Academic and Technical Integrity

- Preserve citations, bibliography entries, quotations, equations, numbering, and cross-references.
- Do not strengthen modality or causality beyond the source.
- Retain assumptions, limitations, uncertainty, negative results, and experimental conditions.
- If no citation style is specified, preserve the existing style.
- Do not add standards, dates, statistics, or references without evidence.

## Reference Use

Read [references/chinese-style-guide.md](references/chinese-style-guide.md) for full reviews or when resolving detailed spacing, punctuation, number, unit, quotation, structure, academic style, or exception questions. Load only relevant sections for focused edits.

## Completion

When editing repository files:

1. Inspect the final diff for unrelated changes.
2. Confirm Markdown links and heading levels when relevant.
3. Run available checks.
4. Report changed files, material editorial decisions, validation, and any unresolved institution-specific choice.
